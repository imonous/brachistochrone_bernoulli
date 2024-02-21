import math
import time

import engine
import analytics

import panel as pn
import holoviews as hv
from holoviews.streams import Pipe

pn.extension(design="material")

in_angle_slider = pn.widgets.FloatSlider(
    name="Initial ray angle",
    start=math.pi / 2.7,
    end=math.pi / 2.2,
    step=0.01,
    value=math.pi / 2.4,
)
gconst_slider = pn.widgets.FloatSlider(
    name="Gravitational Acceleration", start=1, end=20, step=1, value=10
)

pipe = Pipe(data=[])
live_plot = hv.DynamicMap(hv.Curve, streams=[pipe])


def stop_trace(event):
    pass


def trace_path(event):
    bkc_data = engine.ConstructBrachistochrone(
        init_angle=in_angle_slider.value, g=gconst_slider.value
    )
    while bkc_data.step():
        time.sleep(0.5)
        pipe.send(bkc_data.points)


trace_path_btn = pn.widgets.Button(name="Trace path", button_type="primary")
stop_trace_btn = pn.widgets.Button(name="Stop trace", button_type="primary")

trace_path_btn.on_click(trace_path)
stop_trace_btn.on_click(stop_trace)

app = pn.Row(
    pn.Column(pn.Row(trace_path_btn, stop_trace_btn), in_angle_slider, gconst_slider),
    live_plot,
)
app.servable()
