from engine import BernoulliLightMedium, LightRay, LightMedium
import holoviews as hv
from sys import float_info
import numpy as np
import math
from holoviews import opts

from bokeh.plotting import show

hv.extension("bokeh")


def trace_light(iterations: int, medium_height: float) -> list[tuple[float, float]]:
    ray = LightRay(x=1e-3, y=-medium_height)
    x, y = 0, ray.y
    points = [(0, 0), (ray.x, ray.y)]
    m1, m2 = BernoulliLightMedium(0), BernoulliLightMedium(0)
    for _ in range(iterations):
        if y + ray.y >= 0:
            break
        m1.set_v(y)
        m2.set_v(y + ray.y)
        ray.propagate(m1, m2)
        x += ray.x
        y += ray.y
        points.append((x, y))
    return points


def plot(
    points, medium_height: float, file_path: str, save=True
) -> hv.core.layout.Layout:
    alim = np.max(np.abs(np.array(points)))
    # lines = hv.HLines(-np.arange(0, alim, medium_height)).opts(
    #     color="lightgray", line_width=1
    # )

    pad = 1e-1
    xlim = (-alim * pad, alim + alim * pad)
    ylim = (-alim - alim * pad, alim * pad)
    curve = hv.Curve(points).opts(xlim=xlim, ylim=ylim, height=650, width=650)

    # res = lines * curve
    res = curve
    if save:
        # show(hv.render(res))
        hv.save(res, file_path, fmt="png")
    return res


if __name__ == "__main__":
    ITERATIONS = 300000
    MEDIUM_HEIGHT = 0.5
    points = trace_light(ITERATIONS, MEDIUM_HEIGHT)
    plot(points, MEDIUM_HEIGHT, "./data/plot.png")
