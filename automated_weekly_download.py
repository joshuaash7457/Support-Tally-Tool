#!/usr/bin/env python3
"""
Automated Weekly Email Download
Run this script every Monday to automatically download last week's support emails
"""

from gmail_downloader import GmailDownloader
from datetime import datetime

def download_weekly_support_emails():
    """Download last week's support emails automatically"""
    
    print("="*70)
    print("AUTOMATED WEEKLY EMAIL DOWNLOAD")
    print("="*70)
    
    # Initialize downloader
    downloader = GmailDownloader()
    
    # Authenticate
    try:
        downloader.authenticate()
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False
    
    # Configure download parameters
    # CUSTOMIZE THESE FOR YOUR NEEDS:
    
    SEARCH_QUERY = "to:support@ptzoptics.com"  # Change to your support email
    DAYS_BACK = 7  # Last week
    MAX_RESULTS = None  # Download all matching emails
    
    # Generate filename with date
    week_start = datetime.now()
    filename = f"support_emails_{week_start.strftime('%Y%m%d')}.mbox"
    
    print(f"\nDownload Configuration:")
    print(f"  Query: {SEARCH_QUERY}")
    print(f"  Period: Last {DAYS_BACK} days")
    print(f"  Output: {filename}")
    print()
    
    # Download
    try:
        downloader.download_to_mbox(
            output_file=filename,
            query=SEARCH_QUERY,
            max_results=MAX_RESULTS,
            days_back=DAYS_BACK,
            show_progress=True
        )
        
        print(f"\n✓ Weekly download complete!")
        print(f"  File: {filename}")
        print(f"\nNext steps:")
        print(f"  1. Run: python email_analyzer_mbox.py")
        print(f"  2. Enter file: {filename}")
        print(f"  3. Review weekly report")
        
        return True
        
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False


if __name__ == "__main__":
    success = download_weekly_support_emails()
    
    if success:
        print("\n" + "="*70)
        print("SUCCESS - Ready for analysis!")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("FAILED - Check errors above")
        print("="*70)
