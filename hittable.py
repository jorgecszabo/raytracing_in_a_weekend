from abc import ABC, abstractmethod

class HitRecord:
    def __init__(self):
        self.point, self.normal, self.t, self.front_face = None, None, None, None

    def set_face_normal(self, ray, outward_normal):
        # NOTE: the parameter `outward_normal` is assumed to have unit length.
        self.front_face = ray.direction @ outward_normal < 0
        self.normal = outward_normal if self.front_face else -outward_normal

class Hittable(ABC):

    @abstractmethod
    def hit(self, ray, ray_tmin, ray_tmax, hit_record):
        pass
