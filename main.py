import math
from screen import display_on_screen, save_as_png
from hittable import HittableList
from sphere import Sphere
from camera import Camera
from vec3 import Vec3
from material import Lambertian, Metal
import time
import numpy as np

def sierpinski_pyramid(center, radius, depth):
    # List to hold the spheres (center, radius)
    spheres = []

    # Base case: if depth is 0, stop recursion and return a single sphere
    if depth == 0:
        spheres.append((center, radius))
        return spheres

    # Add the current sphere at the given center and radius
    spheres.append((center, radius))

    # Calculate new radius for next spheres
    new_radius = radius / 2

    offset = radius
    # Directions for the 4 spheres around the current one
    directions = [
        [0, 0, offset],                    # Top
        [offset, offset, -offset],         # Bottom-right-front
        [-offset, offset, -offset],        # Bottom-left-front
        [0, -offset, -offset],             # Bottom-back
    ]

    # Create the 4 new spheres recursively
    for direction in directions:
        new_center = [center[0] + direction[0], center[1] + direction[1], center[2] + direction[2]]
        spheres.extend(sierpinski_pyramid(new_center, new_radius, depth - 1))

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
    # world = HittableList()
    # material_ground = Metal(Vec3([0.95, 0.95, 0.96]))
    # world.add(Sphere(Vec3([0.0, -1001.0, -1.0]), 1000.0, material_ground))

    #Big sphere with smaller spheres around it
    # center = Vec3([0.0, 0.0, -1.5])
    # world.add(Sphere(center, 0.8, Metal(Vec3([0.8, 0.81, 0.8]))))
    # points = generate_spiral_points_on_sphere(center, 0.95, 50)
    # for point in points:
    #     material = assign_material()
    #     world.add(Sphere(point, 0.1, material))

    # sierpinski pyramid out of spheres
    # center = Vec3([0.0, 1.0, -5.5])
    # spheres = sierpinski_pyramid(center, 2, 2)
    #
    # for sphere in spheres:
    #     material = assign_material()
    #     world.add(Sphere(Vec3(sphere[0]), sphere[1], material))

    #small spheres on the ground
    # for a in range(-8, 8, 1):
    #     for b in range(-8, 8, 1):
    #         mat = assign_material()
    #         center = Vec3([
    #             a + 0.9 * np.random.rand(),
    #             -1.0,
    #             b + 0.9 * np.random.rand()
    #         ])
    #         radius = np.random.uniform(0.1, 0.3)
    #         world.add(Sphere(center, radius, mat))


    material_ground = Lambertian(Vec3([0.8, 0.8, 0.0]))
    material_center = Lambertian(Vec3([0.1, 0.2, 0.5]))
    material_left = Metal(Vec3([0.9, 0.9, 0.9]))
    material_right = Metal(Vec3([0.8, 0.6, 0.2]))

    world = HittableList()
    world.add(Sphere(Vec3([0.0, -100.5, -1.0]), 100.0, material_ground))
    world.add(Sphere(Vec3([0.0, 0.0, -1.2]), 0.5, material_center))
    world.add(Sphere(Vec3([-1.0, 0.0, -1.0]), 0.5, material_left))
    world.add(Sphere(Vec3([1.0, 0.0, -1.0]), 0.5, material_right))

    camera = Camera(
        image_width=300,
        aspect_ratio=16.0 / 9.0,
        # aspect_ratio=4.0 / 3.0,
        samples_per_pixel=10,
        max_depth=10,

        vfov=20,
        lookfrom=Vec3([-2.0,2.0,1.0]),
        lookat=Vec3([0,0.0,-1.0]),
        vup=Vec3([0.0,1.0,0.0]),

        defocus_angle=10.0,
        focus_dist=3.4
    )

    t0 = time.monotonic()
    image = camera.render(world)
    t1 = time.monotonic()
    print(f"Render took: {t1-t0:.3f} (s)")

    save_as_png(image)
    display_on_screen(image)

if __name__ == '__main__':
    main()

