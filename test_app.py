import sqlite3
import app as gym_app


def test_check_in_updates_count(tmp_path, monkeypatch):
    monkeypatch.setattr(gym_app, "DATABASE", tmp_path / "test.db")
    gym_app.init_db()

    client = gym_app.app.test_client()

    response = client.get("/")
    assert response.status_code == 200
    assert b"Current Crowd Count: 0" in response.data

    response = client.post("/check-in", follow_redirects=True)
    assert response.status_code == 200
    assert b"Current Crowd Count: 1" in response.data

    with sqlite3.connect(gym_app.DATABASE) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM check_ins WHERE active = 1"
        ).fetchone()[0]

    assert count == 1
