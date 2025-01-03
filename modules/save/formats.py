from enum import Enum

from ..ascii_dict.color import AsciiDictColor
from ..ascii_dict.black_and_white import AsciiDictBlackWhite


class DisplayFormats(Enum):
    COLOR = AsciiDictColor
    GRAY_SCALE = AsciiDictColor
    BLACK_AND_WHITE = AsciiDictBlackWhite


class SaveFormats(Enum):
    IMAGE = "image"
    VIDEO = "video"
    TEXT = "text"


# @dataclass
# class OutputFormats:
#     ascii_dict: AsciiDict
#     save_format: SaveFormats
#     display_format: list[DisplayFormats] = field(
#         default_factory=lambda: [DisplayFormats.COLOR]
#     )
#     output: bool = False
