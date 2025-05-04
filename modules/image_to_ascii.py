import cv2
import numpy as np
import numpy.typing as npt
from cairo import FORMAT_ARGB32, FORMAT_RGB24, ImageSurface
from pathlib import Path

from modules.ascii_dict import AsciiDict
from modules.dithering import DitheringStrategy
from modules.save.formats import DisplayFormats
from modules.utils.custom_types import AsciiColors, AsciiImage
from modules.utils.font import Font
from modules.utils.utils import (
    create_ascii_image,
    create_char_array,
    map_to_char_vectorized,
    rescale_image,
)
from modules.edge_detection import EdgeDetection


def process_image(
    image: npt.NDArray[np.uint8],
    char_arrays: list[npt.NDArray[np.str_]],
    dithering_strategy: DitheringStrategy | None = None,
    edge_detection: bool = False,
) -> tuple[list[AsciiImage], AsciiColors, npt.NDArray[np.float64]]:

    # custom grayscale
    gray_array: npt.NDArray[np.float64] = np.clip(
        np.dot(image[..., :3], [0.3090, 0.5670, 0.1240]), 0.0, 255.0
    )

    edge_detection_parameters: EdgeDetection = EdgeDetection()
    if edge_detection:
        edge_detection_parameters.apply_canny(image)
        edge_detection_parameters.apply_sobel(gray_array)

    if dithering_strategy is not None:
        gray_array = dithering_strategy.dithering(gray_array, len(char_arrays[0]))

    ascii_chars: list[npt.NDArray[np.str_]] = [
        map_to_char_vectorized(gray_array, char_array, edge_detection_parameters)
        for char_array in char_arrays
    ]

    grids: list[AsciiImage] = [ascii_char.tolist() for ascii_char in ascii_chars]
    image_colors: AsciiColors = [row.tolist() for row in image]

    return grids, image_colors, gray_array


def ascii_convert(
    image: npt.NDArray[np.uint8],
    char_arrays: list[npt.NDArray[np.str_]],
    dithering_strategy: DitheringStrategy | None,
    display_formats: list[DisplayFormats],
    edge_detection: bool = False,
) -> list[ImageSurface]:
    grids, image_colors, gray_array = process_image(
        image, char_arrays, dithering_strategy, edge_detection
    )

    for i, display_format in enumerate(display_formats):
        if display_format.value == DisplayFormats.BLACK_AND_WHITE.value:
            for row in grids[i]:
                print("".join(row))

    return create_ascii_image(grids, image_colors, gray_array, display_formats)


def run(
    image_path: Path,
    height: int,
    dithering_strategy: DitheringStrategy | None,
    display_formats: list[DisplayFormats],
    edge_detection: bool = False,
) -> None:
    image_name: str = image_path.stem
    image = cv2.cvtColor(cv2.imread(str(image_path)), cv2.COLOR_BGR2RGB)
    rescaled_image: npt.NDArray[np.uint8] = rescale_image(image, height)
    new_height, new_width = rescaled_image.shape[:2]

    ascii_dicts: list[AsciiDict] = [
        (
            display_format.value.HighAsciiDict
            if new_width * new_height
            >= (1600 // Font.Width.value) * (900 // Font.Height.value)
            else display_format.value.LowAsciiDict
        )
        for display_format in display_formats
    ]

    char_arrays: list[npt.NDArray[np.str_]] = [
        create_char_array(ascii_dict) for ascii_dict in ascii_dicts
    ]

    ascii_images: list[ImageSurface] = ascii_convert(
        rescaled_image, char_arrays, dithering_strategy, display_formats, edge_detection
    )
    for ascii_image, display_format in zip(ascii_images, display_formats):
        surface_format = ascii_image.get_format()
        if surface_format == FORMAT_ARGB32:
            cairo_data_bgra: npt.NDArray[np.uint8] = np.ndarray(
                shape=(ascii_image.get_height(), ascii_image.get_width(), 4),
                dtype=np.uint8,
                buffer=ascii_image.get_data(),
                strides=(ascii_image.get_stride(), 4, 1),
            )
            image_bgr = cv2.cvtColor(cairo_data_bgra, cv2.COLOR_BGRA2BGR)
        elif surface_format == FORMAT_RGB24:
            cairo_data_bgrx: npt.NDArray[np.uint8] = np.ndarray(
                shape=(ascii_image.get_height(), ascii_image.get_width(), 4),
                dtype=np.uint8,
                buffer=ascii_image.get_data(),
                strides=(ascii_image.get_stride(), 4, 1),
            )
            image_bgr = cairo_data_bgrx[:, :, :3]
        else:
            print(f"Error: Unsupported Cairo surface format {surface_format}")
            return
        cv2.imwrite(
            f"{image_name}_ascii_{display_format.name}.jpg",
            image_bgr,
            [cv2.IMWRITE_JPEG_QUALITY, 90],
        )
