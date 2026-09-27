# Gym Crowd Tracker — Domain Model

## Final Reviewed Domain Model

```mermaid
erDiagram
    STUDENT {
        int student_id PK
        string name
        boolean is_checked_in
    }

    CHECK_IN {
        int check_in_id PK
        int student_id FK
        datetime check_in_time
        datetime check_out_time
        boolean active
    }

    CROWD_LEVEL {
        int crowd_level_id PK
        string level_name
        int minimum_count
        int maximum_count
    }

    STUDENT ||--o{ CHECK_IN : has
    CHECK_IN }o--|| CROWD_LEVEL : determines

    ## Review Notes

The AI-generated model was reviewed and simplified to match the actual requirements of the Gym Crowd Tracker.

Changes made:
- Removed the Administrator entity because it is not necessary for the first version of the application.
- Kept Student and Check-In because they are needed to track who is currently checked in.
- Kept Crowd Level because the application displays Not Busy, Moderately Busy, or Very Busy based on the current crowd count.
- Kept the domain model simple so it matches the scope of the project.