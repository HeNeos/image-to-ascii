from dataclasses import dataclass
from typing import List, Tuple, TypeAlias, Union

from PIL import Image

Scale: TypeAlias = Union[float, int]
Color: TypeAlias = Tuple[int, int, int]
AsciiImage: TypeAlias = List[List[str]]
AsciiColors: TypeAlias = List[List[Color]]


@dataclass
class FrameData:
    frame: Image.Image
    frame_id: int
    video_name: str


Frames: TypeAlias = List[FrameData]
