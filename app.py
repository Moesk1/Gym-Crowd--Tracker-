from flask import Flask, g, jsonify, make_response, redirect, render_template, request, url_for
import json
import logging
import os
import sqlite3
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

app = Flask(__name__)

DATABASE = Path(__file__).parent / "gym.db"
VISITOR_COOKIE = "gym_visitor_id"
COOKIE_MAX_AGE_SECONDS = 60 * 60 * 24 * 365
MODERATE_CROWD_AT = int(os.getenv("MODERATE_CROWD_AT", "10"))
VERY_BUSY_CROWD_AT = int(os.getenv("VERY_BUSY_CROWD_AT", "25"))

UOFM_LOGO_URL = (
    "https://www.memphis.edu/_resources/images/logos/"
    "leaping_tiger_full_color_white-text.png"
)

# Structured JSON logging setup.
logger = logging.getLogger("gym_crowd_tracker")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)


def log_event(event, level="INFO", **details):
    """Write one machine-parseable JSON log record."""
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "event": event,
        "request_id": getattr(g, "request_id", None),
        "method": request.method,
        "path": request.path,
        **details,
    }

    message = json.dumps(record, separators=(",", ":"))

    if level == "ERROR":
        logger.error(message)
    else:
        logger.info(message)


@app.before_request
def start_request():
    g.request_id = str(uuid.uuid4())
    g.request_started_at = time.perf_counter()
    log_event("request_started")


@app.after_request
def finish_request(response):
    duration_ms = round(
        (time.perf_counter() - getattr(g, "request_started_at", time.perf_counter()))
        * 1000,
        2,
    )
    log_event(
        "request_completed",
        status_code=response.status_code,
        duration_ms=duration_ms,
    )

    response.headers["X-Request-ID"] = g.request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Cache-Control"] = "no-store"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "img-src 'self' https://www.memphis.edu data:; "
        "style-src 'self'; "
        "script-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'none'"
    )
    return response


@app.teardown_request
def log_request_error(error):
    if error is not None:
        log_event(
            "request_failed",
            level="ERROR",
            error_type=type(error).__name__,
        )


