import time
import timeit
from typing import Union

import cv2
from image_to_ascii import process_image
from PIL import Image


def resize_frame(frame, scale):
    height, width, _ = frame.shape
    return cv2.resize(frame, (2 * int(width / scale), int(height / scale)))


def video_convert(video: Union[str, int], scale: Union[float, int]):
    video_capture = cv2.VideoCapture(video)
    while True:
        ret, frame = video_capture.read()
        time_per_frame = None
        to_sleep = None
        if ret:
            if time_per_frame is None:
                start = timeit.timeit()
            resized_frame = Image.fromarray(
                cv2.cvtColor(resize_frame(frame, scale), cv2.COLOR_BGR2RGB)
            )
            ascii_frame = process_image(resized_frame, rescale=False)
            for line in ascii_frame:
                print("".join(line))
            print("\033[H", end="")
            if time_per_frame is None:
                time_per_frame = timeit.timeit() - start
                to_sleep = (1 - 47 * time_per_frame) / 47
            if to_sleep > 0.1:
                time.sleep(to_sleep)
        else:
            break

    video_capture.release()
