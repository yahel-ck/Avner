@echo off
for %%a in ("%~1") do ffmpeg.exe -i "%%a" -map 0:s:%~2 "%%~na.srt"
pause