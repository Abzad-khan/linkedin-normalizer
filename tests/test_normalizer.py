"""
Unit tests for LinkedIn Voyager Profile Normalizer.
Run with:  pytest tests/test_normalizer.py -v
"""

import pytest
from normalizer import normalize_profile, _clean_url, _extract_urn_id, _safe_str


# ---------------------------------------------------------------------------
# Fixtures – sample raw payloads
# ---------------------------------------------------------------------------

@pytest.fixture
def voyager_full():
    """Realistic Voyager-style payload with nested structures."""
    return {
        "entityUrn": "urn:li:fs_profile:ACoAAABjK9oBSample",
        "firstName": "Jane",
        "lastName": "Doe",
        "headline": "Senior Software Engineer @ Acme Corp",
        "summary": "Passionate about scalable systems.",
        "geoLocation": {
            "city": "San Francisco",
            "country": "US",
            "defaultLocalizedName": "San Francisco, California",
        },
        "profileUrl": "https://www.linkedin.com/in/janedoe?trk=public_profile",
        "miniProfile": {
            "picture": {
                "rootUrl": "https://media.licdn.com/dms/image/sample.jpg?e=123"
            }
        },
        "connectionsCount": 523,
        "followersCount": 1200,
        "positionView": {
            "elements": [
                {
                    "title": "Senior Software Engineer",
                    "company": {"miniCompany": {"name": "Acme Corp"}},
                    "timePeriod": {
                        "startDate": {"year": 2021, "month": 3},
                    },
                    "description": "Led backend team.",
                },
                {
                    "title": "Software Engineer",
                    "company": {"miniCompany": {"name": "Beta LLC"}},
                    "timePeriod": {
                        "startDate": {"year": 2018, "month": 6},
                        "endDate": {"year": 2021, "month": 2},
                    },
                    "description": "",
                },
            ]
        },
        "educationView": {
            "elements": [
                {
                    "schoolName": "MIT",
                    "degreeName": "B.S.",
                    "fieldOfStudy": "Computer Science",
                    "timePeriod": {
                        "startDate": {"year": 2014},
                        "endDate": {"year": 2018},
                    },
                }
            ]
        },
        "skillView": {
            "elements": [
                {"name": "Python"},
                {"name": "Distributed Systems"},
                {"name": "Kubernetes"},
            ]
        },
        "contactInfo": {
            "emailAddress": "jane@example.com",
            "phoneNumbers": [{"number": "+1-415-555-0100"}],
            "twitterHandles": [{"name": "janedoe_dev"}],
            "websites": [{"url": "https://janedoe.dev?ref=li"}],
        },
    }


@pytest.fixture
def voyager_minimal():
    """Minimal payload with only required fields."""
    return {
        "firstName": "John",
        "lastName": "Smith",
    }


@pytest.fixture
def voyager_flat():
    """Flat payload shape (alternative Voyager variant)."""
    return {
        "id": "john123",
        "full_name": "John Smith",
        "occupation": "Product Manager",
        "about": "Building great products.",
        "location": "New York, NY",
        "connections": 300,
        "followers": 450,
        "experience": [
            {
                "title": "Product Manager",
                "companyName": "Startup Inc",
                "startDate": {"year": 2020, "month": 1},
                "description": "Led product roadmap.",
            }
        ],
        "education": [
            {
                "schoolName": "Harvard",
                "degree": "MBA",
                "field_of_study": "Business",
                "startYear": 2015,
                "endYear": 2017,
            }
        ],
        "skills": ["Strategy", "Roadmapping", "Agile"],
        "contact": {
            "email": "john@example.com",
        },
    }


@pytest.fixture
def voyager_nested_profile():
    """Payload where everything is under a 'profile' key."""
    return {
        "profile": {
            "entityUrn": "urn:li:fs_profile:XYZ789",
            "firstName": "Alice",
            "lastName": "Wonder",
            "headline": "UX Designer",
        }
    }


# ---------------------------------------------------------------------------
# Core normalization tests
# ---------------------------------------------------------------------------

