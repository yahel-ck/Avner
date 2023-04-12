@echo off
for %%a in ("%1") do ffmpeg.exe -i "%%a" -vcodec copy -acodec copy "%%~na.mp4"
pause