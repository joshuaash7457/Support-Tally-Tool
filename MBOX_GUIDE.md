# Handling Large MBOX Files (10GB+)

## Quick Start for Your 10GB File

### Option 1: Process All Emails (Recommended if you have time)
```bash
python email_analyzer_mbox.py
```
- Enter your mbox file path
- When asked "Process all emails?", type `y`
- This will take time but give you the most accurate results

### Option 2: Sample Processing (Faster for testing)
```bash
python email_analyzer_mbox.py
```
- Enter your mbox file path  
- When asked "Process all emails?", type `n`
- Enter a number like `1000` to process first 1000 emails
- Good for testing keywords before running full analysis

## Performance Expectations

**For a 10GB mbox file:**
- Typical email count: 50,000 - 200,000 emails
- Processing time: 15-60 minutes (depends on your computer)
- Memory usage: ~500MB - 2GB RAM
- Progress updates every 100 emails

The tool is optimized for large files:
- Reads emails one at a time (doesn't load entire file into memory)
- Shows progress so you know it's working
- Can be interrupted with Ctrl+C if needed

## Tips for Large Files

### 1. Start with a Sample
Test with 500-1000 emails first to:
- Verify your keywords are catching the right issues
- Adjust categories before full analysis
- Estimate total processing time

### 2. Optimize Your Keywords
Edit `keywords.json` to:
- Remove categories you don't need
- Add more specific keywords for better accuracy
- Combine similar categories

### 3. Run Overnight
For very large files:
- Start the analysis before leaving work
- It will complete and save the report automatically
- No interaction needed once started

## File Path Examples

**Windows:**
```
C:\Users\YourName\Downloads\support_emails.mbox
```

**Mac:**
```
/Users/YourName/Downloads/support_emails.mbox
```

**If path has spaces, use quotes:**
```
"C:\Users\Your Name\Email Exports\support_emails.mbox"
```

## What Gets Analyzed

From each email, the tool extracts:
- Subject line
- Body text (plain text only)
- Combines both for keyword searching

Attachments and HTML formatting are ignored.

## Expected Output

The report will show:
```
PTZOPTICS SUPPORT EMAIL ANALYSIS REPORT
Generated: 2025-01-27 14:30:00
======================================

Total Emails Analyzed: 147,523

--------------------------------------

CONNECTION ISSUES
  Total Mentions: 8,234
  Emails Affected: 5,421 (3.7%)
  Top Keywords:
    - won't connect: 2,145
    - connection failed: 1,876
    - network issue: 1,234
    ...
```

This tells you:
- **Total Mentions**: How many times keywords appeared across ALL emails
- **Emails Affected**: How many individual emails mentioned this category
- **Percentage**: What % of total emails had this issue

## Troubleshooting

**"Taking forever to load":**
- MBOX files are compressed - first step takes longest
- Wait for "Total messages in mbox: X" to appear
- Then processing begins

**"Memory error":**
- Close other programs
- Use the sample processing option
- Process in chunks (1000-5000 at a time)

**"Wrong counts":**
- Check keywords.json - make them more specific
- Look at the top keywords list to see what's matching
- Edit and re-run

## After Analysis

Review your report and:
1. Look for surprising results (adjust keywords if needed)
2. Compare week-to-week trends
3. Share with engineering team
4. Use data to prioritize support resources

## Questions?

The tool creates a timestamped report file (e.g., `email_report_20250127_143000.txt`) that you can:
- Share with team members
- Archive for historical comparison
- Import into Excel for further analysis
