import fire
import glob
import subprocess
import os


def cli(vids_glob):
    vids_paths = glob.glob(vids_glob)
    for path in vids_paths:
        out_path = os.path.splitext(os.path.basename(path))[0] + ".mp4"
        subprocess.check_call(["ffmpeg.exe", "-i", path, "-vcodec", "copy", "-acodec", "copy", out_path])


if __name__ == "__main__":
    fire.Fire(cli)
