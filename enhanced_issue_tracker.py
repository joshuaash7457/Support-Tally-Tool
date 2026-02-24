import os
import csv
import json
import mailbox
from collections import Counter, defaultdict
from datetime import datetime
import re

class IssueTracker:
    def __init__(self, issue_config_file=None):
        """
        Initialize the Issue Tracker for monitoring specific critical issues
        
        Args:
            issue_config_file: Path to JSON file with issue configuration
        """
        self.issue_config = {}
        self.results = {}
        self.affected_emails = []
        
        if issue_config_file and os.path.exists(issue_config_file):
            self.load_issue_config(issue_config_file)
    
    def calculate_severity_score(self, matched_keywords, matched_symptoms, email_text):
        """Calculate severity score for an email based on keyword matches and content"""
        score = 0
        email_lower = email_text.lower()
        
        # Base score for any match
        score += 1
        
        # Get priority keywords from config if available
        priority_keywords = self.issue_config.get('tracking_metrics', {}).get('priority_keywords', [])
        
        # Priority keyword multiplier
        for keyword in priority_keywords:
            if keyword.lower() in email_lower:
                score += 3
        
        # Multiple keyword matches indicate higher severity
        if len(matched_keywords) >= 3:
            score += 2
        if len(matched_symptoms) >= 3:
            score += 3
        elif len(matched_symptoms) >= 2:
            score += 1
        
        # Check for severity indicators in symptoms
        high_severity_symptoms = ['freezing', 'frozen', 'unresponsive', 'reboot required', 'locked up', 'not working']
        for symptom in matched_symptoms:
            if any(severe in symptom.lower() for severe in high_severity_symptoms):
                score += 2
        
        # Look for urgency indicators
        urgency_words = ['urgent', 'critical', 'broken', 'failed', 'error', 'issue', 'problem']
        for word in urgency_words:
            if word in email_lower:
                score += 1
        
        # Look for impact indicators
        impact_words = ['production', 'live', 'customer', 'client', 'broadcast', 'streaming']
        for word in impact_words:
            if word in email_lower:
                score += 2
        
        # Look for quantity indicators (multiple instances, repeated issues)
        if 'multiple' in email_lower or 'several' in email_lower or 'many' in email_lower:
            score += 1
        
        # Check for specific technical details (numbers, models, etc.)
        if re.search(r'\d+', email_text):  # Contains numbers (versions, quantities, etc.)
            score += 1
        
        return min(score, 20)  # Cap at 20
    
    def load_issue_config(self, filepath):
        """Load issue configuration from JSON file"""
        try:
            with open(filepath, 'r') as f:
                self.issue_config = json.load(f)
            print(f"✓ Loaded issue configuration from {filepath}")
        except Exception as e:
            print(f"✗ Error loading issue config: {e}")
    
    def save_issue_config(self, filepath):
        """Save current issue configuration to JSON file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.issue_config, f, indent=2)
            print(f"✓ Issue configuration saved to {filepath}")
        except Exception as e:
            print(f"✗ Error saving issue config: {e}")
    
    def create_issue_template(self, filepath):
        """Create a template issue configuration file"""
        template = {
            "issue_name": "CMP Autotracking Failure After Update",
            "issue_id": "CMP-AT-2025-001",
            "date_reported": "2025-01-27",
            "severity": "CRITICAL",
            "description": "Camera Management Platform autotracking feature stopped working after firmware update",
            "keywords": {
                "primary": [
                    "cmp",
                    "camera management platform",
                    "autotracking",
                    "auto tracking",
                    "auto-tracking"
                ],
                "symptoms": [
                    "autotracking not working",
                    "autotracking stopped",
                    "autotracking failed",
                    "tracking not working",
                    "won't track",
                    "can't track",
                    "tracking broken"
                ],
                "context": [
                    "after update",
                    "firmware update",
                    "software update",
                    "new version",
                    "upgraded"
                ]
            },
            "exclude_keywords": [
                "resolved",
                "fixed",
                "working now",
                "solved"
            ],
            "affected_products": [
                "cmp",
                "camera management platform",
                "pt20x",
                "pt30x",
                "pt12x"
            ],
            "match_criteria": {
                "require_primary": true,
                "require_symptom": true,
                "require_context": false,
                "match_mode": "any"
            },
            "tracking_metrics": {
                "alert_threshold": 5,
                "escalation_threshold": 10,
                "priority_keywords": [
                    "autotracking",
                    "not working",
                    "failed"
                ]
            }
        }
        
        try:
            with open(filepath, 'w') as f:
                json.dump(template, f, indent=2)
            print(f"✓ Template created: {filepath}")
            print("\nEdit this file to customize for your specific issue.")
        except Exception as e:
            print(f"✗ Error creating template: {e}")
    
    def read_mbox_file(self, filepath, max_emails=None, show_progress=True):
        """Read emails from mbox file"""
        emails = []
        metadata = []
        
        print(f"\nOpening mbox file: {filepath}")
        
        try:
            file_size = os.path.getsize(filepath) / (1024 * 1024)
            print(f"File size: {file_size:.2f} MB")
            
            mbox = mailbox.mbox(filepath)
            total_messages = len(mbox)
            print(f"Total messages: {total_messages}")
            
            if max_emails:
                print(f"Processing first {max_emails} emails...")
            
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
                        
                        # Extract metadata
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
    
    def read_csv_file(self, filepath, email_column='Body', subject_column='Subject'):
        """Read emails from CSV file"""
        emails = []
        metadata = []
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    email_text = ""
                    if subject_column in row:
                        email_text += row[subject_column] + " "
                    if email_column in row:
                        email_text += row[email_column]
                    
                    emails.append(email_text)
                    
                    meta = {
                        'subject': row.get(subject_column, ''),
                        'from': row.get('From', row.get('Sender', '')),
                        'date': row.get('Date', ''),
                        'message_id': f'email_{i}'
                    }
                    metadata.append(meta)
            
            print(f"✓ Loaded {len(emails)} emails from CSV")
        except Exception as e:
            print(f"✗ Error reading CSV: {e}")
        
        return emails, metadata
    
    def analyze_for_issue(self, emails, metadata=None, show_progress=True):
        """
        Analyze emails for the specific issue with severity scoring
        
        Args:
            emails: List of email text strings
            metadata: Optional list of metadata dicts for each email
            show_progress: Show progress during analysis
        """
        if not self.issue_config:
            print("✗ No issue configuration loaded!")
            return None
        
        print(f"\n{'='*70}")
        print(f"Analyzing for: {self.issue_config.get('issue_name', 'Unknown Issue')}")
        print(f"Issue ID: {self.issue_config.get('issue_id', 'N/A')}")
        print(f"{'='*70}\n")
        
        matched_emails = []
        keyword_matches = defaultdict(int)
        symptom_matches = defaultdict(int)
        context_matches = defaultdict(int)
        product_mentions = defaultdict(int)
        severity_scores = []  # NEW: Track severity scores
        
        match_criteria = self.issue_config.get('match_criteria', {})
        require_primary = match_criteria.get('require_primary', True)
        require_symptom = match_criteria.get('require_symptom', True)
        require_context = match_criteria.get('require_context', False)
        
        print(f"Analyzing {len(emails)} emails...")
        
        for i, email in enumerate(emails):
            if show_progress and (i + 1) % 100 == 0:
                print(f"  Analyzed {i + 1}/{len(emails)} emails...")
            
            email_lower = email.lower()
            
            # Check exclude keywords first
            exclude_keywords = self.issue_config.get('exclude_keywords', [])
            if any(keyword.lower() in email_lower for keyword in exclude_keywords):
                continue
            
            # Check for matches
            has_primary = False
            has_symptom = False
            has_context = False
            
            matched_keywords = []
            matched_symptoms = []
            matched_contexts = []
            
            # Primary keywords
            primary_keywords = self.issue_config.get('keywords', {}).get('primary', [])
            for keyword in primary_keywords:
                if keyword.lower() in email_lower:
                    has_primary = True
                    keyword_matches[keyword] += 1
                    matched_keywords.append(keyword)
            
            # Symptom keywords
            symptom_keywords = self.issue_config.get('keywords', {}).get('symptoms', [])
            for symptom in symptom_keywords:
                if symptom.lower() in email_lower:
                    has_symptom = True
                    symptom_matches[symptom] += 1
                    matched_symptoms.append(symptom)
            
            # Context keywords
            context_keywords = self.issue_config.get('keywords', {}).get('context', [])
            for context in context_keywords:
                if context.lower() in email_lower:
                    has_context = True
                    context_matches[context] += 1
                    matched_contexts.append(context)
            
            # Product mentions
            products = self.issue_config.get('affected_products', [])
            mentioned_products = []
            for product in products:
                if product.lower() in email_lower:
                    product_mentions[product] += 1
                    mentioned_products.append(product)
            
            # Apply match criteria
            is_match = True
            if require_primary and not has_primary:
                is_match = False
            if require_symptom and not has_symptom:
                is_match = False
            if require_context and not has_context:
                is_match = False
            
            if is_match:
                # NEW: Calculate severity score
                severity_score = self.calculate_severity_score(
                    matched_keywords + matched_symptoms, 
                    matched_symptoms, 
                    email
                )
                severity_scores.append(severity_score)
                
                email_data = {
                    'email_index': i,
                    'email_text': email[:500] + '...' if len(email) > 500 else email,
                    'matched_keywords': matched_keywords,
                    'matched_symptoms': matched_symptoms,
                    'matched_contexts': matched_contexts,
                    'mentioned_products': mentioned_products,
                    'metadata': metadata[i] if metadata and i < len(metadata) else {},
                    'severity_score': severity_score  # NEW: Include severity score
                }
                matched_emails.append(email_data)
        
        # Sort by severity score (highest first)
        matched_emails.sort(key=lambda x: x['severity_score'], reverse=True)
        
        # NEW: Calculate severity statistics
        avg_severity = sum(severity_scores) / len(severity_scores) if severity_scores else 0
        high_severity_count = len([s for s in severity_scores if s >= 10])
        critical_severity_count = len([s for s in severity_scores if s >= 15])
        
        self.results = {
            'total_emails_analyzed': len(emails),
            'matched_emails_count': len(matched_emails),
            'match_percentage': (len(matched_emails) / len(emails) * 100) if emails else 0,
            'keyword_matches': dict(keyword_matches),
            'symptom_matches': dict(symptom_matches),
            'context_matches': dict(context_matches),
            'product_mentions': dict(product_mentions),
            'matched_emails': matched_emails,
            # NEW: Severity metrics
            'severity_scores': severity_scores,
            'avg_severity': avg_severity,
            'high_severity_count': high_severity_count,
            'critical_severity_count': critical_severity_count
        }
        
        self.affected_emails = matched_emails
        
        print(f"\n✓ Analysis complete!")
        print(f"  Found {len(matched_emails)} emails matching issue criteria")
        print(f"  ({self.results['match_percentage']:.2f}% of total)")
        
        # NEW: Show severity summary
        if severity_scores:
            print(f"  Average severity: {avg_severity:.1f}/20")
            print(f"  High severity cases (10+): {high_severity_count}")
            print(f"  Critical cases (15+): {critical_severity_count}")
            
            # Check alert thresholds
            alert_threshold = self.issue_config.get('tracking_metrics', {}).get('alert_threshold', 5)
            escalation_threshold = self.issue_config.get('tracking_metrics', {}).get('escalation_threshold', 10)
            
            if len(matched_emails) >= escalation_threshold:
                print(f"  🔴 ESCALATION: {len(matched_emails)} cases >= threshold ({escalation_threshold})")
            elif len(matched_emails) >= alert_threshold:
                print(f"  🟡 ALERT: {len(matched_emails)} cases >= threshold ({alert_threshold})")
            else:
                print(f"  🟢 Normal: {len(matched_emails)} cases < alert threshold ({alert_threshold})")
        
        return self.results
    
    def generate_report(self, output_file=None, include_email_details=True):
        """Generate detailed report for the specific issue with severity analysis"""
        if not self.results:
            print("✗ No results to report. Run analyze_for_issue() first.")
            return
        
        lines = []
        lines.append("=" * 80)
        lines.append("CRITICAL ISSUE TRACKER REPORT")
        lines.append("=" * 80)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Issue: {self.issue_config.get('issue_name', 'Unknown Issue')}")
        lines.append(f"Issue ID: {self.issue_config.get('issue_id', 'N/A')}")
        lines.append(f"Severity Level: {self.issue_config.get('severity', 'UNKNOWN')}")
        
        # Summary with severity metrics
        lines.append("\n" + "-" * 80)
        lines.append("SUMMARY")
        lines.append("-" * 80)
        lines.append(f"Total Emails Analyzed: {self.results['total_emails_analyzed']}")
        lines.append(f"Emails Matching Issue: {self.results['matched_emails_count']}")
        lines.append(f"Match Percentage: {self.results['match_percentage']:.2f}%")
        
        # NEW: Severity summary
        if self.results.get('severity_scores'):
            lines.append(f"\nSEVERITY ANALYSIS:")
            lines.append(f"  Average Severity: {self.results['avg_severity']:.1f}/20")
            lines.append(f"  High Severity Cases (10+): {self.results['high_severity_count']}")
            lines.append(f"  Critical Cases (15+): {self.results['critical_severity_count']}")
            
            # Alert status
            alert_threshold = self.issue_config.get('tracking_metrics', {}).get('alert_threshold', 5)
            escalation_threshold = self.issue_config.get('tracking_metrics', {}).get('escalation_threshold', 10)
            
            if self.results['matched_emails_count'] >= escalation_threshold:
                lines.append(f"  🔴 STATUS: ESCALATION REQUIRED (>= {escalation_threshold} cases)")
            elif self.results['matched_emails_count'] >= alert_threshold:
                lines.append(f"  🟡 STATUS: ALERT THRESHOLD REACHED (>= {alert_threshold} cases)")
            else:
                lines.append(f"  🟢 STATUS: Below alert threshold (< {alert_threshold} cases)")
        
        # Keyword breakdown
        if self.results['keyword_matches']:
            lines.append("\n" + "-" * 80)
            lines.append("PRIMARY KEYWORD MATCHES")
            lines.append("-" * 80)
            sorted_keywords = sorted(self.results['keyword_matches'].items(), 
                                    key=lambda x: x[1], reverse=True)
            for keyword, count in sorted_keywords:
                lines.append(f"  • {keyword}: {count} mentions")
        
        # Symptom breakdown
        if self.results['symptom_matches']:
            lines.append("\n" + "-" * 80)
            lines.append("SYMPTOM KEYWORD MATCHES")
            lines.append("-" * 80)
            sorted_symptoms = sorted(self.results['symptom_matches'].items(), 
                                    key=lambda x: x[1], reverse=True)
            for symptom, count in sorted_symptoms:
                lines.append(f"  • {symptom}: {count} mentions")
        
        # Context breakdown
        if self.results['context_matches']:
            lines.append("\n" + "-" * 80)
            lines.append("CONTEXT KEYWORD MATCHES")
            lines.append("-" * 80)
            sorted_context = sorted(self.results['context_matches'].items(), 
                                   key=lambda x: x[1], reverse=True)
            for context, count in sorted_context:
                lines.append(f"  • {context}: {count} mentions")
        
        # Product breakdown
        if self.results['product_mentions']:
            lines.append("\n" + "-" * 80)
            lines.append("AFFECTED PRODUCTS")
            lines.append("-" * 80)
            sorted_products = sorted(self.results['product_mentions'].items(), 
                                    key=lambda x: x[1], reverse=True)
            for product, count in sorted_products:
                lines.append(f"  • {product}: {count} mentions")
        
        # NEW: High severity email details
        if include_email_details and self.affected_emails:
            lines.append("\n" + "=" * 80)
            lines.append("HIGH SEVERITY EMAIL DETAILS (Top 10)")
            lines.append("=" * 80)
            
            # Show top 10 by severity
            for i, email_data in enumerate(self.affected_emails[:10], 1):
                lines.append(f"\n--- Email #{i} (Severity: {email_data.get('severity_score', 0)}/20) ---")
                
                meta = email_data.get('metadata', {})
                if meta.get('subject'):
                    lines.append(f"Subject: {meta['subject']}")
                if meta.get('from'):
                    lines.append(f"From: {meta['from']}")
                if meta.get('date'):
                    lines.append(f"Date: {meta['date']}")
                
                if email_data['matched_keywords']:
                    lines.append(f"Matched Keywords: {', '.join(email_data['matched_keywords'])}")
                if email_data['matched_symptoms']:
                    lines.append(f"Matched Symptoms: {', '.join(email_data['matched_symptoms'])}")
                if email_data['mentioned_products']:
                    lines.append(f"Products: {', '.join(email_data['mentioned_products'])}")
                
                lines.append(f"\nPreview:\n{email_data['email_text']}")
            
            if len(self.affected_emails) > 10:
                lines.append(f"\n... and {len(self.affected_emails) - 10} more emails")
        
        lines.append("\n" + "=" * 80)
        lines.append("END OF REPORT")
        lines.append("=" * 80)
        
        report_text = "\n".join(lines)
        print("\n" + report_text)
        
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(report_text)
                print(f"\n✓ Report saved to {output_file}")
            except Exception as e:
                print(f"✗ Error saving report: {e}")
        
        return report_text
    
    def export_affected_emails(self, output_file):
        """Export list of affected emails to CSV for follow-up"""
        if not self.affected_emails:
            print("✗ No affected emails to export")
            return
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Subject', 'From', 'Date', 'Severity Score', 'Matched Keywords', 
                               'Matched Symptoms', 'Products', 'Preview'])
                
                for email_data in self.affected_emails:
                    meta = email_data.get('metadata', {})
                    writer.writerow([
                        meta.get('subject', ''),
                        meta.get('from', ''),
                        meta.get('date', ''),
                        email_data.get('severity_score', 0),  # NEW: Include severity
                        ', '.join(email_data['matched_keywords']),
                        ', '.join(email_data['matched_symptoms']),
                        ', '.join(email_data['mentioned_products']),
                        email_data['email_text'][:200]
                    ])
            
            print(f"✓ Exported {len(self.affected_emails)} affected emails to {output_file}")
        except Exception as e:
            print(f"✗ Error exporting emails: {e}")


def main():
    """Main program for issue tracking - SAME AS BEFORE"""
    print("=" * 80)
    print("PTZOPTICS CRITICAL ISSUE TRACKER")
    print("=" * 80)
    print("\nTrack specific issues across support emails")
    print("Perfect for monitoring firmware bugs, feature failures, etc.\n")
    
    # Check for existing issue config
    config_file = input("Enter issue config file path (or press Enter to create new): ").strip()
    
    tracker = IssueTracker()
    
    if not config_file or not os.path.exists(config_file):
        print("\nNo config found. Creating template...")
        template_name = input("Template filename (default: issue_template.json): ").strip()
        if not template_name:
            template_name = "issue_template.json"
        
        tracker.create_issue_template(template_name)
        print(f"\n✓ Edit {template_name} with your issue details, then run this program again.")
        return
    
    # Load existing config
    tracker.load_issue_config(config_file)
    
    # Get email file
    print("\n" + "-" * 80)
    email_file = input("Enter path to email file (.mbox, .csv, or .txt): ").strip().strip('"').strip("'")
    
    if not os.path.exists(email_file):
        print(f"✗ File not found: {email_file}")
        return
    
    # Read emails
    emails = []
    metadata = []
    
    if email_file.endswith('.mbox') or email_file.endswith('.mbx'):
        limit = input("\nProcess all emails? (y/n, or enter number to limit): ").strip().lower()
        max_emails = None
        if limit.isdigit():
            max_emails = int(limit)
        elif limit == 'n':
            max_emails = int(input("How many emails to process? "))
        
        emails, metadata = tracker.read_mbox_file(email_file, max_emails=max_emails)
    
    elif email_file.endswith('.csv'):
        body_col = input("Email body column name (default: Body): ").strip() or 'Body'
        subject_col = input("Email subject column name (default: Subject): ").strip() or 'Subject'
        emails, metadata = tracker.read_csv_file(email_file, body_col, subject_col)
    
    if not emails:
        print("✗ No emails found")
        return
    
    # Analyze
    print("\n" + "-" * 80)
    tracker.analyze_for_issue(emails, metadata)
    
    # Generate report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    issue_id = tracker.issue_config.get('issue_id', 'issue').replace(' ', '_')
    report_file = f"issue_report_{issue_id}_{timestamp}.txt"
    csv_file = f"affected_emails_{issue_id}_{timestamp}.csv"
    
    print("\n" + "-" * 80)
    include_details = input("Include full email details in report? (y/n, default: y): ").strip().lower()
    include_details = include_details != 'n'
    
    tracker.generate_report(report_file, include_email_details=include_details)
    
    # Export affected emails
    if tracker.affected_emails:
        export = input("\nExport affected emails to CSV for follow-up? (y/n): ").strip().lower()
        if export == 'y':
            tracker.export_affected_emails(csv_file)
    
    print("\n" + "=" * 80)
    print("✓ TRACKING COMPLETE")
    print(f"  Report: {report_file}")
    if os.path.exists(csv_file):
        print(f"  Affected Emails CSV: {csv_file}")
    print("=" * 80)


if __name__ == "__main__":
    main()
