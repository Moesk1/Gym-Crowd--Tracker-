
from flask import Flask, g, redirect, render_template_string, request, url_for
import json
import logging
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

app = Flask(__name__)

DATABASE = Path(__file__).parent / "gym.db"


# Structured JSON logging setup
logger = logging.getLogger("gym_crowd_tracker")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)


def log_event(event, level="INFO", **details):
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "event": event,
        "request_id": getattr(g, "request_id", None),
        "method": request.method,
        "path": request.path,
        **details,
    }

    message = json.dumps(record)

    if level == "ERROR":
        logger.error(message)
    else:
        logger.info(message)


# Give every request a unique tracking ID
@app.before_request
def start_request():
    g.request_id = str(uuid.uuid4())
    log_event("request_started")


# Log the result of each request
@app.after_request
def finish_request(response):
    log_event(
        "request_completed",
        status_code=response.status_code
    )

    response.headers["X-Request-ID"] = g.request_id
    return response


# Record unexpected request failures
@app.teardown_request
def log_request_error(error):
    if error is not None:
        log_event(
            "request_failed",
            level="ERROR",
            error_type=type(error).__name__
        )


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS check_ins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                active INTEGER NOT NULL DEFAULT 1
            )
        """)
        connection.commit()
    finally:
        connection.close()


def get_crowd_count(connection):
    count = connection.execute(
        "SELECT COUNT(*) FROM check_ins WHERE active = 1"
    ).fetchone()[0]

    return count


def execute_write(sql):
    connection = get_db_connection()

    try:
        connection.execute(sql)
        connection.commit()
    finally:
        connection.close()


@app.route("/")
def home():
    connection = get_db_connection()

    try:
        crowd_count = get_crowd_count(connection)
    finally:
        connection.close()

    log_event(
        "crowd_count_viewed",
        crowd_count=crowd_count
    )

    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Gym Crowd Tracker</title>
            <link rel="icon" href="data:,">
        </head>
        <body>
            <h1>Gym Crowd Tracker</h1>
            <h2>Current Crowd Count: {{ crowd_count }}</h2>

            <form action="{{ url_for('check_in') }}"
                  method="post" style="display:inline">
                <button type="submit">Check In</button>
            </form>

            <form action="{{ url_for('check_out') }}"
                  method="post" style="display:inline">
                <button type="submit"
                    {% if crowd_count == 0 %}disabled{% endif %}>
                    Check Out
                </button>
            </form>
        </body>
        </html>
    """, crowd_count=crowd_count)


@app.route("/check-in", methods=["POST"])
def check_in():
    execute_write(
        "INSERT INTO check_ins (active) VALUES (1)"
    )

    log_event("check_in_completed")

    return redirect(url_for("home"))


@app.route("/check-out", methods=["POST"])
def check_out():
    execute_write("""
        UPDATE check_ins
        SET active = 0
        WHERE id = (
            SELECT id
            FROM check_ins
            WHERE active = 1
            LIMIT 1
        )
    """)

    log_event("check_out_completed")

    return redirect(url_for("home"))


init_db()


if __name__ == "__main__":
    app.run(debug=True)
