import os
import re
import os.path

SUB_FILE_EXT = (".srt",)
VID_FILE_EXT = ("mp4", "mkv", "m4v")

MARKER_RE = re.compile(r"S\d\dE\d\d", flags=re.IGNORECASE)


def find_marker(file_name):
    return MARKER_RE.findall(file_name)[0]


def match_episodes(src_names, dst_names, ignore_no_match=True):
    dst_markers = dict((find_marker(name), name) for name in dst_names)
    for src_name in src_names:
        marker = find_marker(src_name)
        if marker in dst_markers:
            dst_name = dst_markers[marker]
            yield (src_name, dst_name)
        elif not ignore_no_match:
            raise LookupError(f"No episode match for '{src_name}' in {dst_names}")


def rename_subtitle_files():
    file_names = os.listdir(".")
    srt_files = [f for f in file_names if f.lower().endswith(SUB_FILE_EXT)]
    vid_files = [f for f in file_names if f.lower().endswith(VID_FILE_EXT)]

    for srt_file, vid_file in match_episodes(srt_files, vid_files):
        base, _ = os.path.splitext(vid_file)
        _, ext = os.path.splitext(srt_file)
        os.rename(srt_file, base + ext)


if __name__ == "__main__":
    rename_subtitle_files()
