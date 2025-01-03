from enum import Enum

from ..ascii_dict.color import AsciiDictColor
from ..ascii_dict.gray_scale import AsciiDictGrayScale
from ..ascii_dict.black_and_white import AsciiDictBlackWhite


class DisplayFormats(Enum):
    COLOR = AsciiDictColor
    GRAY_SCALE = AsciiDictGrayScale
    BLACK_AND_WHITE = AsciiDictBlackWhite


class SaveFormats(Enum):
    IMAGE = "image"
    VIDEO = "video"
    TEXT = "text"
