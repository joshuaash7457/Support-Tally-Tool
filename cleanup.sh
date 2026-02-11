#!/bin/bash
# Cleanup script for PTZOptics Email Analysis
# Removes downloaded emails and reports for fresh testing

echo "============================================================"
echo "PTZOptics Email Analysis - Cleanup Script"
echo "============================================================"
echo ""
echo "This will delete:"
echo "  - All downloaded email files (data/raw/*.mbox)"
echo "  - All generated reports (reports/*)"
echo "  - Previous week comparison data"
echo ""
echo "Files in root directory will NOT be deleted."
echo ""

read -p "Continue? (y/n): " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo ""
echo "Cleaning up..."
echo ""

# Delete email files
if ls data/raw/*.mbox 1> /dev/null 2>&1; then
    rm -f data/raw/*.mbox
    echo "  ✓ Deleted email files from data/raw/"
else
    echo "  - No email files found in data/raw/"
fi

# Delete report files
if ls reports/*.txt 1> /dev/null 2>&1; then
    rm -f reports/*.txt
    echo "  ✓ Deleted report files from reports/"
else
    echo "  - No report files found in reports/"
fi

if ls reports/*.csv 1> /dev/null 2>&1; then
    rm -f reports/*.csv
    echo "  ✓ Deleted CSV exports from reports/"
else
    echo "  - No CSV files found in reports/"
fi

# Delete comparison data
if [ -f "previous_week_data.json" ]; then
    rm -f previous_week_data.json
    echo "  ✓ Deleted previous week comparison data"
else
    echo "  - No previous week data found"
fi

# Also clean up any files in root (legacy)
if ls *.mbox 1> /dev/null 2>&1; then
    rm -f *.mbox
    echo "  ✓ Deleted legacy mbox files from root"
fi

if ls *_report*.txt 1> /dev/null 2>&1; then
    rm -f *_report*.txt
    echo "  ✓ Deleted legacy report files from root"
fi

echo ""
echo "============================================================"
echo "Cleanup complete!"
echo "============================================================"
echo ""
echo "You can now run a fresh analysis:"
echo "  python monday_morning_automation.py"
echo ""
