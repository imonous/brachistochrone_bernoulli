import numpy as np
import math

import matplotlib as mpl
import matplotlib.pyplot as plt

from sys import float_info


GRAV_ACC = 9.8067


def part_v(y, g=GRAV_ACC):
    return (2 * g * y) ** 0.5


def trace_light(init_angle, height, parts):
    travelled = float_info.min
    x, y = 0, height
    angle = init_angle
    v, v_old = 0, 0

    for iter in range(parts):
        yield x, y
        v = part_v(travelled)

        if iter != 0:
            w = v / v_old * math.sin(angle)
            w = w % 1 if w % 1 != 0 else 1  # domain fix
            angle = math.asin(w)

        d = (height / parts) / math.cos(angle)

        x += math.sin(angle) * d
        y -= height / parts
        travelled += height / parts

        v_old = v
    yield x, y  # final point


trace_light(0, 10, 2)


if __name__ == "__main__":
    import gi

    gi.require_version("Gtk", "3.0")
    mpl.use("module://mplcairo.gtk")

    HEIGHT = 10
    WIDTH = 30
    PARTS = 10

    path = trace_light(0, HEIGHT, PARTS)
    x, y = zip(*path)
    plt.scatter(x, y, zorder=1)

    for n in np.linspace(0, HEIGHT, PARTS):
        plt.axhline(n, color="gainsboro", zorder=0)

    # print(f"Error: {abs(x[-1] - WIDTH)}")

    plt.savefig("result.png", dpi=300)

    # min_err, min_angle = math.inf, math.inf
    # for init_angle in np.linspace(0, math.pi / 2, 100):
    #     x, y = trace_light(init_angle, HEIGHT, PARTS)
    #     err = abs(x[-1] - WIDTH)
    #     if err < min_err:
    #         min_err, min_angle = err, init_angle
    # print(f"Err={min_err}, Angle={min_angle}")
