import numpy as np

GRAV_ACC = 9.8067

def v(t):
    return GRAV_ACC * t


if __name__ == "__main__":
    HEIGHT = 30
    WIDTH = 100
    PARTS = 10

    curr_t = 0 
    final_coord = (0, 0)
    total_t = np.inf
    for init_angle in np.linspace(0, 90, 90):
        for _ in range(PARTS - 1):
            pass



