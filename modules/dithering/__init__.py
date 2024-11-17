from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt


@dataclass
class DitheringStrategy(ABC):
    @staticmethod
    @abstractmethod
    def dithering(
        image: npt.NDArray[np.float32], quantization_levels: int
    ) -> npt.NDArray[np.float32]:
        pass
