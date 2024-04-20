import os
from functools import cached_property, reduce
from os.path import abspath, dirname, join, splitext
from pathlib import Path
from shutil import copyfile
from typing import Dict, List
import re

from PTN import parse as parse_torrent_title

SUB_FILE_EXT = ("srt",)
VID_FILE_EXT = ("mp4", "mkv", "m4v")


class Torrent:
    def __init__(self, name: str) -> None:
        self.name = name

    @cached_property
    def info(self) -> Dict[str, str]:
        return parse_torrent_title(self.name)

    @cached_property
    def marker(self):
        if "season" in self.info and "episode" in self.info:
            return (self.info["season"], self.info["episode"])
        elif "title" in self.info:
            return self.info["title"]
        else:
            return self.info

    def get(self, feature: str) -> str:
        return self.info.get(feature, "").lower()

    def similarity(self, other: "Torrent", features: List[str] = None) -> float:
        """
        Calculates a similarity score ranging from 0 (least similar) to 1
        (identical).
        Returns 0 if the markers are different.

        :param features: Features to compare, ordered by descending importance.
        Each feature should be the name of a field from `info`.
        Defaults to [quality, encoder, network, codec, resolution].
        """
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


def match_episodes(
    src_names: List[str], dst_names: List[str], ignore_no_match: bool = True
):
    """
    For each episode in `dst_names`, find a matching episode from `src_names`,
    if there are multiple matches use the most similar one.
    """
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


def find_original_file_names(path: Path, current_file_names: List[str]):
    """
    :param path: A path to either a file to extract the original names from, or
    to the directory to search for the names file in.
    :param current_file_names: A list of the current file names.

    :return: A list of tuples of (original_name, current_name).
    """
    if path.is_file():
        lines = path.read_text().split("\n")
        return match_episodes(lines, current_file_names)
    elif path.is_dir():
        names_file = _find_original_file_names_file(path)
        if names_file:
            return find_original_file_names(names_file, current_file_names)

        names = list(list(find_original_file_names(p, current_file_names))
                     for p in path.glob("*.txt"))
        if names:
            return max(names, key=len)
        else:
            return []


def _find_original_file_names_file(torrent_dir: Path) -> Path:
    pattern = re.compile(r".*(original|names).*\.txt", re.IGNORECASE)
    for path in torrent_dir.iterdir():
        if pattern.match(path.name):
            return path


def _group_by(mapper, values):
    groups = {}
    for value in values:
        key = mapper(value)
        groups.setdefault(key, []).append(value)
    return groups


def _list_files(dir_path, ext):
    return [f for f in os.listdir(dir_path) if f.lower().endswith(ext)]


def rename_subtitle_files(
    subs_dir=".", 
    vids_dir=".", 
    quality: str = None, 
    overwrite: bool = False
):
    subs_dir = abspath(subs_dir)
    vids_dir = abspath(vids_dir)
    srt_files = _list_files(subs_dir, SUB_FILE_EXT)
    vid_files = _list_files(vids_dir, VID_FILE_EXT)

    if quality:
        srt_files = filter(
            lambda n: Torrent(n).get("quality") == quality,
            srt_files,
        )

    original_file_names = dict(
        find_original_file_names(Path(vids_dir), vid_files))

    if len(original_file_names) != len(vid_files):
        original_file_names = dict(((f, f) for f in vid_files))

    errors =[]
    rename = os.rename if subs_dir == vids_dir else copyfile
    for srt_file, vid_file in match_episodes(srt_files, original_file_names.keys()):
        real_vid_file = original_file_names[vid_file]
        print(f"Matched {vid_file} with {srt_file}")
        base, _ = splitext(real_vid_file)
        _, ext = splitext(srt_file)
        dst_path = join(vids_dir, base + ext)
        if not overwrite and os.path.exists(dst_path):
            errors.append(f"File {dst_path} already exists!")
        rename(join(subs_dir, srt_file), dst_path)
    
    if errors:
        for error in errors:
            print(error)
        os.system("pause")


if __name__ == "__main__":
    import fire
    fire.Fire(rename_subtitle_files)
