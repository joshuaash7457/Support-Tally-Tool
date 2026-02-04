# PTZOptics Support Email Analyzer

A Python tool to analyze support emails and count mentions of specific keywords, categories, and issues.

## Features

- 📊 Count keyword mentions across multiple emails
- 📁 Support for CSV and TXT file formats
- 🔧 Customizable keyword categories
- 📝 Automatic report generation
- 💾 Save and load custom keyword configurations

## Quick Start

### 1. Install Python
Make sure you have Python 3.6 or higher installed on your computer.

### 2. Prepare Your Email Export

**For Gmail/Outlook CSV:**
- Export your emails to CSV format
- Make sure it includes columns for Subject and Body/Content

**For Text Files:**
- Export emails as plain text
- Separate each email with `---` or blank lines

### 3. Run the Analyzer

```bash
python email_analyzer.py
```

The program will:
1. Create a default `keywords.json` file
2. Ask for your email export file path
3. Analyze the emails
4. Generate a report showing counts for each category

## Customizing Keywords

Edit the `keywords.json` file to add your own categories and keywords:

```json
{
  "Your Category Name": [
    "keyword1",
    "keyword2",
    "phrase to search for"
  ],
  "Another Category": [
    "more keywords"
  ]
}
```

**Tips:**
- Keywords are case-insensitive (e.g., "Firmware" matches "firmware")
- Use specific phrases for better accuracy
- Group related keywords under meaningful categories

## Example Output

```
============================================================
EMAIL ANALYSIS REPORT
Generated: 2025-01-27 10:30:45
============================================================

Total Emails Analyzed: 150

------------------------------------------------------------

CONNECTION ISSUES
  Total Mentions: 45
  Emails Affected: 32
  Top Keywords:
    - won't connect: 18
    - connection failed: 12
    - network issue: 8
    - can't connect: 7

FIRMWARE
  Total Mentions: 28
  Emails Affected: 23
  Top Keywords:
    - firmware: 15
    - update: 8
    - version: 5
```

## File Format Requirements

### CSV Files
Your CSV should have columns for:
- **Subject** (or Email Subject, Title)
- **Body** (or Content, Message, Email Body)

Example:
```csv
Subject,Body,Date,From
"Camera won't connect","I can't get my PT20X to connect...",2025-01-20,user@example.com
"Firmware update help","How do I update the firmware?",2025-01-21,user2@example.com
```

### Text Files
Emails should be separated by:
- `---` (three dashes)
- OR blank lines (double or triple newlines)

Example:
```
Subject: Camera won't connect
From: user@example.com

I can't get my PT20X to connect to the network...

---

Subject: Firmware update help
From: user2@example.com

How do I update the firmware on my camera?
```

## Advanced Usage

### Use as a Python Module

```python
from email_analyzer import EmailAnalyzer

# Create analyzer with custom keywords
analyzer = EmailAnalyzer('my_keywords.json')

# Read emails from CSV
emails = analyzer.read_csv_file('support_emails.csv', 
                                email_column='Body',
                                subject_column='Subject')

# Analyze
results = analyzer.analyze_emails(emails)

# Generate report
analyzer.generate_report('my_report.txt')
```

### Add Categories Programmatically

```python
analyzer = EmailAnalyzer()

# Add a new category
analyzer.add_category('New Issue Type', [
    'keyword1',
    'keyword2',
    'specific phrase'
])

# Save updated keywords
analyzer.save_keywords('updated_keywords.json')
```

## Common PTZOptics Keywords

The default configuration includes categories for:
- Connection Issues
- Firmware
- PTZ Control
- Streaming
- Camera Models
- Software
- Power Issues
- Video Quality
- Audio
- Setup/Installation

Feel free to customize these based on your actual support tickets!

## Troubleshooting

**"File not found" error:**
- Make sure you're entering the full path to your file
- On Windows: `C:\Users\YourName\Documents\emails.csv`
- On Mac/Linux: `/Users/YourName/Documents/emails.csv`

**"No emails found" error:**
- Check your CSV column names match what you entered
- Verify your text file has proper email separators

**Wrong counts:**
- Keywords are case-insensitive, so "firmware" matches "FIRMWARE"
- Make keywords more specific if getting false positives
- Use phrases instead of single words (e.g., "won't connect" vs "connect")

## Next Steps

1. Run the tool with a small sample first to test
2. Adjust keywords based on results
3. Add more specific categories for your common issues
4. Run weekly reports to track trends

## Questions?

Feel free to modify and extend this tool for your needs!
