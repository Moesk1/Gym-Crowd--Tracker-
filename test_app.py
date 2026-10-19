
import sqlite3
import pytest
import app as gym_app


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Use a separate database for each test
    monkeypatch.setattr(gym_app, "DATABASE", tmp_path / "test.db")
    gym_app.init_db()
    gym_app.app.config["TESTING"] = True
    return gym_app.app.test_client()


def get_active_count():
    # Read the real count from SQLite
    with sqlite3.connect(gym_app.DATABASE) as connection:
        return connection.execute(
            "SELECT COUNT(*) FROM check_ins WHERE active = 1"
        ).fetchone()[0]


# Acceptance test: test the complete check-in process
def test_student_check_in(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Current Crowd Count: 0" in response.data

    response = client.post("/check-in", follow_redirects=True)

    assert response.status_code == 200
    assert b"Current Crowd Count: 1" in response.data
    assert get_active_count() == 1


# Test checking out
def test_student_check_out(client):
    client.post("/check-in")
    response = client.post("/check-out", follow_redirects=True)

    assert response.status_code == 200
    assert b"Current Crowd Count: 0" in response.data
    assert get_active_count() == 0


# Test checking out when the gym is empty
def test_check_out_when_empty(client):
    response = client.post("/check-out", follow_redirects=True)

    assert response.status_code == 200
    assert b"Current Crowd Count: 0" in response.data
    assert get_active_count() == 0


# Test that multiple check-ins update the count
def test_multiple_check_ins(client):
    client.post("/check-in")
    client.post("/check-in")
    client.post("/check-in")

    response = client.get("/")

    assert b"Current Crowd Count: 3" in response.data
    assert get_active_count() == 3


# Test that refreshing keeps the saved count
def test_count_stays_after_refresh(client):
    client.post("/check-in")
    client.post("/check-in")

    response = client.get("/")

    assert response.status_code == 200
    assert b"Current Crowd Count: 2" in response.data
    assert get_active_count() == 2

def test_crowd_count_empty(client):
    connection = gym_app.get_db_connection()
    try:
        assert gym_app.get_crowd_count(connection) == 0
    finally:
        connection.close()


def test_crowd_count_with_active_records(client):
    client.post("/check-in")
    client.post("/check-in")

    connection = gym_app.get_db_connection()
    try:
        assert gym_app.get_crowd_count(connection) == 2
    finally:
        connection.close()


def test_crowd_count_ignores_inactive_records(client):
    client.post("/check-in")
    client.post("/check-in")
    client.post("/check-out")

    connection = gym_app.get_db_connection()
    try:
        assert gym_app.get_crowd_count(connection) == 1
    finally:
        connection.close()
