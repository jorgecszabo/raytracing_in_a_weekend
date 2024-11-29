import numpy as np
from sphere import DoesNotHitSpere, hit_sphere

class Ray:
    def __init__(self, origin: np.ndarray, direction: np.ndarray):
        self.origin = origin
        self.direction = direction

    def at(self, t: float) -> np.ndarray:
        return self.origin + t * self.direction


unit_vector = lambda v: v / np.linalg.norm(v)


def ray_color(ray):
    try:
        t = hit_sphere(np.array([0.0, 0.0, -1.0]), 0.5, ray)
        N = unit_vector(ray.at(t) - np.array([0.0, 0.0, -1.0]))
        return 0.5 * (N + 1)
    except DoesNotHitSpere:
        unit_direction = unit_vector(ray.direction)
        a = 0.5 * (unit_direction[1] + 1)
        return (1 - a) * np.array([1.0, 1.0, 1.0]) + a * np.array([0.5, 0.7, 1.0])

