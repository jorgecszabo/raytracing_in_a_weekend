from screen import display_on_screen, save_as_png
from hittable import HittableList
from sphere import Sphere
from camera import Camera
from vec3 import Vec3
from material import Lambertian, Metal
import time
import numpy as np

def generate_spiral_points_on_sphere(radius, num_points):
    points = []
    phi = np.pi * (3.0 - np.sqrt(5.0))

    for i in range(num_points):
        y = 1 - (i / float(num_points - 1)) * 2
        radius_at_y = np.sqrt(1 - y ** 2)
        theta = phi * i
        x = radius_at_y * np.cos(theta)
        z = radius_at_y * np.sin(theta)
        points.append(Vec3([radius * x, radius * y, radius * z]) + Vec3([0.0, 0.0, -1.5]))

    return points

def assign_material():
    choose_mat = np.random.rand()
    base = Vec3.random()
    pastel = (base + 1)*2 / 3
    if choose_mat < 0.8:
        material_lambertian = Lambertian(pastel)
        return material_lambertian
    else:
        material_metal = Metal(pastel)
        return material_metal


def main():
    # material_ground = Lambertian(Vec3([0.8, 0.8, 0.0]))
    # material_center = Lambertian(Vec3([0.1, 0.2, 0.5]))
    # material_left = Metal(Vec3([0.8, 0.8, 0.8]))
    # material_right = Metal(Vec3([0.8, 0.6, 0.2]))
    #
    # world = HittableList()
    # world.add(Sphere(Vec3([0.0, -100.5, -1.0]), 100.0, material_ground))
    # world.add(Sphere(Vec3([0.0, 0.0, -1.2]), 0.5, material_center))
    # world.add(Sphere(Vec3([-1.0, 0.0, -1.0]), 0.5, material_left))
    # world.add(Sphere(Vec3([1.0, 0.0, -1.0]), 0.5, material_right))

    world = HittableList()
    material_ground = Metal(Vec3([0.95, 0.95, 0.96]))
    world.add(Sphere(Vec3([0.0, -1001, -1.0]), 1000.0, material_ground))

    world.add(Sphere(Vec3([0.0, 0.0, -1.5]), 0.8, Metal(Vec3([0.8, 0.81, 0.8]))))
    points = generate_spiral_points_on_sphere(0.95, 50)
    for point in points:
        material = assign_material()
        world.add(Sphere(point, 0.1, material))

    camera = Camera(
        image_width=400,
        # aspect_ratio=16.0 / 9.0,
        aspect_ratio=4.0 / 3.0,
        samples_per_pixel=15,
        max_depth=100
    )

    t0 = time.monotonic()
    image = camera.render(world)
    t1 = time.monotonic()
    print(f"Render took: {t1-t0:.3f} (s)")

    save_as_png(image)
    display_on_screen(image)

if __name__ == '__main__':
    main()