def get_db_connection():
    connection = sqlite3.connect(DATABASE, timeout=5)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Create the database and apply small backwards-compatible migrations."""
    connection = get_db_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS check_ins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                active INTEGER NOT NULL DEFAULT 1,
                visitor_id TEXT,
                checked_in_at TEXT,
                checked_out_at TEXT
            )
            """
        )

        columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(check_ins)").fetchall()
        }
        if "visitor_id" not in columns:
            connection.execute("ALTER TABLE check_ins ADD COLUMN visitor_id TEXT")
        if "checked_in_at" not in columns:
            connection.execute("ALTER TABLE check_ins ADD COLUMN checked_in_at TEXT")
        if "checked_out_at" not in columns:
            connection.execute("ALTER TABLE check_ins ADD COLUMN checked_out_at TEXT")

        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_check_ins_active ON check_ins(active)"
        )
        connection.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_one_active_checkin_per_visitor
            ON check_ins(visitor_id)
            WHERE active = 1 AND visitor_id IS NOT NULL
            """
        )
        connection.commit()
    finally:
        connection.close()


def get_crowd_count(connection):
    return connection.execute(
        "SELECT COUNT(*) FROM check_ins WHERE active = 1"
    ).fetchone()[0]


def get_crowd_level(crowd_count):
    """Return the prototype crowd level and short student guidance."""
    if crowd_count >= VERY_BUSY_CROWD_AT:
        return {
            "label": "Very Busy",
            "slug": "very-busy",
            "guidance": "Expect a busy gym. If your schedule is flexible, consider visiting later.",
        }
    if crowd_count >= MODERATE_CROWD_AT:
        return {
            "label": "Moderately Busy",
            "slug": "moderate",
            "guidance": "There is a noticeable crowd, but you should still have options.",
        }
    return {
        "label": "Not Busy",
        "slug": "not-busy",
        "guidance": "The gym looks relatively quiet based on active student check-ins.",
    }


def get_student_check_in_status(connection, visitor_id):
    if not visitor_id:
        return False

    row = connection.execute(
        """
        SELECT id
        FROM check_ins
        WHERE visitor_id = ? AND active = 1
        LIMIT 1
        """,
        (visitor_id,),
    ).fetchone()
    return row is not None


def execute_write(sql, parameters=()):
    connection = get_db_connection()

    try:
        cursor = connection.execute(sql, parameters)
        connection.commit()
        return cursor.rowcount
    finally:
        connection.close()


def get_status_message(status):
    messages = {
        "checked-in": ("success", "You’re checked in. Thanks for helping other Tigers see the crowd."),
        "checked-out": ("success", "You’re checked out. Your visit is no longer included in the count."),
        "already-in": ("warning", "You’re already checked in, so the crowd count was not changed."),
        "not-in": ("warning", "You aren’t currently checked in, so the crowd count was not changed."),
    }
    return messages.get(status)


@app.route("/")
def home():
    visitor_id = request.cookies.get(VISITOR_COOKIE)
    new_visitor = visitor_id is None
    if new_visitor:
        visitor_id = str(uuid.uuid4())

    connection = get_db_connection()
    try:
        crowd_count = get_crowd_count(connection)
        is_checked_in = get_student_check_in_status(connection, visitor_id)
    finally:
        connection.close()

    crowd_level = get_crowd_level(crowd_count)
    meter_percent = min(100, round((crowd_count / VERY_BUSY_CROWD_AT) * 100))
    status_message = get_status_message(request.args.get("status"))

    log_event(
        "crowd_count_viewed",
        crowd_count=crowd_count,
        crowd_level=crowd_level["label"],
        student_checked_in=is_checked_in,
    )

    response = make_response(
        render_template(
            "index.html",
            crowd_count=crowd_count,
            crowd_level=crowd_level,
            is_checked_in=is_checked_in,
            meter_percent=meter_percent,
            moderate_at=MODERATE_CROWD_AT,
            very_busy_at=VERY_BUSY_CROWD_AT,
            status_message=status_message,
            uofm_logo_url=UOFM_LOGO_URL,
        )
    )

    if new_visitor:
        response.set_cookie(
            VISITOR_COOKIE,
            visitor_id,
            max_age=COOKIE_MAX_AGE_SECONDS,
            httponly=True,
            samesite="Lax",
            secure=request.is_secure,
        )

    return response


@app.route("/check-in", methods=["POST"])
def check_in():
    visitor_id = request.cookies.get(VISITOR_COOKIE)
    now = datetime.now(timezone.utc).isoformat()

    try:
        if visitor_id:
            execute_write(
                """
                INSERT INTO check_ins (active, visitor_id, checked_in_at)
                VALUES (1, ?, ?)
                """,
                (visitor_id, now),
            )
        else:
            # Backwards-compatible path for non-browser/legacy callers that do not
            # yet have the anonymous visitor cookie issued by the homepage.
            execute_write(
                "INSERT INTO check_ins (active, checked_in_at) VALUES (1, ?)",
                (now,),
            )
    except sqlite3.IntegrityError:
        log_event("check_in_rejected", reason="already_checked_in")
        return redirect(url_for("home", status="already-in"))

    log_event("check_in_completed")
    return redirect(url_for("home", status="checked-in"))


@app.route("/check-out", methods=["POST"])
def check_out():
    visitor_id = request.cookies.get(VISITOR_COOKIE)
    now = datetime.now(timezone.utc).isoformat()

    if visitor_id:
        changed = execute_write(
            """
            UPDATE check_ins
            SET active = 0, checked_out_at = ?
            WHERE id = (
                SELECT id
                FROM check_ins
                WHERE active = 1 AND visitor_id = ?
                ORDER BY id DESC
                LIMIT 1
            )
            """,
            (now, visitor_id),
        )
    else:
        # Keep the original route behavior for legacy callers without a cookie.
        changed = execute_write(
            """
            UPDATE check_ins
            SET active = 0, checked_out_at = ?
            WHERE id = (
                SELECT id
                FROM check_ins
                WHERE active = 1
                ORDER BY id
                LIMIT 1
            )
            """,
            (now,),
        )

    if changed == 0:
        log_event("check_out_rejected", reason="not_checked_in")
        return redirect(url_for("home", status="not-in"))

    log_event("check_out_completed")
    return redirect(url_for("home", status="checked-out"))


@app.route("/health")
def health():
    try:
        connection = get_db_connection()
        try:
            connection.execute("SELECT 1").fetchone()
        finally:
            connection.close()
    except sqlite3.Error as error:
        log_event("health_check_failed", level="ERROR", error_type=type(error).__name__)
        return jsonify({"status": "error", "database": "unavailable"}), 503

    return jsonify({"status": "ok", "database": "ok"})


init_db()


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
