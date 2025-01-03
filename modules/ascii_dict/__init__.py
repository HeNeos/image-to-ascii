from typing import TypeAlias

# from dataclasses import dataclass

from .black_and_white import AsciiDictBlackWhite
from .color import AsciiDictColor

AsciiDict: TypeAlias = AsciiDictBlackWhite | AsciiDictColor


# @dataclass
# class AsciiDict:
#     black_and_white = AsciiDictBlackWhite
#     color = AsciiDictColor
