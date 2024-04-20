import fire
import glob
import subprocess
import os


def cli(vids_glob: str, skip_existing: bool = True):
    vids_paths = glob.glob(vids_glob)
    for path in vids_paths:
        out_path = f"{os.path.splitext(os.path.basename(path))[0]}.mp4"
        if not (skip_existing and os.path.exists(out_path)):
            subprocess.check_call(
                [
                    "ffmpeg.exe",
                    "-i",
                    path,
                    "-vcodec",
                    "copy",
                    "-acodec",
                    "copy",
                    out_path,
                ]
            )
        else:
            print(f"{out_path} already exists, skipping")
    print("Finished successfully :)")


if __name__ == "__main__":
    fire.Fire(cli)