class TestNormalizeProfile:

    def test_returns_dict(self, voyager_full):
        result = normalize_profile(voyager_full)
        assert isinstance(result, dict)

    def test_raises_on_non_dict(self):
        with pytest.raises(TypeError):
            normalize_profile("not a dict")

    def test_raises_on_none(self):
        with pytest.raises(TypeError):
            normalize_profile(None)

    def test_empty_dict_returns_canonical_shape(self):
        result = normalize_profile({})
        assert set(result.keys()) == {
            "id", "name", "headline", "summary", "location",
            "profile_url", "photo_url", "connections", "followers",
            "experience", "education", "skills", "contact",
        }


class TestIdExtraction:

    def test_urn_id_extracted(self, voyager_full):
        result = normalize_profile(voyager_full)
        assert result["id"] == "ACoAAABjK9oBSample"

    def test_flat_id_used(self, voyager_flat):
        result = normalize_profile(voyager_flat)
        assert result["id"] == "john123"

    def test_nested_urn_extracted(self, voyager_nested_profile):
        result = normalize_profile(voyager_nested_profile)
        assert result["id"] == "XYZ789"

    def test_empty_id_when_missing(self, voyager_minimal):
        result = normalize_profile(voyager_minimal)
        assert result["id"] == ""


class TestNameNormalization:

    def test_first_last_full(self, voyager_full):
        name = normalize_profile(voyager_full)["name"]
        assert name["first"] == "Jane"
        assert name["last"] == "Doe"
        assert name["full"] == "Jane Doe"

    def test_minimal_name(self, voyager_minimal):
        name = normalize_profile(voyager_minimal)["name"]
        assert name["first"] == "John"
        assert name["last"] == "Smith"
        assert name["full"] == "John Smith"

    def test_full_name_flat(self, voyager_flat):
        name = normalize_profile(voyager_flat)["name"]
        assert name["full"] == "John Smith"

    def test_nested_profile_name(self, voyager_nested_profile):
        name = normalize_profile(voyager_nested_profile)["name"]
        assert name["first"] == "Alice"
        assert name["last"] == "Wonder"


class TestHeadline:

    def test_headline_extracted(self, voyager_full):
        assert normalize_profile(voyager_full)["headline"] == "Senior Software Engineer @ Acme Corp"

    def test_occupation_fallback(self, voyager_flat):
        assert normalize_profile(voyager_flat)["headline"] == "Product Manager"

    def test_empty_headline_when_missing(self, voyager_minimal):
        assert normalize_profile(voyager_minimal)["headline"] == ""


class TestSummary:

    def test_summary_extracted(self, voyager_full):
        assert normalize_profile(voyager_full)["summary"] == "Passionate about scalable systems."

    def test_about_fallback(self, voyager_flat):
        assert normalize_profile(voyager_flat)["summary"] == "Building great products."


class TestLocation:

    def test_full_location_object(self, voyager_full):
        loc = normalize_profile(voyager_full)["location"]
        assert loc["city"] == "San Francisco"
        assert loc["country"] == "US"
        assert "San Francisco" in loc["full"]

    def test_string_location(self, voyager_flat):
        loc = normalize_profile(voyager_flat)["location"]
        assert loc["full"] == "New York, NY"

    def test_missing_location(self, voyager_minimal):
        loc = normalize_profile(voyager_minimal)["location"]
        assert loc == {"city": "", "country": "", "full": ""}


class TestProfileUrl:

    def test_tracking_params_stripped(self, voyager_full):
        url = normalize_profile(voyager_full)["profile_url"]
        assert "?" not in url
        assert url.startswith("https://")

    def test_auto_generated_url_from_id(self, voyager_nested_profile):
        url = normalize_profile(voyager_nested_profile)["profile_url"]
        assert "XYZ789" in url

    def test_http_upgraded_to_https(self):
        raw = {"id": "test", "profileUrl": "http://www.linkedin.com/in/test"}
        url = normalize_profile(raw)["profile_url"]
        assert url.startswith("https://")


class TestPhotoUrl:

    def test_photo_from_mini_profile(self, voyager_full):
        photo = normalize_profile(voyager_full)["photo_url"]
        assert "licdn.com" in photo
        assert "?" not in photo

    def test_missing_photo_is_empty(self, voyager_minimal):
        assert normalize_profile(voyager_minimal)["photo_url"] == ""


