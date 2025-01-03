from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from numba import jit

from . import DitheringStrategy


@dataclass
class DitheringJarvisJudiceNinke(DitheringStrategy):
    name = "jarvis_judice_ninke"

    @staticmethod
    @jit(
        "float64[:, :](float64[:, :], int64)",
        nopython=True,
        nogil=True,
        fastmath=True,
        cache=True,
    )
    def dithering(
        image_array: npt.NDArray[np.float64], quantization_levels: int
    ) -> npt.NDArray[np.float64]:
        height: int = image_array.shape[0]
        width: int = image_array.shape[1]

        scale: float = 255 / (quantization_levels - 1)

        for row in range(height):
            for column in range(width):
                old_pixel = image_array[row, column]
                new_pixel = np.round(old_pixel / scale) * scale
                image_array[row, column] = new_pixel
                error = new_pixel - old_pixel
                if column + 1 < width:
                    image_array[row, column + 1] += error * 7 / 48
                if column + 2 < width:
                    image_array[row, column + 2] += error * 5 / 48

                if row + 1 < height and column - 1 > 0:
                    image_array[row + 1, column - 2] += error * 3 / 48
                if row + 1 < height and column > 0:
                    image_array[row + 1, column - 1] += error * 5 / 48
                if row + 1 < height:
                    image_array[row + 1, column] += error * 7 / 48
                if row + 1 < height and column + 1 < width:
                    image_array[row + 1, column + 1] += error * 5 / 48
                if row + 1 < height and column + 2 < width:
                    image_array[row + 1, column + 2] += error * 3 / 48

                if row + 2 < height and column - 1 > 0:
                    image_array[row + 2, column - 2] += error * 1 / 48
                if row + 2 < height and column > 0:
                    image_array[row + 2, column - 1] += error * 3 / 48
                if row + 2 < height:
                    image_array[row + 2, column] += error * 5 / 48
                if row + 2 < height and column + 1 < width:
                    image_array[row + 2, column + 1] += error * 3 / 48
                if row + 2 < height and column + 2 < width:
                    image_array[row + 2, column + 2] += error * 1 / 48

        image_array = np.clip(image_array, 0.0, 255.0)

        return image_array
