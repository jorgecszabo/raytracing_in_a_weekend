from screen import display_on_screen, save_as_png
from hittable import HittableList
from sphere import Sphere
from camera import Camera
from vec3 import Vec3
from material import Lambertian, Metal
import time

def main():


    material_ground = Lambertian(Vec3([0.8, 0.8, 0.0]))
    material_center = Lambertian(Vec3([0.1, 0.2, 0.5]))
    material_left = Metal(Vec3([0.8, 0.8, 0.8]))
    material_right = Metal(Vec3([0.8, 0.6, 0.2]))

    world = HittableList()
    world.add(Sphere(Vec3([0.0, -100.5, -1.0]), 100.0, material_ground))
    world.add(Sphere(Vec3([0.0, 0.0, -1.2]), 0.5, material_center))
    world.add(Sphere(Vec3([-1.0, 0.0, -1.0]), 0.5, material_left))
    world.add(Sphere(Vec3([1.0, 0.0, -1.0]), 0.5, material_right))

    camera = Camera(
        image_width=400,
        aspect_ratio=16.0 / 9.0,
        samples_per_pixel=10,
        max_depth=50
    )

    t0 = time.monotonic()
    image = camera.render(world)
    t1 = time.monotonic()
    print(f"Render took: {t1-t0:.3f} (s)")

    save_as_png(image)
    display_on_screen(image)

if __name__ == '__main__':
    main()

