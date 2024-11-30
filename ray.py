import numpy as np
from vec3 import Vec3

class Ray:
    def __init__(self, origin: np.ndarray, direction: np.ndarray):
        self.origin = origin
        self.direction = direction

    def at(self, t: float) -> np.ndarray:
        return self.origin + t * self.direction


"""

def ray_color(ray, world):
    hit_record = HitRecord()
    hit_anything, hit_record = world.hit(ray, Interval(0, np.inf), hit_record)
    if hit_anything:
        return 0.5 * (hit_record.normal + Vec3([1.0, 1.0, 1.0]))
    else:
        unit_direction = unit_vector(ray.direction)
        a = 0.5 * (unit_direction[1] + 1.0)
        return (1.0 - a) * Vec3([1.0, 1.0, 1.0]) + a * Vec3([0.5, 0.7, 1.0])
"""
