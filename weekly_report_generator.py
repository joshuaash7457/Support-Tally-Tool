#!/usr/bin/env python3
"""
Automated Weekly Report Generator
Creates formatted team reports from email analysis
"""

import os
import json
from datetime import datetime, timedelta
from email_analyzer_mbox import EmailAnalyzer
from enhanced_issue_tracker import IssueTracker

class WeeklyReportGenerator:
    def __init__(self):
        self.week_start = None
        self.week_end = None
        self.general_results = None
        self.issue_results = {}
        self.previous_week_data = None
        
    def load_previous_week_data(self, filepath='previous_week_data.json'):
        """Load last week's data for comparison"""
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    self.previous_week_data = json.load(f)
                print(f"✓ Loaded previous week data for comparison")
            except Exception as e:
                print(f"⚠ Could not load previous week data: {e}")
    
    def save_current_week_data(self, filepath='previous_week_data.json'):
        """Save this week's data for next week's comparison"""
        try:
            data = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'total_emails': self.general_results['total_emails'],
                'categories': {}
            }
            
            for category, info in self.general_results['categories'].items():
                data['categories'][category] = {
                    'total_mentions': info['total_mentions'],
                    'emails_with_category': info['emails_with_category']
                }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✓ Saved current week data for future comparison")
        except Exception as e:
            print(f"⚠ Could not save week data: {e}")
    
    def get_trend_indicator(self, current, previous):
        """Get trend arrow and percentage change"""
        if previous is None or previous == 0:
            return "NEW", 0
        
        change = ((current - previous) / previous) * 100
        
        if change > 5:
            return "↑", change
        elif change < -5:
            return "↓", change
        else:
            return "→", change
    
    def analyze_general_trends(self, mbox_file, keywords_file='keywords.json'):
        """Run general email analysis"""
        print("\n" + "="*70)
        print("RUNNING GENERAL TREND ANALYSIS")
        print("="*70)
        
        analyzer = EmailAnalyzer(keywords_file)
        emails = analyzer.read_mbox_file(mbox_file, show_progress=True)
        
        if not emails:
            print("❌ No emails found")
            return False
        
        self.general_results = analyzer.analyze_emails(emails, show_progress=True)
        return True
    
    def track_critical_issues(self, mbox_file, issue_configs):
        """Track specific critical issues"""
        print("\n" + "="*70)
        print("TRACKING CRITICAL ISSUES")
        print("="*70)
        
        for config_file in issue_configs:
            if not os.path.exists(config_file):
                print(f"⚠ Skipping {config_file} - not found")
                continue
            
            tracker = IssueTracker(config_file)
            emails, metadata = tracker.read_mbox_file(mbox_file, show_progress=False)
            
            if emails:
                results = tracker.analyze_for_issue(emails, metadata, show_progress=False)
                issue_name = tracker.issue_config.get('issue_name', 'Unknown Issue')
                issue_id = tracker.issue_config.get('issue_id', 'Unknown')
                
                self.issue_results[issue_id] = {
                    'name': issue_name,
                    'matched_count': results['matched_emails_count'],
                    'percentage': results['match_percentage'],
                    'severity': tracker.issue_config.get('severity', 'UNKNOWN'),
                    # NEW: Add severity tracking data
                    'avg_severity': results.get('avg_severity', 0),
                    'high_severity_count': results.get('high_severity_count', 0),
                    'critical_severity_count': results.get('critical_severity_count', 0),
                    'alert_threshold': tracker.issue_config.get('tracking_metrics', {}).get('alert_threshold', 5),
                    'escalation_threshold': tracker.issue_config.get('tracking_metrics', {}).get('escalation_threshold', 10)
                }
    
    def generate_team_report(self, output_file=None):
        """Generate formatted team report"""
        if not self.general_results:
            print("❌ No analysis results. Run analyze_general_trends() first.")
            return
        
        # Calculate date range
        self.week_end = datetime.now()
        self.week_start = self.week_end - timedelta(days=7)
        
        lines = []
        
        # Header
        lines.append("="*70)
        lines.append("PTZOPTICS SUPPORT - WEEKLY SUMMARY REPORT")
        lines.append("="*70)
        lines.append(f"\nReport Period: {self.week_start.strftime('%B %d, %Y')} - {self.week_end.strftime('%B %d, %Y')}")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Total emails
        total = self.general_results['total_emails']
        lines.append(f"\n{'─'*70}")
        lines.append("📊 VOLUME METRICS")
        lines.append(f"{'─'*70}")
        
        if self.previous_week_data:
            prev_total = self.previous_week_data.get('total_emails', 0)
            trend, change = self.get_trend_indicator(total, prev_total)
            lines.append(f"\nTotal Support Emails: {total} {trend} ({change:+.1f}% vs last week)")
        else:
            lines.append(f"\nTotal Support Emails: {total}")
        
        # Top issues
        lines.append(f"\n{'─'*70}")
        lines.append("🔥 TOP ISSUES THIS WEEK")
        lines.append(f"{'─'*70}")
        
        # Sort categories by mentions
        sorted_categories = sorted(
            self.general_results['categories'].items(),
            key=lambda x: x[1]['total_mentions'],
            reverse=True
        )
        
        top_n = 5
        for i, (category, data) in enumerate(sorted_categories[:top_n], 1):
            mentions = data['total_mentions']
            emails = data['emails_with_category']
            percentage = (emails / total * 100) if total > 0 else 0
            
            # Compare to last week if available
            trend_str = ""
            if self.previous_week_data:
                prev_categories = self.previous_week_data.get('categories', {})
                if category in prev_categories:
                    prev_mentions = prev_categories[category]['total_mentions']
                    trend, change = self.get_trend_indicator(mentions, prev_mentions)
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
        if self.issue_results:
            lines.append(f"\n{'─'*70}")
            lines.append("⚠️  CRITICAL ISSUES TRACKED")
            lines.append(f"{'─'*70}")
            
            for issue_id, data in self.issue_results.items():
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
                lines.append(f"   • Reports this week: {data['matched_count']} ({data['percentage']:.2f}% of emails)")
                
                # NEW: Add severity analysis
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
                
                # TODO: Add week-over-week comparison when we track historical issue data
        
        # Key insights section
        lines.append(f"\n{'─'*70}")
        lines.append("💡 KEY INSIGHTS")
        lines.append(f"{'─'*70}")
        
        insights = self._generate_insights()
        for insight in insights:
            lines.append(f"\n• {insight}")
        
        # Action items
        lines.append(f"\n{'─'*70}")
        lines.append("✅ RECOMMENDED ACTIONS")
        lines.append(f"{'─'*70}")
        
        actions = self._generate_action_items()
        for action in actions:
            lines.append(f"\n• {action}")
        
        # Footer
        lines.append(f"\n{'─'*70}")
        lines.append("📎 ATTACHMENTS")
        lines.append(f"{'─'*70}")
        lines.append("\n• Detailed analysis: email_report_[timestamp].txt")
        if self.issue_results:
            lines.append("• Critical issue reports: issue_report_*.txt")
            lines.append("• Affected customer lists: affected_emails_*.csv")
        
        lines.append("\n" + "="*70)
        lines.append("End of Weekly Report")
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
                print(f"\n✓ Report saved to: {output_file}")
            except Exception as e:
                print(f"❌ Error saving report: {e}")
        
        return report_text
    
    def _generate_insights(self):
        """Generate automated insights from data"""
        insights = []
        
        if not self.general_results:
            return insights
        
        total = self.general_results['total_emails']
        categories = self.general_results['categories']
        
        # Find highest volume category
        if categories:
            top_category = max(categories.items(), key=lambda x: x[1]['total_mentions'])
            cat_name, cat_data = top_category
            percentage = (cat_data['emails_with_category'] / total * 100) if total > 0 else 0
            insights.append(f"{cat_name} is the dominant issue this week, affecting {percentage:.1f}% of support emails")
        
        # Check for trends
        if self.previous_week_data:
            prev_total = self.previous_week_data.get('total_emails', 0)
            if total > prev_total * 1.2:
                increase = ((total - prev_total) / prev_total * 100)
                insights.append(f"Support volume increased {increase:.1f}% compared to last week - monitor for capacity needs")
            elif total < prev_total * 0.8:
                decrease = ((prev_total - total) / prev_total * 100)
                insights.append(f"Support volume decreased {decrease:.1f}% compared to last week")
            
            # Check for category spikes
            prev_cats = self.previous_week_data.get('categories', {})
            for cat_name, cat_data in categories.items():
                if cat_name in prev_cats:
                    current = cat_data['total_mentions']
                    previous = prev_cats[cat_name]['total_mentions']
                    if previous > 0 and current > previous * 1.5:
                        increase = ((current - previous) / previous * 100)
                        insights.append(f"{cat_name} spiked {increase:.1f}% - investigate for new issues or trends")
        
        # Critical issue insights
        for issue_id, data in self.issue_results.items():
            if data['severity'] == 'CRITICAL' and data['matched_count'] > 0:
                insights.append(f"CRITICAL: {data['name']} affecting {data['matched_count']} customers - escalate to engineering")
        
        return insights if insights else ["No significant trends detected this week"]
    
    def _generate_action_items(self):
        """Generate recommended action items"""
        actions = []
        
        if not self.general_results:
            return actions
        
        categories = self.general_results['categories']
        total = self.general_results['total_emails']
        
        # Top issue action
        if categories:
            top_category = max(categories.items(), key=lambda x: x[1]['total_mentions'])
            cat_name, cat_data = top_category
            
            if cat_data['emails_with_category'] / total > 0.15:  # More than 15% of emails
                actions.append(f"Create/update knowledge base article for {cat_name} (high volume)")
        
        # Critical issues
        for issue_id, data in self.issue_results.items():
            if data['severity'] == 'CRITICAL' and data['matched_count'] > 0:
                actions.append(f"Escalate {issue_id} to engineering team immediately")
                actions.append(f"Prepare customer communication for {data['name']} ({data['matched_count']} affected)")
            elif data['severity'] == 'HIGH' and data['matched_count'] > 5:
                actions.append(f"Monitor {issue_id} - consider hotfix if reports continue")
        
        # Trend-based actions
        if self.previous_week_data:
            prev_cats = self.previous_week_data.get('categories', {})
            for cat_name, cat_data in categories.items():
                if cat_name in prev_cats:
                    current = cat_data['total_mentions']
                    previous = prev_cats[cat_name]['total_mentions']
                    if previous > 0 and current > previous * 2:
                        actions.append(f"Investigate root cause of {cat_name} spike (doubled from last week)")
        
        return actions if actions else ["Continue monitoring support trends"]


