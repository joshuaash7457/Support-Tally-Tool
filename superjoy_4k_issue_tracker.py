#!/usr/bin/env python3
"""
Enhanced Issue Tracker for SuperJoy 4K Freezing Issues
Specialized tracker for monitoring SuperJoy controller freezing when handling high-bitrate 4K streams
"""

import os
import csv
import json
import mailbox
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import re

class SuperJoyIssueTracker:
    def __init__(self, issue_config_file=None):
        """
        Initialize the SuperJoy Issue Tracker for monitoring 4K freezing issues
        
        Args:
            issue_config_file: Path to JSON file with issue configuration
        """
        self.issue_config = {}
        self.results = {}
        self.affected_emails = []
        self.severity_scores = {}
        
        if issue_config_file and os.path.exists(issue_config_file):
            self.load_issue_config(issue_config_file)
    
    def load_issue_config(self, filepath):
        """Load issue configuration from JSON file"""
        try:
            with open(filepath, 'r') as f:
                self.issue_config = json.load(f)
            print(f"✓ Loaded SuperJoy 4K issue configuration from {filepath}")
            print(f"  Tracking: {self.issue_config.get('issue_name', 'Unknown Issue')}")
            print(f"  Issue ID: {self.issue_config.get('issue_id', 'N/A')}")
        except Exception as e:
            print(f"✗ Error loading issue config: {e}")
    
    def read_mbox_file(self, filepath, max_emails=None, show_progress=True):
        """Read emails from mbox file"""
        emails = []
        metadata = []
        
        print(f"\nOpening mbox file: {filepath}")
        
        try:
            mbox = mailbox.mbox(filepath)
            total_messages = len(mbox)
            print(f"Total messages: {total_messages}")
            
            count = 0
            for i, message in enumerate(mbox):
                if max_emails and count >= max_emails:
                    break
                
                if show_progress and (i + 1) % 100 == 0:
                    print(f"  Processed {i + 1} emails...")
                
                try:
                    email_text = self._extract_email_content(message)
                    if email_text:
                        emails.append(email_text)
                        
                        meta = {
                            'subject': message.get('Subject', ''),
                            'from': message.get('From', ''),
                            'date': message.get('Date', ''),
                            'message_id': message.get('Message-ID', f'email_{count}')
                        }
                        metadata.append(meta)
                        count += 1
                except:
                    continue
            
            print(f"✓ Loaded {len(emails)} emails")
            
        except Exception as e:
            print(f"✗ Error reading mbox: {e}")
        
        return emails, metadata
    
    def _extract_email_content(self, message):
        """Extract text content from email message"""
        email_text = ""
        
        subject = message.get('Subject', '')
        if subject:
            email_text += subject + " "
        
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == 'text/plain':
                    try:
                        payload = part.get_payload(decode=True)
                        if payload:
                            email_text += payload.decode('utf-8', errors='ignore')
                    except:
                        pass
        else:
            try:
                payload = message.get_payload(decode=True)
                if payload:
                    email_text += payload.decode('utf-8', errors='ignore')
            except:
                pass
        
        return email_text
    
    def calculate_severity_score(self, matched_keywords, matched_symptoms, email_text):
        """Calculate severity score for an affected email based on keyword matches"""
        score = 0
        severity_factors = {
            'critical_symptoms': ['freezing', 'frozen', 'unresponsive', 'reboot required', 'locked up'],
            '4k_indicators': ['4k', '4k video', '4k stream', 'high bitrate'],
            'hdmi_issues': ['hdmi output', 'hdmi not working', 'monitor issues', 'display problems'],
            'performance_impact': ['slows down', 'impacts performance', 'high bandwidth', 'processing load']
        }
        
        email_lower = email_text.lower()
        
        # Base score for any match
        score += 1
        
        # Critical symptom multiplier
        for symptom in severity_factors['critical_symptoms']:
            if symptom in email_lower:
                score += 3
        
        # 4K context multiplier
        for indicator in severity_factors['4k_indicators']:
            if indicator in email_lower:
                score += 2
        
        # HDMI output issues
        for hdmi_term in severity_factors['hdmi_issues']:
            if hdmi_term in email_lower:
                score += 2
        
        # Performance impact
        for perf_term in severity_factors['performance_impact']:
            if perf_term in email_lower:
                score += 1
        
        # Multiple keyword matches indicate severity
        if len(matched_keywords) >= 3:
            score += 2
        if len(matched_symptoms) >= 3:
            score += 3
        
        # Look for specific bitrate mentions
        bitrate_pattern = r'(\d+)\s*mbps|(\d+)\s*mb/s'
        bitrate_matches = re.findall(bitrate_pattern, email_lower)
        for match in bitrate_matches:
            bitrate = int(match[0] or match[1])
            if bitrate > 25:  # High bitrate indicator
                score += 3
            elif bitrate > 15:
                score += 1
        
        return min(score, 20)  # Cap at 20
    
    def analyze_for_superjoy_issue(self, emails, metadata):
        """Analyze emails for SuperJoy 4K freezing issues"""
        if not self.issue_config:
            print("No issue configuration loaded")
            return
        
        print(f"\nAnalyzing {len(emails)} emails for SuperJoy 4K issues...")
        
        keywords = self.issue_config.get('keywords', {})
        exclude_words = self.issue_config.get('exclude_keywords', [])
        
        # Initialize results
        self.results = {
            'total_emails': len(emails),
            'affected_emails': 0,
            'severity_scores': []
        }
        
        self.affected_emails = []
        
        for i, email_text in enumerate(emails):
            email_lower = email_text.lower()
            email_meta = metadata[i] if i < len(metadata) else {}
            
            # Skip excluded emails
            if any(exclude_word.lower() in email_lower for exclude_word in exclude_words):
                continue
            
            # Check for matches
            matched_primary = [kw for kw in keywords.get('primary', []) if kw.lower() in email_lower]
            matched_symptoms = [kw for kw in keywords.get('symptoms', []) if kw.lower() in email_lower]
            matched_video = [kw for kw in keywords.get('video_related', []) if kw.lower() in email_lower]
            
            # Must have SuperJoy mention and symptoms
            if not matched_primary or not matched_symptoms:
                continue
            
            # Calculate severity score
            severity_score = self.calculate_severity_score(matched_primary + matched_symptoms, matched_symptoms, email_text)
            
            # Store affected email
            email_data = {
                'email_text': email_text[:300] + "..." if len(email_text) > 300 else email_text,
                'metadata': email_meta,
                'matched_keywords': matched_primary,
                'matched_symptoms': matched_symptoms,
                'matched_video': matched_video,
                'severity_score': severity_score
            }
            
            self.affected_emails.append(email_data)
            self.results['affected_emails'] += 1
            self.results['severity_scores'].append(severity_score)
        
        # Sort by severity
        self.affected_emails.sort(key=lambda x: x['severity_score'], reverse=True)
        
        print(f"Found {self.results['affected_emails']} emails with SuperJoy 4K issues")
        
        if self.results['affected_emails'] > 0:
            avg_severity = sum(self.results['severity_scores']) / len(self.results['severity_scores'])
            print(f"Average severity score: {avg_severity:.1f}")
    
    def generate_report(self, output_file=None):
        """Generate SuperJoy 4K issue report"""
        if not self.results:
            print("No results to report")
            return
        
        lines = []
        lines.append("=" * 60)
        lines.append("SUPERJOY 4K FREEZING ISSUE REPORT")
        lines.append("=" * 60)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Issue: {self.issue_config.get('issue_name', 'SuperJoy 4K Freezing')}")
        
        # Summary
        lines.append(f"\nTotal Emails: {self.results['total_emails']}")
        lines.append(f"SuperJoy 4K Issues Found: {self.results['affected_emails']}")
        
        if self.results['affected_emails'] > 0:
            percentage = (self.results['affected_emails'] / self.results['total_emails']) * 100
            lines.append(f"Percentage Affected: {percentage:.1f}%")
            
            avg_severity = sum(self.results['severity_scores']) / len(self.results['severity_scores'])
            lines.append(f"Average Severity: {avg_severity:.1f}/20")
            
            # Alert status
            alert_threshold = self.issue_config.get('tracking_metrics', {}).get('alert_threshold', 5)
            if self.results['affected_emails'] >= alert_threshold:
                lines.append(f"\n*** ALERT: {self.results['affected_emails']} cases exceed threshold of {alert_threshold} ***")
        
        # Top cases
        if self.affected_emails:
            lines.append(f"\nTop 10 Cases by Severity:")
            lines.append("-" * 60)
            
            for i, email_data in enumerate(self.affected_emails[:10], 1):
                lines.append(f"\n{i}. Severity: {email_data['severity_score']}/20")
                meta = email_data.get('metadata', {})
                if meta.get('subject'):
                    lines.append(f"   Subject: {meta['subject']}")
                lines.append(f"   Symptoms: {', '.join(email_data['matched_symptoms'])}")
                lines.append(f"   Preview: {email_data['email_text'][:200]}...")
        
        # Recommendations
        solutions = self.issue_config.get('solutions', {})
        lines.append(f"\nRecommended Actions:")
        lines.append("-" * 60)
        for action in solutions.get('immediate_workarounds', [])[:5]:
            lines.append(f"• {action}")
        
        lines.append("\n" + "=" * 60)
        
        report_text = "\n".join(lines)
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
    """Main program for SuperJoy 4K issue tracking"""
    print("SUPERJOY 4K FREEZING ISSUE TRACKER")
    print("=" * 50)
    
    # Get config file
    config_file = input("Enter SuperJoy config file path: ").strip().strip('"').strip("'")
    
    if not os.path.exists(config_file):
        print(f"Config file not found: {config_file}")
        return
    
    # Get email file
    email_file = input("Enter email file path (.mbox): ").strip().strip('"').strip("'")
    
    if not os.path.exists(email_file):
        print(f"Email file not found: {email_file}")
        return
    
    # Initialize tracker and load config
    tracker = SuperJoyIssueTracker()
    tracker.load_issue_config(config_file)
    
    # Read emails
    emails, metadata = tracker.read_mbox_file(email_file)
    
    if not emails:
        print("No emails found")
        return
    
    # Analyze
    tracker.analyze_for_superjoy_issue(emails, metadata)
    
    # Generate report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f"superjoy_report_{timestamp}.txt"
    tracker.generate_report(report_file)


if __name__ == "__main__":
    main()
