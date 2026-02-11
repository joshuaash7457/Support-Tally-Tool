# PTZOptics Email Analysis System - First Time Setup Guide

**Welcome!** This guide will walk you through setting up the complete email analysis system from scratch. Follow these steps in order and you'll be running automated reports in about 30 minutes.

---

## 📋 What You'll Need

- [ ] Windows PC (or Mac/Linux - commands are similar)
- [ ] Python 3.6 or higher installed
- [ ] Gmail account with access to support emails
- [ ] 30 minutes of time
- [ ] Internet connection

---

## 🎯 Overview: What We're Setting Up

By the end of this guide, you'll have:
- ✅ All tools installed and configured
- ✅ Gmail API connected for fast email downloads
- ✅ Automated weekly reports ready to run
- ✅ Critical issue tracking configured

---

## 📁 STEP 1: Create Your Project Folder

### Windows:
1. Open File Explorer
2. Navigate to a location you'll remember (e.g., `C:\Users\YourName\Documents\`)
3. Right-click → New → Folder
4. Name it: `PTZOptics-Email-Analysis`

### Mac:
1. Open Finder
2. Go to your home folder or Documents
3. Right-click → New Folder
4. Name it: `PTZOptics-Email-Analysis`

### Your folder path will be something like:
- **Windows:** `C:\Users\YourName\Documents\PTZOptics-Email-Analysis`
- **Mac:** `/Users/YourName/Documents/PTZOptics-Email-Analysis`

**📝 Write down this path - you'll need it!**

---

## 📥 STEP 2: Download All Files

You should have received all these files. Place them ALL in your `PTZOptics-Email-Analysis` folder:

### Core Programs (Required):
```
gmail_downloader.py
email_analyzer_mbox.py
issue_tracker.py
weekly_report_generator.py
monday_morning_automation.py
automated_weekly_download.py
```

### Configuration Files (Required):
```
keywords.json
.gitignore
requirements.txt
```

### Example Issue Configs (Optional but Recommended):
```
cmp_autotracking_issue.json
example_firmware_reboot_issue.json
example_ndi_obs_issue.json
example_preset_issue.json
```

### Documentation (Keep for Reference):
```
README.md
GMAIL_SETUP_GUIDE.md
MBOX_GUIDE.md
ISSUE_TRACKER_GUIDE.md
QUICK_REFERENCE.md
SECURITY_GUIDE.md
AUTOMATED_REPORTING_GUIDE.md
COMPLETE_OVERVIEW.md
```

### After downloading, your folder should look like this:
```
PTZOptics-Email-Analysis/
├── gmail_downloader.py
├── email_analyzer_mbox.py
├── issue_tracker.py
├── weekly_report_generator.py
├── monday_morning_automation.py
├── keywords.json
├── requirements.txt
├── .gitignore
├── (all the other files)
└── (documentation .md files)
```

**✅ Checkpoint:** You should have about 20 files total in your folder.

---

## 🐍 STEP 3: Verify Python Installation

### Check if Python is Installed:

1. **Open Command Prompt (Windows) or Terminal (Mac):**
   - **Windows:** Press `Win + R`, type `cmd`, press Enter
   - **Mac:** Press `Cmd + Space`, type `terminal`, press Enter

