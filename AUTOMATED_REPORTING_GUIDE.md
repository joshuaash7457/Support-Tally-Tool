# Automated Weekly Reporting Guide

## 🎯 Overview

You now have **3 levels of automation** for generating weekly support reports!

---

## 📊 What Gets Automated

The automated reports include:

### 📈 Volume Metrics
- Total emails this week
- Week-over-week comparison
- Trend indicators (↑ ↓ →)

### 🔥 Top Issues
- Top 5 issue categories
- Mention counts and percentages
- Week-over-week trends
- Top keywords per category

### ⚠️ Critical Issues Tracked
- Specific bugs/problems you're monitoring
- Severity levels (🔴 Critical, 🟠 High, etc.)
- Impact percentages
- Customer count

### 💡 Key Insights (AI-Generated)
- Automated trend detection
- Volume spike alerts
- Category trend analysis
- Critical issue escalation flags

### ✅ Recommended Actions
- Automatically generated action items
- Based on data patterns
- Prioritized by severity

---

## 🚀 Three Ways to Generate Reports

### Option 1: Full Automation (Monday Morning Script) ⭐ RECOMMENDED

**One command does everything:**

```bash
python monday_morning_automation.py
```

**What it does:**
1. ✅ Downloads last week's emails from Gmail (30 seconds)
2. ✅ Runs general trend analysis
3. ✅ Tracks all critical issues
4. ✅ Generates formatted team report
5. ✅ Saves comparison data for next week

**Perfect for:** Weekly routine, consistent timing

---

### Option 2: Semi-Automated (Report Generator Only)

**If you already have the mbox file:**

```bash
python weekly_report_generator.py
```

**What it does:**
1. ✅ Analyzes existing mbox file
2. ✅ Tracks critical issues
3. ✅ Generates formatted team report
4. ✅ Week-over-week comparison

**Perfect for:** Custom time periods, ad-hoc analysis

---

### Option 3: Manual (Individual Tools)

**Full control over each step:**

```bash
# Step 1: Download
python gmail_downloader.py

# Step 2: Analyze trends
python email_analyzer_mbox.py

# Step 3: Track issues
python issue_tracker.py

# Step 4: Create report manually
```

**Perfect for:** Deep dives, troubleshooting, learning

---

## ⚙️ Configuration

### Customize Monday Morning Script

Edit `monday_morning_automation.py`:

```python
# Line 24-26: Gmail search
GMAIL_QUERY = "to:support@ptzoptics.com"  # Your support email
DAYS_BACK = 7  # Number of days to look back

# Line 29-32: Critical issues to track
ISSUE_CONFIGS = [
    'cmp_autotracking_issue.json',
    'firmware_reboot_issue.json',
    'your_custom_issue.json'  # Add your issues here
]

# Line 35: Output location
OUTPUT_DIR = ""  # Leave empty or set to "reports/"
```

### Customize Keywords

Edit `keywords.json` to change what categories are tracked:

```json
{
  "Your Custom Category": [
    "keyword1",
    "keyword2",
    "specific phrase"
  ]
}
```

### Create Issue Trackers

Create new `*_issue.json` files for problems you want to monitor:

```json
{
  "issue_name": "Your Issue Name",
  "issue_id": "ISSUE-001",
  "severity": "CRITICAL",
  "keywords": {
    "primary": ["main terms"],
    "symptoms": ["problem words"],
    "context": ["when it happens"]
  }
}
```

---

## 📅 Weekly Workflow

### Monday Morning (5 minutes):

1. **Run automation:**
   ```bash
   python monday_morning_automation.py
   ```

2. **Review report:**
   - Open `weekly_team_report_YYYYMMDD.txt`
   - Check top issues
   - Review critical issues
   - Note action items

3. **Share with team:**
   - Email report to team
   - Present in standup/meeting
   - Post to Slack/Teams

4. **Take action:**
   - Follow up on critical issues
   - Create KB articles for common problems
   - Escalate to engineering if needed

### During the Week:

- Monitor critical issues as they occur
- Run issue tracker on demand for new problems
- Keep issue configs updated

---

## 📊 Sample Report Output

```
======================================================================
PTZOPTICS SUPPORT - WEEKLY SUMMARY REPORT
======================================================================

Report Period: February 03, 2026 - February 10, 2026
Generated: 2026-02-10 09:00:00

──────────────────────────────────────────────────────────────────────
📊 VOLUME METRICS
──────────────────────────────────────────────────────────────────────

Total Support Emails: 1,247 ↑ (+12.3% vs last week)

──────────────────────────────────────────────────────────────────────
🔥 TOP ISSUES THIS WEEK
──────────────────────────────────────────────────────────────────────

1. Connection Issues ↑ (+8.5%)
   • 245 total mentions
   • 189 emails affected (15.2% of total)
   • Top keywords: won't connect (87), connection failed (56), network issue (43)

2. Firmware → (-2.1%)
   • 178 total mentions
   • 142 emails affected (11.4% of total)
   • Top keywords: firmware (98), update (45), version (35)

3. PTZ Control ↓ (-15.3%)
   • 134 total mentions
   • 98 emails affected (7.9% of total)
   • Top keywords: preset (67), pan (34), tilt (33)

──────────────────────────────────────────────────────────────────────
⚠️  CRITICAL ISSUES TRACKED
──────────────────────────────────────────────────────────────────────

🔴 CMP Autotracking Failure After Update
   • Issue ID: CMP-AT-2025-001
   • Severity: CRITICAL
   • Reports this week: 47 (3.77% of emails)

🟠 Firmware 3.2.1 Power Cycling
   • Issue ID: FW-321-PWR-001
   • Severity: HIGH
   • Reports this week: 23 (1.84% of emails)

──────────────────────────────────────────────────────────────────────
💡 KEY INSIGHTS
──────────────────────────────────────────────────────────────────────

• Connection Issues is the dominant issue this week, affecting 15.2% of support emails
• Support volume increased 12.3% compared to last week - monitor for capacity needs
• Connection Issues spiked 8.5% - investigate for new issues or trends
• CRITICAL: CMP Autotracking Failure affecting 47 customers - escalate to engineering

──────────────────────────────────────────────────────────────────────
✅ RECOMMENDED ACTIONS
──────────────────────────────────────────────────────────────────────

• Create/update knowledge base article for Connection Issues (high volume)
• Escalate CMP-AT-2025-001 to engineering team immediately
• Prepare customer communication for CMP Autotracking Failure (47 affected)
• Monitor FW-321-PWR-001 - consider hotfix if reports continue

──────────────────────────────────────────────────────────────────────
📎 ATTACHMENTS
──────────────────────────────────────────────────────────────────────

• Detailed analysis: email_report_20260210.txt
• Critical issue reports: issue_report_*.txt
• Affected customer lists: affected_emails_*.csv

======================================================================
End of Weekly Report
======================================================================
```

