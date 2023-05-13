import glob
from matchsubs import match_episodes
import subprocess
import shutil
import os.path


def fix_subtitles(reference_paths, subtitles_paths):
    ref_paths = glob.glob(reference_paths)
    subs_paths = glob.glob(subtitles_paths)
    for subs_path, ref_path in match_episodes(subs_paths, ref_paths):
        backup_file(subs_path)
        subprocess.call(
            ["alass", ref_path, subs_path, subs_path],
            shell=True,
        )


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
