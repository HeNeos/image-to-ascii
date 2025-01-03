from dataclasses import dataclass
import numpy as np
import numpy.typing as npt
from numba import njit

from . import DitheringStrategy


@njit(
    "void(int64, int64, float64[:, :], int64, int64[:])",
    nogil=True,
    fastmath=True,
    cache=True,
)
def dither_pixel(
    cur_x: int,
    cur_y: int,
    img: npt.NDArray[np.float64],
    img_width: int,
    weights: npt.NDArray[np.int64],
) -> None:
    SIZE = len(weights)
    error = np.zeros(SIZE, dtype=np.float64)
    pixel_value = img[cur_y, cur_x]
    err_sum = 0.0
    for i in range(SIZE):
        err_sum += error[i] * weights[i]
    quantized_value = min(max(pixel_value + err_sum / weights[-1], 0.0), 255.0)
    quantized_value = 255.0 if quantized_value >= 128.0 else 0.0
    new_error = pixel_value - quantized_value
    img[cur_y, cur_x] = quantized_value
    for i in range(SIZE - 1):
        error[i] = error[i + 1]
    error[SIZE - 1] = new_error


@njit(
    "void(int64, int64, float64[:, :], int64, int64, int64[:], int64[:], int64[:])",
    nogil=True,
    fastmath=True,
    cache=True,
)
def move_and_dither(
    cur_x: int,
    cur_y: int,
    img: npt.NDArray[np.float64],
    img_width: int,
    img_height: int,
    weights: npt.NDArray[np.int64],
    pos: npt.NDArray[np.int64],
    direction: npt.NDArray[np.int64],
) -> None:
    if 0 <= pos[0] < img_width and 0 <= pos[1] < img_height:
        dither_pixel(pos[0], pos[1], img, img_width, weights)

    if direction[0] == 1:
        pos[0] += 1
    elif direction[0] == 2:
        pos[1] -= 1
    elif direction[0] == 3:
        pos[0] -= 1
    elif direction[0] == 4:
        pos[1] += 1


@njit(
    "void(int64, int64, float64[:, :], int64, int64, int64[:], int64[:], int64[:])",
    nogil=True,
    fastmath=True,
    cache=True,
)
def hilbert_level_1(
    level: int,
    direction: int,
    img: npt.NDArray[np.float64],
    img_width: int,
    img_height: int,
    weights: npt.NDArray[np.int64],
    pos: npt.NDArray[np.int64],
    dir_array: npt.NDArray[np.int64],
) -> None:
    if direction == 1:
        dir_array[0] = 3
        move_and_dither(0, 0, img, img_width, img_height, weights, pos, dir_array)
        dir_array[0] = 2
        move_and_dither(0, 0, img, img_width, img_height, weights, pos, dir_array)
        dir_array[0] = 1
        move_and_dither(0, 0, img, img_width, img_height, weights, pos, dir_array)
    elif direction == 2:
        dir_array[0] = 4
        move_and_dither(0, 0, img, img_width, img_height, weights, pos, dir_array)
        dir_array[0] = 1
        move_and_dither(0, 0, img, img_width, img_height, weights, pos, dir_array)
        dir_array[0] = 2
        move_and_dither(0, 0, img, img_width, img_height, weights, pos, dir_array)
    elif direction == 3:
        dir_array[0] = 1
        move_and_dither(0, 0, img, img_width, img_height, weights, pos, dir_array)
        dir_array[0] = 4
        move_and_dither(0, 0, img, img_width, img_height, weights, pos, dir_array)
        dir_array[0] = 3
        move_and_dither(0, 0, img, img_width, img_height, weights, pos, dir_array)
    elif direction == 4:
        dir_array[0] = 2
        move_and_dither(0, 0, img, img_width, img_height, weights, pos, dir_array)
        dir_array[0] = 3
        move_and_dither(0, 0, img, img_width, img_height, weights, pos, dir_array)
        dir_array[0] = 4
        move_and_dither(0, 0, img, img_width, img_height, weights, pos, dir_array)


@njit(
    "void(int64, int64, float64[:, :], int64, int64, int64[:], int64[:], int64[:])",
    nogil=True,
    fastmath=True,
    # cache=True,
)
def hilbert_level(
    level: int,
    direction: int,
    img: npt.NDArray[np.float64],
    img_width: int,
    img_height: int,
    weights: npt.NDArray[np.int64],
    pos: npt.NDArray[np.int64],
    dir_array: npt.NDArray[np.int64],
) -> None:
    if level == 1:
        hilbert_level_1(
            level, direction, img, img_width, img_height, weights, pos, dir_array
        )
    else:
        if direction == 1:
            hilbert_level(
                level - 1, 4, img, img_width, img_height, weights, pos, dir_array
            )
            dir_array[0] = 3
            move_and_dither(0, 0, img, img_width, img_height, weights, pos, dir_array)
            hilbert_level(
                level - 1, 1, img, img_width, img_height, weights, pos, dir_array
            )
            dir_array[0] = 2
            move_and_dither(0, 0, img, img_width, img_height, weights, pos, dir_array)
            hilbert_level(
                level - 1, 1, img, img_width, img_height, weights, pos, dir_array
            )
            dir_array[0] = 1
            move_and_dither(0, 0, img, img_width, img_height, weights, pos, dir_array)
            hilbert_level(
                level - 1, 2, img, img_width, img_height, weights, pos, dir_array
            )


@dataclass
class DitheringRiemersma(DitheringStrategy):
    name = "riemersma"

    @staticmethod
    @njit(
        "float64[:, :](float64[:, :], int64)",
        nogil=True,
        fastmath=True,
        cache=True,
    )
    def dithering(
        image_array: npt.NDArray[np.float64], quantization_levels: int
    ) -> npt.NDArray[np.float64]:
        height: int = image_array.shape[0]
        width: int = image_array.shape[1]

        SIZE = quantization_levels
        MAX = quantization_levels
        weights = np.zeros(SIZE, dtype=np.int64)
        multiplier = np.exp(np.log(float(MAX)) / float(SIZE - 1))
        val = 1.0
        for i in range(SIZE):
            weights[i] = int(val + 0.5)
            val *= multiplier

        largest_side = max(width, height)
        level = int(np.ceil(np.log2(float(largest_side))))

        pos = np.zeros(2, dtype=np.int64)  # [x, y]
        dir_array = np.zeros(1, dtype=np.int64)  # Current direction

        hilbert_level(level, 2, image_array, width, height, weights, pos, dir_array)

        return np.clip(image_array, 0.0, 255.0)
