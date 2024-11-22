import glob
import subprocess
import os


def copy_to_mp4(in_path: str, out_path: str, audio_track=None):
    args = ["ffmpeg.exe", "-i", in_path]
    if audio_track is not None:
        args.extend(
            [
                "-map",
                "0:v:0",
                "-map",
                "0:a:{}".format(audio_track),
            ]
        )
    args.extend(
        [
            "-vcodec",
            "copy",
            "-acodec",
            "copy",
            out_path,
        ]
    )

    print("Copying video '{}' to '{}'".format(in_path, out_path))
    print("Running {}".format(args))
    subprocess.check_call(args)
    print("Process finished\n")


def cli(
    vids_glob: str,
    skip_existing: bool = True,
    simple_glob: bool = True,
    audio_track=None,
):
    if simple_glob:
        vids_glob = "*".join(map(glob.escape, vids_glob.split("*")))
    print(vids_glob)
    vids_paths = glob.glob(vids_glob)
    print(vids_paths)
    for path in vids_paths:
        out_path = f"{os.path.splitext(os.path.basename(path))[0]}.mp4"
        if not (skip_existing and os.path.exists(out_path)):
            copy_to_mp4(path, out_path, audio_track)
        else:
            print(f"{out_path} already exists, skipping")
    print("Finished successfully :)")


if __name__ == "__main__":
    import fire

    fire.Fire(cli)
