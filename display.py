import holoviews as hv
import numpy as np
import math

from analytics import cycloid
import engine

hv.extension("bokeh")


def plot(
    points: list[tuple[float, float]], medium_height: float, file_path=None, save=False
) -> hv.core.layout.Layout:
    alim = np.max(np.abs(np.array(points)))
    # lines = hv.HLines(-np.arange(0, alim, medium_height)).opts(
    #     color="lightgray", line_width=1
    # )

    pad = 1e-1
    xlim = (-alim * pad, alim + alim * pad)
    ylim = (-alim - alim * pad, alim * pad)
    curve = hv.Curve(points).opts(
        xlim=xlim, ylim=ylim, height=650, width=650
    ) * hv.Curve(cycloid(820, 500))

    # res = lines * curve
    res = curve
    if save:
        hv.save(res, file_path, fmt="png")
    return res


def main(init_angles: list[float]) -> None:
    for i, angle in enumerate(init_angles):
        bkc = engine.ConstructBrachistochrone(init_angle=angle)
        while bkc.step():
            continue
        plot(bkc.points, bkc.step_height, file_path=f"./data/plot{i}.png", save=True)


if __name__ == "__main__":
    main(
        [math.pi / 2.01]
    )  # , math.pi / 2.2, math.pi / 2.25, math.pi / 2.75, math.pi / 3])
