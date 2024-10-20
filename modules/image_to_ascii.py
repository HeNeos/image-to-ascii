import numpy as np
from PIL import Image
from cairo import ImageSurface
from modules.ascii_dict import AsciiDict
from modules.utils.utils import (
    create_char_array,
    map_to_char_vectorized,
    create_ascii_image,
    rescale_image,
)
from modules.utils.save import SaveFormats
from modules.utils.custom_types import AsciiImage, AsciiColors


def process_image(image: Image.Image) -> tuple[AsciiImage, AsciiColors]:
    img_array = np.array(image)
    height, width, _ = img_array.shape

    gray_array = np.dot(img_array[..., :3], [0.2989, 0.5870, 0.1140])

    ascii_dict = (
        AsciiDict.HighAsciiDict
        if width * height >= 180 * 180
        else AsciiDict.LowAsciiDict
    )
    char_array = create_char_array(ascii_dict)

    ascii_chars = map_to_char_vectorized(gray_array, char_array)

    grid: AsciiImage = ascii_chars.tolist()
    image_colors: AsciiColors = [row.tolist() for row in img_array]

    return grid, image_colors


def ascii_convert(image: Image.Image) -> ImageSurface:
    grid, image_colors = process_image(image=image)
    return create_ascii_image(grid, image_colors)


def run(image_path: str, scale: int, save_format: SaveFormats):
    image: Image.Image = Image.open(image_path).convert("RGB")
    rescaled_image: Image.Image = rescale_image(image, scale)
    ascii_image: ImageSurface = ascii_convert(rescaled_image)
    ascii_image.write_to_png(f"{image_path}_ascii.png")
    # ascii_image.save(f"{image_path}_ascii.png")
