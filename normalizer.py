import re


def normalize_profile(data):
    def clean(x):
        return re.sub(r"\s+", " ", str(x or "")).strip()

    # ---------- PUBLIC ID ----------
    public_id = clean(data.get("public_identifier"))

    # ---------- LINKEDIN URL ----------
    linkedin_url = data.get("linkedin_url")
    if linkedin_url:
        linkedin_url = clean(linkedin_url)
    else:
        linkedin_url = f"https://www.linkedin.com/in/{public_id}/"

    # ---------- NAME ----------
    full = clean(data.get("full_name"))

    if full:
        parts = full.split(" ", 1)
        first = parts[0]
        last = parts[1] if len(parts) > 1 else ""
    else:
        first = clean(data.get("first_name"))
        last = clean(data.get("last_name"))
        full = f"{first} {last}".strip()

    # ---------- BASIC FIELDS ----------
    headline = clean(data.get("headline"))
    summary = clean(data.get("summary"))
    location = clean(data.get("location_name"))

    # ---------- POSITIONS ----------
    positions = data.get("positions") or []

    clean_positions = []
    for p in positions:
        clean_positions.append({
            "title": clean(p.get("title")),
            "company_name": clean(p.get("company_name")),
            "location": clean(p.get("location")),
        })

    # ---------- CURRENT ROLE ----------
    current = {}
    for p in positions:
        if p.get("date_range", {}).get("end") is None:
            current = p
            break

    if not current and positions:
        current = positions[0]

    current_title = clean(current.get("title"))
    current_company = clean(current.get("company_name"))

    # ---------- EDUCATIONS ----------
    educations = data.get("educations") or []

    clean_educations = []
    for e in educations:
        clean_educations.append({
            "school_name": clean(e.get("school_name")),
            "degree_name": clean(e.get("degree_name")),
            "field_of_study": clean(e.get("field_of_study")),
        })

    # ---------- PROFILE TEXT ----------
    profile_parts = []

    if headline:
        profile_parts.append(headline)

    if location:
        profile_parts.append(location)

    for p in clean_positions:
        if p["title"]:
            profile_parts.append(p["title"])
        if p["company_name"]:
            profile_parts.append(p["company_name"])

    profile_text = " ".join(profile_parts).lower()

    # ---------- FINAL OUTPUT ----------
    return {
        "public_identifier": public_id,
        "linkedin_url": linkedin_url,
        "first_name": first,
        "last_name": last,
        "full_name": full,
        "headline": headline,
        "current_role_title": current_title,
        "company_name": current_company,
        "location_name": location,
        "summary": summary,
        "positions": clean_positions,
        "educations": clean_educations,
        "profile_text": profile_text,
    }