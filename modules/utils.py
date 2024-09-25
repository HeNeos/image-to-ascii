from typing import Optional, Tuple, Union, List

# ascii_chars: str = " `.',-~:;=+*#%@M"  # black background
# ascii_chars = "M@%#*+=;:~-,'.` "  # white background

ascii_chars: str = " `.',-_:;~\"!^=+*/o#%se&8B$MW&@"  # black background
# ascii_chars: str = " .`'-,^\":;~!_+=<>()|/\\1[]{}?i!lIftjrxnvczusSLoXYZOE9VwkmFAB8W#@$&%M"

def map_to_char_high(gray_scale: float) -> str:
    position: int = int(((len(ascii_chars) - 1) * gray_scale) / 255)
    return ascii_chars[position]


def calculate_scale(
    image_size: Tuple[int, int], scale: Optional[Union[int, float]] = None
) -> int:
    if scale:
        return int(scale)
    max_length = 200
    max_size = max(image_size)
    new_scale: int = (max_size + max_length - 1) // max_length
    return new_scale


def cut_grid(grid: List[List[str]]) -> List[List[str]]:
    resized_grid: List[List[str]] = []
    for line in grid:
        if not all(column == " " for column in line):
            resized_grid.append(line)
    return resized_grid
