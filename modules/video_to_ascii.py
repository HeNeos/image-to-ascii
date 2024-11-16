import os
import shutil
from multiprocessing import Pool, cpu_count

import progressbar
from cairo import ImageSurface
from cv2 import COLOR_BGR2RGB, VideoCapture, cvtColor
from cv2.typing import MatLike
from PIL import Image

from modules.image_to_ascii import ascii_convert
from modules.utils.custom_types import FrameData, Frames
from modules.utils.ffmpeg import (add_audio_to_video, extract_audio,
                                  get_total_frames, get_video_framerate,
                                  get_video_resolution, merge_frames,
                                  resize_video)
from modules.utils.font import Font

batch_size: int = 100


def extract_frame(video_capture: VideoCapture) -> tuple[bool, MatLike]:
    ret, frame = video_capture.read()
    return ret, frame


def extract_frames(
    video_capture: VideoCapture,
    video_name: str,
    latest_frame_id: int,
    batch_size: int = 50,
) -> tuple[Frames, bool]:
    frame_id: int = latest_frame_id + 1
    frames: Frames = []
    ret: bool = False
    for _ in range(batch_size):
        ret, frame = extract_frame(video_capture)
        if ret:
            resized_frame: Image.Image = Image.fromarray(cvtColor(frame, COLOR_BGR2RGB))
            frames.append(
                FrameData(frame=resized_frame, frame_id=frame_id, video_name=video_name)
            )
            frame_id += 1
        else:
            break
    return frames, ret


def process_frame(frame_data: FrameData) -> None:
    frame: Image.Image = frame_data.frame
    frame_id: int = frame_data.frame_id
    video_name: str = frame_data.video_name
    ascii_image: ImageSurface = ascii_convert(frame)
    ascii_image.write_to_png(f"./{video_name}/{frame_id:04d}.png")


def process_frames(
    video_capture: VideoCapture, video_name: str, video_frames: int
) -> list[str]:
    frame_id: int = 0
    latest_ret: bool = True
    frames_filenames: list[str] = []
    with progressbar.ProgressBar(
        max_value=video_frames,
        widgets=[
            progressbar.Percentage(),
            " ",
            progressbar.GranularBar(),
            " ",
            progressbar.ETA(),
        ],
    ) as bar:
        while latest_ret:
            frames, latest_ret = extract_frames(
                video_capture=video_capture,
                video_name=video_name,
                latest_frame_id=frame_id,
                batch_size=batch_size,
            )
            frame_id += batch_size
            pool = Pool(cpu_count())
            frames_filenames.extend(
                [
                    f"./{video_name}/{frame_data.frame_id:04d}.png"
                    for frame_data in frames
                ]
            )
            pool.map(process_frame, frames)
            bar.update(len(frames_filenames))
        bar.update(video_frames)
    return frames_filenames


def video_image_convert(video: str, height: int) -> None:
    video_name: str = video.split(".")[0]
    video_width, video_height = get_video_resolution(video)
    new_height: int = int(height / Font.Height.value)

    scale_factor: float = new_height / video_height
    new_width = int(Font.Height.value / Font.Width.value * scale_factor * video_width)
    if new_width % 2 == 1:
        new_width += 1

    downsize_video_path: str = f"{video_name}-downsize.mp4"
    resize_video(video, new_width, new_height, downsize_video_path)

    video_framerate: float = get_video_framerate(downsize_video_path)
    video_frames: int = get_total_frames(downsize_video_path)

    if os.path.exists(f"./{video_name}") and os.path.isdir(f"./{video_name}"):
        shutil.rmtree(f"./{video_name}")
    os.makedirs(f"./{video_name}")

    audio_path: str = f"./{video_name}/audio.mp3"
    extract_audio(downsize_video_path, audio_path)

    video_capture: VideoCapture = VideoCapture(downsize_video_path)

    frames_filenames: list[str] = process_frames(
        video_capture, video_name, video_frames
    )
    video_capture.release()

    video_path = f"/tmp/{video_name}.mp4"
    merge_frames(frames_filenames, video_framerate, video_path)
    output_path = f"{video_name}_ascii.mp4"
    add_audio_to_video(video_path, audio_path, output_path)
