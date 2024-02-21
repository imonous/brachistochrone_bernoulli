import numpy as np
import math

import matplotlib as mpl
import matplotlib.pyplot as plt

from scipy.optimize import newton

from sys import float_info


GRAV_ACC = 9.8067
PATH = "/home/anon/Programming/projects/brachistochrone_bernoulli/data"


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


def format_data(data):
    output = ""
    for entry in data:
        angle, x, y = entry.values()
        angle, x, y = (
            format(angle, ".3f"),
            [format(n, ".3e") for n in x],
            [format(n, ".3e") for n in y],
        )
        output += f"ANGLE: {angle}deg\nx: {x}\ny: {y}\n\n"
    return output[:-2]  # trim last \n


def percentage_error(y, y_fit):
    y, y_fit = y[1:], y_fit[1:]
    PE = np.abs((y - y_fit) / y)
    PE = np.insert(PE, 0, 1)
    print(PE)
    return np.mean(PE)


if __name__ == "__main__":
    pass
