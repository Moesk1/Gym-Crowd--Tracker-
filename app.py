from flask import Flask, redirect, render_template_string, url_for
import sqlite3
from pathlib import Path

app = Flask(__name__)
DATABASE = Path(__file__).parent / "gym.db"


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


@app.route("/")
def home():
    connection = get_db_connection()
    try:
        crowd_count = connection.execute(
            "SELECT COUNT(*) FROM check_ins WHERE active = 1"
        ).fetchone()[0]
    finally:
        connection.close()

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

            <form action="{{ url_for('check_in') }}" method="post" style="display:inline">
                <button type="submit">Check In</button>
            </form>

            <form action="{{ url_for('check_out') }}" method="post" style="display:inline">
                <button type="submit" {% if crowd_count == 0 %}disabled{% endif %}>Check Out</button>
            </form>
        </body>
        </html>
    """, crowd_count=crowd_count)


@app.route("/check-in", methods=["POST"])
def check_in():
    connection = get_db_connection()
    try:
        connection.execute("INSERT INTO check_ins (active) VALUES (1)")
        connection.commit()
    finally:
        connection.close()

    return redirect(url_for("home"))


@app.route("/check-out", methods=["POST"])
def check_out():
    connection = get_db_connection()
    try:
        connection.execute(
            "UPDATE check_ins SET active = 0 "
            "WHERE id = (SELECT id FROM check_ins WHERE active = 1 LIMIT 1)"
        )
        connection.commit()
    finally:
        connection.close()

    return redirect(url_for("home"))


init_db()

if __name__ == "__main__":
    app.run(debug=True)