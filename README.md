# PTZOptics Email Analysis System

Automated support email analysis and reporting for PTZOptics. Download emails from Gmail, analyze trends, track critical issues, and generate formatted weekly reports—all with a single command.

---

## 🚀 Quick Start

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Set Up Gmail API
Follow [FIRST_TIME_SETUP_GUIDE.md](FIRST_TIME_SETUP_GUIDE.md) to:
- Create Google Cloud project
- Enable Gmail API
- Download credentials.json

### 3. Run Weekly Report
```bash
python monday_morning_automation.py
```

Done! Your weekly report is generated in 2-3 minutes.

---

## 📊 What You Get

**Automated Weekly Reports with:**
- Volume metrics (total emails, week-over-week trends)
- Top 5 issues by category
- Critical issue tracking
- AI-generated insights
- Recommended action items

**Example Output:**
```
Total Support Emails: 1,247 ↑ (+12.3% vs last week)

TOP ISSUES:
1. Connection Issues ↑ (+8.5%) - 245 mentions
2. Firmware → (-2.1%) - 178 mentions
3. PTZ Control ↓ (-15.3%) - 134 mentions

CRITICAL ISSUES:
🔴 CMP Autotracking Failure - 47 customers affected

KEY INSIGHTS:
• Connection Issues spiked - investigate for new problems
• CRITICAL: Escalate CMP Autotracking to engineering
```

---

## 🛠️ Tools Included

### Core Scripts

**`monday_morning_automation.py`** - Complete weekly workflow (recommended)
- Downloads last week's emails
- Analyzes trends
- Tracks critical issues
- Generates formatted report

**`gmail_downloader.py`** - Fast email downloads
- Downloads emails in 30 seconds (vs 9 hours with Google Takeout)
- Filter by date, sender, subject
- Saves to mbox format

**`email_analyzer_mbox.py`** - General trend analysis
- 10+ customizable categories
- Keyword tracking
- Volume analysis

**`issue_tracker.py`** - Critical issue monitoring
- Track specific bugs/features
- Configurable match criteria
- Export affected customer lists

**`weekly_report_generator.py`** - Report generation
- Formatted team reports
- Week-over-week comparison
- Automated insights

---

## 📋 Weekly Workflow

**Every Monday (5 minutes):**

```bash
# 1. Open terminal in project folder
cd path/to/PTZOptics-Email-Analysis

# 2. Run automation
python monday_morning_automation.py

# 3. Wait 2-3 minutes (script runs automatically)

# 4. Review report
open weekly_team_report_YYYYMMDD.txt

# 5. Share with team
```

**That's it!**

---

## ⚙️ Configuration

### Customize Email Source
Edit `monday_morning_automation.py`:
```python
GMAIL_QUERY = "to:your-support@email.com"  # Your support email
DAYS_BACK = 7  # Number of days to analyze
```

### Customize Keywords
Edit `keywords.json` to add/remove categories:
```json
{
  "Your Category": ["keyword1", "keyword2"],
  "Connection Issues": ["won't connect", "connection failed"]
}
```

### Track Critical Issues
Create issue config files (see examples in repo):
```json
{
  "issue_name": "Feature X Broken After Update",
  "keywords": {
    "primary": ["feature x"],
    "symptoms": ["not working", "broken"]
  }
}
```

---

## 📖 Documentation

- **[FIRST_TIME_SETUP_GUIDE.md](FIRST_TIME_SETUP_GUIDE.md)** - Complete setup walkthrough (start here!)
- **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** - Printable setup checklist
- **[AUTOMATED_REPORTING_GUIDE.md](AUTOMATED_REPORTING_GUIDE.md)** - Report customization
- **[GMAIL_SETUP_GUIDE.md](GMAIL_SETUP_GUIDE.md)** - Detailed Gmail API setup
- **[ISSUE_TRACKER_GUIDE.md](ISSUE_TRACKER_GUIDE.md)** - Critical issue tracking
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common problems & solutions
- **[SECURITY_GUIDE.md](SECURITY_GUIDE.md)** - Security & privacy info

---
## 💡 Key Features

- ⚡ **Fast:** 30-second email downloads vs 9-hour Google Takeout
- 🤖 **Automated:** One command generates complete weekly reports
- 📊 **Insightful:** AI-generated insights and trend detection
- 🎯 **Precise:** Track specific issues with configurable criteria
- 📈 **Historical:** Week-over-week comparison and trending
- 🔒 **Secure:** Read-only Gmail access, no data retention


---


