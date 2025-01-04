from typing import TypeAlias

from .black_and_white import AsciiDictBlackWhite
from .color import AsciiDictColor
from .gray_scale import AsciiDictGrayScale

AsciiDict: TypeAlias = AsciiDictBlackWhite | AsciiDictGrayScale | AsciiDictColor
