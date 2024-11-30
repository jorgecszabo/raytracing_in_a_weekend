import numpy as np
from hittable import HitRecord
from interval import Interval
from hittable import HittableList
from sphere import Sphere
from ray import Ray
from color import write_color


unit_vector = lambda v: v / np.linalg.norm(v)

class Camera:
    def __init__(self, image_width=100, aspect_ratio=1.0):
        self._aspect_ratio = aspect_ratio
        self._image_width = image_width
        self._image_height = None
        self._center = None
        self._pixel00_loc = None
        self._pixel_delta_u = None
        self._pixel_delta_v = None


    def render(self, world):
        self._initialize()
        image = np.zeros((self._image_width, self._image_height, 3))

        for j in range(self._image_height):
            for i in range(self._image_width):
                pixel_center = self._pixel00_loc + (i * self._pixel_delta_u) + (j * self._pixel_delta_v)
                ray_direction = pixel_center - self._center
                ray = Ray(self._center, ray_direction)
                image[i, j] = write_color(self._ray_color(ray, world))

        return image


    def _initialize(self):
        self._image_height = int(self._image_width / self._aspect_ratio)
        self._image_height = 1 if self._image_height < 1 else self._image_height

        focal_length = 1
        viewport_height = 2
        viewport_width = viewport_height * (self._image_width / self._image_height)
        self._center = np.array([0, 0, 0], np.double)

        viewport_u = np.array([viewport_width, 0, 0], np.double)
        viewport_v = np.array([0, -viewport_height, 0], np.double)

        self._pixel_delta_u = viewport_u / self._image_width
        self._pixel_delta_v = viewport_v / self._image_height

        viewport_upper_left = (
                self._center -
                np.array([0, 0, focal_length], np.double) -
                viewport_u / 2 -
                viewport_v / 2
        )

        self._pixel00_loc = viewport_upper_left + 0.5 * (self._pixel_delta_u + self._pixel_delta_v)

    def _ray_color(self, ray, world):
        hit_record = HitRecord()
        hit_anything, hit_record = world.hit(ray, Interval(0, np.inf), hit_record)
        if hit_anything:
            return 0.5 * (hit_record.normal + np.array([1.0, 1.0, 1.0]))
        else:
            unit_direction = unit_vector(ray.direction)
            a = 0.5 * (unit_direction[1] + 1.0)
            return (1.0 - a) * np.array([1.0, 1.0, 1.0]) + a * np.array([0.5, 0.7, 1.0])