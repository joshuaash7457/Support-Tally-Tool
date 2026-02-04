import os
import csv
import json
import mailbox
from collections import Counter
from datetime import datetime
import email
from email import policy
from email.parser import BytesParser

class EmailAnalyzer:
    def __init__(self, keywords_file=None):
        """
        Initialize the Email Analyzer
        
        Args:
            keywords_file: Optional path to a JSON file containing categories and keywords
        """
        self.keyword_categories = {}
        self.results = {}
        
        if keywords_file and os.path.exists(keywords_file):
            self.load_keywords(keywords_file)
        else:
            # Default keywords - customize these for PTZOptics support
            self.keyword_categories = {
                "Connection Issues": [
                    "won't connect", "can't connect", "connection failed", 
                    "not connecting", "connection error", "network issue",
                    "can not connect", "unable to connect", "no connection",
                    "connection timeout", "network problem"
                ],
                "Firmware": [
                    "firmware", "update", "upgrade", "version", 
                    "flash", "software update", "latest firmware",
                    "firmware download", "firmware version"
                ],
                "PTZ Control": [
                    "pan", "tilt", "zoom", "ptz", "movement", 
                    "control", "joystick", "preset", "position",
                    "camera movement", "ptz control"
                ],
                "Streaming": [
                    "stream", "streaming", "rtmp", "rtsp", "srt",
                    "video quality", "latency", "buffering", "live stream",
                    "video output", "ndi", "sdi"
                ],
                "Camera Models": [
                    "20x", "12x", "30x", "move 4k", "move se",
                    "pt20x", "pt12x", "pt30x", "supercam"
                ],
                "Software": [
                    "ptzoptics app", "ip camera tool", "obs",
                    "vmix", "companion", "software", "application",
                    "desktop app"
                ],
                "Power Issues": [
                    "won't turn on", "no power", "power supply",
                    "not powering", "power issue", "poe",
                    "power adapter", "power problem"
                ],
                "Video Quality": [
                    "blurry", "pixelated", "poor quality", "grainy",
                    "dark", "overexposed", "image quality", "video quality",
                    "focus", "clarity"
                ],
                "Audio": [
                    "audio", "sound", "microphone", "no audio",
                    "mic", "audio input", "audio output", "volume"
                ],
                "Setup/Installation": [
                    "setup", "install", "installation", "configuration",
                    "configure", "initial setup", "getting started"
                ]
            }
    
    def load_keywords(self, filepath):
        """Load keywords from a JSON file"""
        try:
            with open(filepath, 'r') as f:
                self.keyword_categories = json.load(f)
            print(f"Loaded keywords from {filepath}")
        except Exception as e:
            print(f"Error loading keywords: {e}")
    
    def save_keywords(self, filepath):
        """Save current keywords to a JSON file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.keyword_categories, f, indent=2)
            print(f"Keywords saved to {filepath}")
        except Exception as e:
            print(f"Error saving keywords: {e}")
    
    def add_category(self, category_name, keywords):
        """Add a new category with keywords"""
        self.keyword_categories[category_name] = keywords
    
    def read_mbox_file(self, filepath, max_emails=None, show_progress=True):
        """
        Read emails from an mbox file (efficient for large files)
        
        Args:
            filepath: Path to the mbox file
            max_emails: Optional limit on number of emails to process (None = all)
            show_progress: Show progress while reading
        
        Returns:
            List of email texts (subject + body combined)
        """
        emails = []
        print(f"\nOpening mbox file: {filepath}")
        print("This may take a moment for large files...")
        
        try:
            # Get file size for progress tracking
            file_size = os.path.getsize(filepath)
            file_size_mb = file_size / (1024 * 1024)
            print(f"File size: {file_size_mb:.2f} MB")
            
            mbox = mailbox.mbox(filepath)
            total_messages = len(mbox)
            print(f"Total messages in mbox: {total_messages}")
            
            if max_emails:
                print(f"Processing first {max_emails} emails...")
            else:
                print("Processing all emails...")
            
            count = 0
            for i, message in enumerate(mbox):
                if max_emails and count >= max_emails:
                    break
                
                # Show progress every 100 emails
                if show_progress and (i + 1) % 100 == 0:
                    print(f"  Processed {i + 1}/{total_messages if not max_emails else max_emails} emails...")
                
                try:
                    email_text = self._extract_email_content(message)
                    if email_text:
                        emails.append(email_text)
                        count += 1
                except Exception as e:
                    # Skip problematic emails
                    continue
            
            print(f"\nSuccessfully loaded {len(emails)} emails from mbox file")
            
        except Exception as e:
            print(f"Error reading mbox file: {e}")
        
        return emails
    
    def _extract_email_content(self, message):
        """
        Extract subject and body content from an email message
        
        Args:
            message: Email message object
        
        Returns:
            Combined text string
        """
        email_text = ""
        
        # Get subject
        subject = message.get('Subject', '')
        if subject:
            email_text += subject + " "
        
        # Get body
        if message.is_multipart():
            # Handle multipart messages
            for part in message.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    try:
                        payload = part.get_payload(decode=True)
                        if payload:
                            email_text += payload.decode('utf-8', errors='ignore')
                    except:
                        pass
        else:
            # Handle simple messages
            try:
                payload = message.get_payload(decode=True)
                if payload:
                    email_text += payload.decode('utf-8', errors='ignore')
            except:
                pass
        
        return email_text
    
    def read_csv_file(self, filepath, email_column='Body', subject_column='Subject'):
        """
        Read emails from a CSV file
        
        Args:
            filepath: Path to the CSV file
            email_column: Name of the column containing email body
            subject_column: Name of the column containing email subject
        
        Returns:
            List of email texts (subject + body combined)
        """
        emails = []
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    email_text = ""
                    if subject_column in row:
                        email_text += row[subject_column] + " "
                    if email_column in row:
                        email_text += row[email_column]
                    emails.append(email_text)
            print(f"Loaded {len(emails)} emails from {filepath}")
        except Exception as e:
            print(f"Error reading CSV file: {e}")
        return emails
    
    def read_text_file(self, filepath):
        """
        Read emails from a plain text file
        Assumes emails are separated by a delimiter or blank lines
        """
        emails = []
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                emails = content.split('\n\n---\n\n')
                if len(emails) == 1:
                    emails = content.split('\n\n\n')
            print(f"Loaded {len(emails)} emails from {filepath}")
        except Exception as e:
            print(f"Error reading text file: {e}")
        return emails
    
    def analyze_emails(self, emails, show_progress=True):
        """
        Analyze emails for keyword occurrences
        
        Args:
            emails: List of email text strings
            show_progress: Show progress during analysis
        
        Returns:
            Dictionary with results
        """
        print(f"\nAnalyzing {len(emails)} emails...")
        
        self.results = {
            'total_emails': len(emails),
            'categories': {},
            'keyword_details': {}
        }
        
        for category, keywords in self.keyword_categories.items():
            category_count = 0
            emails_with_category = 0
            keyword_counts = Counter()
            
            for i, email in enumerate(emails):
                if show_progress and (i + 1) % 100 == 0:
                    print(f"  Analyzing email {i + 1}/{len(emails)}...")
                
                email_lower = email.lower()
                email_has_category = False
                
                for keyword in keywords:
                    keyword_lower = keyword.lower()
                    count = email_lower.count(keyword_lower)
                    if count > 0:
                        category_count += count
                        keyword_counts[keyword] += count
                        email_has_category = True
                
                if email_has_category:
                    emails_with_category += 1
            
            self.results['categories'][category] = {
                'total_mentions': category_count,
                'emails_with_category': emails_with_category,
                'keywords': dict(keyword_counts)
            }
        
        print("Analysis complete!")
        return self.results
    
    def generate_report(self, output_file=None):
        """
        Generate a human-readable report
        
        Args:
            output_file: Optional path to save the report
        """
        if not self.results:
            print("No results to report. Run analyze_emails() first.")
            return
        
        report_lines = []
        report_lines.append("=" * 70)
        report_lines.append("PTZOPTICS SUPPORT EMAIL ANALYSIS REPORT")
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("=" * 70)
        report_lines.append(f"\nTotal Emails Analyzed: {self.results['total_emails']}")
        report_lines.append("\n" + "-" * 70)
        
        # Sort categories by total mentions (descending)
        sorted_categories = sorted(
            self.results['categories'].items(),
            key=lambda x: x[1]['total_mentions'],
            reverse=True
        )
        
        for category, data in sorted_categories:
            if data['total_mentions'] == 0:
                continue  # Skip categories with no mentions
            
            report_lines.append(f"\n{category.upper()}")
            report_lines.append(f"  Total Mentions: {data['total_mentions']}")
            report_lines.append(f"  Emails Affected: {data['emails_with_category']} " + 
                              f"({data['emails_with_category']/self.results['total_emails']*100:.1f}%)")
            
            if data['keywords']:
                report_lines.append("  Top Keywords:")
                sorted_keywords = sorted(
                    data['keywords'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10]  # Top 10 keywords
                for keyword, count in sorted_keywords:
                    report_lines.append(f"    - {keyword}: {count}")
        
        report_lines.append("\n" + "=" * 70)
        
        report_text = "\n".join(report_lines)
        print("\n" + report_text)
        
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    f.write(report_text)
                print(f"\nReport saved to {output_file}")
            except Exception as e:
                print(f"Error saving report: {e}")
        
        return report_text


def main():
    """Main program with mbox support"""
    print("=" * 70)
    print("PTZOptics Email Analyzer - MBOX Edition")
    print("=" * 70)
    
    # Initialize analyzer
    keywords_file = 'keywords.json'
    if os.path.exists(keywords_file):
        analyzer = EmailAnalyzer(keywords_file)
        print(f"\nLoaded keywords from {keywords_file}")
    else:
        analyzer = EmailAnalyzer()
        analyzer.save_keywords(keywords_file)
        print(f"\nCreated default keywords file: {keywords_file}")
        print("You can edit this file to customize categories and keywords.")
    
    # Get file path from user
    print("\n" + "-" * 70)
    file_path = input("\nEnter the path to your email file (.mbox, .csv, or .txt): ").strip()
    
    # Remove quotes if user wrapped the path
    file_path = file_path.strip('"').strip("'")
    
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return
    
    # Determine file type and read emails
    emails = []
    
    if file_path.endswith('.mbox') or file_path.endswith('.mbx'):
        # For large mbox files, ask if they want to limit the number
        print("\n" + "-" * 70)
        print("MBOX file detected!")
        limit = input("Process all emails? (y/n, or enter a number to limit): ").strip().lower()
        
        max_emails = None
        if limit.isdigit():
            max_emails = int(limit)
        elif limit == 'n':
            max_emails = int(input("How many emails to process? "))
        
        emails = analyzer.read_mbox_file(file_path, max_emails=max_emails)
        
    elif file_path.endswith('.csv'):
        print("\nFor CSV files, common column names are:")
        print("  - 'Body', 'Content', 'Message', 'Email Body'")
        print("  - 'Subject', 'Email Subject', 'Title'")
        body_col = input("Enter the body column name (or press Enter for 'Body'): ").strip() or 'Body'
        subject_col = input("Enter the subject column name (or press Enter for 'Subject'): ").strip() or 'Subject'
        emails = analyzer.read_csv_file(file_path, body_col, subject_col)
        
    elif file_path.endswith('.txt'):
        emails = analyzer.read_text_file(file_path)
        
    else:
        print("Unsupported file format. Please use .mbox, .csv, or .txt files.")
        return
    
    if not emails:
        print("No emails found in file.")
        return
    
    # Analyze emails
    print("\n" + "-" * 70)
    analyzer.analyze_emails(emails)
    
    # Generate and save report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f"email_report_{timestamp}.txt"
    analyzer.generate_report(report_file)
    
    print("\n" + "=" * 70)
    print("Analysis complete!")
    print(f"Report saved to: {report_file}")
    print("=" * 70)


if __name__ == "__main__":
    main()
