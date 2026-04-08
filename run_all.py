import json
import os
from normalizer import normalize_profile

# Folder path
fixtures_folder = "candidate_pack/fixtures"

total = 0
passed = 0

print("\n🚀 RUNNING ALL FILES...\n")

for file in os.listdir(fixtures_folder):
    if file.endswith(".json"):
        total += 1
        path = os.path.join(fixtures_folder, file)

        print(f"\n📄 Processing: {file}")

        try:
            # Load JSON
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Run your normalizer
            result = normalize_profile(data)

            # -------- VALIDATION --------

            # Required keys (as per checklist)
            required_keys = [
                "linkedin_url",
                "first_name",
                "last_name",
                "full_name",
                "current_role_title",
                "company_name",
                "positions",
                "educations",
                "profile_text"
            ]

            missing = [k for k in required_keys if k not in result]

            if missing:
                print(f"❌ Missing keys: {missing}")
                continue

            # Check types
            if not isinstance(result["positions"], list):
                print("❌ positions should be list")
                continue

            if not isinstance(result["educations"], list):
                print("❌ educations should be list")
                continue

            # Check profile_text lowercase
            if result["profile_text"] != result["profile_text"].lower():
                print("❌ profile_text not lowercase")
                continue

            print("✅ PASS")
            passed += 1

        except Exception as e:
            print(f"❌ ERROR: {e}")

# -------- FINAL REPORT --------

print("\n📊 FINAL RESULT")
print(f"TOTAL FILES: {total}")
print(f"PASSED: {passed}")
print(f"FAILED: {total - passed}")

if total == passed:
    print("\n🎉 ALL FILES PASSED SUCCESSFULLY!")
else:
    print("\n⚠️ SOME FILES FAILED")