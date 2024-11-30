from abc import ABC, abstractmethod
from vec3 import Vec3
from ray import Ray

class Material(ABC):
    def __init__(self, albedo):
        self._albedo = albedo

    @abstractmethod
    def scatter(self, hit_ray, hit_record):
        return False, None, None

class Lambertian(Material):

    def scatter(self, hit_ray, hit_record):
        scatter_direction = hit_record.normal + Vec3.random_unit_vector()

        if scatter_direction.near_zero():
            scatter_direction = hit_record.normal

        scattered_ray = Ray(hit_record.point, scatter_direction)
        attenuation = self._albedo
        return True, attenuation, scattered_ray

class Metal(Material):
    def scatter(self, hit_ray, hit_record):
        reflected = hit_ray.direction.reflect(hit_record.normal)

        scattered_ray = Ray(hit_record.point, reflected)
        attenuation = self._albedo
        return True, attenuation, scattered_ray