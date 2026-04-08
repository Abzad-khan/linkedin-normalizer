# Submission Checklist

Use this before submitting your solution.

- I return one normalized object per input profile.
- Every normalized object contains all required top-level fields.
- All final text fields are strings, not null.
- All final array fields are arrays, not null.
- `linkedin_url` is built when missing and preserved when already present.
- `full_name` is composed or split correctly.
- `current_role_title` comes from the first current position.
- `company_name` comes from the selected current position.
- `positions` only contains `title`, `company_name`, and `location`.
- `educations` only contains `school_name`, `degree_name`, and `field_of_study`.
- `profile_text` is lowercase.
- My script does not crash on missing or incomplete fields.
