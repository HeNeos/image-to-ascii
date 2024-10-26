import numpy as np
import numpy.typing as npt
from cairo import ImageSurface
from PIL import Image

from modules.ascii_dict import AsciiDict
from modules.utils.custom_types import AsciiColors, AsciiImage
from modules.utils.font import Font
from modules.utils.utils import (create_ascii_image, create_char_array,
                                 map_to_char_vectorized, rescale_image)


def process_image(image: Image.Image) -> tuple[AsciiImage, AsciiColors]:
    img_array: npt.NDArray[np.uint8] = np.array(image)
    height, width, _ = img_array.shape

    gray_array: npt.NDArray[np.float64] = np.dot(
        img_array[..., :3], [0.2989, 0.5870, 0.1140]
    )

    ascii_dict = (
        AsciiDict.HighAsciiDict
        if width * height >= (1920 // Font.Width.value) * (1080 // Font.Height.value)
        else AsciiDict.LowAsciiDict
    )
    char_array: npt.NDArray[np.str_] = create_char_array(ascii_dict)

    ascii_chars: npt.NDArray[np.str_] = map_to_char_vectorized(gray_array, char_array)

    grid: AsciiImage = ascii_chars.tolist()
    image_colors: AsciiColors = [row.tolist() for row in img_array]

    return grid, image_colors


def ascii_convert(image: Image.Image) -> ImageSurface:
    grid, image_colors = process_image(image=image)
    return create_ascii_image(grid, image_colors)


def run(image_path: str, height: int) -> None:
    image_name: str = image_path.split(".")[0]
    image: Image.Image = Image.open(image_path).convert("RGB")
    rescaled_image: Image.Image = rescale_image(image, height)
    ascii_image: ImageSurface = ascii_convert(rescaled_image)
    ascii_image.write_to_png(f"{image_name}_ascii.png")
    # ascii_image.save(f"{image_path}_ascii.png")
