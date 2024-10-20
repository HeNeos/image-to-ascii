from cairo import ImageSurface
import cv2
from cv2.typing import MatLike
from modules.image_to_ascii import ascii_convert
from PIL import Image
from multiprocessing import Pool, cpu_count

from modules.utils.font import Font
from modules.utils.custom_types import Scale, Frames, FrameData
from modules.utils.ffmpeg import get_video_resolution, resize_video

batch_size: int = 50


def extract_frame(video_capture: cv2.VideoCapture) -> tuple[bool, MatLike]:
    ret, frame = video_capture.read()
    return ret, frame


def extract_frames(
    video_capture: cv2.VideoCapture,
    video_name: str,
    latest_frame_id: int,
    batch_size: int = 50,
) -> tuple[Frames, bool]:
    frame_id: int = latest_frame_id + 1
    frames: Frames = []
    for _ in range(batch_size):
        ret, frame = extract_frame(video_capture)
        if ret:
            resized_frame: Image.Image = Image.fromarray(
                cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            )
            frames.append(
                FrameData(frame=resized_frame, frame_id=frame_id, video_name=video_name)
            )
            frame_id += 1
        else:
            break
    return frames, ret


def process_frame(frame_data: FrameData):
    frame: Image.Image = frame_data.frame
    frame_id: int = frame_data.frame_id
    video_name: str = frame_data.video_name
    ascii_image: ImageSurface = ascii_convert(frame)
    ascii_image.write_to_png(f"./{video_name}/{frame_id:04d}.png")


def process_frames(video_capture: cv2.VideoCapture, video_name: str):
    frame_id: int = 0
    latest_ret: bool = True
    while latest_ret:
        frames, latest_ret = extract_frames(
            video_capture=video_capture,
            video_name=video_name,
            latest_frame_id=frame_id,
            batch_size=batch_size,
        )
        frame_id += batch_size
        pool = Pool(cpu_count())
        pool.map(process_frame, frames)


def video_image_convert(video: str, scale: Scale):
    video_name: str = video.split(".")[0]
    video_width, video_height = get_video_resolution(video)
    new_height: int = int(scale / Font.Height.value)

    scale_factor: float = new_height / video_height
    new_width = int(Font.Height.value / Font.Width.value * scale_factor * video_width)
    if new_width % 2 == 1:
        new_width += 1

    downsize_video_path: str = f"{video_name}-downsize.mp4"

    resize_video(video, new_width, new_height, downsize_video_path)

    video_capture: cv2.VideoCapture = cv2.VideoCapture(downsize_video_path)

    process_frames(video_capture, video_name)
    video_capture.release()
