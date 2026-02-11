# Critical Issue Tracker - User Guide

## 🎯 Purpose

This tool is designed for tracking **specific critical issues** in your support emails, like:
- Firmware bugs affecting specific features
- Feature failures after updates
- Product-specific problems
- Known issues you need to monitor

Perfect for situations like: *"We released CMP update 2.5 and autotracking broke - how many customers are affected?"*

---

## 🚀 Quick Start

### Step 1: Create Issue Configuration

Run the tracker:
```bash
python issue_tracker.py
```

When prompted, press Enter (no config file). It will create `issue_template.json`.

### Step 2: Customize the Config

Edit the JSON file with your issue details:

```json
{
  "issue_name": "CMP Autotracking Failure After Update",
  "issue_id": "CMP-AT-2025-001",
  "severity": "CRITICAL",
  "keywords": {
    "primary": ["cmp", "autotracking"],
    "symptoms": ["not working", "stopped", "broken"],
    "context": ["after update", "new version"]
  }
}
```

### Step 3: Run the Tracker

```bash
python issue_tracker.py
```

Enter your config file path and email file path. Get instant results!

---

## 📋 Configuration Breakdown

### Issue Information
```json
{
  "issue_name": "Short descriptive name",
  "issue_id": "Unique ID for tracking (e.g., FW-BUG-001)",
  "date_reported": "When you first identified this issue",
  "severity": "CRITICAL / HIGH / MEDIUM",
  "description": "Detailed explanation of the issue"
}
```

### Keywords (The Most Important Part!)

#### **Primary Keywords** (Required)
Core terms that MUST appear for an email to match:
```json
"primary": [
  "cmp",
  "camera management platform",
  "autotracking"
]
```

#### **Symptom Keywords** (What's broken)
Descriptions of the problem:
```json
"symptoms": [
  "not working",
  "stopped working",
  "broken",
  "failed",
  "doesn't work"
]
```

#### **Context Keywords** (Optional)
When/how it happened:
```json
"context": [
  "after update",
  "firmware 2.5",
  "since upgrade",
  "new version"
]
```

### Exclude Keywords
Filter out resolved issues:
```json
"exclude_keywords": [
  "resolved",
  "fixed",
  "working now",
  "problem solved"
]
```

### Match Criteria
Control how strict the matching is:
```json
"match_criteria": {
  "require_primary": true,    // Must have at least 1 primary keyword
  "require_symptom": true,    // Must have at least 1 symptom keyword
  "require_context": false    // Context keywords are optional
}
```

**Example Matching:**
- `require_primary: true, require_symptom: true` = Must mention CMP AND have a problem
- `require_primary: true, require_symptom: false` = Just needs to mention CMP (less strict)

---

## 🔍 Real-World Examples

### Example 1: CMP Autotracking Bug

**Situation:** CMP update broke autotracking for all cameras

**Config:**
```json
{
  "issue_name": "CMP Autotracking Failure",
  "issue_id": "CMP-AT-001",
  "keywords": {
    "primary": ["cmp", "camera management platform", "autotracking"],
    "symptoms": ["not working", "stopped", "broken", "won't track"],
    "context": ["after update", "version 2.5"]
  },
  "match_criteria": {
    "require_primary": true,
    "require_symptom": true,
    "require_context": false
  }
}
```

**Matches:**
✅ "CMP autotracking stopped working after I updated"
✅ "Camera Management Platform - autotracking feature broken"
✅ "My autotracking won't work in CMP anymore"

**Doesn't Match:**
❌ "CMP is working great!" (no symptom keyword)
❌ "Autotracking broken on camera" (no CMP mention)

---

### Example 2: Firmware Power Issue

**Situation:** Firmware 3.2.1 causes random power cycling

**Config:**
```json
{
  "issue_name": "Firmware 3.2.1 Power Cycling",
  "issue_id": "FW-321-PWR-001",
  "keywords": {
    "primary": ["firmware 3.2.1", "version 3.2.1", "fw 3.2.1"],
    "symptoms": ["power cycling", "rebooting", "restarting", "power issue"],
    "context": []
  },
  "affected_products": ["pt20x", "pt30x"],
  "match_criteria": {
    "require_primary": true,
    "require_symptom": true,
    "require_context": false
  }
}
```

