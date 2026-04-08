# Public Fixture Notes

## profile_1.json

- missing `linkedin_url`, so URL building is exercised
- missing `full_name`, so name composition is exercised
- `summary` is null
- current role appears before the past role
- past role includes a null nested location

## profile_2.json

- `linkedin_url` must be built
- `first_name` and `last_name` must be derived from `full_name`
- `headline` is null
- current role has a null title
- education includes a null degree name

## profile_3.json

- existing `linkedin_url` must be preserved
- `first_name` and `last_name` must be derived from `full_name`
- current role appears after a past role
- `summary` is null
- education includes a null `field_of_study`
