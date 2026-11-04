# Gym Crowd Tracker — Incident Runbook

## Incident: Check In Returns an Error

### 1. Observable Symptom

A student clicks the Check In button, but the application displays an error instead of completing the check-in.

The operator may observe an HTTP 500 response in the application logs.

### 2. Initial Investigation

1. Open the Terminal where the Flask application is running.
2. Look for JSON log entries with `status_code` equal to 500 or an event named `request_failed`.
3. Find the `request_id` associated with the failed request.
4. Compare log entries with that same `request_id` to trace the operation.
5. Record the error type, timestamp, request path, and request ID.

### 3. Diagnose the Problem

A possible cause is that the SQLite database is unavailable, locked, or inaccessible.

From the project directory, run:

    ls -l gym.db
    df -h .

Check whether the database exists, whether the application has permission to access it, and whether the disk has free space.

Check database integrity using:

    python3 -c 'import sqlite3; c=sqlite3.connect("gym.db", timeout=2); print(c.execute("PRAGMA quick_check").fetchone()[0]); c.close()'

A result of `ok` means SQLite did not detect an integrity problem.

If the command fails, record the error message. Do not assume the database is corrupted.

### 4. Recovery Steps

1. Record the error and request ID before making changes.
2. If disk space is exhausted, notify the system owner and safely free space.
3. If database permissions are incorrect, ask the system owner to correct them.
4. If the database is locked, investigate other processes accessing it.
5. Once the underlying issue is resolved, restart the Flask application if needed.
6. Never delete or overwrite `gym.db` as a quick fix.

### 5. Verify Recovery

1. Open the Gym Crowd Tracker homepage.
2. Confirm that the crowd count loads successfully.
3. With permission, perform one test check-in and check-out.
4. Verify that both operations work and the count returns to its original value.
5. Check the JSON logs for successful requests and matching request IDs.

### 6. Escalation

If the error continues, contact the application maintainer.

Provide the timestamp, request ID, HTTP status, error type, diagnostic results, and actions already attempted.

Do not reset the database or change application code without approval.
