# LinkedIn Profile Normalizer

This project processes LinkedIn-style profile JSON data and converts it into a clean, structured format.

---

## 🧰 Requirements

- Python 3 installed  

Check Python version:

```bash
python --version
```

---

## 📥 Setup

### Option 1: Clone from GitHub

```bash
git clone https://github.com/Abzad-khan/linkedin-normalizer.git
cd linkedin-normalizer
```

### Option 2: Download ZIP

1. Download ZIP from GitHub  
2. Extract it  
3. Open terminal inside the folder  

---

## 📂 Project Structure

```
linkedin_normalizer/
├── normalizer.py
├── run_all.py
├── candidate_pack/
│   ├── fixtures/
│   │   ├── profile_1.json
│   │   ├── profile_2.json
│   │   └── profile_3.json
```

---

## 🚀 How to Run

### Step 1: Open terminal in project folder

```bash
cd linkedin_normalizer
```

### Step 2: Run script

```bash
python run_all.py
```

---

## ✅ Expected Output

You should see:

```
🚀 RUNNING ALL FILES...

📄 Processing: profile_1.json
✅ PASS

📄 Processing: profile_2.json
✅ PASS

📄 Processing: profile_3.json
✅ PASS

📊 FINAL RESULT
TOTAL FILES: 3
PASSED: 3
FAILED: 0

🎉 ALL FILES PASSED SUCCESSFULLY!
```

---

## ❗ Troubleshooting

### If python command not working

```bash
python3 run_all.py
```

---

### If file not found error

Make sure this folder exists:

```
candidate_pack/fixtures/
```

---

### If module error occurs

Ensure both files are in the same folder:

```
normalizer.py
run_all.py
```

---

## 📌 What This Project Does

- Reads all JSON profiles from candidate_pack/fixtures
- Normalizes them using normalizer.py
- Cleans and standardizes the data
- Validates output
- Displays pass/fail results
