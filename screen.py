import cv2
import numpy as np


def display_on_screen(image):
    image_uint8 = np.clip(image, 0, 255).astype(np.uint8)
    image_uint8 = cv2.cvtColor(image_uint8, cv2.COLOR_RGB2BGR)
    image_uint8 = cv2.rotate(image_uint8, cv2.ROTATE_90_CLOCKWISE)
    image_uint8 = cv2.flip(image_uint8, 1)
    cv2.imshow('image', image_uint8)
    cv2.waitKey(0)
