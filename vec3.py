import numpy as np

class Vec3(np.ndarray):
    def __new__(cls, input_array, *args, **kwargs):
        obj = np.asarray(input_array).view(cls)
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
    def __reduce__(self):
        pickled_state = super().__reduce__()
        return pickled_state

    def as_unit_vector(self):
        return self / np.linalg.norm(self)

    def random_on_hemisphere(self):
        on_unit_sphere = self.__class__.random_unit_vector()
        if np.dot(on_unit_sphere, self) > 0.0:
            return on_unit_sphere
        else:
            return -on_unit_sphere

    def near_zero(self):
        return np.all(self < 1e-8)

    def reflect(self, n):
        return self - 2 * np.dot(self, n) * n

    def refract(self, n, etai_over_etat):
        cos_theta = min(np.dot(-self, n), 1.0)
        r_out_prep = etai_over_etat * (self + cos_theta * n)
        r_out_parallel = -np.sqrt(abs(1.0 - (r_out_prep @ r_out_prep))) * n
        return r_out_prep + r_out_parallel

    @classmethod
    def random_in_unit_disk(cls):
        while True:
            p = Vec3([np.random.uniform(-1, 1), np.random.uniform(-1, 1), 0])
            if np.linalg.norm(p) < 1:
                return p

    @classmethod
    def random(cls, min=0, max=1):
        return cls(np.random.uniform(min, max, (3,)))
    @classmethod
    def random_unit_vector(cls):
        while True:
            p = cls.random()
            lensq = p @ p
            if 1e-160 < lensq <= 1:
                return p / np.sqrt(lensq)
