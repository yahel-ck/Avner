@echo off
python "%~dp0alassall.py" %*
if errorlevel 1 (
    pause
)
