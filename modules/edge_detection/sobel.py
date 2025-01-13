import numpy as np
import numpy.typing as npt

from numba import njit
from cv2 import Sobel, CV_64F


@njit(fastmath=True, cache=True)
def calculate_magnitudes_and_angles(
    grad_x: npt.NDArray[np.float64],
    grad_y: npt.NDArray[np.float64],
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    magnitudes = np.sqrt(grad_x**2 + grad_y**2)
    max_value = np.max(magnitudes)
    if max_value > 0:
        magnitudes /= max_value
    angles = np.arctan2(grad_y, grad_x) * 180 / np.pi
    return angles, magnitudes


def sobel_filter(
    dog_array: npt.NDArray[np.float64],
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    grad_x = Sobel(dog_array, CV_64F, 1, 0, ksize=3)
    grad_y = Sobel(dog_array, CV_64F, 0, 1, ksize=3)

    angles, magnitudes = calculate_magnitudes_and_angles(grad_x, grad_y)

    return angles, magnitudes
