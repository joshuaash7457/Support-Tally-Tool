# Quick Troubleshooting Guide

## 🆘 Use This When Something Goes Wrong

---

## Problem: "python: command not found"

### Solution:
Try using `python3` instead:
```bash
python3 gmail_downloader.py
```

**If that doesn't work:**
- Python might not be installed
- Go to https://www.python.org/downloads/
- Download and install Python 3.x
- **Important:** Check "Add Python to PATH" during installation
- Restart terminal and try again

---

## Problem: "No module named 'googleapiclient'"

### Solution:
Install the required libraries:
```bash
pip install -r requirements.txt
```

**Or:**
```bash
pip3 install -r requirements.txt
```

**Or:**
```bash
python -m pip install -r requirements.txt
```

---

## Problem: "credentials.json not found"

### Check:
1. Is the file in your project folder?
2. Is it named EXACTLY `credentials.json` (lowercase)?
3. Is it in the same folder as `gmail_downloader.py`?

### Solution:
- Re-download from Google Cloud Console
- Make sure to rename it to `credentials.json`
- Put it in your project folder

---

## Problem: Gmail authorization keeps failing

### Solution 1: Re-authorize
```bash
# Delete the old token
# Windows:
del token.pickle

# Mac/Linux:
rm token.pickle

# Then run again:
python gmail_downloader.py
```

### Solution 2: Check OAuth setup
1. Go to https://console.cloud.google.com/
2. Select your project
3. APIs & Services → OAuth consent screen
4. Make sure your email is listed under "Test users"
5. Try authorization again

---

## Problem: "Google hasn't verified this app" warning

### This is NORMAL!

**What to do:**
1. Click "Advanced" (small link at bottom)
2. Click "Go to PTZOptics Email Downloader (unsafe)"
3. Click "Allow"

**Why this happens:**
- It's YOUR app, not a public app
- Google shows this warning for personal projects
- It's completely safe to proceed

---

## Problem: "No emails found"

### Check:
1. Is your Gmail query correct?
   - Check `monday_morning_automation.py` line 24
   - Make sure the email address is right
2. Are there actually emails in that time period?
3. Try a broader search:
   - Leave query blank (all emails)
   - Increase days back to 30

### Test:
```bash
python gmail_downloader.py
# Query: [leave blank]
# Days: 30
# Max: 10
```

If this finds emails, your query was too specific.

---

## Problem: Analysis shows weird results

### Check keywords.json:
1. Open `keywords.json`
2. Look for typos
3. Make sure it's valid JSON (use https://jsonlint.com/)
4. Keywords might be too broad or too specific

### Solution:
- Review top keywords in report
- Adjust keywords based on what's matching
- Re-run analysis

---

## Problem: Script crashes or freezes

### Solution 1: Check file size
Large mbox files take time. For a 10GB file:
- Expected time: 15-30 minutes
- This is normal!
- Look for progress messages

### Solution 2: Run with smaller dataset
```bash
python gmail_downloader.py
# Max emails: 100  ← Just download 100 for testing
```

### Solution 3: Check system resources
- Close other programs
- Make sure you have enough disk space
- Check that antivirus isn't blocking

---

## Problem: Can't find generated report

### Where to look:
Reports are saved in your project folder:
- `weekly_team_report_YYYYMMDD.txt`
- `email_report_YYYYMMDD.txt`
- `issue_report_*.txt`

### Check:
```bash
# Windows:
dir *.txt

# Mac/Linux:
ls *.txt
```

This shows all .txt files in your folder.

---

## Problem: Week-over-week comparison not showing

### This is normal for first run!

The system needs data from a previous week to compare.

**After your second week**, you'll see trends like:
- ↑ (+12.3%)
- ↓ (-5.2%)
- → (+1.1%)

---

## Problem: Multiple team members sharing setup

### Don't share credentials!

Each person needs:
1. Their own `credentials.json`
2. Their own authorization
3. Access to the support Gmail account

**Setup per person:**
- Follow FIRST_TIME_SETUP_GUIDE.md
- Each person authorizes their own account
- Keep credential files private

---

## Problem: File permission errors

### Windows:
- Right-click project folder → Properties
- Make sure "Read-only" is unchecked
- Click Apply

### Mac/Linux:
```bash
chmod -R 755 /path/to/PTZOptics-Email-Analysis
```

---

## Problem: Gmail API quota exceeded

**Very rare, but if you see this:**

- Gmail API has generous limits
- Usually means you downloaded 10,000+ emails in an hour
- Wait 1 hour and try again
- Consider downloading in smaller batches

---

## Problem: Report looks messy in email

### Solution:
Reports are plain text formatted for terminal viewing.

**To share:**
1. Attach the .txt file to email (don't paste content)
2. Recipients open as attachment
3. Or copy key sections only

**Future improvement:**
- Consider converting to PDF or HTML for prettier sharing

---

## Problem: Can't run automated Task Scheduler

### Windows Task Scheduler:
Make sure you used full paths:
- **Program:** Full path to python.exe
  - Example: `C:\Python39\python.exe`
- **Arguments:** Just the script name
  - Example: `monday_morning_automation.py`
- **Start in:** Full path to project folder
  - Example: `C:\Users\YourName\Documents\PTZOptics-Email-Analysis`

---

## Problem: Getting duplicate emails

### Check:
Are you running the downloader multiple times on the same day?

### Solution:
- Delete old mbox files before downloading new ones
- Or use different filenames
- The automation script uses dated filenames automatically

---

## Quick Diagnostic Commands

### Check Python:
```bash
python --version
# or
python3 --version
```

### Check Libraries:
```bash
pip list | grep google
# Should show: google-api-python-client, google-auth, etc.
```

### Check Files:
```bash
# Windows:
dir

# Mac/Linux:
ls -la
```

### Test Gmail Connection:
```bash
python gmail_downloader.py
# If authentication works, Gmail API is set up correctly
```

---

## Still Stuck?

### Review These Guides:
1. **FIRST_TIME_SETUP_GUIDE.md** - Complete setup steps
2. **GMAIL_SETUP_GUIDE.md** - Detailed Gmail API instructions
3. **SECURITY_GUIDE.md** - Credential issues

### Common Mistakes Checklist:
- [ ] Using `python` when you need `python3`
- [ ] `credentials.json` not in project folder
- [ ] `credentials.json` has wrong name (includes numbers)
- [ ] Not in project folder when running commands
- [ ] OAuth consent screen not configured
- [ ] Email not added as test user
- [ ] Trying to share credentials between users

---

## Emergency Reset

If everything is broken and you want to start fresh:

### 1. Delete authentication files:
```bash
# Windows:
del token.pickle
del credentials.json

# Mac/Linux:
rm token.pickle
rm credentials.json
```

### 2. Delete in Google Cloud:
- Go to https://console.cloud.google.com/
- Select your project
- APIs & Services → Credentials
- Delete the OAuth Client ID
- Go to OAuth consent screen → Reset to configure again

### 3. Start over from STEP 5 in FIRST_TIME_SETUP_GUIDE.md

---

## Contact / Help

- Review documentation in your project folder
- All guides are .md files you can open in any text editor
- Take screenshots of error messages if asking for help
