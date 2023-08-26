import numpy as np
import math

import matplotlib as mpl
import matplotlib.pyplot as plt

from scipy.optimize import newton

from sys import float_info


GRAV_ACC = 9.8067
PATH = "/home/anon/Programming/projects/brachistochrone_bernoulli/investigation"


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


# HEIGHT = 10
# PARTS = 100

# path = trace_light(float_info.min, HEIGHT, PARTS)
# x, y = zip(*path)
# plt.plot(x, y, zorder=1)

# for n in np.linspace(0, HEIGHT, PARTS + 1):
#     plt.axhline(n, color="gainsboro", zorder=0)

# plt.ylim(HEIGHT, 0)
# plt.savefig("result.png", dpi=300)


def cycloid(x2, y2, N=100):
    def f(theta):
        return y2 / x2 - (1 - np.cos(theta)) / (theta - np.sin(theta))

    theta2 = newton(f, np.pi / 2)

    R = y2 / (1 - np.cos(theta2))

    theta = np.linspace(0, theta2, N)
    x = R * (theta - np.sin(theta))
    y = R * (1 - np.cos(theta))

    return x, y


if __name__ == "__main__":
    import gi

    gi.require_version("Gtk", "3.0")
    mpl.use("module://mplcairo.gtk")

    raw_data = []
    x2 = 1
    for y2 in np.linspace(0.1, 2, 4):
        x, y = cycloid(1, y2)
        y *= -1
        raw_data.append((x, y))

    with open(f"{PATH}/raw_data.txt", "w") as file:
        file.write(str(raw_data))

    # for x, y in raw_data:
    #     plt.plot(x, y)
    # lim = max(max(x), max(abs(y)))
    # plt.xlim(0, lim)
    # plt.ylim(-lim, 0)
    # plt.savefig("processed_data.png", dpi=300)
