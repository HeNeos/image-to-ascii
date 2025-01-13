from dataclasses import dataclass
import numpy.typing as npt
import numpy as np


@dataclass
class EdgeDetection:
    canny_array: npt.NDArray[np.float64] | None = None
    angles: npt.NDArray[np.float64] | None = None
    magnitudes: npt.NDArray[np.float64] | None = None

    def apply_canny(self, img_array: npt.NDArray[np.uint8]) -> None:
        from cv2 import Canny

        self.canny_array = Canny(img_array, 100, 200).astype(np.float64)

    def apply_sobel(self, dog_array: npt.NDArray[np.float64]) -> None:
        from modules.edge_detection.sobel import sobel_filter

        self.angles, self.magnitudes = sobel_filter(dog_array)
