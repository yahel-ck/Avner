import os
import re
import os.path

SUB_FILE_EXT = (".srt",)
VID_FILE_EXT = ("mp4", "mkv", "m4v")

MARKER_RE = re.compile(r"S\d\dE\d\d", flags=re.IGNORECASE)


def find_marker(file_name):
    return MARKER_RE.findall(file_name)[0]


def rename_subtitle_files():
    file_names = os.listdir(".")
    srt_files = [f for f in file_names if f.lower().endswith(SUB_FILE_EXT)]
    vid_files = [f for f in file_names if f.lower().endswith(VID_FILE_EXT)]

    vid_markers = dict((find_marker(f), f) for f in vid_files)

    for srt_file in srt_files:
        marker = find_marker(srt_file)
        vid_file = vid_markers[marker]
        base, _ = os.path.splitext(vid_file)
        _, ext = os.path.splitext(srt_file)
        os.rename(srt_file, base + ext)


if __name__ == "__main__":
    rename_subtitle_files()
