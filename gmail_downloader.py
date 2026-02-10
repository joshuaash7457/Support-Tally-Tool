#!/usr/bin/env python3
"""
Gmail Email Downloader
Downloads emails from Gmail and saves to mbox format for analysis
"""

import os
import sys
import pickle
import base64
import mailbox
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import email

# Gmail API scope - readonly access
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailDownloader:
    def __init__(self, credentials_file='credentials.json', token_file='token.pickle'):
        """
        Initialize Gmail Downloader
        
        Args:
            credentials_file: Path to OAuth credentials from Google Cloud Console
            token_file: Path to save authorization token (auto-generated)
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
    
    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        
        # Check if we have a saved token
        if os.path.exists(self.token_file):
            print("Loading saved credentials...")
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("Refreshing expired credentials...")
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    print(f"\n❌ ERROR: {self.credentials_file} not found!")
                    print("\nYou need to set up Gmail API credentials first.")
                    print("See GMAIL_SETUP_GUIDE.md for instructions.")
                    sys.exit(1)
                
                print("\nFirst time setup - opening browser for authorization...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next time
            print("Saving credentials...")
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        print("✓ Authentication successful!")
        self.service = build('gmail', 'v1', credentials=creds)
        return self.service
    
    def get_messages(self, query='', max_results=None, days_back=7):
        """
        Get list of messages matching query
        
        Args:
            query: Gmail search query (e.g., 'from:support@example.com')
            max_results: Maximum number of messages to retrieve (None = all)
            days_back: Number of days to look back (default: 7)
        
        Returns:
            List of message IDs
        """
        if not self.service:
            print("Not authenticated! Call authenticate() first.")
            return []
        
        # Add date filter to query
        date_filter = self._get_date_query(days_back)
        if query:
            full_query = f"{query} {date_filter}"
        else:
            full_query = date_filter
        
        print(f"\nSearching Gmail with query: {full_query}")
        
        messages = []
        page_token = None
        
        try:
            while True:
                results = self.service.users().messages().list(
                    userId='me',
                    q=full_query,
                    pageToken=page_token,
                    maxResults=500
                ).execute()
                
                if 'messages' in results:
                    messages.extend(results['messages'])
                    print(f"  Found {len(messages)} messages so far...")
                
                page_token = results.get('nextPageToken')
                
                if not page_token or (max_results and len(messages) >= max_results):
                    break
            
            if max_results:
                messages = messages[:max_results]
            
            print(f"✓ Total messages found: {len(messages)}")
            
        except Exception as e:
            print(f"❌ Error searching messages: {e}")
            return []
        
        return messages
    
    def _get_date_query(self, days_back):
        """Generate date query for Gmail search"""
        date_from = datetime.now() - timedelta(days=days_back)
        date_str = date_from.strftime('%Y/%m/%d')
        return f"after:{date_str}"
    
    def download_message(self, msg_id):
        """
        Download a single message in RFC822 format
        
        Args:
            msg_id: Gmail message ID
        
        Returns:
            Email message object or None
        """
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=msg_id,
                format='raw'
            ).execute()
            
            # Decode the raw message
            msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
            mime_msg = email.message_from_bytes(msg_str)
            
            return mime_msg
            
        except Exception as e:
            print(f"  ⚠ Error downloading message {msg_id}: {e}")
            return None
    
    def download_to_mbox(self, output_file, query='', max_results=None, days_back=7, show_progress=True):
        """
        Download messages and save to mbox file
        
        Args:
            output_file: Path to output mbox file
            query: Gmail search query
            max_results: Max messages to download (None = all)
            days_back: Days to look back (default: 7)
            show_progress: Show download progress
        """
        print("\n" + "="*70)
        print("GMAIL EMAIL DOWNLOADER")
        print("="*70)
        
        # Authenticate if needed
        if not self.service:
            self.authenticate()
        
        # Get message list
        messages = self.get_messages(query, max_results, days_back)
        
        if not messages:
            print("\n⚠ No messages found matching criteria")
            return
        
        # Create mbox file
        print(f"\nDownloading {len(messages)} messages to {output_file}...")
        mbox = mailbox.mbox(output_file)
        mbox.lock()
        
        try:
            downloaded = 0
            skipped = 0
            
            for i, msg_info in enumerate(messages, 1):
                if show_progress and i % 10 == 0:
                    print(f"  Progress: {i}/{len(messages)} ({i/len(messages)*100:.1f}%)")
                
                msg = self.download_message(msg_info['id'])
                
                if msg:
                    mbox.add(msg)
                    downloaded += 1
                else:
                    skipped += 1
            
            mbox.unlock()
            mbox.close()
            
            print("\n" + "="*70)
            print("✓ DOWNLOAD COMPLETE!")
            print("="*70)
            print(f"  Downloaded: {downloaded} emails")
            if skipped > 0:
                print(f"  Skipped: {skipped} emails (errors)")
            print(f"  Saved to: {output_file}")
            print(f"  File size: {os.path.getsize(output_file) / (1024*1024):.2f} MB")
            print("="*70)
            
        except Exception as e:
            print(f"\n❌ Error during download: {e}")
            mbox.unlock()
            mbox.close()


def main():
    """Interactive mode for downloading emails"""
    print("="*70)
    print("PTZOPTICS GMAIL EMAIL DOWNLOADER")
    print("="*70)
    
    downloader = GmailDownloader()
    
    # Authenticate
    try:
        downloader.authenticate()
    except Exception as e:
        print(f"\n❌ Authentication failed: {e}")
        print("\nMake sure you have:")
        print("1. Created credentials.json (see GMAIL_SETUP_GUIDE.md)")
        print("2. Enabled Gmail API in Google Cloud Console")
        return
    
    print("\n" + "-"*70)
    print("DOWNLOAD OPTIONS")
    print("-"*70)
    
    # Get download preferences
    print("\nWhat emails do you want to download?")
    print("Examples:")
    print("  - All emails: just press Enter")
    print("  - From specific address: from:support@ptzoptics.com")
    print("  - To specific address: to:support@ptzoptics.com")
    print("  - Subject contains: subject:camera")
    print("  - Label/folder: label:support")
    print("  - Combine: from:customer@example.com subject:urgent")
    
    query = input("\nEnter search query (or Enter for all): ").strip()
    
    # Time period
    print("\nHow far back should I look?")
    days_input = input("Enter number of days (default: 7 for last week): ").strip()
    days_back = int(days_input) if days_input.isdigit() else 7
    
    # Max results
    print("\nLimit number of emails?")
    max_input = input("Max emails to download (or Enter for all): ").strip()
    max_results = int(max_input) if max_input.isdigit() else None
    
    # Output file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    default_filename = f"gmail_emails_{timestamp}.mbox"
    output_file = input(f"\nOutput filename (default: {default_filename}): ").strip()
    if not output_file:
        output_file = default_filename
    
    # Add .mbox extension if missing
    if not output_file.endswith('.mbox'):
        output_file += '.mbox'
    
    # Confirm
    print("\n" + "-"*70)
    print("DOWNLOAD SUMMARY")
    print("-"*70)
    print(f"  Query: {query if query else 'All emails'}")
    print(f"  Time period: Last {days_back} days")
    print(f"  Max results: {max_results if max_results else 'Unlimited'}")
    print(f"  Output file: {output_file}")
    print("-"*70)
    
    confirm = input("\nProceed with download? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("Download cancelled.")
        return
    
    # Download!
    downloader.download_to_mbox(
        output_file=output_file,
        query=query,
        max_results=max_results,
        days_back=days_back
    )
    
    print(f"\n✓ Ready to analyze! Run:")
    print(f"  python email_analyzer_mbox.py")
    print(f"  Then enter: {output_file}")


if __name__ == "__main__":
    main()
