#!/usr/bin/env python3
"""
Quick test script to demonstrate the Email Analyzer
"""

from email_analyzer import EmailAnalyzer

def main():
    print("=" * 60)
    print("PTZOptics Email Analyzer - Quick Test")
    print("=" * 60)
    
    # Initialize analyzer
    print("\n1. Initializing analyzer with default keywords...")
    analyzer = EmailAnalyzer()
    
    # Load sample emails
    print("\n2. Loading sample emails from sample_emails.txt...")
    emails = analyzer.read_text_file('sample_emails.txt')
    
    if not emails:
        print("Error: Could not load sample emails")
        return
    
    # Analyze
    print("\n3. Analyzing emails for keyword mentions...")
    results = analyzer.analyze_emails(emails)
    
    # Generate report
    print("\n4. Generating report...\n")
    analyzer.generate_report('test_report.txt')
    
    print("\n" + "=" * 60)
    print("Test complete!")
    print("Check 'test_report.txt' for the full report.")
    print("=" * 60)

if __name__ == "__main__":
    main()
