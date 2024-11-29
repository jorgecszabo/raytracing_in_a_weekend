import numpy as np
from color import write_color
from ray import Ray, ray_color
from screen import display_on_screen


def main():
    aspect_ratio = 16 / 9
    image_width = 600

    image_height = int(image_width / aspect_ratio)
    image_height = 1 if image_height < 1 else image_height

    focal_length = 1
    viewport_height = 2
    viewport_width = viewport_height * (image_width / image_height)
    camera_center = np.array([0,0,0], np.double)

    viewport_u = np.array([viewport_width, 0, 0], np.double)
    viewport_v = np.array([0, -viewport_height, 0], np.double)

    pixel_delta_u = viewport_u / image_width
    pixel_delta_v = viewport_v / image_height

    viewport_upper_left = (
            camera_center -
            np.array([0, 0, focal_length], np.double) -
            viewport_u / 2 -
            viewport_v / 2
    )

    pixel00_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v)

    image = np.zeros((image_width, image_height, 3))

    for j in range(image_height):
        for i in range(image_width):
            pixel_center = pixel00_loc + (i * pixel_delta_u) + (j * pixel_delta_v)
            ray_direction = pixel_center - camera_center
            ray = Ray(camera_center, ray_direction)
            image[i, j] = write_color(ray_color(ray))

    display_on_screen(image)

if __name__ == '__main__':
    main()

