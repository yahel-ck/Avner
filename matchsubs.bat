@echo off
python "%~dp0matchsubs.py" %*
if errorlevel 1 (
    pause
)
