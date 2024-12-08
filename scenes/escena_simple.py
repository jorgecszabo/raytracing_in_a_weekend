from camera import Camera
from hittable import HittableList
from material import Lambertian, Metal, Dielectric
from sphere import Sphere
from vec3 import Vec3

def escena_simple():
    material_ground = Lambertian(Vec3([0.1, 0.1, 0.1]))
    material_lambertian = Lambertian(Vec3([0.1, 0.2, 0.5]))
    material_metal_low_fuzz = Metal(Vec3([0.7, 0.6, 0.5]), 0.1)
    material_dielectric = Dielectric(1.5)

    world = HittableList()
    world.add(Sphere(Vec3([0.0, -100.5, -1.0]), 100.0, material_ground))
    world.add(Sphere(Vec3([0.0, 0.0, -1.2]), 0.5, material_lambertian))
    world.add(Sphere(Vec3([-1.0, 0.0, -1.0]), 0.5, material_metal_low_fuzz))
    world.add(Sphere(Vec3([1.0, 0.0, -1.0]), 0.5, material_dielectric))
    world.add(Sphere(Vec3([0.0, 3.14, -2.25]), 2.4, material_metal_low_fuzz))

    camera = Camera(
        image_width=400,
        aspect_ratio=16.0 / 9.0,
        samples_per_pixel=50,
        max_depth=10,
        lookfrom=Vec3([0.0, 0.25, 0.25]),
        vfov=85,

    )
    return camera, world