class TestCounts:

    def test_connections_and_followers(self, voyager_full):
        result = normalize_profile(voyager_full)
        assert result["connections"] == 523
        assert result["followers"] == 1200

    def test_flat_connections(self, voyager_flat):
        result = normalize_profile(voyager_flat)
        assert result["connections"] == 300
        assert result["followers"] == 450

    def test_zero_when_missing(self, voyager_minimal):
        result = normalize_profile(voyager_minimal)
        assert result["connections"] == 0
        assert result["followers"] == 0


class TestExperience:

    def test_experience_count(self, voyager_full):
        exp = normalize_profile(voyager_full)["experience"]
        assert len(exp) == 2

    def test_current_position_has_no_end(self, voyager_full):
        exp = normalize_profile(voyager_full)["experience"]
        current = exp[0]
        assert current["current"] is True
        assert current["end"] is None

    def test_past_position_has_end(self, voyager_full):
        exp = normalize_profile(voyager_full)["experience"]
        past = exp[1]
        assert past["current"] is False
        assert past["end"]["year"] == 2021

    def test_flat_experience(self, voyager_flat):
        exp = normalize_profile(voyager_flat)["experience"]
        assert exp[0]["title"] == "Product Manager"
        assert exp[0]["company"] == "Startup Inc"

    def test_empty_experience(self, voyager_minimal):
        assert normalize_profile(voyager_minimal)["experience"] == []


class TestEducation:

    def test_education_extracted(self, voyager_full):
        edu = normalize_profile(voyager_full)["education"]
        assert len(edu) == 1
        assert edu[0]["school"] == "MIT"
        assert edu[0]["degree"] == "B.S."
        assert edu[0]["field"] == "Computer Science"
        assert edu[0]["start_year"] == 2014
        assert edu[0]["end_year"] == 2018

    def test_flat_education(self, voyager_flat):
        edu = normalize_profile(voyager_flat)["education"]
        assert edu[0]["school"] == "Harvard"
        assert edu[0]["degree"] == "MBA"


class TestSkills:

    def test_skills_from_skill_view(self, voyager_full):
        skills = normalize_profile(voyager_full)["skills"]
        assert "Python" in skills
        assert "Kubernetes" in skills

    def test_flat_skills_list(self, voyager_flat):
        skills = normalize_profile(voyager_flat)["skills"]
        assert skills == ["Strategy", "Roadmapping", "Agile"]

    def test_skills_deduplicated(self):
        raw = {"skills": ["Python", "Python", "Go"]}
        skills = normalize_profile(raw)["skills"]
        assert skills.count("Python") == 1

    def test_empty_skills(self, voyager_minimal):
        assert normalize_profile(voyager_minimal)["skills"] == []


class TestContact:

    def test_contact_full(self, voyager_full):
        contact = normalize_profile(voyager_full)["contact"]
        assert contact["email"] == "jane@example.com"
        assert contact["phone"] == "+1-415-555-0100"
        assert contact["twitter"] == "janedoe_dev"
        assert len(contact["websites"]) == 1
        assert "?" not in contact["websites"][0]

    def test_flat_contact(self, voyager_flat):
        contact = normalize_profile(voyager_flat)["contact"]
        assert contact["email"] == "john@example.com"

    def test_missing_contact(self, voyager_minimal):
        contact = normalize_profile(voyager_minimal)["contact"]
        assert contact == {"email": "", "phone": "", "twitter": "", "websites": []}


# ---------------------------------------------------------------------------
# Helper function tests
# ---------------------------------------------------------------------------

class TestHelpers:

    def test_clean_url_strips_query(self):
        assert _clean_url("https://example.com/path?foo=bar") == "https://example.com/path"

    def test_clean_url_strips_trailing_slash(self):
        assert _clean_url("https://example.com/") == "https://example.com"

    def test_clean_url_upgrades_http(self):
        assert _clean_url("http://example.com") == "https://example.com"

    def test_clean_url_empty(self):
        assert _clean_url(None) == ""
        assert _clean_url("") == ""

    def test_extract_urn_id(self):
        assert _extract_urn_id("urn:li:fs_profile:ABC123") == "ABC123"

    def test_extract_urn_id_empty(self):
        assert _extract_urn_id("") == ""
        assert _extract_urn_id(None) == ""

    def test_safe_str_none(self):
        assert _safe_str(None) == ""

    def test_safe_str_strips(self):
        assert _safe_str("  hello  ") == "hello"
