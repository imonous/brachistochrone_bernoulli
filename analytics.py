import numpy as np
import math


def cycloid(r, N=100):
    """
    x = r(t - sin t)
    y = r(1 - cos t)
    """
    out = []
    for t in np.linspace(0, 6, N):
        x = r * (t - np.sin(t))
        y = -r * (1 - np.cos(t))
        out.append((x, y))
    return out


def percentage_error(y, y_fit):
    y, y_fit = y[1:], y_fit[1:]
    PE = np.abs((y - y_fit) / y)
    PE = np.insert(PE, 0, 1)
    print(PE)
    return np.mean(PE)


if __name__ == "__main__":
    points = cycloid(1)
    print(points)
