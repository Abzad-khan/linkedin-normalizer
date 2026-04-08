# LinkedIn Voyager Profile Normalizer

A lightweight Python utility that transforms messy, inconsistently shaped
**LinkedIn Voyager-style JSON payloads** into a single clean canonical profile
object — no external dependencies required.

---

## Project Structure

```
linkedin_normalizer/
├── normalizer.py          # Core normalization logic
├── tests/
│   └── test_normalizer.py # Full pytest test suite
└── README.md
```

---

## What It Does

LinkedIn's internal Voyager API returns profile data in many shapes depending
on the endpoint, API version, and fields requested. This utility handles:

| Variant | Example |
|---|---|
| Nested Voyager (`positionView`, `educationView`, `skillView`) | Standard `/identity/profiles/{id}` response |
| Flat / simplified shape | Lightweight or third-party scraped payloads |
| `profile`-wrapped payloads | Responses where data is nested under a `profile` key |
| Mixed / partial payloads | Profiles missing optional fields |

### Canonical Output Shape

```python
{
    "id": "ACoAAABjK9oBSample",        # extracted from URN or id field
    "name": {
        "first": "Jane",
        "last": "Doe",
        "full": "Jane Doe"
    },
    "headline": "Senior Software Engineer @ Acme Corp",
    "summary": "Passionate about scalable systems.",
    "location": {
        "city": "San Francisco",
        "country": "US",
        "full": "San Francisco, California"
    },
    "profile_url": "https://www.linkedin.com/in/janedoe",
    "photo_url": "https://media.licdn.com/dms/image/sample.jpg",
    "connections": 523,
    "followers": 1200,
    "experience": [
        {
            "title": "Senior Software Engineer",
            "company": "Acme Corp",
            "start": {"year": 2021, "month": 3},
            "end": None,
            "current": True,
            "description": "Led backend team."
        }
    ],
    "education": [
        {
            "school": "MIT",
            "degree": "B.S.",
            "field": "Computer Science",
            "start_year": 2014,
            "end_year": 2018
        }
    ],
    "skills": ["Python", "Distributed Systems", "Kubernetes"],
    "contact": {
        "email": "jane@example.com",
        "phone": "+1-415-555-0100",
        "twitter": "janedoe_dev",
        "websites": ["https://janedoe.dev"]
    }
}
```

---

## Requirements

- **Python 3.8+**
- No third-party packages needed for the core utility
- `pytest` for running tests

---

## Installation

```bash
# Clone or copy the project folder
cd linkedin_normalizer

# (Optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install pytest (only needed for tests)
pip install pytest
```

---

## Usage

```python
from normalizer import normalize_profile

raw_payload = {
    "entityUrn": "urn:li:fs_profile:ACoAAExample",
    "firstName": "Jane",
    "lastName": "Doe",
    "headline": "Engineer @ Acme",
    # ... rest of Voyager payload
}

profile = normalize_profile(raw_payload)
print(profile["name"]["full"])   # Jane Doe
print(profile["headline"])       # Engineer @ Acme
```

### Error Handling

```python
try:
    profile = normalize_profile(raw)
except TypeError as e:
    print(f"Invalid input: {e}")
```

---

## Running Tests

From the **project root** (`linkedin_normalizer/`):

```bash
# Run all tests with verbose output
pytest tests/test_normalizer.py -v

# Run a specific test class
pytest tests/test_normalizer.py::TestExperience -v

# Run with coverage (requires pytest-cov)
pip install pytest-cov
pytest tests/test_normalizer.py --cov=normalizer --cov-report=term-missing
```

### Expected Output

```
tests/test_normalizer.py::TestNormalizeProfile::test_returns_dict          PASSED
tests/test_normalizer.py::TestNormalizeProfile::test_raises_on_non_dict    PASSED
...
============= 45 passed in 0.12s =============
```

---

## Key Design Decisions

- **Zero dependencies** — uses only the Python standard library (`re`, `typing`)
- **Defensive fallbacks** — every field gracefully handles `None`, missing keys, and unexpected types
- **URL sanitisation** — strips tracking query params, normalises HTTP→HTTPS, removes trailing slashes
- **Deduplication** — skills list is deduplicated while preserving insertion order
- **URN parsing** — extracts the canonical ID from LinkedIn URN strings automatically

---

## Extending

To add support for a new payload field, add a `_normalize_*` helper in
`normalizer.py` and include its output in the `normalize_profile` return dict.
Follow the existing pattern: accept `raw: dict`, return a clean value.
