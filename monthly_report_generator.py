#!/usr/bin/env python3
"""
Monthly Report Generator
Complete automated workflow: Download emails → Analyze → Generate monthly report
Run this monthly for comprehensive insights into support trends over the last 30 days!
"""

import os
from datetime import datetime
from gmail_downloader import GmailDownloader
from weekly_report_generator import WeeklyReportGenerator

def monthly_report():
    """Complete automated workflow for monthly reporting"""
    
    print("="*70)
    print("📅 MONTHLY REPORT GENERATOR")
    print("="*70)
    print("\nThis script will:")
    print("  1. Download last 30 days of support emails from Gmail")
    print("  2. Analyze trends and issues over monthly period")
    print("  3. Generate comprehensive monthly team report")
    print("  4. Save for presentation/email")
    print("\n" + "="*70)
    
    # ========================================
    # CONFIGURATION - CUSTOMIZE THIS SECTION
    # ========================================
    
    # Gmail search parameters
    GMAIL_QUERY = "to:support@ptzoptics.com"  # Change to your support email
    DAYS_BACK = 30  # Last month
    
    # Issue configs to track (add your critical issue files here)
    ISSUE_CONFIGS = [
        'cmp_autotracking_issue.json',
        'example_firmware_reboot_issue.json',
        'superjoy_4k_freezing_issue.json',
        'dark_image_issues.json',
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
    mbox_filename = f"monthly_support_emails_{timestamp}.mbox"
    
    mbox_path = os.path.join(DATA_DIR, mbox_filename)
    report_path = os.path.join(REPORTS_DIR, f"monthly_team_report_{timestamp}.txt")
    
    # Step 1: Download emails
    print("\n" + "="*70)
    print("STEP 1: DOWNLOADING MONTHLY EMAILS FROM GMAIL")
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
    print("STEP 2: ANALYZING EMAILS & GENERATING MONTHLY REPORT")
    print("="*70)
    
    # Use WeeklyReportGenerator but customize the output for monthly reporting
    reporter = WeeklyReportGenerator()
    
    # Load previous month for comparison (if available)
    reporter.load_previous_week_data('previous_month_data.json')
    
    # Run general analysis
    print("\nRunning monthly trend analysis...")
    success = reporter.analyze_general_trends(mbox_path, 'keywords.json')
    
    if not success:
        print("❌ Analysis failed")
        return False
    
    # Track critical issues
    print("\nTracking critical issues over 30-day period...")
    active_configs = [cfg for cfg in ISSUE_CONFIGS if os.path.exists(cfg)]
    
    if active_configs:
        print(f"Found {len(active_configs)} active issue config(s)")
        reporter.track_critical_issues(mbox_path, active_configs)
    else:
        print("No issue configs found (this is okay for general reports)")
    
    # Generate monthly report (customize the report title)
    print("\nGenerating formatted monthly team report...")
    
    # Temporarily modify the report generator to show monthly context
    original_method = reporter.generate_team_report
    
    def generate_monthly_team_report(output_file=None):
        """Generate monthly team report with appropriate headers"""
        if not reporter.general_results:
            print("❌ No analysis results. Run analyze_general_trends() first.")
            return
        
        # Calculate date range for monthly report
        reporter.week_end = datetime.now()
        from datetime import timedelta
        reporter.week_start = reporter.week_end - timedelta(days=DAYS_BACK)
        
        lines = []
        
        # Monthly Header
        lines.append("="*70)
        lines.append("PTZOPTICS SUPPORT - MONTHLY SUMMARY REPORT")
        lines.append("="*70)
        lines.append(f"\nReport Period: {reporter.week_start.strftime('%B %d, %Y')} - {reporter.week_end.strftime('%B %d, %Y')}")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Analysis Period: {DAYS_BACK} days")
        
        # Total emails
        total = reporter.general_results['total_emails']
        lines.append(f"\n{'─'*70}")
        lines.append("📊 MONTHLY VOLUME METRICS")
        lines.append(f"{'─'*70}")
        
        if reporter.previous_week_data:
            prev_total = reporter.previous_week_data.get('total_emails', 0)
            trend, change = reporter.get_trend_indicator(total, prev_total)
            lines.append(f"\nTotal Support Emails: {total} {trend} ({change:+.1f}% vs last month)")
            lines.append(f"Daily Average: {total/DAYS_BACK:.1f} emails per day")
        else:
            lines.append(f"\nTotal Support Emails: {total}")
            lines.append(f"Daily Average: {total/DAYS_BACK:.1f} emails per day")
        
        # Monthly insights
        lines.append(f"\n{'─'*70}")
        lines.append("🔥 TOP ISSUES THIS MONTH")
        lines.append(f"{'─'*70}")
        
        # Sort categories by mentions
        sorted_categories = sorted(
            reporter.general_results['categories'].items(),
            key=lambda x: x[1]['total_mentions'],
            reverse=True
        )
        
        top_n = 8  # Show more for monthly report
        for i, (category, data) in enumerate(sorted_categories[:top_n], 1):
            mentions = data['total_mentions']
            emails = data['emails_with_category']
            percentage = (emails / total * 100) if total > 0 else 0
            
            # Compare to last month if available
            trend_str = ""
            if reporter.previous_week_data:
                prev_categories = reporter.previous_week_data.get('categories', {})
                if category in prev_categories:
                    prev_mentions = prev_categories[category]['total_mentions']
                    trend, change = reporter.get_trend_indicator(mentions, prev_mentions)
                    trend_str = f" {trend} ({change:+.1f}%)"
            
            lines.append(f"\n{i}. {category}{trend_str}")
            lines.append(f"   • {mentions} total mentions")
            lines.append(f"   • {emails} emails affected ({percentage:.1f}% of total)")
            
            # Top keywords in this category
            if data['keywords']:
                top_keywords = sorted(data['keywords'].items(), key=lambda x: x[1], reverse=True)[:3]
                keyword_list = ", ".join([f"{kw} ({count})" for kw, count in top_keywords])
                lines.append(f"   • Top keywords: {keyword_list}")
        
        # Critical issues tracked
        if reporter.issue_results:
            lines.append(f"\n{'─'*70}")
            lines.append("⚠️  CRITICAL ISSUES TRACKED (30-DAY PERIOD)")
            lines.append(f"{'─'*70}")
            
            for issue_id, data in reporter.issue_results.items():
                severity = data['severity']
                severity_emoji = {
                    'CRITICAL': '🔴',
                    'HIGH': '🟠',
                    'MEDIUM': '🟡',
                    'LOW': '🟢'
                }.get(severity, '⚪')
                
                lines.append(f"\n{severity_emoji} {data['name']}")
                lines.append(f"   • Issue ID: {issue_id}")
                lines.append(f"   • Severity: {severity}")
                lines.append(f"   • Reports this month: {data['matched_count']} ({data['percentage']:.2f}% of emails)")
                lines.append(f"   • Monthly average: {data['matched_count']/DAYS_BACK*30:.1f} cases per 30 days")
                
                # NEW: Add severity analysis if available
                if data.get('avg_severity', 0) > 0:
                    lines.append(f"   • Average severity: {data['avg_severity']:.1f}/20")
                    lines.append(f"   • High severity cases (10+): {data['high_severity_count']}")
                    lines.append(f"   • Critical cases (15+): {data['critical_severity_count']}")
                    
                    # Alert status
                    if data['matched_count'] >= data.get('escalation_threshold', 10):
                        lines.append(f"   • 🔴 STATUS: ESCALATION REQUIRED")
                    elif data['matched_count'] >= data.get('alert_threshold', 5):
                        lines.append(f"   • 🟡 STATUS: ALERT THRESHOLD REACHED")
                    else:
                        lines.append(f"   • 🟢 STATUS: Normal levels")
        
        # Monthly insights section
        lines.append(f"\n{'─'*70}")
        lines.append("💡 MONTHLY KEY INSIGHTS")
        lines.append(f"{'─'*70}")
        
        insights = reporter._generate_insights()
        # Add monthly-specific insights
        monthly_insights = []
        
        # Volume insights
        if total > 0:
            weekly_avg = total / 4.3  # Approximate weeks in a month
            monthly_insights.append(f"Monthly volume of {total} emails averages {weekly_avg:.1f} emails per week")
        
        # Seasonal patterns
        current_month = datetime.now().strftime('%B')
        monthly_insights.append(f"{current_month} support patterns show the trends above - monitor for seasonal variations")
        
        for insight in (monthly_insights + insights):
            lines.append(f"\n• {insight}")
        
        # Monthly action items
        lines.append(f"\n{'─'*70}")
        lines.append("✅ MONTHLY RECOMMENDED ACTIONS")
        lines.append(f"{'─'*70}")
        
        actions = reporter._generate_action_items()
        
        # Add monthly-specific actions
        monthly_actions = []
        if reporter.issue_results:
            critical_issues = [data for data in reporter.issue_results.values() if data['severity'] == 'CRITICAL']
            if critical_issues:
                monthly_actions.append("Review all critical issues for potential product/documentation improvements")
        
        for action in (monthly_actions + actions):
            lines.append(f"\n• {action}")
        
        # Footer
        lines.append(f"\n{'─'*70}")
        lines.append("📎 MONTHLY ATTACHMENTS")
        lines.append(f"{'─'*70}")
        lines.append(f"\n• Raw email data: {mbox_filename}")
        lines.append(f"• Detailed analysis: email_report_[timestamp].txt")
        if reporter.issue_results:
            lines.append("• Critical issue reports: issue_report_*.txt")
            lines.append("• Affected customer lists: affected_emails_*.csv")
        
        lines.append("\n" + "="*70)
        lines.append("End of Monthly Report")
        lines.append("="*70)
        
        # Generate report text
        report_text = "\n".join(lines)
        
        # Print to console
        print("\n" + report_text)
        
        # Save to file
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(report_text)
                print(f"\n✓ Monthly report saved to: {output_file}")
            except Exception as e:
                print(f"❌ Error saving report: {e}")
        
        return report_text
    
    # Use custom monthly report generator
    generate_monthly_team_report(report_path)
    
    # Save data for next month's comparison
    reporter.save_current_week_data('previous_month_data.json')
    
    # Success summary
    print("\n" + "="*70)
    print("✅ MONTHLY REPORT GENERATION COMPLETE!")
    print("="*70)
    print(f"\n📧 Email File: {mbox_path}")
    print(f"📊 Monthly Report: {report_path}")
    
    file_size = os.path.getsize(mbox_path) / (1024 * 1024)
    print(f"\n📈 Monthly Statistics:")
    print(f"  • Email file size: {file_size:.2f} MB")
    print(f"  • Total emails: {reporter.general_results['total_emails']}")
    print(f"  • Daily average: {reporter.general_results['total_emails']/DAYS_BACK:.1f} emails per day")
    print(f"  • Critical issues tracked: {len(reporter.issue_results)}")
    
    print("\n" + "="*70)
    print("🎯 NEXT STEPS:")
    print("="*70)
    print("\n1. Review the monthly report:")
    print(f"   Open: {report_path}")
    print("\n2. Share with management team (via email or presentation)")
    print("\n3. Discuss monthly trends and action items in team meeting")
    print("\n4. Archive for quarterly and annual trend analysis")
    print("\n5. Use insights for:\n   - Resource planning\n   - Product improvement priorities\n   - Documentation updates\n   - Training focus areas")
    
    print("\n" + "="*70)
    print("See you next month! 📅")
    print("="*70)
    
    return True


def quick_config_check():
    """Check configuration before running"""
    print("\n" + "="*70)
    print("MONTHLY CONFIGURATION CHECK")
    print("="*70)
    
    issues = []
    
    # Check for credentials
    if not os.path.exists('credentials.json'):
        issues.append("❌ credentials.json not found - Gmail API not set up")
        issues.append("   → See GMAIL_SETUP_GUIDE.md")
    else:
        print("✅ credentials.json found")
    
    # Check for keywords
    if not os.path.exists('keywords.json'):
        issues.append("⚠️  keywords.json not found - will use defaults")
    else:
        print("✅ keywords.json found")
    
    # Check for issue configs
    issue_configs = [f for f in os.listdir('.') if f.endswith('_issue.json') or (f.startswith('issue_') and f.endswith('.json'))]
    if issue_configs:
        print(f"✅ Found {len(issue_configs)} issue config(s)")
    else:
        print("⚠️  No issue configs found (optional for monthly reports)")
    
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
    
    print("\n✅ Configuration looks good for monthly reporting!")
    return True


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                                                                      ║
    ║                    MONTHLY REPORT GENERATOR                          ║
    ║                                                                      ║
    ║     📅 30-day comprehensive support analysis                         ║
    ║     📊 Monthly trends and issue tracking                             ║
    ║     📈 Management-ready insights and metrics                         ║
    ║                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Check configuration first
    if not quick_config_check():
        print("\nPlease fix configuration issues and try again.")
        exit(1)
    
    # Confirm run
    print("\n" + "="*70)
    confirm = input("Ready to generate monthly report (last 30 days)? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("Cancelled. Run again when ready!")
        exit(0)
    
    # Run monthly automation
    success = monthly_report()
    
    exit(0 if success else 1)
