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


def plot(
    points: list[tuple[float, float]],
    medium_height: float = None,
    file_path=None,
) -> hv.core.layout.Layout:
    alim = np.max(np.abs(np.array(points)))
    if medium_height:
        lines = hv.HLines(-np.arange(0, alim, medium_height)).opts(
            color="lightgray", line_width=1
        )

    pad = 1e-1
    xlim = (-alim * pad, alim + alim * pad)
    ylim = (-alim - alim * pad, alim * pad)
    curve = hv.Curve(points).opts(xlim=xlim, ylim=(-3, 0), aspect=2.0)

    res = lines * curve
    if file_path:
        hv.save(res, file_path, fmt="png")
    return res


def bkc_plot(
    angle: float,
    g: float = 9.8067,
    fname: str = "",
) -> None:
    """Brachistochrone curve plot."""
    bkc = engine.ConstructBrachistochrone(init_angle=angle, g=g)
    while bkc.step():
        continue
    return plot(bkc.points, bkc.step_height, file_path=fname)


if __name__ == "__main__":
    pass
    # pts = main(math.pi / 2.3, fname="./data/plot.png")
    # print(pts)

    # pts = main(math.pi / 2.3, g=5, fname="./data/plot2.png")
    # print(pts)

    # xdata1, ydata1 = [], []
    # xdata2, ydata2 = [], []
    # for i in range(len(pts) // 2):
    #     xdata1.append(pts[i][0])
    #     ydata1.append(pts[i][1])
    # for i in range(len(pts) // 2 + 1, len(pts)):
    #     xdata2.append(pts[i][0])
    #     ydata2.append(pts[i][1])

    # data1 = {"x, m": xdata1, "y, m": ydata1}
    # data2 = {"x, m": xdata2, "y, m": ydata2}
    # df1 = pd.DataFrame(data1)
    # df2 = pd.DataFrame(data2)

    # df1 = df1.reset_index(drop=True)
    # df2 = df2.reset_index(drop=True)

    # df1.set_index(list(range(23, -1, -1)))

    # table1 = hv.Table(df1).opts(height=700)

    # table2 = hv.Table(df2).opts(height=700)

    # hv.save(table1, "./data/table1.png", fmt="png", dpi=300)
    # hv.save(table2, "./data/table2.png", fmt="png", dpi=300)

if __name__ == "__main__":
    points = cycloid(1)
    print(points)