2. **Check Python version:**
   ```bash
   python --version
   ```
   
   **OR** (if above doesn't work):
   ```bash
   python3 --version
   ```

3. **You should see something like:**
   ```
   Python 3.9.7
   ```
   
   **✅ Good:** Any version 3.6 or higher works!
   
   **❌ Problem:** If you see "command not found" or an error, you need to install Python first.

### If You Need to Install Python:

1. Go to: https://www.python.org/downloads/
2. Download the latest Python 3.x version
3. **IMPORTANT:** During installation, check the box that says "Add Python to PATH"
4. Install and restart your computer
5. Try the version check again

**📝 Note:** Some systems use `python3` instead of `python`. Use whichever works!

---

## 📦 STEP 4: Install Required Libraries

Now we'll install the Python libraries needed for Gmail API.

### Navigate to Your Project Folder:

**Windows:**
```bash
cd C:\Users\YourName\Documents\PTZOptics-Email-Analysis
```

**Mac:**
```bash
cd /Users/YourName/Documents/PTZOptics-Email-Analysis
```

**💡 Tip:** You can type `cd ` (with a space) and then drag your project folder into the terminal window - it will auto-fill the path!

### Install Libraries:

```bash
pip install -r requirements.txt
```

**OR** (if `pip` doesn't work):
```bash
pip3 install -r requirements.txt
```

**What you'll see:**
```
Collecting google-api-python-client
Downloading...
Installing...
Successfully installed google-api-python-client-2.x.x ...
```

**This will take 1-2 minutes.**

**✅ Checkpoint:** You should see "Successfully installed" messages with no errors.

**❌ If you see errors:** Try:
```bash
python -m pip install -r requirements.txt
```

---

## 🔑 STEP 5: Set Up Gmail API (Most Important!)

This is the one-time setup to connect to Gmail. Follow carefully!

### 5.1: Go to Google Cloud Console

1. Open your web browser
2. Go to: https://console.cloud.google.com/
3. Sign in with your Google account (the one with support email access)

### 5.2: Create a New Project

1. Click **"Select a project"** at the top of the page
2. Click **"NEW PROJECT"** in the popup
3. **Project name:** `PTZOptics Email Downloader`
4. Click **"CREATE"**
5. Wait 5-10 seconds for it to create
6. Click **"Select a project"** again and select your new project

**✅ Checkpoint:** You should see "PTZOptics Email Downloader" at the top of the page.

### 5.3: Enable Gmail API

1. In the left sidebar, click **"APIs & Services"** → **"Library"**
   - OR go directly to: https://console.cloud.google.com/apis/library
2. In the search box, type: **"Gmail API"**
3. Click on **"Gmail API"** in the results
4. Click the blue **"ENABLE"** button
5. Wait a few seconds

**✅ Checkpoint:** You should see "API enabled" with a green checkmark.

### 5.4: Configure OAuth Consent Screen

1. In the left sidebar, click **"APIs & Services"** → **"OAuth consent screen"**
2. Select **"External"** (unless you have Google Workspace, then choose Internal)
3. Click **"CREATE"**

**Fill in the form:**
- **App name:** `PTZOptics Email Downloader`
- **User support email:** Select your email from dropdown
- **Developer contact information:** Enter your email

4. Click **"SAVE AND CONTINUE"**

**On the Scopes page:**
- Just click **"SAVE AND CONTINUE"** (don't add anything)

**On the Test users page:**
- Click **"ADD USERS"**
- Enter your email address
- Click **"ADD"**
- Click **"SAVE AND CONTINUE"**

5. Review the summary and click **"BACK TO DASHBOARD"**

**✅ Checkpoint:** OAuth consent screen is configured!

### 5.5: Create OAuth Credentials

1. In the left sidebar, click **"APIs & Services"** → **"Credentials"**
2. Click **"CREATE CREDENTIALS"** at the top
3. Select **"OAuth client ID"**

**Fill in the form:**
- **Application type:** Select **"Desktop app"**
- **Name:** `PTZOptics Email Downloader`

4. Click **"CREATE"**

### 5.6: Download Credentials File

**A popup will appear with your credentials:**

1. Click **"DOWNLOAD JSON"** button
2. The file will download (usually to your Downloads folder)
3. **Find the downloaded file** - it will be named something like:
   - `client_secret_123456789-abc.apps.googleusercontent.com.json`

4. **Rename it to exactly:** `credentials.json`

5. **Move it to your project folder:**
   - Cut/Copy the file from Downloads
   - Paste it into your `PTZOptics-Email-Analysis` folder

**✅ CRITICAL CHECKPOINT:** 
You should now have a file called `credentials.json` in your project folder next to all the .py files.

**❌ Common mistake:** The file MUST be named exactly `credentials.json` (all lowercase, no extra numbers)

---

## 🔐 STEP 6: First Authorization (One-Time)

Now we'll connect your Google account to the tool.

### 6.1: Open Terminal in Project Folder

**Windows:**
```bash
cd C:\Users\YourName\Documents\PTZOptics-Email-Analysis
```

**Mac:**
```bash
cd /Users/YourName/Documents/PTZOptics-Email-Analysis
```

### 6.2: Run the Downloader

```bash
python gmail_downloader.py
```

**OR:**
```bash
python3 gmail_downloader.py
```

### 6.3: Authorize in Browser

**Your web browser will automatically open.**

**You might see a warning:** "Google hasn't verified this app"

**This is normal! It's YOUR app, so it's safe.**

**Click:**
1. **"Advanced"** (small text at bottom)
2. **"Go to PTZOptics Email Downloader (unsafe)"**
3. Select your Google account
4. **Click "Continue"**
5. Review permissions (it's read-only access to Gmail)
6. **Click "Allow"**

**Browser will show:** "The authentication flow has completed."

**You can close the browser.**

### 6.4: Verify Authorization

Back in your terminal, you should see:

```
✓ Authentication successful!

DOWNLOAD OPTIONS
--------------------------------------------------
What emails do you want to download?
```

**Perfect!** Type `Ctrl+C` to exit for now. Authorization is complete!

**✅ Checkpoint:** A file called `token.pickle` was created in your folder.

**🎉 You'll never need to do this authorization again!**

---

## ⚙️ STEP 7: Configure for Your Support Email

Now let's customize the settings for PTZOptics.

### 7.1: Edit Monday Morning Automation

1. Open `monday_morning_automation.py` in a text editor (Notepad, VS Code, etc.)
2. Find lines 24-26 (near the top):

**Current:**
```python
GMAIL_QUERY = "to:support@ptzoptics.com"
DAYS_BACK = 7
```

**Change to your actual support email:**
```python
GMAIL_QUERY = "to:YOUR-ACTUAL-SUPPORT-EMAIL@ptzoptics.com"
DAYS_BACK = 7
```

3. **Save the file**

### 7.2: Customize Keywords (Optional)

The default keywords are good for PTZOptics, but you can customize:

1. Open `keywords.json` in a text editor
2. Add/remove/modify categories and keywords as needed
3. Save the file

**💡 Tip:** Start with the defaults and adjust after your first report!

### 7.3: Review Issue Configs (Optional)

Check out the example issue configs:
- `cmp_autotracking_issue.json`
- `example_firmware_reboot_issue.json`
- `example_ndi_obs_issue.json`

These track specific critical issues. You can:
- Use them as-is
- Modify them for your needs
- Create new ones (copy an example and edit)

**For now, the examples are fine to start with.**

---

## 🧪 STEP 8: Test Run (Make Sure Everything Works!)

Let's do a test to make sure everything is working.

### 8.1: Test Gmail Download

In your terminal (in project folder):

```bash
python gmail_downloader.py
```

**When prompted:**
- **Search query:** Press Enter (leave blank for all emails)
- **Days back:** Type `2` (just last 2 days for testing)
- **Max emails:** Type `10` (just 10 emails for testing)
- **Output filename:** Press Enter (use default)

**You should see:**
```
Searching Gmail with query: after:2025/02/08
Found 10 messages
Downloading 10 messages...
Progress: 10/10 (100.0%)

✓ DOWNLOAD COMPLETE!
Downloaded: 10 emails
Saved to: gmail_emails_20250210_143022.mbox
```

**✅ Success!** You just downloaded emails!

### 8.2: Test Analysis

```bash
python email_analyzer_mbox.py
```

**When prompted:**
- **File path:** Enter the name of the mbox file from step 8.1
  (e.g., `gmail_emails_20250210_143022.mbox`)

**You should see:**
```
Loaded 10 emails from gmail_emails_20250210_143022.mbox
Analyzing emails...

EMAIL ANALYSIS REPORT
=====================
Total Emails Analyzed: 10
[... report data ...]
```

**✅ Success!** Analysis is working!

---

## 🎉 STEP 9: Your First Real Weekly Report

Now let's generate your first actual weekly report!

### 9.1: Run Monday Morning Automation

```bash
python monday_morning_automation.py
```

**The script will:**
1. ✅ Ask for confirmation - type `y` and press Enter
2. ✅ Download last week's emails (~30 seconds)
3. ✅ Analyze all categories
4. ✅ Track critical issues
5. ✅ Generate formatted team report

**You'll see:**
```
✓ DOWNLOAD COMPLETE!
✓ Analysis complete!
✓ Report saved to: weekly_team_report_20250210.txt

See you next Monday! 👋
```

### 9.2: Review Your Report

1. Open `weekly_team_report_20250210.txt` in your project folder
2. You should see a formatted report with:
   - Volume metrics
   - Top 5 issues
   - Critical issues tracked
   - Key insights
   - Recommended actions

**🎉 Congratulations! You just generated your first automated report!**

---

## 📅 STEP 10: Set Up for Weekly Use

Now that everything works, here's your weekly routine:

### Every Monday Morning:

1. **Open terminal in project folder**
2. **Run:**
   ```bash
   python monday_morning_automation.py
   ```
3. **Wait 2-3 minutes** (grab coffee ☕)
4. **Review report:** `weekly_team_report_YYYYMMDD.txt`
5. **Share with team** via email or meeting

**That's it!** 5 minutes total.

---

## 🔄 Optional: Full Automation

Want it to run automatically every Monday at 9 AM?

### Windows (Task Scheduler):

1. Open **Task Scheduler** (search in Start menu)
2. Click **"Create Basic Task"**
3. **Name:** "PTZOptics Weekly Report"
4. **Trigger:** Weekly, Monday, 9:00 AM
5. **Action:** Start a program
   - **Program:** `python` (or `python3`)
   - **Arguments:** `monday_morning_automation.py`
   - **Start in:** `C:\Users\YourName\Documents\PTZOptics-Email-Analysis`
6. **Finish**

Now it runs automatically every Monday!

### Mac (Cron - Advanced):

```bash
# Edit crontab
crontab -e

# Add this line:
0 9 * * 1 cd /Users/YourName/Documents/PTZOptics-Email-Analysis && python3 monday_morning_automation.py
```

---

## 🆘 Troubleshooting Common Issues

### "python: command not found"
**Fix:** Use `python3` instead of `python` everywhere

### "credentials.json not found"
**Fix:** Make sure `credentials.json` is in your project folder and named exactly that

### "No module named 'googleapiclient'"
**Fix:** Re-run: `pip install -r requirements.txt`

### "Authentication failed"
**Fix:** Delete `token.pickle` and run `gmail_downloader.py` again to re-authorize

### "No emails found"
**Fix:** Check your GMAIL_QUERY is correct and there are actually emails in that time period

### Gmail authorization keeps asking to sign in
**Fix:** Make sure you added your email as a "test user" in OAuth consent screen

---

## 📋 Quick Reference Card (Print This!)

### Monday Morning Routine:
```
1. Open Terminal
2. cd C:\Users\YourName\Documents\PTZOptics-Email-Analysis
3. python monday_morning_automation.py
4. Review weekly_team_report_YYYYMMDD.txt
5. Share with team
```

### Manual Email Download:
```
python gmail_downloader.py
```

### Track Specific Issue:
```
python issue_tracker.py
```

### Analyze Existing mbox:
```
python email_analyzer_mbox.py
```

---

## ✅ Setup Complete Checklist

Go through this checklist to make sure everything is set up:

- [ ] Python 3.6+ installed and working
- [ ] Project folder created with all files
- [ ] Libraries installed (`pip install -r requirements.txt`)
- [ ] Google Cloud project created
- [ ] Gmail API enabled
- [ ] OAuth consent screen configured
- [ ] OAuth credentials created
- [ ] `credentials.json` downloaded and in project folder
- [ ] First authorization completed (`token.pickle` exists)
- [ ] Email address configured in `monday_morning_automation.py`
- [ ] Test download successful
- [ ] Test analysis successful
- [ ] First weekly report generated successfully

**If all boxes are checked, you're ready to go! 🎉**

---

## 📞 Getting Help

### Check the Documentation:
- **GMAIL_SETUP_GUIDE.md** - Detailed Gmail API setup
- **AUTOMATED_REPORTING_GUIDE.md** - Report customization
- **COMPLETE_OVERVIEW.md** - Full system overview
- **SECURITY_GUIDE.md** - Security best practices

### Common Questions:

**Q: Can multiple team members use this?**
A: Yes! Each person needs their own `credentials.json` and does their own authorization. Don't share credential files!

**Q: Will this delete emails?**
A: No! It's read-only access. Cannot delete or modify emails.

**Q: Can I customize the categories?**
A: Yes! Edit `keywords.json` to add/remove/change categories.

**Q: How do I track a new issue?**
A: Copy an example issue config, rename it, edit the keywords, and it will be tracked automatically.

**Q: What if I work from multiple computers?**
A: Set it up on each computer separately (each needs its own credentials).

---

## 🎓 Next Steps

Once you're comfortable with the basics:

1. **Customize keywords** to match your actual support patterns
2. **Create issue configs** for known problems
3. **Set up automation** so reports run automatically
4. **Archive reports** for historical trending
5. **Share insights** with engineering team regularly

---

## 🎉 Congratulations!

You now have a professional-grade email analysis system that:
- ✅ Downloads emails in 30 seconds (not 9 hours!)
- ✅ Analyzes trends automatically
- ✅ Tracks critical issues
- ✅ Generates formatted team reports
- ✅ Provides week-over-week insights
- ✅ Runs with one command

**Welcome to data-driven support! 🚀**

---

**Version:** 1.0
**Last Updated:** February 2026
**For:** PTZOptics Support Team
