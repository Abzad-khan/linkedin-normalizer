import re


# -------------------- HELPERS --------------------

def clean(text):
    """Convert to string, remove extra spaces"""
    return re.sub(r"\s+", " ", str(text or "")).strip()


def build_linkedin_url(public_id, existing_url):
    """Preserve or build LinkedIn URL"""
    if existing_url:
        return clean(existing_url)
    return f"https://www.linkedin.com/in/{clean(public_id)}"


def extract_name(first, last, full):
    """Ensure first, last, full are consistent"""
    full = clean(full)

    if full:
        parts = full.split(" ", 1)
        first = clean(parts[0])
        last = clean(parts[1]) if len(parts) > 1 else ""
    else:
        first = clean(first)
        last = clean(last)
        full = f"{first} {last}".strip()

    return first, last, full


def get_current_position(positions):
    """Find current role (end = None)"""
    for p in positions:
        if p.get("date_range", {}).get("end") is None:
            return p
    return positions[0] if positions else {}


# -------------------- MAIN NORMALIZER --------------------

def normalize_profile(data):
    if not isinstance(data, dict):
        raise TypeError("Input must be a dictionary")

    # ---------- NAME ----------
    first_name, last_name, full_name = extract_name(
        data.get("first_name"),
        data.get("last_name"),
        data.get("full_name"),
    )

    # ---------- LINKEDIN URL ----------
    linkedin_url = build_linkedin_url(
        data.get("public_identifier"),
        data.get("linkedin_url"),
    )

    # ---------- POSITIONS ----------
    raw_positions = data.get("positions") or []
    clean_positions = []

    for p in raw_positions:
        clean_positions.append({
            "title": clean(p.get("title")),
            "company_name": clean(p.get("company_name")),
            "location": clean(p.get("location")),
        })

    # ---------- CURRENT ROLE ----------
    current = get_current_position(raw_positions)

    current_role_title = clean(current.get("title"))
    company_name = clean(current.get("company_name"))

    # ---------- EDUCATIONS ----------
    raw_educations = data.get("educations") or []
    clean_educations = []

    for e in raw_educations:
        clean_educations.append({
            "school_name": clean(e.get("school_name")),
            "degree_name": clean(e.get("degree_name")),
            "field_of_study": clean(e.get("field_of_study")),
        })

    # ---------- PROFILE TEXT ----------
    headline = clean(data.get("headline"))
    summary = clean(data.get("summary"))

    profile_text = f"{headline} {summary}".strip().lower()

    # ---------- FINAL OUTPUT ----------
    return {
        "linkedin_url": linkedin_url,
        "first_name": first_name,
        "last_name": last_name,
        "full_name": full_name,
        "current_role_title": current_role_title,
        "company_name": company_name,
        "positions": clean_positions,
        "educations": clean_educations,
        "profile_text": profile_text,
    }