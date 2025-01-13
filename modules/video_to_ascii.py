import os
import shutil
from multiprocessing import Pool, cpu_count
from typing import Any

import numpy as np
import numpy.typing as npt
import progressbar
from cairo import ImageSurface
from cv2 import COLOR_BGR2RGB, VideoCapture, cvtColor
from cv2.typing import MatLike
from PIL import Image

from modules.ascii_dict import AsciiDict
from modules.dithering import DitheringStrategy
from modules.image_to_ascii import ascii_convert
from modules.save.formats import DisplayFormats
from modules.utils.custom_types import FrameData, Frames
from modules.utils.ffmpeg import (
    add_audio_to_video,
    extract_audio,
    get_total_frames,
    get_video_framerate,
    get_video_resolution,
    merge_frames,
    resize_video,
)
from modules.utils.font import Font
from modules.utils.utils import create_char_array

batch_size: int = 80


class ProcessingParameters:
    _instance = None

    def __init__(self, *_: Any) -> None:
        pass

    def __new__(
        cls,
        width: int,
        height: int,
        display_formats: list[DisplayFormats],
        dithering_strategy: DitheringStrategy | None,
        edge_detection: bool = False,
    ) -> "ProcessingParameters":
        if not cls._instance:
            cls._instance = super(ProcessingParameters, cls).__new__(cls)
            ascii_dicts: list[AsciiDict] = [
                (
                    display_format.value.HighAsciiDict
                    if width * height
                    >= (1600 // Font.Width.value) * (900 // Font.Height.value)
                    else display_format.value.LowAsciiDict
                )
                for display_format in display_formats
            ]
            cls._instance._char_arrays = [
                create_char_array(ascii_dict) for ascii_dict in ascii_dicts
            ]
            cls._instance._display_formats = display_formats
            cls._instance._dithering_strategy = dithering_strategy
            cls._instance._edge_detection = edge_detection

        return cls._instance

    @staticmethod
    def get_instance() -> "ProcessingParameters":
        return ProcessingParameters(0, 0, [DisplayFormats], DitheringStrategy)

    @property
    def char_arrays(self) -> list[npt.NDArray[np.str_]]:
        return self._char_arrays

    @char_arrays.setter
    def char_arrays(self, char_arrays: list[npt.NDArray[np.str_]]) -> None:
        self._char_arrays = char_arrays

    @property
    def display_formats(self) -> list[DisplayFormats]:
        return self._display_formats

    @display_formats.setter
    def display_formats(self, display_formats: list[DisplayFormats]) -> None:
        self._display_formats = display_formats

    @property
    def dithering_strategy(self) -> DitheringStrategy | None:
        return self._dithering_strategy

    @dithering_strategy.setter
    def dithering_strategy(self, dithering_strategy: DitheringStrategy | None) -> None:
        self._dithering_strategy = dithering_strategy

    @property
    def edge_detection(self) -> bool:
        return self._edge_detection

    @edge_detection.setter
    def edge_detection(self, edge_detection: bool) -> None:
        self._edge_detection = edge_detection


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
    ascii_image: list[ImageSurface] = ascii_convert(
        frame,
        ProcessingParameters.get_instance().char_arrays,
        ProcessingParameters.get_instance().dithering_strategy,
        ProcessingParameters.get_instance().display_formats,
        ProcessingParameters.get_instance().edge_detection,
    )
    ascii_image[0].write_to_png(f"./{video_name}/{frame_id:04d}.png")


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


def video_image_convert(
    video: str,
    height: int,
    dithering_strategy: DitheringStrategy | None,
    display_format: "DisplayFormats",
    edge_detection: bool = False,
) -> None:
    if height % 2 == 1:
        height += 1
    video_name: str = video.split(".")[0]
    video_width, video_height = get_video_resolution(video)
    width = int(video_width * height / video_height)
    if width % 2 == 1:
        width += 1
    downsize_height: int = int(height / Font.Height.value)
    if downsize_height % 2 == 1:
        downsize_height += 1

    downsize_width = int(
        downsize_height
        * video_width
        * (Font.Height.value / Font.Width.value)
        / video_height
    )
    if downsize_width % 2 == 1:
        downsize_width += 1

    downsize_video_path: str = f"{video_name}-downsize.mp4"
    resize_video(video, downsize_width, downsize_height, downsize_video_path)

    ProcessingParameters(
        downsize_width,
        downsize_height,
        [display_format],
        dithering_strategy,
        edge_detection,
    )

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
    output_path = f"{video_name}_ascii_temp.mp4"
    add_audio_to_video(video_path, audio_path, output_path)
    output_video_width, output_video_height = get_video_resolution(output_path)

    if output_video_height != height or output_video_width != width:
        resize_video(
            output_path,
            width,
            height,
            f"{video_name}_ascii.mp4",
            compression_level=22,
        )
        os.remove(output_path)
    else:
        os.rename(output_path, f"{video_name}_ascii.mp4")
