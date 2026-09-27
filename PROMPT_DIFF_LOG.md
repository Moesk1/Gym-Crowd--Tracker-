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