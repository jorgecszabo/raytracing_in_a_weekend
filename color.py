import numpy as np
from interval import Interval

_intensity = Interval(0.0, 0.999)

def write_color(pixel_color: np.ndarray) -> np.ndarray:
    pixel_color = np.nan_to_num(np.sqrt(pixel_color))
    return _intensity.clamp(pixel_color) * 256
