# Prompt-and-Diff Log

## AI Tool

GitHub Copilot

## Prompt

> Elicit requirements for a simple Gym Crowd Tracker web application. The app allows students to check into and out of a campus gym and see the current crowd level based on active check-ins. Give me 6–8 user stories with acceptance criteria and 3 non-functional requirements.

## AI Use

GitHub Copilot was used to generate a separate set of proposed requirements for comparison with the team's requirements.

## Changes Made After AI Review

The AI-generated requirements were not copied directly into the requirements document. The team reviewed the response and identified requirements that were missing, invented, or useful.

The team's requirements document was written separately and kept focused on the current scope of the Gym Crowd Tracker.

## Diff Summary

* Added the team's own 7 user stories and 3 non-functional requirements.
* Did not add campus authentication because it was not part of the current project scope.
* Did not add historical occupancy trends or administrator capacity settings because they were outside the current scope.
* Kept the requirement that invalid check-in and check-out actions must not change the crowd count.
* Kept the three crowd levels: Not Busy, Moderately Busy, and Very Busy.
## Domain Model AI Use

AI Tool: ChatGPT

Prompt:
Using my M2 requirements for the Gym Crowd Tracker, draft an ER domain model for the application. Provide the domain model in Mermaid ER diagram syntax. Include the entities, important attributes, and relationships you think the application needs.

AI Output:
The AI suggested Student, Check-In, Crowd Level, and Administrator entities with their attributes and relationships.

Changes After Review:
- Removed the Administrator entity because it was not necessary for the first version.
- Kept Student and Check-In for tracking gym check-ins and check-outs.
- Kept Crowd Level for displaying Not Busy, Moderately Busy, or Very Busy.
- Simplified the model to better match the project requirements.

Final Result:
The reviewed domain model is saved in `DOMAIN_MODEL.md`. The original AI draft is saved in `AI_DOMAIN_MODEL_FIRST_DRAFT.md`.
## ADR-001 AI Use

AI Tool: ChatGPT

Prompt:
Help me review an Architecture Decision Record for my Gym Crowd Tracker. The real decision is using SQLite to store student check-in and check-out data instead of keeping the data only in Python memory or using PostgreSQL. The ADR needs context, the decision, alternatives considered, and consequences.

AI Assistance:
AI was used to help organize the ADR and explain the tradeoffs between SQLite, Python in-memory storage, and PostgreSQL.

Changes After Review:
- Kept SQLite because it is already part of the project stack and fits a small local application.
- Included Python in-memory storage as an alternative because it is simpler but loses data when the app restarts.
- Included PostgreSQL as an alternative because it can support a larger system but requires more setup.
- Added disadvantages of SQLite, including limitations with many simultaneous writes and possible migration work if the application grows.
- Kept the ADR focused on a decision that was actually made for the Gym Crowd Tracker.

Final Result:
The final architecture decision record is saved in `docs/adr/ADR-001.md`.
## Walking Skeleton and CI

### AI Tool
GitHub Copilot

### Prompt
Help me create a simple end-to-end walking skeleton for my Gym Crowd Tracker using Flask, SQLite, pytest, and GitHub Actions. The app should allow a user to check in and check out, store the data, and display the current crowd count.

### AI Output
GitHub Copilot helped with the Flask routes, SQLite storage, testing, and GitHub Actions CI setup.

### Changes After Review
- Kept the application simple and focused on the gym crowd count.
- Used SQLite for real data storage instead of mock data.
- Added Check In and Check Out functionality.
- Added a test to verify the application works.
- Added GitHub Actions to automatically run the test.
- Did not add extra features that were outside the current milestone.

### Final Result
The app now has a working end-to-end path from the webpage to Flask, SQLite storage, and back to the webpage. The GitHub Actions CI workflow also runs successfully.

## Testing and Bug-Injection Milestone

### AI Tool
ChatGPT

### Prompt
Help me write acceptance tests and unit tests for my Gym Crowd Tracker using Flask, SQLite, and pytest. Help me generate a coverage report and prove that my tests can catch a realistic bug.

### AI Assistance
AI helped me expand my original test suite from 1 test to 8 tests. It also helped me separate the crowd-counting logic into its own function.

### Changes Made
- Added tests for checking in and checking out.
- Added a test for checking out when the gym is empty.
- Tested multiple check-ins and refreshing the webpage.
- Added unit tests for the crowd-counting function.
- Used real temporary SQLite databases instead of mock data.
- Generated a code coverage report using pytest-cov.

### Bug-Injection Demonstration
I intentionally changed one line in the crowd-counting function.

Original code:
`SELECT COUNT(*) FROM check_ins WHERE active = 1`

Buggy code:
`SELECT COUNT(*) FROM check_ins WHERE active = 0`

This caused the application to count inactive records instead of active check-ins.

### Test Results
Before injecting the bug: 8 tests passed.

After injecting the bug: 5 tests failed and 3 passed.

After fixing the bug: All 8 tests passed again.

### What I Learned
This demonstration showed that my tests can catch a real counting mistake. I learned that passing tests are important, but it is also important to prove that the tests fail when the application behaves incorrectly.

### Final Result
The application has acceptance tests, counting-function tests, a coverage report, and evidence showing that the test suite detects an intentionally introduced bug.

## Refactoring Milestone

### AI Tool
ChatGPT

### Prompt Summary
Help me refactor repeated database code without changing how my Gym Crowd Tracker works, and verify the same tests pass before and after.

### AI Assistance and Changes
ChatGPT helped review the repeated SQLite write code and verify the refactor. The Check In and Check Out routes repeated the steps for opening a connection, executing SQL, committing, and closing the connection. I replaced those repeated steps with one execute_write(sql) helper.

### What I Kept
I kept the same SQL operations, routes, redirects, and crowd-counting behavior. I left test_app.py unchanged.

### Verification
All eight tests passed before the refactor, and the same eight passed afterward. The SHA-256 hashes of the original and final test files matched exactly.

### What Became Easier
The routes are shorter and easier to follow. If I need to change how database writes are handled, I can update the helper instead of repeating the change in both routes.
