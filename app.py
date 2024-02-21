import panel as pn
import math

import engine
import analytics

import holoviews as hv

pn.extension(design="material")

ITERATIONS = 300000
MEDIUM_HEIGHT = 0.5

# bokeh_pane = pn.pane.Bokeh(plot)
bkc = hv.DynamicMap(analytics.bkc_plot, kdims=["angle", "g"])
bkc = bkc.redim.range(angle=(math.pi / 2.7, math.pi / 2.2), g=(5, 20))


# angle_slider = pn.widgets.FloatSlider(
#     name="Angle", start=0.5, end=89.5, step=0.5, value=45
# )

app = pn.Row(bkc)
app.servable()

# def plot(
#     points: list[tuple[float, float]], medium_height: float, file_path=None, save=False
# ) -> hv.core.layout.Layout:
#     alim = np.max(np.abs(np.array(points)))
#     # lines = hv.HLines(-np.arange(0, alim, medium_height)).opts(
#     #     color="lightgray", line_width=1
#     # )

#     pad = 1e-1
#     xlim = (-alim * pad, alim + alim * pad)
#     ylim = (-alim - alim * pad, alim * pad)
#     curve = hv.Curve(points).opts(xlim=xlim, ylim=ylim, height=650, width=650)

#     # res = lines * curve
#     res = curve
#     if save:
#         # show(hv.render(res))
#         hv.save(res, file_path, fmt="png")
#     return res
