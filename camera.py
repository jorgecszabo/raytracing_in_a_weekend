import math

import numpy as np
from hittable import HitRecord
from interval import Interval
from hittable import HittableList
from sphere import Sphere
from ray import Ray
from color import write_color
from vec3 import Vec3
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count

unit_vector = lambda v: v / np.linalg.norm(v)


class Camera:
    def __init__(self,
                 image_width=100,
                 aspect_ratio=1.0,
                 samples_per_pixel=10,
                 max_depth=10, vfov=90,
                 lookfrom=Vec3([0, 0, 0]),
                 lookat=Vec3([0, 0, -1]),
                 vup=Vec3([0, 1, 0]),
                 defocus_angle=0,
                 focus_dist=10):
        self._aspect_ratio = aspect_ratio
        self._image_width = image_width
        self._samples_per_pixel = samples_per_pixel
        self._max_depth = max_depth
        self._image_height = None
        self._center = None
        self._pixel00_loc = None
        self._pixel_delta_u = None
        self._pixel_delta_v = None
        self._pixel_samples_scale = None
        self._vfov = vfov
        self._lookfrom = lookfrom
        self._lookat = lookat
        self._vup = vup
        self._u = None
        self._v = None
        self._w = None
        self._defocus_angle = defocus_angle
        self._focus_dist = focus_dist
        self._defocus_disk_u = None
        self._defocus_disk_v = None

    def _process_row(self, j, world):
        pixel_color = np.zeros((self._image_width, 3))
        for i in range(self._image_width):
            for sample in range(self._samples_per_pixel):
                ray = self._get_ray(i, j)
                pixel_color[i] += self._ray_color(ray, self._max_depth, world)
        pixel_color *= self._pixel_samples_scale
        pixel_color = write_color(pixel_color)
        return j, pixel_color

    def render(self, world, max_workers=cpu_count()):
        self._initialize()
        image = np.zeros((self._image_width, self._image_height, 3))

        total_rows = self._image_height
        num_done = 0
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self._process_row, j, world) for j in range(total_rows)]

            for future in futures:
                j, row_colors = future.result()
                image[:, j] = row_colors
                num_done += 1

                print(f"{num_done}/{total_rows} rows processed (%{int(num_done / total_rows * 100)})")

        # for j in range(self._image_height):
        #     print(f"%{j/self._image_height*100}")
        #     for i in range(self._image_width):
        #         pixel_color = np.zeros(3)
        #         for sample in range(self._samples_per_pixel):
        #             ray = self._get_ray(i, j)
        #             pixel_color += self._ray_color(ray, self._max_depth, world)
        #         pixel_color *= self._pixel_samples_scale
        #         image[i, j] = write_color(pixel_color)

        return image

    def _get_ray(self, i, j):
        offset = Vec3([np.random.rand() - 0.5, np.random.rand() - 0.5, 0.0])
        pixel_sample = (
                self._pixel00_loc +
                ((i + offset[0]) * self._pixel_delta_u) +
                ((j + offset[1]) * self._pixel_delta_v)
        )

        ray_origin = self._center if self._defocus_angle <= 0 else self._defocus_disk_sample()

        ray_direction = pixel_sample - ray_origin
        return Ray(ray_origin, ray_direction)

    def _defocus_disk_sample(self):
        p = Vec3.random_in_unit_disk()
        return self._center + (p[0] * self._defocus_disk_u) + (p[1] * self._defocus_disk_v)

    def _initialize(self):
        self._image_height = int(self._image_width / self._aspect_ratio)
        self._image_height = 1 if self._image_height < 1 else self._image_height

        self._pixel_samples_scale = 1.0 / self._samples_per_pixel

        self._center = self._lookfrom

        theta = np.deg2rad(self._vfov)
        h = math.tan(theta / 2)
        viewport_height = 2 * h * self._focus_dist
        viewport_width = viewport_height * (self._image_width / self._image_height)

        self._w = Vec3.as_unit_vector(self._lookfrom - self._lookat)
        self._u = Vec3.as_unit_vector(np.cross(self._vup, self._w))
        self._v = np.cross(self._w, self._u)

        viewport_u = viewport_width * self._u
        viewport_v = viewport_height * (-self._v)

        self._pixel_delta_u = viewport_u / self._image_width
        self._pixel_delta_v = viewport_v / self._image_height

        viewport_upper_left = (
                self._center -
                (self._focus_dist * self._w) -
                viewport_u / 2 -
                viewport_v / 2
        )

        self._pixel00_loc = viewport_upper_left + 0.5 * (self._pixel_delta_u + self._pixel_delta_v)

        defocus_radius = self._focus_dist * math.tan(np.deg2rad(self._defocus_angle / 2))
        self._defocus_disk_u = self._u * defocus_radius
        self._defocus_disk_v = self._v * defocus_radius

    def _ray_color(self, ray, depth, world):
        if depth <= 0:
            return Vec3([0, 0, 0])
        hit_record = HitRecord()
        hit_anything, hit_record = world.hit(ray, Interval(0.001, np.inf), hit_record)
        if hit_anything:
            did_scatter, attenuation, scattered = hit_record.material.scatter(ray, hit_record)
            if did_scatter:
                return attenuation * self._ray_color(scattered, depth - 1, world)
            else:
                Vec3([0.0, 0.0, 0.0])
        else:
            unit_direction = unit_vector(ray.direction)
            a = 0.5 * (unit_direction[1] + 1.0)
            return (1.0 - a) * Vec3([1.0, 1.0, 1.0]) + a * Vec3([0.5, 0.7, 1.0])
