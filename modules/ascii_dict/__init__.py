from typing import TypeAlias

from .black_and_white import AsciiDictBlackWhite
from .color import AsciiDictColor

AsciiDict: TypeAlias = AsciiDictBlackWhite | AsciiDictColor
