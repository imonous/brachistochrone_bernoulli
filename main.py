import numpy as np
import math


GRAV_ACC = 9.8067


def part_v(t):
    return GRAV_ACC * t


def calc_err(expect, real):
    x = abs(expect[0] - real[0])
    y = abs(expect[1] - real[1])
    return math.sqrt(x**2 + y**2)


def trace_light(init_angle, height, parts):
    t = 1e-30
    x, y = 0, 0
    angle = init_angle
    v, v_old = 0, 0
    for iter in range(PARTS - 1):
        yield x, y
        v = part_v(t)
        if iter != 0:
            w = v / v_old * math.sin(angle)
            w = w % 1 if w != 1 else 1  # domain fix
            angle = math.asin(w)
        d = (height / parts) / math.cos(angle)
        t += d / v
        x += math.sin(angle) * d
        y += height / parts
        v_old = v
    yield x, y  # final point


if __name__ == "__main__":
    HEIGHT = 3
    WIDTH = 10
    PARTS = 10**4

    min_err, min_angle = math.inf, math.inf
    for init_angle in np.linspace(0, math.pi / 2, 100):
        x, y = trace_light(init_angle, HEIGHT, WIDTH, PARTS)
        err = calc_err((WIDTH, HEIGHT), (x, y))
        if err < min_err:
            min_err, min_angle = err, init_angle
    print(f"{min_err}, {min_angle}")
