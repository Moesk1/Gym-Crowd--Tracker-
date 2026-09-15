# Gym Crowd Tracker — Requirements

## User Stories

### US-01 — Student Check-In

**As a** student,
**I want** to check into the gym,
**so that** I can be included in the current crowd count.

**Acceptance Criteria:**

* The student can select a check-in option.
* A successful check-in increases the active user count by 1.
* The same student cannot be counted as checked in twice.
### US-02 — Student Check-Out

**As a** student,
**I want** to check out of the gym,
**so that** I am no longer included in the current crowd count.

**Acceptance Criteria:**

* The student can select a check-out option.
* A successful check-out decreases the active user count by 1.
* A student who is not checked in cannot check out.
### US-03 — View Current Crowd Count

**As a** student,
**I want** to see the current number of people checked into the gym,
**so that** I can know how many people are currently there.

**Acceptance Criteria:**

* The current number of active check-ins is displayed.
* The count increases after a successful check-in.
* The count decreases after a successful check-out.
* The displayed count cannot be negative.
### US-04 — View Crowd Level

**As a** student,
**I want** to see whether the gym is not busy, moderately busy, or very busy,
**so that** I can quickly decide when to visit.

**Acceptance Criteria:**

* The app displays one of three crowd levels: **Not Busy, Moderately Busy, or Very Busy**.
* The crowd level is based on the current number of active check-ins.
* The crowd level changes when the active check-in count reaches a different level.
### US-04 — View Crowd Level

**As a** student,
**I want** to see whether the gym is not busy, moderately busy, or very busy,
**so that** I can quickly decide when to visit.

**Acceptance Criteria:**

* The app displays one of three crowd levels: **Not Busy, Moderately Busy, or Very Busy**.
* The crowd level is based on the current number of active check-ins.
* The crowd level changes when the active check-in count reaches a different level.
### US-05 — Check-In Status

**As a** student,
**I want** to know whether I am currently checked into the gym,
**so that** I know whether I should check in or check out.

**Acceptance Criteria:**

* The app shows whether the student is currently checked in.
* A checked-in student has a check-out option.
* A student who is not checked in has a check-in option.
### US-06 — Store Check-In Information

**As a** system administrator,
**I want** the app to store check-in and check-out information,
**so that** the current crowd count can be calculated accurately.

**Acceptance Criteria:**

* A successful check-in is stored in the database.
* A successful check-out updates the student's status.
* The system can use the stored information to calculate the current number of checked-in students.
### US-07 — Prevent Invalid Check-In and Check-Out

**As a** student,
**I want** the app to prevent invalid check-in and check-out actions,
**so that** the crowd count stays accurate.

**Acceptance Criteria:**

* A student cannot check in twice without checking out.
* A student cannot check out if they are not checked in.
* The app displays an error message when an invalid action is attempted.
* An invalid action does not change the crowd count.
## Non-Functional Requirements

### NFR-01 — Response Time

The app must display the result of a check-in or check-out action within **2 seconds** on the local development machine.

### NFR-02 — Crowd Count Accuracy

The displayed crowd count must match the number of active check-ins stored in the database with **0 difference** after every successful check-in or check-out.

### NFR-03 — Application Startup

The app must successfully start and display the main page using the documented startup command on a computer with **Python 3.13, Flask, and SQLite** installed.