def main():
    """Interactive weekly report generation"""
    print("="*70)
    print("AUTOMATED WEEKLY REPORT GENERATOR")
    print("="*70)
    print("\nThis will create a formatted team report from your email analysis\n")
    
    # Get mbox file
    mbox_file = input("Enter path to mbox file: ").strip().strip('"').strip("'")
    
    if not os.path.exists(mbox_file):
        print(f"❌ File not found: {mbox_file}")
        return
    
    # Initialize report generator
    reporter = WeeklyReportGenerator()
    
    # Load previous week data for comparison
    reporter.load_previous_week_data()
    
    # Run general analysis
    keywords_file = 'keywords.json'
    if not os.path.exists(keywords_file):
        print(f"⚠ keywords.json not found, using defaults")
        keywords_file = None
    
    success = reporter.analyze_general_trends(mbox_file, keywords_file)
    
    if not success:
        return
    
    # Ask about critical issues
    print("\n" + "-"*70)
    track_issues = input("Track critical issues? (y/n, default: y): ").strip().lower()
    
    if track_issues != 'n':
        print("\nLooking for issue config files...")
        issue_configs = []
        
        # Find all issue config files
        for file in os.listdir('.'):
            if file.endswith('_issue.json') or file.startswith('issue_') and file.endswith('.json'):
                issue_configs.append(file)
        
        if issue_configs:
            print(f"Found {len(issue_configs)} issue config(s):")
            for config in issue_configs:
                print(f"  • {config}")
            
            use_all = input("\nTrack all issues? (y/n, default: y): ").strip().lower()
            
            if use_all == 'n':
                selected = input("Enter config filenames (comma-separated): ").strip()
                issue_configs = [f.strip() for f in selected.split(',')]
            
            reporter.track_critical_issues(mbox_file, issue_configs)
        else:
            print("No issue config files found (files ending in _issue.json)")
    
    # Generate report
    print("\n" + "="*70)
    print("GENERATING REPORT")
    print("="*70)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f"weekly_team_report_{timestamp}.txt"
    
    reporter.generate_team_report(report_file)
    
    # Save data for next week
    reporter.save_current_week_data()
    
    print("\n" + "="*70)
    print("✓ REPORT GENERATION COMPLETE")
    print("="*70)
    print(f"\nTeam Report: {report_file}")
    print("\nYou can now:")
    print("  • Email this report to your team")
    print("  • Present in Monday meetings")
    print("  • Archive for historical tracking")
    print("="*70)


if __name__ == "__main__":
    main()
