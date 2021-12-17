import codecs
import os


def get_subtitle_files():
    """
    Returns a list of subtitle files in the current directory.
    """
    subtitle_files = []
    for file in os.listdir():
        if file.endswith(".srt"):
            subtitle_files.append(file)
    return subtitle_files


def fix_subtitle_file(subtitle_file):
    """
    Fixes the encoding of a subtitle file.
    """
    with codecs.open(subtitle_file, "r", "cp1255") as file:
        text = file.read()
    with codecs.open(subtitle_file, "w", "utf-8") as file:
        file.write(text)


def fix_subtitles_in_current_dir():
    subtitle_files = get_subtitle_files()
    for subtitle_file in subtitle_files:
        try:
            fix_subtitle_file(subtitle_file)
        except UnicodeDecodeError:
            pass


if __name__ == '__main__':
    fix_subtitles_in_current_dir()

