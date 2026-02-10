# Gmail API Setup Guide

This guide will help you set up the Gmail API so you can download emails quickly and easily.

**One-time setup takes about 5-10 minutes. After that, downloading emails takes 30 seconds!**

---

## 📋 Prerequisites

- Google account with Gmail access
- Python 3.6 or higher installed
- Internet connection

---

## 🚀 Step-by-Step Setup

### Step 1: Install Required Python Libraries

Open terminal/command prompt and run:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

**Windows users:** You might need to use `pip3` instead of `pip`

---

### Step 2: Create Google Cloud Project

1. **Go to Google Cloud Console:**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create a new project:**
   - Click "Select a project" at the top
   - Click "NEW PROJECT"
   - Project name: "PTZOptics Email Downloader" (or anything you want)
   - Click "CREATE"
   - Wait a few seconds for it to be created

3. **Select your new project:**
   - Click "Select a project" again
   - Click on your newly created project

---

### Step 3: Enable Gmail API

1. **Open API Library:**
   - In the left sidebar, click "APIs & Services" → "Library"
   - Or visit: https://console.cloud.google.com/apis/library

2. **Enable Gmail API:**
   - Search for "Gmail API"
   - Click on "Gmail API" in the results
   - Click the blue "ENABLE" button
   - Wait a few seconds

---

### Step 4: Create OAuth Credentials

1. **Go to Credentials page:**
   - In the left sidebar, click "APIs & Services" → "Credentials"
   - Or visit: https://console.cloud.google.com/apis/credentials

2. **Configure OAuth consent screen (first time only):**
   - Click "CONFIGURE CONSENT SCREEN"
   - Choose "External" (unless you have Google Workspace)
   - Click "CREATE"
   
   Fill in the required fields:
   - **App name:** PTZOptics Email Downloader
   - **User support email:** Your email
   - **Developer contact:** Your email
   - Click "SAVE AND CONTINUE"
   
   On "Scopes" page:
   - Just click "SAVE AND CONTINUE" (no changes needed)
   
   On "Test users" page:
   - Click "ADD USERS"
   - Enter your email address
   - Click "ADD"
   - Click "SAVE AND CONTINUE"
   
   Review and click "BACK TO DASHBOARD"

3. **Create OAuth Client ID:**
   - Click "CREATE CREDENTIALS" at the top
   - Select "OAuth client ID"
   - Application type: "Desktop app"
   - Name: "PTZOptics Email Downloader"
   - Click "CREATE"

4. **Download credentials:**
   - A popup will appear with your credentials
   - Click "DOWNLOAD JSON"
   - Save the file as `credentials.json` in the same folder as `gmail_downloader.py`

---

### Step 5: First Run (Authorization)

1. **Run the downloader:**
   ```bash
   python gmail_downloader.py
   ```

2. **Authorize access:**
   - Your web browser will open automatically
   - You may see a "Google hasn't verified this app" warning
   - Click "Advanced" → "Go to PTZOptics Email Downloader (unsafe)"
   - This is safe - it's YOUR app!
   
3. **Grant permissions:**
   - Click "Continue"
   - Select your Google account
   - Review permissions (read-only access to Gmail)
   - Click "Allow"

4. **Complete!**
   - Browser will show "The authentication flow has completed"
   - You can close the browser
   - A `token.pickle` file will be created
   - You won't need to authorize again!

---

## ✅ You're All Set!

Now you can download emails anytime with:

```bash
python gmail_downloader.py
```

The script will ask you:
- What emails to download (or all)
- How many days back (default: 7)
- Where to save them

**Example weekly workflow:**
```bash
python gmail_downloader.py
# Query: to:support@ptzoptics.com
# Days back: 7
# Output: weekly_support_emails.mbox
# Takes 30 seconds!
```

---

## 🔍 Search Query Examples

When the script asks for a search query, you can use:

### Basic Queries
```
from:customer@example.com          # From specific sender
to:support@ptzoptics.com           # To specific address  
subject:urgent                      # Subject contains word
label:support                       # Emails in a label/folder
```

### Combined Queries
```
to:support@ptzoptics.com subject:camera
from:support@ptzoptics.com label:important
subject:(firmware OR update)
```

### Date Queries (in addition to days_back)
```
after:2025/01/01                   # After specific date
before:2025/01/31                  # Before specific date
```

### Leave blank to download ALL emails from the time period!

---

## 📁 File Locations

Make sure these files are in the same folder:

```
your-project-folder/
├── gmail_downloader.py          # The script
├── credentials.json             # Downloaded from Google Cloud
├── token.pickle                 # Auto-generated on first run
├── email_analyzer_mbox.py       # Your analyzer
└── issue_tracker.py             # Your issue tracker
```

---

## 🔧 Troubleshooting

### "credentials.json not found"
- Make sure you downloaded it from Google Cloud Console
- Put it in the same folder as gmail_downloader.py
- Check the filename is exactly `credentials.json`

### "Authentication failed"
- Delete `token.pickle` and run again
- Make sure you completed OAuth consent screen setup
- Check that your email is listed as a test user

### "Gmail API is not enabled"
- Go back to Google Cloud Console
- Make sure Gmail API is enabled for your project

### "Access denied"
- Check that you clicked "Allow" during authorization
- Make sure you're using the correct Google account

### "Module not found: googleapiclient"
Run the install command again:
```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

---

## 🎯 Weekly Usage Workflow

Once set up, your weekly routine is:

**Monday morning:**
```bash
python gmail_downloader.py
```
- Query: `to:support@ptzoptics.com` (or whatever your support address is)
- Days back: `7`
- Output: `weekly_emails.mbox`
- Takes ~30 seconds to download 1000 emails

**Then analyze:**
```bash
python email_analyzer_mbox.py
```
- File: `weekly_emails.mbox`
- Get your weekly report!

---

## 🔐 Security Notes

- `credentials.json` - Contains your app credentials (keep private)
- `token.pickle` - Contains your authorization token (keep private)
- **Never commit these files to GitHub!**
- The script has READ-ONLY access to Gmail
- You can revoke access anytime at: https://myaccount.google.com/permissions

---

## 📞 Common Questions

**Q: Will this delete emails from Gmail?**
A: No! The script only has read-only access. It cannot delete or modify emails.

**Q: Can I use this for multiple email accounts?**
A: Yes, but you'll need separate credentials for each account. Just use different credential filenames.

**Q: How fast is it?**
A: Typically downloads 100-200 emails per second. A week of emails (1000 emails) takes about 30 seconds.

**Q: Does this cost money?**
A: No! Gmail API has a free tier that's more than enough for this use case (1 billion quota units per day).

**Q: Can I automate this to run every Monday?**
A: Yes! Once set up, you can use Task Scheduler (Windows) or cron (Mac/Linux) to run it automatically.

---

## 🎉 Success!

Once you see "✓ DOWNLOAD COMPLETE!" you're ready to analyze your emails. The downloaded mbox file works with both:
- `email_analyzer_mbox.py` - For general trends
- `issue_tracker.py` - For specific issues

Much faster than Google Takeout! 🚀
