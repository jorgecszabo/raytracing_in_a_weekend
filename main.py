import numpy as np
from screen import display_on_screen, save_as_png
from hittable import HittableList
from sphere import Sphere
from camera import Camera
from vec3 import Vec3
import time

def main():
    world = HittableList()
    world.add(Sphere(Vec3([0.0, 0.0, -1.0]), 0.5))
    world.add(Sphere(Vec3([0.0, -100.5, -1.0]), 100))

    camera = Camera(
        image_width=400,
        aspect_ratio=16.0 / 9.0,
        samples_per_pixel=15,
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

