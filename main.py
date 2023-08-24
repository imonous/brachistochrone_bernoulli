import numpy as np
import math

import matplotlib as mpl
import matplotlib.pyplot as plt

from scipy.optimize import newton

from sys import float_info


GRAV_ACC = 9.8067


def part_v(y, g=GRAV_ACC):
    return (2 * g * y) ** 0.5


def trace_light(init_angle, height, parts):
    x, y = 0, float_info.min
    angle = init_angle
    v, v_old = 0, 0

    for iter in range(parts):
        yield x, y
        v = part_v(y)

        if iter != 0:
            w = v / v_old * math.sin(angle)
            angle = math.asin(w)

        x += (height / parts) * math.tan(angle)
        y += height / parts

        v_old = v
    yield x, y  # final point


def cycloid(x2, y2, N=100):
    # First find theta2 from (x2, y2) numerically (by Newton-Rapheson).
    def f(theta):
        return y2 / x2 - (1 - np.cos(theta)) / (theta - np.sin(theta))

    theta2 = newton(f, np.pi / 2)

    # The radius of the circle generating the cycloid.
    R = y2 / (1 - np.cos(theta2))

    theta = np.linspace(0, theta2, N)
    x = R * (theta - np.sin(theta))
    y = R * (1 - np.cos(theta))

    return x, y


if __name__ == "__main__":
    import gi

    gi.require_version("Gtk", "3.0")
    mpl.use("module://mplcairo.gtk")

    HEIGHT = 10
    # WIDTH = 30
    PARTS = 100

    # path = trace_light(float_info.min, HEIGHT, PARTS)
    # x, y = zip(*path)
    # plt.plot(x, y, zorder=1)

    # for n in np.linspace(0, HEIGHT, PARTS + 1):
    #     plt.axhline(n, color="gainsboro", zorder=0)

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

    plt.ylim(HEIGHT, 0)
    plt.savefig("result.png", dpi=300)
