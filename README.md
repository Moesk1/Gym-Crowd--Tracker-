# Gym Crowd Tracker

A student-built Flask prototype that helps students estimate how crowded the campus gym is before they make the trip.

> **Student prototype:** this is not an official University of Memphis service.

## What students can do

- See the current active crowd count.
- See a simple **Not Busy / Moderately Busy / Very Busy** crowd level.
- Check in when they arrive.
- Check out when they leave.
- Get clear feedback when they try an invalid action.
- Avoid duplicate check-ins from the same browser.

## Student experience

The interface is responsive for phones and laptops and uses the current University of Memphis primary color palette. The academic logo is referenced from the University's official site without modifying the mark.

The crowd thresholds can be adjusted without changing code:

```bash
MODERATE_CROWD_AT=10 VERY_BUSY_CROWD_AT=25 python app.py
```

## Reliability and observability

- SQLite persists check-in state.
- Existing databases are migrated automatically with backwards-compatible columns.
- Every request has a structured JSON log and request ID.
- Response duration is recorded in the logs.
- `/health` checks whether the application and SQLite database are reachable.
- Basic browser security headers are added to responses.
- GitHub Actions runs the automated test suite on pushes and pull requests.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

Optional local debug mode:

```bash
FLASK_DEBUG=1 python app.py
```

## Run tests

```bash
python -m pytest -v
```

## Stack

- Python 3.13
- Flask
- SQLite
- pytest
- GitHub Actions

## Branding

The prototype uses University of Memphis brand colors and the University's hosted academic logo. University marks remain the property of the University of Memphis. Do not present this student project as an official University service.
