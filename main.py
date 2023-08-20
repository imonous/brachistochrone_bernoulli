import numpy as np
import math

GRAV_ACC = 9.8067


def part_v(t):
    return GRAV_ACC * t

def calc_err(expect, real):
    x = abs(expect[0] - real[0])
    y = abs(expect[1] - real[1])
    return math.sqrt(x**2 + y**2)


if __name__ == "__main__":
    HEIGHT = 3
    WIDTH = 10
    PARTS = 10**6

    min_err = math.inf
    # for init_angle in np.linspace(0, math.pi / 2, 100):
    for init_angle in [math.pi / 6]:
        t = 1e-30
        x, y = 0, 0
        angle = init_angle
        v, v_old = 0, 0
        init = True
        for _ in range(PARTS - 1):
            v = part_v(t)

            # 1 / v * sin(angle) = 1 / v_new * sin(angle_new)
            # new_angle = arcsin(v_new / v * sin(angle))
            if not init:
                w = v / v_old * math.sin(angle)
                w = w % 1 if w != 1 else 1 # fix domain
                angle = math.asin(w)

            # cos(a) = height / long; long = height / cos(a)
            d = (HEIGHT / PARTS) / math.cos(angle) 

            # d = vt; t = d / v
            t += d / v

            # sin(a) = width / long; x += sin(a) * long; y += height
            x += math.sin(angle) * d
            y += HEIGHT / PARTS

            if init:
                init = False
            v_old = v

        err = calc_err((WIDTH, HEIGHT), (x, y))  
        if err < min_err:
            min_err = err

    print(min_err)

