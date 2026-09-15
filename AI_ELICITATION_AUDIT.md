# Gym Crowd Tracker — AI Elicitation Audit

## AI Tool Used

GitHub Copilot

## Prompt Used

> Elicit requirements for a simple Gym Crowd Tracker web application. The app allows students to check into and out of a campus gym and see the current crowd level based on active check-ins. Give me 6–8 user stories with acceptance criteria and 3 non-functional requirements.

## What the AI Got Right

The AI correctly identified several important requirements for the Gym Crowd Tracker. It included student check-in and check-out, viewing the current crowd level, and viewing personal check-in status. It also correctly recognized that the occupancy count should increase after check-in and decrease after check-out. The AI also included requirements to prevent multiple active check-ins and prevent check-out when a student is not checked in.

## What the AI Missed

The AI missed some requirements that we considered important. It did not specifically require that the displayed crowd count cannot become negative. It also did not state that an invalid check-in or check-out must not change the crowd count. The AI also did not include our specific application startup requirement using Python 3.13, Flask, and SQLite.

## What the AI Invented

The AI added several features that were not part of our original project idea. It assumed that students would need to authenticate using campus credentials. It also added occupancy warnings, historical occupancy trends, and administrator capacity settings. These features were not required for our small version of the project.

The AI also changed the crowd categories to Low, Medium, High, and Full. Our requirements use three categories: Not Busy, Moderately Busy, and Very Busy.

## What the AI Added That We Had Not Thought Of

The AI introduced the idea of automatically updating the crowd information without requiring a full page refresh. It also suggested showing the timestamp of a student's active check-in. These could be useful features in a future version, but they are not necessary for the current scope.

## Final Judgment

The AI response was useful for finding additional ideas, but it should not be accepted as the final requirements document. It included features outside the current scope and missed some requirements that are important for keeping the crowd count accurate. The team's requirements are better for the current project because they keep the application simple and focused on checking in, checking out, and displaying the current crowd level.
