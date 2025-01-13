import numpy as np

AsciiDictEdges = np.array(list("|_/\\"))


def map_angle_to_ascii(angle: float) -> int:
    if -22.5 <= angle < 22.5 or 157.5 <= angle <= 180 or -180 <= angle < -157.5:
        return 0
    elif 67.5 <= angle < 112.5 or -112.5 <= angle < -67.5:
        return 1
    elif 22.5 <= angle < 67.5 or -157.5 <= angle < -112.5:
        return 2
    elif 112.5 <= angle < 157.5 or -67.5 <= angle < -22.5:
        return 3
    else:
        return -1  # No edge
