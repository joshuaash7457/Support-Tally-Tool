# Issue Tracker - Quick Reference Card

## ⚡ Quick Start
```bash
python issue_tracker.py
```

## 🎯 When to Use This Tool

✅ **USE for:**
- Tracking specific known bugs
- Measuring impact of firmware issues  
- Monitoring feature failures
- Post-update problem tracking
- Creating customer follow-up lists

❌ **DON'T USE for:**
- General support trends (use email_analyzer_mbox.py)
- Exploring unknown issues
- Weekly category reports

---

## 📝 Config File Template

```json
{
  "issue_name": "Brief descriptive name",
  "issue_id": "UNIQUE-ID-001",
  "date_reported": "YYYY-MM-DD",
  "severity": "CRITICAL / HIGH / MEDIUM / LOW",
  "description": "What's the problem?",
  
  "keywords": {
    "primary": ["main", "terms", "that", "identify", "issue"],
    "symptoms": ["not working", "broken", "failed"],
    "context": ["after update", "version X"]
  },
  
  "exclude_keywords": ["resolved", "fixed", "working"],
  "affected_products": ["pt20x", "pt30x"],
  
  "match_criteria": {
    "require_primary": true,
    "require_symptom": true,
    "require_context": false
  }
}
```

---

## 🔍 Match Criteria Settings

| Setting | Effect |
|---------|--------|
| `require_primary: true` | MUST mention main product/feature |
| `require_symptom: true` | MUST describe a problem |
| `require_context: true` | MUST mention trigger (update, version, etc.) |

### Common Combinations:

**Strict** (fewest matches, highest accuracy)
```json
"require_primary": true,
"require_symptom": true,
"require_context": true
```

**Balanced** (recommended)
```json
"require_primary": true,
"require_symptom": true,
"require_context": false
```

**Loose** (most matches, may include false positives)
```json
"require_primary": true,
"require_symptom": false,
"require_context": false
```

---

## 💡 Keyword Tips

### Primary Keywords (What is it?)
```json
"primary": [
  "cmp",
  "camera management platform",
  "autotracking",
  "auto-tracking"
]
```

### Symptom Keywords (What's wrong?)
Use customer language:
```json
"symptoms": [
  "not working",
  "doesn't work", 
  "won't work",
  "stopped working",
  "broken",
  "failed",
  "not functioning"
]
```

### Context Keywords (When/How?)
```json
"context": [
  "after update",
  "firmware 3.2.1",
  "since upgrade",
  "new version"
]
```

### Exclude Keywords
Filter noise:
```json
"exclude_keywords": [
  "resolved",
  "fixed",
  "working now",
  "solved",
  "nevermind"
]
```

---

## 📊 Output Files

1. **issue_report_[ID]_[timestamp].txt**
   - Full analysis with keyword breakdowns
   - First 50 affected emails with details

2. **affected_emails_[ID]_[timestamp].csv**  
   - Spreadsheet of all affected emails
   - Perfect for follow-up campaigns

---

## 🚨 Common Scenarios

### Firmware Bug
```json
{
  "issue_name": "Firmware X.X.X Bug Name",
  "keywords": {
    "primary": ["firmware x.x.x", "version x.x.x"],
    "symptoms": ["specific symptom here"]
  }
}
```

### Feature Failure After Update
```json
{
  "issue_name": "Feature Stopped After Update",
  "keywords": {
    "primary": ["feature name"],
    "symptoms": ["not working", "stopped"],
    "context": ["after update", "since update"]
  }
}
```

### Product-Specific Issue
```json
{
  "issue_name": "PT20X Specific Problem",
  "keywords": {
    "primary": ["pt20x", "20x"],
    "symptoms": ["symptom here"]
  },
  "affected_products": ["pt20x"]
}
```

### Software Compatibility
```json
{
  "issue_name": "OBS Compatibility Issue",
  "keywords": {
    "primary": ["camera feature"],
    "symptoms": ["not showing", "not detected"],
    "context": ["obs", "obs studio"]
  },
  "match_criteria": {
    "require_context": true
  }
}
```

---

## 🎯 Example Workflow

### Day 1: Issue Reported
1. Create config file for the issue
2. Run on recent emails (past week)
3. Get baseline count

### Daily Monitoring
1. Run on previous day's emails
2. Track if reports increasing/decreasing
3. Alert team if spike

### Week 1 Review
1. Run on full week
2. Export CSV of affected customers
3. Coordinate follow-up

### Post-Fix Verification
1. Continue running tracker
2. Confirm reports declining
3. Archive config when resolved

---

## 📞 Support Team Use Cases

**Monday Morning Check:**
"How many CMP autotracking complaints this weekend?"
```bash
python issue_tracker.py
# Use cmp_autotracking_issue.json
# Point at weekend email export
```

**Post-Release Monitoring:**
"Did firmware 3.2.1 cause any new issues?"
```bash
# Create config for fw 3.2.1
# Run daily for first week
# Track trends
```

**Customer Outreach:**
"Get list of everyone affected by X"
```bash
# Run tracker
# Export CSV
# Import to email campaign tool
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Too many matches (>50%) | Add more specific keywords, enable stricter criteria |
| No matches (0%) | Broaden keywords, relax match criteria |
| Wrong emails matching | Add exclude keywords |
| Missing obvious matches | Check keyword spelling, add variations |

---

## 📁 Example Configs Provided

- `cmp_autotracking_issue.json` - CMP autotracking failure
- `example_firmware_reboot_issue.json` - Reboot after update
- `example_ndi_obs_issue.json` - NDI streaming problem
- `example_preset_issue.json` - PTZ preset issues

Use these as templates!

---

## 💻 Command Line Quick Copy

```bash
# Create new config from template
python issue_tracker.py
[Press Enter when asked for config]

# Run existing config
python issue_tracker.py
[Enter path to your .json config]
[Enter path to email .mbox file]

# Process limited emails (testing)
python issue_tracker.py
[Enter config]
[Enter email file]
[Enter number like 1000 when asked]
```

---

**Remember:** This is a laser-focused tool for specific issues. For general trends, use `email_analyzer_mbox.py`!
