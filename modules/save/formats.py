from dataclasses import dataclass, field
from enum import Enum


class DisplayFormats(Enum):
    COLOR = "color"
    GRAY_SCALE = "gray_scale"
    BLACK_AND_WHITE = "black_and_white"


class SaveFormats(Enum):
    IMAGE = "image"
    VIDEO = "video"
    TEXT = "text"


@dataclass
class OutputFormats:
    save_format: SaveFormats
    display_format: list[DisplayFormats] = field(
        default_factory=lambda: [DisplayFormats.COLOR]
    )
    output: bool = False
