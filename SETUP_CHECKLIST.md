# PTZOptics Email Analysis - Setup Checklist
**Print this page and check off each step as you complete it!**

---

## 📋 Pre-Setup

- [ ] I have a Windows/Mac computer
- [ ] I have Python 3.6 or higher installed
- [ ] I have access to PTZOptics support Gmail account
- [ ] I have 30 minutes available
- [ ] I have internet connection

---

## 📁 Step 1: Project Folder

- [ ] Created folder: `PTZOptics-Email-Analysis`
- [ ] I know the full path to my folder
- [ ] Path written down: ___________________________________

---

## 📥 Step 2: Files Downloaded

Downloaded and placed in project folder:

**Core Programs:**
- [ ] gmail_downloader.py
- [ ] email_analyzer_mbox.py
- [ ] issue_tracker.py
- [ ] weekly_report_generator.py
- [ ] monday_morning_automation.py

**Configuration:**
- [ ] keywords.json
- [ ] requirements.txt
- [ ] .gitignore

**Examples:**
- [ ] cmp_autotracking_issue.json
- [ ] example_firmware_reboot_issue.json
- [ ] example_ndi_obs_issue.json

**Documentation:**
- [ ] README.md
- [ ] FIRST_TIME_SETUP_GUIDE.md
- [ ] All other .md guide files

**TOTAL FILES: Should have ~20 files in folder**

---

## 🐍 Step 3: Python Verified

- [ ] Opened terminal/command prompt
- [ ] Ran: `python --version` or `python3 --version`
- [ ] Confirmed version 3.6 or higher
- [ ] Know which command works: python ☐  OR  python3 ☐

---

## 📦 Step 4: Libraries Installed

- [ ] Navigated to project folder in terminal
- [ ] Ran: `pip install -r requirements.txt`
- [ ] Saw "Successfully installed" messages
- [ ] No errors appeared

---

## 🔑 Step 5: Gmail API Setup

### Google Cloud Console:
- [ ] Logged into https://console.cloud.google.com/
- [ ] Created new project: "PTZOptics Email Downloader"
- [ ] Project selected in dropdown at top

### Gmail API:
- [ ] Went to APIs & Services → Library
- [ ] Found and enabled "Gmail API"
- [ ] Saw "API enabled" confirmation

### OAuth Consent Screen:
- [ ] Configured OAuth consent screen
- [ ] Selected "External" user type
- [ ] Filled in app name and emails
- [ ] Added myself as test user
- [ ] Saved all screens

### Credentials:
- [ ] Created OAuth Client ID
- [ ] Selected "Desktop app" type
- [ ] Downloaded credentials JSON file
- [ ] Renamed file to exactly: `credentials.json`
- [ ] Moved to project folder
- [ ] File is in same folder as .py files

**CRITICAL: credentials.json is in project folder ✓**

---

## 🔐 Step 6: First Authorization

- [ ] Ran: `python gmail_downloader.py` (or `python3`)
- [ ] Browser opened automatically
- [ ] Clicked "Advanced" → "Go to... (unsafe)"
- [ ] Selected my Google account
- [ ] Clicked "Allow" for permissions
- [ ] Browser showed "authentication flow completed"
- [ ] Closed browser
- [ ] Terminal showed "Authentication successful!"
- [ ] File `token.pickle` created in project folder

**DONE WITH ONE-TIME SETUP! ✓**

---

## ⚙️ Step 7: Configuration

- [ ] Opened `monday_morning_automation.py` in text editor
- [ ] Changed `GMAIL_QUERY` to actual support email
- [ ] Email changed to: ___________________________________
- [ ] Saved file

---

## 🧪 Step 8: Test Run

### Test Download:
- [ ] Ran: `python gmail_downloader.py`
- [ ] Downloaded 10 test emails (2 days back)
- [ ] Mbox file created successfully
- [ ] Mbox filename: ___________________________________

### Test Analysis:
- [ ] Ran: `python email_analyzer_mbox.py`
- [ ] Entered mbox filename from above
- [ ] Report generated successfully
- [ ] No errors occurred

**TESTS PASSED! ✓**

---

## 🎉 Step 9: First Weekly Report

- [ ] Ran: `python monday_morning_automation.py`
- [ ] Confirmed with 'y'
- [ ] Downloaded last week's emails
- [ ] Analysis completed
- [ ] Report generated
- [ ] Opened weekly_team_report_YYYYMMDD.txt
- [ ] Report looks good!

**FIRST REPORT COMPLETE! 🎊**

---

## 📅 Step 10: Weekly Setup

- [ ] Know how to run weekly: `python monday_morning_automation.py`
- [ ] Understand the 5-minute Monday routine
- [ ] (Optional) Set up Task Scheduler automation
- [ ] Scheduled for: Day _________ Time _________

---

## ✅ FINAL VERIFICATION

Everything working:
- [ ] Can download emails from Gmail (fast!)
- [ ] Can analyze emails automatically
- [ ] Can generate formatted team reports
- [ ] Week-over-week comparison working (after 2nd week)
- [ ] No errors in any step

---

## 📝 NOTES / ISSUES

Write down any problems or questions:

_______________________________________________________________

_______________________________________________________________

_______________________________________________________________

_______________________________________________________________

---

## 🆘 IF STUCK

Check these in order:
1. [ ] TROUBLESHOOTING.md in project folder
2. [ ] FIRST_TIME_SETUP_GUIDE.md (detailed steps)
3. [ ] GMAIL_SETUP_GUIDE.md (Gmail API help)

---

## 🎯 SUCCESS!

If all boxes above are checked, you're ready to use the system!

**Your Monday Morning Routine:**
1. Open terminal
2. Navigate to project folder
3. Run: `python monday_morning_automation.py`
4. Wait 2-3 minutes
5. Review and share report

**That's it! 🚀**

---

**Setup Completed By:** ___________________________________

**Date:** ___________________________________

**Python Version:** ___________________________________

**Project Folder Path:** ___________________________________

_______________________________________________________________

---

**Print Date:** _______________    **Version:** 1.0
