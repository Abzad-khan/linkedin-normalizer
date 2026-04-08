# Expected Output Contract

This document is safe to share with participants.

## Target Output Shape

For each input profile JSON, produce one normalized JSON object with this exact shape:

```json
{
  "public_identifier": "string",
  "linkedin_url": "string",
  "first_name": "string",
  "last_name": "string",
  "full_name": "string",
  "headline": "string",
  "current_role_title": "string",
  "company_name": "string",
  "location_name": "string",
  "summary": "string",
  "positions": [
    {
      "title": "string",
      "company_name": "string",
      "location": "string"
    }
  ],
  "educations": [
    {
      "school_name": "string",
      "degree_name": "string",
      "field_of_study": "string"
    }
  ],
  "profile_text": "string"
}
```

## Field Expectations

- Every top-level field above must exist in the final output.
- Use empty strings for missing text values.
- Use empty arrays for missing array values.
- `positions` must contain only:
  - `title`
  - `company_name`
  - `location`
- `educations` must contain only:
  - `school_name`
  - `degree_name`
  - `field_of_study`

## Normalization Rules

- Trim and collapse whitespace in all strings.
- Convert null text fields to empty strings.
- Convert null arrays to `[]`.
- If `linkedin_url` is missing and `public_identifier` exists, build:
  - `https://www.linkedin.com/in/<public_identifier>/`
- If `linkedin_url` is already present, preserve it exactly.
- If `full_name` is missing but `first_name` and/or `last_name` exist, build `full_name` from them.
- If `first_name` and `last_name` are missing but `full_name` exists, split it sensibly.
- For deterministic evaluation, use:
  - first token -> `first_name`
  - remaining tokens -> `last_name`
- `current_role_title` should come from the first current position.
- A position counts as current if `date_range.end` is missing or null.
- `company_name` should come from the same chosen current position.
- `profile_text` should be a lowercase concatenation of:
  - headline
  - summary
  - location_name
  - position titles
  - position company names
  - position locations
  - education school names
  - education degree names
  - education field_of_study values

## Output Behavior Requirements

- Produce one normalized object per input file.
- Do not crash on incomplete payloads.
- Preserve valid existing values when the rule does not require rebuilding them.
- Return valid JSON.

## Accepted Submission Output Styles

If you are being tested with the shared evaluator, your submission may return results in any of these ways:

1. Print JSON to stdout
2. Write one combined JSON file
3. Write one JSON file per input profile into an output directory

Accepted JSON container styles:

1. A list of normalized objects in fixture order
2. A dictionary keyed by filename like `profile_1.json`
3. A dictionary keyed by stem like `profile_1`
4. A wrapper object containing `profiles`, `results`, `items`, or `data`

## Public Reminder

The public fixtures are examples only. Final evaluation may include additional hidden cases that follow the same contract and normalization rules.
