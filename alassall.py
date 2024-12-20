import glob
from matchsubs import match_episodes
import subprocess
import shutil
import os.path


def fix_subtitles(reference_glob, subtitles_glob, simple_glob=True):
    if simple_glob:
        reference_glob = "*".join(map(glob.escape, reference_glob.split("*")))
        subtitles_glob = "*".join(map(glob.escape, subtitles_glob.split("*")))
    ref_paths = _get_paths(reference_glob)
    subs_paths = _get_paths(subtitles_glob)
    for subs_path, ref_path in match_episodes(subs_paths, ref_paths):
        backup_file(subs_path)
        subprocess.call(
            ["alass", ref_path, subs_path, subs_path],
            shell=True,
        )


def _get_paths(glob_path):
    paths = glob.glob(glob_path)
    if len(paths) == 0:
        raise FileNotFoundError(f"No file(s) found for path {glob_path}")
    return paths


def backup_file(path):
    backup_path = get_backup_path(path)
    if not os.path.exists(backup_path):
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        shutil.copyfile(path, backup_path)


def get_backup_path(path):
    dirname, filename = os.path.split(path)
    return os.path.join(dirname, "subs_backup", filename)


if __name__ == "__main__":
    import fire
    fire.Fire(fix_subtitles)
