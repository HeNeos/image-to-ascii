import numpy as np
import numpy.typing as npt
from cairo import ImageSurface
from PIL import Image

from modules.ascii_dict import AsciiDict
from modules.dithering import DitheringStrategy
from modules.save.formats import DisplayFormats
from modules.utils.custom_types import AsciiColors, AsciiImage
from modules.utils.font import Font
from modules.utils.utils import (create_ascii_image, create_char_array,
                                 map_to_char_vectorized, rescale_image)


def process_image(
    image: Image.Image,
    char_array: npt.NDArray[np.str_],
    dithering_strategy: type[DitheringStrategy] | None = None,
) -> tuple[AsciiImage, AsciiColors, npt.NDArray[np.float64]]:
    img_array: npt.NDArray[np.uint8] = np.array(image, dtype=np.uint8)

    # custom grayscale
    gray_array: npt.NDArray[np.float64] = np.clip(
        np.dot(img_array[..., :3], [0.3190, 0.5870, 0.1240]), 0.0, 255.0
    )

    if dithering_strategy is not None:
        gray_array = dithering_strategy.dithering(gray_array, len(char_array))

    ascii_chars: npt.NDArray[np.str_] = map_to_char_vectorized(gray_array, char_array)

    grid: AsciiImage = ascii_chars.tolist()
    image_colors: AsciiColors = [row.tolist() for row in img_array]

    return grid, image_colors, gray_array


def ascii_convert(
    image: Image.Image,
    char_array: npt.NDArray[np.str_],
    dithering_strategy: type[DitheringStrategy] | None,
    display_formats: list[DisplayFormats],
) -> list[ImageSurface]:
    grid, image_colors, gray_array = process_image(
        image, char_array, dithering_strategy
    )
    return create_ascii_image(grid, image_colors, gray_array, display_formats)


def run(
    image_path: str,
    height: int,
    dithering_strategy: type[DitheringStrategy] | None,
    display_formats: list[DisplayFormats] = [
        DisplayFormats.COLOR,
        DisplayFormats.GRAY_SCALE,
        DisplayFormats.BLACK_AND_WHITE,
    ],
) -> None:
    image_name: str = image_path.split(".")[0]
    image: Image.Image = Image.open(image_path).convert("RGB")
    rescaled_image: Image.Image = rescale_image(image, height)
    new_width, new_height = rescaled_image.size

    ascii_dict = (
        AsciiDict.HighAsciiDict
        if new_width * new_height
        >= (1600 // Font.Width.value) * (900 // Font.Height.value)
        else AsciiDict.LowAsciiDict
    )
    char_array: npt.NDArray[np.str_] = create_char_array(ascii_dict)

    ascii_images: list[ImageSurface] = ascii_convert(
        rescaled_image, char_array, dithering_strategy, display_formats
    )
    for ascii_image, display_format in zip(ascii_images, display_formats):
        ascii_image.write_to_png(f"{image_name}_ascii_{display_format.value}.png")
