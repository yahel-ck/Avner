for %%a in ("*.mkv") do ffmpeg.exe -i "%%a" -vcodec copy -acodec copy "%%~na .mp4"
pause