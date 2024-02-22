import numpy as np
import math

import engine

import holoviews as hv

hv.extension("bokeh")


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


# def percentage_error(y, y_fit):
#     y, y_fit = y[1:], y_fit[1:]
#     PE = np.abs((y - y_fit) / y)
#     PE = np.insert(PE, 0, 1)
#     print(PE)
#     return np.mean(PE)


# def plot(
#     points: list[tuple[float, float]],
#     medium_height: float = None,
#     file_path=None,
# ) -> hv.core.layout.Layout:
#     alim = np.max(np.abs(np.array(points)))
#     if medium_height:
#         lines = hv.HLines(-np.arange(0, alim, medium_height)).opts(
#             color="lightgray", line_width=1
#         )

#     pad = 1e-1
#     xlim = (-alim * pad, alim + alim * pad)
#     ylim = (-alim - alim * pad, alim * pad)
#     curve = hv.Curve(points).opts(xlim=xlim, ylim=(-3, 0), aspect=2.0)

#     res = lines * curve
#     if file_path:
#         hv.save(res, file_path, fmt="png")
#     return res


if __name__ == "__main__":
    pass
