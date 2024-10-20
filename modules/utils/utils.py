import cairo
import numpy as np

from typing import List
from modules.ascii_dict import AsciiDict
from modules.utils.font import Font
from modules.utils.custom_types import AsciiColors, AsciiImage
from PIL import Image


def create_char_array(ascii_dict: AsciiDict) -> np.ndarray:
    return np.array(list(ascii_dict.value))


def map_to_char_vectorized(values: np.ndarray, char_array: np.ndarray) -> np.ndarray:
    return char_array[np.digitize(values, np.linspace(0, 256, len(char_array) + 1)) - 1]


def map_to_char(gray_scale: float, ascii_dict: AsciiDict) -> str:
    position: int = int(((len(ascii_dict.value) - 1) * gray_scale) / 255)
    return ascii_dict.value[position]


def create_ascii_image(
    ascii_art: AsciiImage, image_colors: AsciiColors
) -> cairo.ImageSurface:
    rows = len(ascii_art)
    columns = len(ascii_art[0])

    surface_width = int(Font.Width.value * columns)
    surface_height = int(Font.Height.value * rows)

    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, surface_width, surface_height)
    context = cairo.Context(surface)

    context.select_font_face(
        "Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL
    )
    context.set_font_size(12)

    y = 0
    for row in range(rows):
        x = 0
        for column in range(columns):
            char = ascii_art[row][column]
            color = image_colors[row][column]
            context.set_source_rgb(color[0] / 255, color[1] / 255, color[2] / 255)
            context.move_to(x, y + Font.Height.value)
            context.show_text(char)
            x += Font.Width.value

        y += Font.Height.value

    return surface


def rescale_image(image: Image.Image, scale: int) -> Image.Image:
    width, height = image.size
    resized_height: int = scale // Font.Height.value
    scale: float = resized_height / height
    resized_width: int = int(width * (Font.Height.value / Font.Width.value) * scale)
    resized_image = image.resize((resized_width, resized_height))
    return resized_image


def cut_grid(grid: List[List[str]]) -> List[List[str]]:
    resized_grid: List[List[str]] = []
    for line in grid:
        if not all(column == " " for column in line):
            resized_grid.append(line)
    return resized_grid
