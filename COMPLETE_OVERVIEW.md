# PTZOptics Email Analysis System - Complete Overview

## 📦 What You Have Now

A complete email analysis toolkit with **3 main components**:

### 1. **Gmail Downloader** (NEW!)
Fast email collection from Gmail
- Downloads emails in seconds (vs hours with Google Takeout)
- Filter by date, sender, subject, labels
- Saves to mbox format
- **Use this weekly to get new emails**

### 2. **General Email Analyzer**
Track overall support trends
- Analyzes 10+ categories at once
- Shows keyword breakdowns
- Weekly trend reports
- **Use this for weekly reports**

### 3. **Critical Issue Tracker**
Monitor specific problems
- Laser-focused on ONE issue
- Precise matching criteria
- Customer follow-up lists
- **Use this for firmware bugs, feature failures, etc.**

---

## 🚀 Complete Weekly Workflow

### Monday Morning Routine (5 minutes)

**Step 1: Download Last Week's Emails (30 seconds)**
```bash
python gmail_downloader.py
```
- Query: `to:support@ptzoptics.com`
- Days: `7`
- Output: `weekly_emails.mbox`

**Step 2: Generate General Report (2 minutes)**
```bash
python email_analyzer_mbox.py
```
- File: `weekly_emails.mbox`
- Get overview of all issue categories

**Step 3: Check Critical Issues (1 minute each)**
```bash
python issue_tracker.py
```
- Use existing issue configs (CMP autotracking, firmware bugs, etc.)
- See if any issues spiking

**Done! Share reports with team.**

---

## 📁 Files Explained

### Core Programs
```
gmail_downloader.py              # Downloads emails from Gmail
email_analyzer_mbox.py           # General trend analysis
issue_tracker.py                 # Specific issue tracking
automated_weekly_download.py     # Optional automation
```

### Configuration Files
```
credentials.json                 # Gmail API credentials (you create)
token.pickle                     # Gmail auth token (auto-generated)
keywords.json                    # General analyzer categories
cmp_autotracking_issue.json      # Example issue config
example_*.json                   # More issue examples
```

### Documentation
```
GMAIL_SETUP_GUIDE.md            # How to set up Gmail API (one-time)
MBOX_GUIDE.md                   # Using the general analyzer
ISSUE_TRACKER_GUIDE.md          # Using the issue tracker
QUICK_REFERENCE.md              # Cheat sheet
README.md                       # Original project readme
```

### Generated Files (examples)
```
weekly_emails.mbox              # Downloaded emails
email_report_20250127.txt       # General analysis report
issue_report_CMP-AT-001.txt     # Issue tracking report
affected_emails_CMP-AT-001.csv  # Customer follow-up list
```

---

## 🎯 Use Case Examples

### Use Case 1: Weekly Support Overview

**Goal:** What did customers complain about this week?

**Tools:** Gmail Downloader → General Analyzer

**Steps:**
1. Download: `python gmail_downloader.py` (last 7 days)
2. Analyze: `python email_analyzer_mbox.py`
3. Review report showing top issues by category

**Output:** 
```
CONNECTION ISSUES: 45 mentions (32 emails)
FIRMWARE: 28 mentions (23 emails)
PTZ CONTROL: 14 mentions (12 emails)
```

---

### Use Case 2: Firmware Bug Monitoring

**Goal:** Track specific bug in firmware 3.2.1 causing reboots

**Tools:** Gmail Downloader → Issue Tracker

**Steps:**
1. Create config: `example_firmware_reboot_issue.json`
2. Download emails: `python gmail_downloader.py`
3. Track issue: `python issue_tracker.py`
4. Export affected customers for follow-up

**Output:**
```
Issue: Firmware 3.2.1 Reboots
Affected: 47 customers (3.2% of emails)
Products: PT20X (28), PT30X (19)
+ CSV of all 47 customers for outreach
```

---

### Use Case 3: Post-Release Check

**Goal:** Did yesterday's CMP update break anything?

**Tools:** Gmail Downloader → Issue Tracker

**Steps:**
1. Download: last 2 days of emails
2. Run multiple issue trackers (autotracking, streaming, presets)
3. Compare to baseline from before release

**Output:** Immediate alert if issue spike detected

---

### Use Case 4: Monthly Trend Analysis

**Goal:** What are the trends over the past month?

**Tools:** Gmail Downloader → General Analyzer

**Steps:**
1. Download: last 30 days
2. Run general analyzer
3. Compare to previous months

**Output:** Long-term trend data for resource planning

---

## ⚡ Speed Comparison

### Old Way (Google Takeout):
```
Request export          → 5 minutes
Wait for email         → 2-8 hours
Download zip           → 10-30 minutes
Extract files          → 5 minutes
Find correct file      → 5 minutes
TOTAL: 3-9 HOURS 😫
```

### New Way (Gmail API):
```
Run gmail_downloader.py → 30 seconds
TOTAL: 30 SECONDS 🚀
```

**That's 360x - 1080x faster!**

---

## 🔄 Automation Options

