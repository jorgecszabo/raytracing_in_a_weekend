import math
from screen import display_on_screen, save_as_png
from hittable import HittableList
from sphere import Sphere
from camera import Camera
from vec3 import Vec3
from material import Lambertian, Metal
import time
import numpy as np

def sierpinski_triangle(center, radius, depth):
    if depth == 0:
        return [(center, radius)]

    spheres = [(center, radius)]

    directions = [
        np.array([1, 1, 1]),
        np.array([1, -1, -1]),
        np.array([-1, 1, -1]),
        np.array([-1, -1, 1])
    ]

    directions = [point / np.linalg.norm(point) * radius for point in directions]

    for direction in directions:
        new_center = center + direction
        spheres.extend(sierpinski_triangle(new_center, radius / 2, depth - 1))

    return spheres

def generate_spiral_points_on_sphere(center, radius, num_points):
    points = []
    phi = np.pi * (3.0 - np.sqrt(5.0))

    for i in range(num_points):
        y = 1 - (i / float(num_points - 1)) * 2
        radius_at_y = np.sqrt(1 - y ** 2)
        theta = phi * i
        x = radius_at_y * np.cos(theta)
        z = radius_at_y * np.sin(theta)
        points.append(Vec3([radius * x, radius * y, radius * z]) + center)

    return points

def assign_material():
    choose_mat = np.random.rand()
    base = Vec3.random()
    pastel = (base + 1)*2 / 3
    if choose_mat < 0.5:
        material_lambertian = Lambertian(pastel)
        return material_lambertian
    else:
        material_metal = Metal(pastel)
        return material_metal


def main():
    #ground
    world = HittableList()
    material_ground = Lambertian(Vec3([0.95, 0.95, 0.95]))
    world.add(Sphere(Vec3([0.0, -1000, -1.0]), 1000.0, material_ground))

    #Big sphere with smaller spheres around it
    center = Vec3([0.0, 1.2, 1.9])
    world.add(Sphere(center, 0.5, Metal(Vec3([0.8, 0.81, 0.8]))))
    points = generate_spiral_points_on_sphere(center, 1.0, 30)
    for point in points:
        material = assign_material()
        world.add(Sphere(point, 0.2, material))

    # sierpinski pyramid out of spheres
    center = Vec3([4.8, 1.0, 0.0])
    spheres = sierpinski_triangle(center, 1.0, 4)

    for sphere in spheres:
        # material = assign_material()
        material = Metal(Vec3([0.96, 0.93, 0.97]))
        world.add(Sphere(Vec3(sphere[0]), sphere[1], material))

    #small spheres on the ground
    p1 = Vec3([0.0, 1.2, 1.9])
    p2 = Vec3([4.8, 1.0, 0.0])
    r1 = 1.4
    r2 = 1.1

    for a in range(-11, 11, 1):
        for b in range(-11, 11, 1):
            mat = assign_material()
            radius = np.random.uniform(0.1, 0.3)
            center = Vec3([
                a + 0.9 * np.random.rand(),
                radius,
                b + 0.9 * np.random.rand()
            ])

            dist_p1 = np.linalg.norm(center - p1)
            dist_p2 = np.linalg.norm(center - p2)

            if dist_p1 < r1 or dist_p2 < r2:
                continue

            world.add(Sphere(center, radius, mat))

    camera = Camera(
        image_width=150,
        aspect_ratio=16.0 / 9.0,
        samples_per_pixel=10,
        max_depth=5,

        vfov=22,
        lookfrom=Vec3([13.0,2.0,3.0]),
        lookat=Vec3([0,0.35,-0.25]),
        vup=Vec3([0.0,1.0,0.0]),

        defocus_angle=0.8,
        focus_dist=10.0
    )

    t0 = time.monotonic()
    image = camera.render(world)
    t1 = time.monotonic()
    print(f"Render took: {t1-t0:.3f} (s)")

    save_as_png(image)
    display_on_screen(image)

if __name__ == '__main__':
    main()

