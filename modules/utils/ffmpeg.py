import subprocess
from uuid import uuid4


def get_video_resolution(video_path: str) -> tuple[int, int]:
    ffprobe_command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "stream=width,height",
        "-of",
        "csv=s=x:p=0",
        video_path,
    ]
    ffprobe_result = subprocess.run(ffprobe_command, capture_output=True, text=True)
    video_width, video_height = map(int, ffprobe_result.stdout.strip().split("x"))
    return video_width, video_height


def resize_video(video_path: str, width: int, height: int, output_path: str) -> None:
    ffmpeg_command = [
        "ffmpeg",
        "-i",
        video_path,
        "-vf",
        f"scale={width}:{height}",
        "-crf",
        "15",
        "-preset",
        "fast",
        output_path,
    ]
    subprocess.run(ffmpeg_command, check=True)


def add_audio_to_video(video_path: str, audio_path: str, output_path: str) -> None:
    command = [
        "ffmpeg",
        "-i",
        video_path,
        "-i",
        audio_path,
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-shortest",
        output_path,
    ]

    subprocess.run(command, check=True)


def merge_videos(video_files: list[str], output_path: str) -> None:
    random_id = uuid4()
    concat_file = f"/tmp/concat_list-{random_id}.txt"
    with open(concat_file, "w") as f:
        for video_file in video_files:
            f.write(f"file '{video_file}'\n")

    command = [
        "ffmpeg",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        concat_file,
        "-b:v",
        "4M",
        "-crf",
        "24",
        "-preset",
        "medium",
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        output_path,
    ]

    subprocess.run(command, check=True)
