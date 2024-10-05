import os
from PIL import Image
from typing import Tuple, Optional
from modules.ascii_dict import AsciiDict
from modules.utils import calculate_scale, map_to_char
from modules.save import SaveFormats, save_ascii
from modules.font import Font
from modules.types import Scale, AsciiImage, AsciiColors


def rescale_image(
    image: Image.Image, image_path: str, rescale: Scale
) -> Tuple[Image.Image, str]:
    width, height = image.size
    image_name, image_extension = image_path.split(".")
    rescale: int = calculate_scale((width, height), rescale)
    resized_width: int = int(width * (Font.Height.value / Font.Width.value) // rescale)
    resized_height: int = height // rescale
    resized_image_name: str = f"{image_name}_resized.{image_extension}"
    image.resize((resized_width, resized_height)).save(resized_image_name)
    resized_image: Image.Image = Image.open(resized_image_name)
    return resized_image, resized_image_name


def process_image(
    image: Image.Image, image_path: str = "", rescale: Optional[Scale] = None
) -> Tuple[AsciiImage, AsciiColors]:
    if rescale:
        image, resized_image_name = rescale_image(image, image_path, rescale)
    pix = image.load()

    gray_image: Image.Image = image.convert("LA")
    width, height = gray_image.size

    ascii_dict = (
        AsciiDict.HighAsciiDict
        if width * height >= 150 * 150
        else AsciiDict.LowAsciiDict
    )

    grid: AsciiImage = [["X"] * width for _ in range(height)]
    image_colors: AsciiColors = [[(255, 255, 255)] * width for _ in range(height)]

    gray_pixels = gray_image.load()
    for y in range(height):
        for x in range(width):
            current_char: str = map_to_char(gray_pixels[x, y][0], ascii_dict)
            grid[y][x] = current_char
            image_colors[y][x] = pix[x, y]
    if rescale:
        os.remove(resized_image_name)

    return grid, image_colors


def ascii_convert(
    image_path: str,
    scale: Optional[Scale] = None,
    save_format: SaveFormats = SaveFormats.Show,
) -> AsciiImage:

    image_name, image_extension = image_path.split(".")
    image: Image.Image = Image.open(image_path).convert("RGB")
    grid, image_colors = process_image(
        image=image, image_path=image_path, rescale=scale
    )

    # resized_grid: List[List[str]] = cut_grid(grid)

    if save_format is SaveFormats.Show:
        for row in grid:
            print("".join(row))
    else:
        save_ascii(
            ascii_art=grid,
            save_format=save_format,
            image_name=image_name,
            image_colors=image_colors,
        )
    return grid