---

### Example 3: Streaming Codec Problem

**Situation:** H.265 codec causing stream failures in OBS

**Config:**
```json
{
  "issue_name": "H.265 Codec OBS Stream Failure",
  "issue_id": "CODEC-H265-OBS-001",
  "keywords": {
    "primary": ["h.265", "h265", "hevc"],
    "symptoms": ["stream failed", "won't stream", "streaming issue", "no video"],
    "context": ["obs", "obs studio"]
  },
  "match_criteria": {
    "require_primary": true,
    "require_symptom": true,
    "require_context": true  // Must mention OBS too
  }
}
```

---

## 📊 Understanding the Report

### Summary Section
```
Total Emails Analyzed: 5,234
Emails Matching Issue: 147
Match Rate: 2.81%
```

This tells you:
- How many emails were searched
- How many mention this specific issue
- Percentage affected (great for severity assessment)

### Keyword Breakdown
```
PRIMARY KEYWORD MATCHES
  • cmp: 132 mentions
  • camera management platform: 48 mentions
  • autotracking: 178 mentions
```

Shows which terms customers are using most.

### Affected Email Details
First 50 matching emails with:
- Subject
- Sender
- Date
- What keywords matched
- Preview of email content

### CSV Export
Optional CSV file with all affected emails for:
- Follow-up campaigns
- Customer outreach
- Engineering analysis

---

## 💡 Pro Tips

### 1. Start Broad, Then Narrow
First run:
```json
"require_primary": true,
"require_symptom": false,
"require_context": false
```

See what you get, then make it stricter.

### 2. Use Word Variations
Include all ways customers might say it:
```json
"primary": [
  "cmp",
  "camera management platform",
  "cam management platform",
  "camera manager"
]
```

### 3. Common Symptom Phrases
These work well:
- "not working", "doesn't work", "won't work"
- "stopped working", "stopped functioning"
- "broken", "failed", "failure"
- "issue", "problem", "error"

### 4. Version-Specific Tracking
Track each firmware version separately:
```json
"issue_id": "FW-310-BUG-001",  // Version 3.1.0
"issue_id": "FW-320-BUG-001",  // Version 3.2.0
```

### 5. Use Exclude Keywords Wisely
Filter out noise:
```json
"exclude_keywords": [
  "resolved",
  "fixed",
  "working now",
  "solved",
  "nevermind",
  "false alarm"
]
```

---

## 🔄 Workflow Suggestions

### Weekly Monitoring
1. Run tracker Monday morning on last week's emails
2. Review match count and percentage
3. Alert engineering if spike detected
4. Export CSV for customer follow-up

### Post-Release Tracking
1. Create config for each new release
2. Run daily for first week after release
3. Track trends (increasing/decreasing reports)
4. Identify issues early

### Quarterly Reviews
1. Run all active issue configs on full quarter data
2. Compare issue prevalence over time
3. Identify patterns and trends

---

## 🎯 When to Use This vs. General Analyzer

**Use Issue Tracker When:**
- Tracking a specific known problem
- Need to measure impact of a bug
- Want precise match criteria
- Need follow-up email list

**Use General Email Analyzer When:**
- Exploring overall support trends
- Don't know what you're looking for
- Want broad category breakdown
- Generating weekly reports

---

## 📁 File Outputs

The tracker creates:

1. **issue_report_[ID]_[timestamp].txt**
   - Full analysis report
   - Keyword breakdowns
   - Email details

2. **affected_emails_[ID]_[timestamp].csv**
   - Spreadsheet of affected emails
   - For follow-up and analysis

---

## 🆘 Troubleshooting

**"Too many matches" (like 80% of emails match)**
→ Your keywords are too broad. Make them more specific or set stricter match criteria.

**"No matches found" (0 emails match)**
→ Keywords might be too specific. Try broader terms or check spelling.

**"Wrong emails matching"**
→ Add exclude keywords to filter false positives.

---

## 📝 Example Configs Included

We've included `cmp_autotracking_issue.json` as a real example. Use it as a template for your own issues!

---

## Questions?

This tool gives you laser-focused tracking of specific critical issues. Combine with the general email analyzer for comprehensive support insights!
