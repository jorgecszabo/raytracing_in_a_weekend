import numpy as np
from vec3 import Vec3

class Ray:
    def __init__(self, origin: np.ndarray, direction: np.ndarray):
        self.origin = origin
        self.direction = direction

    def at(self, t: float) -> np.ndarray:
        return self.origin + t * self.direction
