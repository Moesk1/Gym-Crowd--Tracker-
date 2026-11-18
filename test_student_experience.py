import sqlite3

import pytest
import app as gym_app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(gym_app, "DATABASE", tmp_path / "student_experience.db")
    gym_app.init_db()
    gym_app.app.config["TESTING"] = True
    return gym_app.app.test_client()


def active_count():
    with sqlite3.connect(gym_app.DATABASE) as connection:
        return connection.execute(
            "SELECT COUNT(*) FROM check_ins WHERE active = 1"
        ).fetchone()[0]


def test_homepage_issues_visitor_cookie_and_shows_brand(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Gym Crowd Tracker" in response.data
    assert b"The University of Memphis" in response.data
    assert gym_app.VISITOR_COOKIE in response.headers.get("Set-Cookie", "")
    assert response.headers.get("X-Request-ID")


def test_same_browser_cannot_check_in_twice(client):
    client.get("/")
    client.post("/check-in")
    response = client.post("/check-in", follow_redirects=True)

    assert active_count() == 1
    assert b"already checked in" in response.data


def test_browser_can_check_in_then_check_out(client):
    client.get("/")
    client.post("/check-in")
    response = client.post("/check-out", follow_redirects=True)

    assert response.status_code == 200
    assert active_count() == 0
    assert b"checked out" in response.data


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "database": "ok"}


def test_crowd_levels():
    assert gym_app.get_crowd_level(0)["label"] == "Not Busy"
    assert gym_app.get_crowd_level(gym_app.MODERATE_CROWD_AT)["label"] == "Moderately Busy"
    assert gym_app.get_crowd_level(gym_app.VERY_BUSY_CROWD_AT)["label"] == "Very Busy"


def test_security_headers(client):
    response = client.get("/")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    assert "default-src 'self'" in response.headers["Content-Security-Policy"]
