import numpy as np
from hittable import HitRecord
from interval import Interval
from hittable import HittableList
from sphere import Sphere
from ray import Ray
from color import write_color
from vec3 import Vec3


unit_vector = lambda v: v / np.linalg.norm(v)

class Camera:
    def __init__(self, image_width=100, aspect_ratio=1.0, samples_per_pixel=10, max_depth=10):
        self._aspect_ratio = aspect_ratio
        self._image_width = image_width
        self._samples_per_pixel = samples_per_pixel
        self._max_depth = 10
        self._image_height = None
        self._center = None
        self._pixel00_loc = None
        self._pixel_delta_u = None
        self._pixel_delta_v = None
        self._pixel_samples_scale = None


    def render(self, world):
        self._initialize()
        image = np.zeros((self._image_width, self._image_height, 3))

        for j in range(self._image_height):
            for i in range(self._image_width):
                pixel_color = np.zeros(3)
                for sample in range(self._samples_per_pixel):
                    ray = self._get_ray(i, j)
                    pixel_color += self._ray_color(ray, self._max_depth, world)
                pixel_color *= self._pixel_samples_scale
                image[i, j] = write_color(pixel_color)

        return image


    def _get_ray(self, i, j):
        offset = Vec3([np.random.rand() - 0.5, np.random.rand() - 0.5, 0.0])
        pixel_sample = (
            self._pixel00_loc +
            ((i + offset[0]) * self._pixel_delta_u) +
            ((j + offset[1]) * self._pixel_delta_v)
        )
        ray_origin = self._center
        ray_direction = pixel_sample - ray_origin
        return Ray(ray_origin, ray_direction)

    def _initialize(self):
        self._image_height = int(self._image_width / self._aspect_ratio)
        self._image_height = 1 if self._image_height < 1 else self._image_height

        self._pixel_samples_scale = 1.0 / self._samples_per_pixel

        focal_length = 1
        viewport_height = 2
        viewport_width = viewport_height * (self._image_width / self._image_height)
        self._center = Vec3([0, 0, 0], np.double)

        viewport_u = Vec3([viewport_width, 0, 0], np.double)
        viewport_v = Vec3([0, -viewport_height, 0], np.double)

        self._pixel_delta_u = viewport_u / self._image_width
        self._pixel_delta_v = viewport_v / self._image_height

        viewport_upper_left = (
                self._center -
                Vec3([0, 0, focal_length], np.double) -
                viewport_u / 2 -
                viewport_v / 2
        )

        self._pixel00_loc = viewport_upper_left + 0.5 * (self._pixel_delta_u + self._pixel_delta_v)

    def _ray_color(self, ray, depth, world):
        if depth <= 0:
            return Vec3([0, 0, 0])
        hit_record = HitRecord()
        hit_anything, hit_record = world.hit(ray, Interval(0.001, np.inf), hit_record)
        if hit_anything:
            did_scatter, scattered, attenuation = hit_record.material.scatter(ray, hit_record)
            if did_scatter:
                return attenuation * self._ray_color(scattered, depth - 1, world)
            else:
                Vec3([0.0, 0.0, 0.0])
        else:
            unit_direction = unit_vector(ray.direction)
            a = 0.5 * (unit_direction[1] + 1.0)
            return (1.0 - a) * Vec3([1.0, 1.0, 1.0]) + a * Vec3([0.5, 0.7, 1.0])