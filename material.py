from abc import ABC, abstractmethod
from vec3 import Vec3
from ray import Ray
import numpy as np
import math

class Material(ABC):
    @abstractmethod
    def scatter(self, hit_ray, hit_record):
        return False, None, None

class Lambertian(Material):
    def __init__(self, albedo):
        self._albedo = albedo

    def scatter(self, hit_ray, hit_record):
        scatter_direction = hit_record.normal + Vec3.random_unit_vector()

        if scatter_direction.near_zero():
            scatter_direction = hit_record.normal

        scattered_ray = Ray(hit_record.point, scatter_direction)
        attenuation = self._albedo
        return True, attenuation, scattered_ray

class Metal(Material):
    def __init__(self, albedo, fuzz):
        self._albedo = albedo
        self._fuzz = fuzz

    def scatter(self, hit_ray, hit_record):
        reflected = hit_ray.direction.reflect(hit_record.normal)
        reflected = reflected.as_unit_vector() + (self._fuzz * Vec3.random_unit_vector())
        scattered_ray = Ray(hit_record.point, reflected)
        attenuation = self._albedo
        did_scatter = np.dot(scattered_ray.direction, hit_record.normal) > 0
        return did_scatter, attenuation, scattered_ray

class Dielectric(Material):
    def __init__(self, refraction_index):
        self._refraction_index = refraction_index

    def scatter(self, hit_ray, hit_record):
        attenuation = Vec3([1.0, 1.0, 1.0])
        refraction_index = (1.0 / self._refraction_index) if hit_record.front_face else self._refraction_index

        unit_direction = hit_ray.direction.as_unit_vector()
        cos_theta = min(np.dot(-unit_direction, hit_record.normal), 1.0)
        sin_theta = np.sqrt(1.0 - cos_theta * cos_theta)

        cannot_refract = refraction_index * sin_theta > 1.0
        if cannot_refract or self._reflectance(cos_theta, refraction_index) > np.random.random():
            direction = unit_direction.reflect(hit_record.normal)
        else:
            direction = unit_direction.refract(hit_record.normal, refraction_index)
        scattered_ray = Ray(hit_record.point, direction)
        return True, attenuation, scattered_ray

    def _reflectance(self, cosine, refraction_index):
        r0 = (1 - refraction_index) / (1 + refraction_index)
        r0 = r0 * r0
        return r0 + (1 - r0) * pow((1 - cosine), 5)