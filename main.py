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
    down = True

    for iter in range(parts):
        yield x, y
        v = part_v(travelled)

        if iter != 0:
            w = v / v_old * math.sin(angle)
            if w < 1:
                angle = math.asin(w)
            else:  # total internal reflection
                down = not down

        x += (height / parts) * math.tan(angle)
        if down:
            y -= height / parts
            travelled += height / parts
        else:
            y += height / parts
            travelled -= height / parts

        v_old = v
    yield x, y  # final point


if __name__ == "__main__":
    import gi

    gi.require_version("Gtk", "3.0")
    mpl.use("module://mplcairo.gtk")

    HEIGHT = 10
    # WIDTH = 30
    PARTS = 100

    # y = list(trace_light(float_info.min, HEIGHT, PARTS))
    # x = range(len(y))
    # plt.scatter(x, y)
    # plt.show()

    path = trace_light(float_info.min, HEIGHT, PARTS)
    x, y = zip(*path)
    plt.plot(x, y, zorder=1)

    for n in np.linspace(0, HEIGHT, PARTS + 1):
        plt.axhline(n, color="gainsboro", zorder=0)

    #  print(f"Error: {abs(x[-1] - WIDTH)}")

    # min_err, min_angle = math.inf, math.inf
    # for init_angle in np.linspace(float_info.min, math.pi / 2, 100):
    #     path = trace_light(init_angle, HEIGHT, PARTS)
    #     try:
    #         x, y = zip(*path)
    #     except:
    #         print(init_angle)
    #         continue
    #     err = abs(x[-1] - WIDTH)
    #     if err < min_err:
    #         min_err, min_angle = err, init_angle
    # print(f"Err={min_err}, Angle={min_angle}")

    plt.savefig("result.png", dpi=300)