### Option 1: Manual Weekly (Recommended to Start)
- Run `gmail_downloader.py` every Monday
- Quick and simple
- Full control

### Option 2: Semi-Automated
- Edit `automated_weekly_download.py` with your settings
- Run it weekly: `python automated_weekly_download.py`
- One command does everything

### Option 3: Fully Automated (Advanced)
**Windows:** Task Scheduler
**Mac/Linux:** cron job

Example cron (runs every Monday at 9 AM):
```
0 9 * * 1 cd /path/to/project && python automated_weekly_download.py
```

---

## 🎨 Customization Guide

### Customize General Analyzer
Edit `keywords.json`:
```json
{
  "Your Category Name": [
    "keyword1",
    "keyword2",
    "specific phrase"
  ]
}
```

### Customize Issue Tracker
Create new JSON config:
```json
{
  "issue_name": "Your Issue Name",
  "issue_id": "YOUR-ID-001",
  "keywords": {
    "primary": ["must have these"],
    "symptoms": ["problem words"],
    "context": ["when it happens"]
  },
  "match_criteria": {
    "require_primary": true,
    "require_symptom": true,
    "require_context": false
  }
}
```

### Customize Gmail Downloader
Edit `automated_weekly_download.py`:
```python
SEARCH_QUERY = "to:your-support@email.com"
DAYS_BACK = 7
```

---

## 📊 Reporting Suggestions

### Weekly Team Report Template

**Subject:** Support Summary - Week of [Date]

**Total Emails:** [X]

**Top Issues:**
1. Connection Issues - [X] mentions
2. Firmware - [X] mentions  
3. PTZ Control - [X] mentions

**Critical Issues Tracked:**
- CMP Autotracking: [X] reports (↑↓ vs last week)
- Firmware 3.2.1 Reboots: [X] reports (↑↓ vs last week)

**Action Items:**
- [Issue with spike] - Escalate to engineering
- [Common request] - Create KB article

---

## 🔐 Security & Privacy

### What Has Access:
- Gmail API: READ-ONLY access to your Gmail
- Cannot delete, modify, or send emails
- Only downloads what you request

### What's Private:
- `credentials.json` - Keep secret (your app credentials)
- `token.pickle` - Keep secret (your auth token)
- Downloaded `.mbox` files - Contain customer emails
- **Never commit these to public GitHub!**

### Revoke Access Anytime:
https://myaccount.google.com/permissions

---

## 🆘 Troubleshooting Quick Reference

| Problem | Solution |
|---------|----------|
| Gmail auth fails | Delete `token.pickle`, run again |
| "credentials.json not found" | Complete GMAIL_SETUP_GUIDE.md |
| Download too slow | Normal first time, subsequent runs faster |
| Analyzer finds nothing | Check mbox file has content |
| Issue tracker too many matches | Make keywords more specific |
| Issue tracker no matches | Broaden keywords, check spelling |

---

## 📚 Where to Learn More

**First Time Setup:**
→ Read `GMAIL_SETUP_GUIDE.md`

**General Analysis:**
→ Read `MBOX_GUIDE.md`

**Issue Tracking:**
→ Read `ISSUE_TRACKER_GUIDE.md`

**Quick Commands:**
→ Read `QUICK_REFERENCE.md`

---

## 🎯 Recommended Getting Started Path

### Week 1: Setup & Test
1. Complete Gmail API setup (GMAIL_SETUP_GUIDE.md)
2. Download 100 test emails
3. Run general analyzer
4. Familiarize yourself with reports

### Week 2: Live Tracking
1. Download last week's emails Monday morning
2. Generate weekly report
3. Share with team
4. Gather feedback on categories

### Week 3: Issue Tracking
1. Create issue config for known problem
2. Run issue tracker
3. Export affected customers
4. Start follow-up campaign

### Week 4: Optimization
1. Adjust keyword categories based on results
2. Create issue configs for common problems
3. Consider automation
4. Train team members

---

## 💡 Pro Tips

1. **Keep a "issues" folder** with all your issue configs organized by severity
2. **Archive weekly mbox files** for historical analysis
3. **Create templates** for common issue configs (firmware, feature, product-specific)
4. **Export CSVs weekly** to track customer sentiment over time
5. **Combine tools**: Run general analyzer first to spot new issues, then create issue tracker for them

---

## 🎉 You Now Have

- ⚡ **Fast email downloads** (30 seconds vs 9 hours)
- 📊 **Automated trend analysis** (10+ categories)
- 🎯 **Precision issue tracking** (specific bugs/features)
- 📧 **Customer follow-up lists** (export to CSV)
- 📈 **Historical tracking** (compare week to week)
- 🤖 **Automation ready** (weekly scheduled runs)

**You've gone from manual Google Takeout exports to a professional support analytics system!**

---

## 📞 Next Steps

1. Set up Gmail API (GMAIL_SETUP_GUIDE.md)
2. Download your first batch of emails
3. Run the general analyzer
4. Share results with your team
5. Start tracking critical issues

Questions? Check the guides or create a GitHub issue!