---

## 🔄 Week-Over-Week Comparison

The system automatically tracks week-over-week changes:

### How It Works:

1. **First Week:** Generates baseline data
2. **Following Weeks:** Compares to previous week
3. **Shows Trends:** ↑ increasing, ↓ decreasing, → stable

### Data Stored:

`previous_week_data.json` contains:
- Total email count
- Category mention counts
- Automatically updated each week

### Reset Comparison:

Delete `previous_week_data.json` to start fresh (useful after holidays, etc.)

---

## 🎨 Customization Examples

### Add Custom Insights

Edit `weekly_report_generator.py` → `_generate_insights()`:

```python
# Add your custom logic
if cat_name == "Streaming" and cat_data['total_mentions'] > 100:
    insights.append("High streaming issue volume - check CDN status")
```

### Add Custom Actions

Edit `weekly_report_generator.py` → `_generate_action_items()`:

```python
# Add your custom actions
if cat_name == "Setup/Installation" and percentage > 20:
    actions.append("Consider creating video tutorial for setup")
```

### Change Report Format

Edit `weekly_report_generator.py` → `generate_team_report()`:

```python
# Customize headers, sections, formatting
lines.append("YOUR CUSTOM SECTION")
```

---

## 📧 Sharing Reports

### Via Email:

**Option 1:** Copy/paste report text into email

**Option 2:** Attach the `.txt` file

**Option 3:** Convert to HTML for better formatting (future feature)

### Via Slack/Teams:

```
📊 Weekly Support Report - Feb 10, 2026

Total Emails: 1,247 ↑ (+12.3%)

Top Issues:
1. Connection Issues - 245 mentions ↑
2. Firmware - 178 mentions →
3. PTZ Control - 134 mentions ↓

🔴 Critical: CMP Autotracking - 47 reports
Full report attached 👆
```

### In Meetings:

- Project the report file
- Walk through each section
- Discuss action items
- Assign ownership

---

## 🔧 Troubleshooting

**"No previous week data for comparison"**
→ Normal for first run. Next week will show trends.

**"No insights generated"**
→ Not enough data or no significant changes. This is okay!

**"Issue tracker failed"**
→ Check that issue config files exist and are valid JSON

**"Gmail download failed"**
→ Check credentials.json and token.pickle are present

---

## 📈 Advanced Features

### Track Multiple Time Periods

```bash
# Last 2 weeks
python weekly_report_generator.py
# Enter days: 14

# Last month
# Enter days: 30

# Specific date range - use Gmail download with date filters
```

### Archive Historical Reports

```bash
# Create reports folder
mkdir reports/

# Edit monday_morning_automation.py
OUTPUT_DIR = "reports/"

# All reports saved to reports/ folder
```

### Automate with Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Weekly, Monday, 9:00 AM
4. Action: Start a program
5. Program: `python`
6. Arguments: `C:\path\to\monday_morning_automation.py`
7. Start in: `C:\path\to\your\project`

### Automate with Cron (Mac/Linux)

```bash
# Edit crontab
crontab -e

# Add line (runs every Monday at 9 AM):
0 9 * * 1 cd /path/to/project && python monday_morning_automation.py
```

---

## 🎯 Pro Tips

1. **Run Monday mornings** for consistent weekly cadence
2. **Review previous reports** to track long-term trends
3. **Update issue configs** as problems are resolved
4. **Archive mbox files** for historical analysis
5. **Share insights** with engineering team regularly
6. **Celebrate wins** when categories decrease!

---

## ✅ Success Metrics

You'll know it's working when:

- ✅ Team meetings start with data-driven discussions
- ✅ Engineering gets early warning of issues
- ✅ Knowledge base articles target actual problems
- ✅ Support capacity planning is proactive
- ✅ Customer follow-up is faster and targeted

---

## 🎉 You Now Have

- 🤖 **Fully automated weekly reports**
- 📊 **Week-over-week trend analysis**
- 🎯 **Critical issue monitoring**
- 💡 **AI-generated insights**
- ✅ **Automated action items**
- ⚡ **5-minute Monday morning routine**

**From manual email exports to professional support analytics - all automated!** 🚀
