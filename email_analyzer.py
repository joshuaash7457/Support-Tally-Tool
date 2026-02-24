import os
import csv
import json
from collections import Counter
from datetime import datetime

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
                    "not connecting", "connection error", "network issue"
                ],
                "Firmware": [
                    "firmware", "update", "upgrade", "version", 
                    "flash", "software update"
                ],
                "PTZ Control": [
                    "pan", "tilt", "zoom", "movement", 
                    "control", "preset"
                ],
                "Streaming": [
                    "stream", "streaming", "rtmp", "rtsp", "srt",
                    "video quality", "latency", "buffering"
                ],
                "Camera Models": [
                    "move 4k", "move se",
                    "g2", "studio pro", "studio se", "studio 4k", "simpltrack",
                    "simpletrack"
                ],
                "Software": [
                    "ptzoptics app", "ip camera tool",
                    "companion", "software", "cmp", "camera management platform",
                    "1.4.1 app"
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
                    # Combine subject and body for searching
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
                # Split by common email separators
                # Adjust this based on your export format
                emails = content.split('\n\n---\n\n')  # Common separator
                if len(emails) == 1:
                    emails = content.split('\n\n\n')  # Try triple newline
            print(f"Loaded {len(emails)} emails from {filepath}")
        except Exception as e:
            print(f"Error reading text file: {e}")
        return emails
    
    def analyze_emails(self, emails):
        """
        Analyze emails for keyword occurrences
        
        Args:
            emails: List of email text strings
        
        Returns:
            Dictionary with results
        """
        self.results = {
            'total_emails': len(emails),
            'categories': {},
            'keyword_details': {}
        }
        
        for category, keywords in self.keyword_categories.items():
            category_count = 0
            emails_with_category = 0
            keyword_counts = Counter()
            
            for email in emails:
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
        report_lines.append("=" * 60)
        report_lines.append("EMAIL ANALYSIS REPORT")
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("=" * 60)
        report_lines.append(f"\nTotal Emails Analyzed: {self.results['total_emails']}")
        report_lines.append("\n" + "-" * 60)
        
        # Sort categories by total mentions (descending)
        sorted_categories = sorted(
            self.results['categories'].items(),
            key=lambda x: x[1]['total_mentions'],
            reverse=True
        )
        
        for category, data in sorted_categories:
            report_lines.append(f"\n{category.upper()}")
            report_lines.append(f"  Total Mentions: {data['total_mentions']}")
            report_lines.append(f"  Emails Affected: {data['emails_with_category']}")
            
            if data['keywords']:
                report_lines.append("  Top Keywords:")
                # Sort keywords by count
                sorted_keywords = sorted(
                    data['keywords'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]  # Top 5 keywords
                for keyword, count in sorted_keywords:
                    report_lines.append(f"    - {keyword}: {count}")
        
        report_lines.append("\n" + "=" * 60)
        
        report_text = "\n".join(report_lines)
        print(report_text)
        
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    f.write(report_text)
                print(f"\nReport saved to {output_file}")
            except Exception as e:
                print(f"Error saving report: {e}")
        
        return report_text


def main():
    """Example usage"""
    print("PTZOptics Email Analyzer")
    print("-" * 40)
    
    # Initialize analyzer
    analyzer = EmailAnalyzer()
    
    # Example: Save default keywords to a file for editing
    analyzer.save_keywords('keywords.json')
    print("\nDefault keywords saved to 'keywords.json'")
    print("You can edit this file to customize categories and keywords.\n")
    
    # Get file path from user
    file_path = input("Enter the path to your email export file: ").strip()
    
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return
    
    # Determine file type and read emails
    emails = []
    if file_path.endswith('.csv'):
        # For CSV files, you might need to adjust column names
        print("\nFor CSV files, common column names are:")
        print("  - 'Body', 'Content', 'Message', 'Email Body'")
        print("  - 'Subject', 'Email Subject', 'Title'")
        body_col = input("Enter the body column name (or press Enter for 'Body'): ").strip() or 'Body'
        subject_col = input("Enter the subject column name (or press Enter for 'Subject'): ").strip() or 'Subject'
        emails = analyzer.read_csv_file(file_path, body_col, subject_col)
    elif file_path.endswith('.txt'):
        emails = analyzer.read_text_file(file_path)
    else:
        print("Unsupported file format. Please use .csv or .txt files.")
        return
    
    if not emails:
        print("No emails found in file.")
        return
    
    # Analyze emails
    print("\nAnalyzing emails...")
    analyzer.analyze_emails(emails)
    
    # Generate and save report
    report_file = f"email_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    analyzer.generate_report(report_file)


if __name__ == "__main__":
    main()
