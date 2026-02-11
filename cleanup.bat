@echo off
REM Cleanup script for PTZOptics Email Analysis
REM Removes downloaded emails and reports for fresh testing

echo ============================================================
echo PTZOptics Email Analysis - Cleanup Script
echo ============================================================
echo.
echo This will delete:
echo   - All downloaded email files (data/raw/*.mbox)
echo   - All generated reports (reports/*)
echo   - Previous week comparison data
echo.
echo Files in root directory will NOT be deleted.
echo.

set /p confirm="Continue? (y/n): "
if /i not "%confirm%"=="y" (
    echo Cleanup cancelled.
    exit /b
)

echo.
echo Cleaning up...
echo.

REM Delete email files
if exist "data\raw\*.mbox" (
    del /q "data\raw\*.mbox"
    echo   ✓ Deleted email files from data/raw/
) else (
    echo   - No email files found in data/raw/
)

REM Delete report files
if exist "reports\*.txt" (
    del /q "reports\*.txt"
    echo   ✓ Deleted report files from reports/
) else (
    echo   - No report files found in reports/
)

if exist "reports\*.csv" (
    del /q "reports\*.csv"
    echo   ✓ Deleted CSV exports from reports/
) else (
    echo   - No CSV files found in reports/
)

REM Delete comparison data
if exist "previous_week_data.json" (
    del /q "previous_week_data.json"
    echo   ✓ Deleted previous week comparison data
) else (
    echo   - No previous week data found
)

REM Also clean up any files in root (legacy)
if exist "*.mbox" (
    del /q "*.mbox"
    echo   ✓ Deleted legacy mbox files from root
)

if exist "*_report*.txt" (
    del /q "*_report*.txt"
    echo   ✓ Deleted legacy report files from root
)

echo.
echo ============================================================
echo Cleanup complete!
echo ============================================================
echo.
echo You can now run a fresh analysis:
echo   python monday_morning_automation.py
echo.
pause
