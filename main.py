from scenes.escena_simple import escena_simple
from scenes.escena_caratula import escena_caratula
from screen import save_as_png, display_on_screen
import time
import numpy as np
import argparse

np.random.seed(sum(map(ord, "Como me gusta la computación gráfica")))


def main():
    parser = argparse.ArgumentParser(description="Seleccionar escena para renderizar. La escena simple tarda unos ")
    parser.add_argument(
        "--scene",
        choices=["escena_simple", "escena_caratula"],
        required=True,
        help="Seleccioná una escena para renderizar: escena_simple or escena_caratula.",
    )
    parser.add_argument(
        "--max-cpus",
        type=int,
        required=False,
        help="Seleccioná una escena para renderizar: escena_simple or escena_caratula.",
    )
    args = parser.parse_args()

    if args.scene == "escena_caratula":
        camera, world = escena_caratula()
    else:
        camera, world = escena_simple()

    t0 = time.monotonic()
    if args.max_cpus:
        image = camera.render(world, args.max_cpus)
    else:
        image = camera.render(world)
    t1 = time.monotonic()
    print(f"Render took: {t1-t0:.3f} (s)")

    save_as_png(image)
    display_on_screen(image)


if __name__ == '__main__':
    main()

