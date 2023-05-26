import os
import re
from functools import cached_property, reduce
from os.path import abspath, dirname, join, splitext
from shutil import copyfile
from typing import Dict

from PTN import parse as parse_torrent_title

SUB_FILE_EXT = (".srt",)
VID_FILE_EXT = ("mp4", "mkv", "m4v")


class Torrent:
    def __init__(self, name: str) -> None:
        self.name = name

    @cached_property
    def info(self) -> Dict[str, str]:
        return parse_torrent_title(self.name)

    @cached_property
    def marker(self):
        return (self.info["title"], self.info["season"], self.info["episode"])

    def get(self, feature: str) -> str:
        return self.info.get(feature, "").lower()

    def similarity(self, other: "Torrent", features=None) -> float:
        if self.name == other.name:
            return 1.0
        if self.marker != other.marker:
            return 0.0

        if features is None:
            features = ("quality", "encoder", "network", "codec", "resolution")

        comp = [self.get(f) == other.get(f) for f in features]
        similarity = reduce(lambda acc, v: (acc << 1) + int(v), comp)
        similarity /= 2 ** len(comp)
        return similarity


def match_episodes(src_names, dst_names, ignore_no_match=True):
    src_torrents = map(Torrent, src_names)
    dst_torrents = map(Torrent, dst_names)
    src_markers = _group_by(lambda t: t.marker, src_torrents)

    for dst_torrent in dst_torrents:
        if dst_torrent.marker in src_markers:
            src_torrent = max(
                src_markers[dst_torrent.marker],
                key=dst_torrent.similarity,
            )
            yield src_torrent.name, dst_torrent.name
        elif not ignore_no_match:
            raise LookupError(
                f"No episode match for '{src_torrent.name}' in {dst_names}",
            )


def _group_by(mapper, values):
    groups = {}
    for value in values:
        key = mapper(value)
        groups.setdefault(key, []).append(value)
    return groups


def _list_files(dir_path, ext):
    return [f for f in os.listdir(dir_path) if f.lower().endswith(ext)]


def rename_subtitle_files(subs_dir=".", vids_dir="."):
    subs_dir = abspath(subs_dir)
    vids_dir = abspath(vids_dir)
    srt_files = _list_files(subs_dir, SUB_FILE_EXT)
    vid_files = _list_files(vids_dir, VID_FILE_EXT)

    rename = os.rename if subs_dir == vids_dir else copyfile
    for srt_file, vid_file in match_episodes(srt_files, vid_files):
        print(f"Matched {vid_file} with {srt_file}")
        base, _ = splitext(vid_file)
        _, ext = splitext(srt_file)
        rename(join(subs_dir, srt_file), join(vids_dir, base + ext))


if __name__ == "__main__":
    import fire
    fire.Fire(rename_subtitle_files)
