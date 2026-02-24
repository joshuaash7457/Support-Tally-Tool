#!/usr/bin/env python3
"""
Monday Morning Automation
Complete automated workflow: Download emails → Analyze → Generate team report
Run this every Monday morning for instant weekly insights!
"""

import os
from datetime import datetime
from gmail_downloader import GmailDownloader
from weekly_report_generator import WeeklyReportGenerator

def monday_morning_report():
    """Complete automated workflow"""
    
    print("="*70)
    print("🌅 MONDAY MORNING AUTOMATION")
    print("="*70)
    print("\nThis script will:")
    print("  1. Download last week's support emails from Gmail")
    print("  2. Analyze trends and issues")
    print("  3. Generate formatted team report")
    print("  4. Save for presentation/email")
    print("\n" + "="*70)
    
    # ========================================
    # CONFIGURATION - CUSTOMIZE THIS SECTION
    # ========================================
    
    # Gmail search parameters
    GMAIL_QUERY = "to:support@ptzoptics.com"  # Change to your support email
    DAYS_BACK = 7  # Last week
    
    # Issue configs to track (add your critical issue files here)
    ISSUE_CONFIGS = [
        'cmp_autotracking_issue.json',
        'example_firmware_reboot_issue.json',
        'superjoy_4k_freezing_issue.json',
        # Add more issue config files here as needed
    ]
    
    # Output directories
    DATA_DIR = "data/raw"  # Where to save downloaded emails
    REPORTS_DIR = "reports"  # Where to save reports
    
    # ========================================
    # END CONFIGURATION
    # ========================================
    
    # Create directories if they don't exist
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    mbox_filename = f"support_emails_{timestamp}.mbox"
    
    mbox_path = os.path.join(DATA_DIR, mbox_filename)
    report_path = os.path.join(REPORTS_DIR, f"weekly_team_report_{timestamp}.txt")
    
    # Step 1: Download emails
    print("\n" + "="*70)
    print("STEP 1: DOWNLOADING EMAILS FROM GMAIL")
    print("="*70)
    
    downloader = GmailDownloader()
    
    try:
        downloader.authenticate()
    except Exception as e:
        print(f"\n❌ Gmail authentication failed: {e}")
        print("\nPlease set up Gmail API first (see GMAIL_SETUP_GUIDE.md)")
        return False
    
    print(f"\nDownloading emails...")
    print(f"  Query: {GMAIL_QUERY}")
    print(f"  Period: Last {DAYS_BACK} days")
    
    try:
        downloader.download_to_mbox(
            output_file=mbox_path,
            query=GMAIL_QUERY,
            max_results=None,
            days_back=DAYS_BACK,
            show_progress=True
        )
    except Exception as e:
        print(f"\n❌ Download failed: {e}")
        return False
    
    # Check if download successful
    if not os.path.exists(mbox_path):
        print(f"\n❌ Mbox file not created: {mbox_path}")
        return False
    
    # Step 2: Generate report
    print("\n" + "="*70)
    print("STEP 2: ANALYZING EMAILS & GENERATING REPORT")
    print("="*70)
    
    reporter = WeeklyReportGenerator()
    
    # Load previous week for comparison
    reporter.load_previous_week_data()
    
    # Run general analysis
    print("\nRunning general trend analysis...")
    success = reporter.analyze_general_trends(mbox_path, 'keywords.json')
    
    if not success:
        print("❌ Analysis failed")
        return False
    
    # Track critical issues
    print("\nTracking critical issues...")
    active_configs = [cfg for cfg in ISSUE_CONFIGS if os.path.exists(cfg)]
    
    if active_configs:
        print(f"Found {len(active_configs)} active issue config(s)")
        reporter.track_critical_issues(mbox_path, active_configs)
    else:
        print("No issue configs found (this is okay for general reports)")
    
    # Generate report
    print("\nGenerating formatted team report...")
    reporter.generate_team_report(report_path)
    
    # Save data for next week's comparison
    reporter.save_current_week_data()
    
    # Success summary
    print("\n" + "="*70)
    print("✅ MONDAY MORNING AUTOMATION COMPLETE!")
    print("="*70)
    print(f"\n📧 Email File: {mbox_path}")
    print(f"📊 Team Report: {report_path}")
    
    file_size = os.path.getsize(mbox_path) / (1024 * 1024)
    print(f"\n📈 Statistics:")
    print(f"  • Email file size: {file_size:.2f} MB")
    print(f"  • Total emails: {reporter.general_results['total_emails']}")
    print(f"  • Critical issues tracked: {len(reporter.issue_results)}")
    
    print("\n" + "="*70)
    print("🎯 NEXT STEPS:")
    print("="*70)
    print("\n1. Review the team report:")
    print(f"   Open: {report_path}")
    print("\n2. Share with team (via email or Slack)")
    print("\n3. Discuss action items in team meeting")
    print("\n4. Archive for historical tracking")
    
    print("\n" + "="*70)
    print("See you next Monday! 👋")
    print("="*70)
    
    return True


def quick_check():
    """Quick configuration check before running"""
    print("\n" + "="*70)
    print("CONFIGURATION CHECK")
    print("="*70)
    
    issues = []
    
    # Check for credentials
    if not os.path.exists('credentials.json'):
        issues.append("❌ credentials.json not found - Gmail API not set up")
        issues.append("   → See GMAIL_SETUP_GUIDE.md")
    else:
        print("✓ credentials.json found")
    
    # Check for keywords
    if not os.path.exists('keywords.json'):
        issues.append("⚠ keywords.json not found - will use defaults")
    else:
        print("✓ keywords.json found")
    
    # Check for issue configs
    issue_configs = [f for f in os.listdir('.') if f.endswith('_issue.json')]
    if issue_configs:
        print(f"✓ Found {len(issue_configs)} issue config(s)")
    else:
        print("⚠ No issue configs found (optional)")
    
    if issues:
        print("\n" + "-"*70)
        print("ISSUES DETECTED:")
        print("-"*70)
        for issue in issues:
            print(issue)
        print("-"*70)
        
        if "credentials.json" in issues[0]:
            print("\nCannot proceed without Gmail API setup.")
            return False
    
    print("\n✓ Configuration looks good!")
    return True


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║              PTZOPTICS MONDAY MORNING AUTOMATION                 ║
    ║                                                                  ║
    ║     One command → Complete weekly support report ready! 🚀       ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Check configuration first
    if not quick_check():
        print("\nPlease fix configuration issues and try again.")
        exit(1)
    
    # Confirm run
    print("\n" + "="*70)
    confirm = input("Ready to generate this week's report? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("Cancelled. Run again when ready!")
        exit(0)
    
    # Run automation
    success = monday_morning_report()
    
    exit(0 if success else 1)
