import cv2
import numpy as np
import os
import logging

logger = logging.getLogger(__name__)

def reformat_image_to_uint8(image):
    image_uint8 = np.clip(image, 0, 255).astype(np.uint8)
    image_uint8 = cv2.cvtColor(image_uint8, cv2.COLOR_RGB2BGR)
    image_uint8 = cv2.rotate(image_uint8, cv2.ROTATE_90_CLOCKWISE)
    image_uint8 = cv2.flip(image_uint8, 1)
    return image_uint8


def display_on_screen(image, in_place=False):
    if not in_place:
        image = image.copy()
    image_uint8 = reformat_image_to_uint8(image)
    cv2.imshow('image', image_uint8)
    cv2.waitKey(0)

def save_as_png(image, path=os.getcwd(), in_place=False):
    if not in_place:
        image = image.copy()
    image_uint8 = reformat_image_to_uint8(image)
    try:
        cv2.imwrite(os.path.join(path, 'output.png'), image_uint8)
    except Exception:
        logger.error(f"Can't write image to {path}. Saving to current working directory.")
        cv2.imwrite(os.path.join(os.getcwd(), 'output.png'), image_uint8)