from dataclasses import dataclass
from typing import List, Tuple, TypeAlias, Union
import numpy as np
import numpy.typing as npt

Scale: TypeAlias = Union[float, int]
Color: TypeAlias = Tuple[int, int, int]
AsciiImage: TypeAlias = List[List[str]]
AsciiColors: TypeAlias = List[List[Color]]


@dataclass
class FrameData:
    frame: npt.NDArray[np.uint8]
    frame_id: int
    video_name: str


Frames: TypeAlias = List[FrameData]
