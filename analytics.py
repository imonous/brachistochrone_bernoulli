import numpy as np
from math import floor, log10
import pandas as pd
import os
import engine
import holoviews as hv
import plotly.io as pio
from sigfig import round

hv.extension("bokeh")

SIGFIG = 5


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
    PE = np.abs((y - y_fit) / y_fit)
    PE = np.insert(PE, 0, 0)
    return np.mean(PE)


# def plot(
#     points: list[tuple[float, float]],
#     medium_height: float = None,
#     file_path=None,
# ) -> hv.core.layout.Layout:
#     if medium_height:
#         lines = hv.HLines(-np.arange(0, alim, medium_height)).opts(
#             color="lightgray", line_width=1
#         )

#     pad = 1e-1
#     alim = np.max(np.abs(np.array(points)))
#     xlim = (-alim * pad, alim + alim * pad)
#     ylim = (-alim - alim * pad, alim * pad)
#     curve = hv.Curve(points).opts(xlim=xlim, ylim=ylim)  # , aspect=2.0)

#     out = lines * curve
#     if file_path:
#         hv.save(out, file_path, fmt="png")
#     return out


def save_table(df, fname, width, height):
    df = df.map(lambda x: round(str(x), SIGFIG))
    plt = hv.Table(df).opts(height=height, width=width)
    hv.save(plt, fname, dpi=300)


if __name__ == "__main__":
    TRIALS = 3
    cases = [
        "angle1-31_g100.csv",
        "angle1-31_g1.csv",
        "angle1-31_g20.csv",
        "angle1-31_g9-81.csv",
    ]
    cases = ["./data/" + case for case in cases]

    # for case in cases:
    #     for t in range(TRIALS):
    #         fname = os.path.splitext(case)[0] + f"_{t}"
    #         df = pd.read_csv(fname + ".csv")
    #         save_table(df, fname + ".png", height=400, width=600)
    #         print(t)
    #     print(f"Case {case}: DONE")

    # data = pd.DataFrame(
    #     {
    #         "Case (g, m/s^2)": [],
    #         "T#1 (avg x, m)": [],
    #         "T#2 (avg x, m)": [],
    #         "T#3 (avg x, m)": [],
    #         "Avg, m": [],
    #         "Abs. uncert.": [],
    #         "Rel. uncert., %": [],
    #     }
    # )
    # for case in cases:
    #     g = float(os.path.splitext(case)[0].split("_")[1][1:].replace("-", "."))
    #     trials = []
    #     for t in range(TRIALS):
    #         fname = os.path.splitext(case)[0] + f"_{t}" + ".csv"
    #         df = pd.read_csv(fname)
    #         trials.append(df["x, m"].mean())
    #     avg = sum(trials) / len(trials)
    #     abs_unc = (max(trials) - min(trials)) / 2
    #     rel_unc = abs_unc / avg

    #     data.loc[len(data)] = [g, *trials, avg, abs_unc, rel_unc]
    # save_table(data, "./data/processed_data.png", height=140, width=620)

    df = pd.read_csv("./data/angle1-31_g9-81_0.csv")
    theory_data = cycloid(0.25, len(df))

    # theory = hv.Curve(theory_data)
    # experiment = hv.Curve(df)
    # layout = (theory * experiment).opts(width=400)
    # hv.save(layout, "./data/comparison.png")

    err = percentage_error(df["y, m"], [p[1] for p in theory_data])
    print(round(err * 100, SIGFIG))
