# import time
# import timeit
from typing import Tuple

import cv2
from cv2.typing import MatLike
from modules.image_to_ascii import process_image
from PIL import Image
from multiprocessing import Pool, cpu_count

from modules.save import SaveFormats, save_ascii
from modules.font import Font
from modules.types import Scale, Frames, FrameData

batch_size: int = 100


def resize_frame(frame, scale: Scale):
    height, width, _ = frame.shape
    return cv2.resize(
        frame,
        (
            int(Font.Height.value / Font.Width.value * width / scale),
            int(height / scale),
        ),
    )


# def video_convert(video: Union[str, int], scale: Scale):
#     video_capture = cv2.VideoCapture(video)
#     while True:
#         ret, frame = video_capture.read()
#         time_per_frame = None
#         to_sleep = None
#         if ret:
#             if time_per_frame is None:
#                 start = timeit.timeit()
#             resized_frame = Image.fromarray(
#                 cv2.cvtColor(resize_frame(frame, scale), cv2.COLOR_BGR2RGB)
#             )
#             ascii_frame = process_image(image=resized_frame)
#             for line in ascii_frame:
#                 print("".join(line))
#             print("\033[H", end="")
#             if time_per_frame is None:
#                 time_per_frame = timeit.timeit() - start
#                 to_sleep = (1 - 47 * time_per_frame) / 47
#             if to_sleep > 0.1:
#                 time.sleep(to_sleep)
#         else:
#             break

#     video_capture.release()


def extract_frame(video_capture: cv2.VideoCapture) -> Tuple[bool, MatLike]:
    ret, frame = video_capture.read()
    return ret, frame


def extract_frames(
    video_capture: cv2.VideoCapture,
    scale: Scale,
    video_name: str,
    latest_frame_id: int,
    batch_size: int = 100,
) -> Tuple[Frames, bool]:
    frame_id: int = latest_frame_id + 1
    frames: Frames = []
    for _ in range(batch_size):
        ret, frame = extract_frame(video_capture)
        if ret:
            resized_frame: Image.Image = Image.fromarray(
                cv2.cvtColor(resize_frame(frame, scale), cv2.COLOR_BGR2RGB)
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
    grid, image_colors = process_image(image=frame)
    save_ascii(
        ascii_art=grid,
        save_format=SaveFormats.Image,
        image_name=f"./{video_name}/{frame_id:08d}",
        image_colors=image_colors,
    )


def process_frames(video_capture: cv2.VideoCapture, scale: Scale, video_name: str):
    frame_id: int = 0
    latest_ret: bool = True
    while latest_ret:
        frames, latest_ret = extract_frames(
            video_capture=video_capture,
            scale=scale,
            video_name=video_name,
            latest_frame_id=frame_id,
            batch_size=batch_size,
        )
        frame_id += batch_size
        pool = Pool(cpu_count())
        pool.map(process_frame, frames)


def video_image_convert(video: str, scale: Scale):
    video_name: str = video.split(".")[0]
    video_capture: cv2.VideoCapture = cv2.VideoCapture(video)

    process_frames(video_capture, scale, video_name)
    video_capture.release()
