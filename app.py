import math
import time
import asyncio

import engine

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

is_tracing = False
trace_path_btn = pn.widgets.Button(name="Trace path", button_type="primary")


async def trace_path_toggle(event):
    global is_tracing

    if not is_tracing:
        is_tracing = True
        trace_path_btn.name = "Stop trace"
        bkc_data = engine.ConstructBrachistochrone(
            init_angle=in_angle_slider.value, g=gconst_slider.value
        )
        while bkc_data.step() and is_tracing:
            time.sleep(0.5)
            await asyncio.sleep(1)
            pipe.send(bkc_data.points)
    else:
        is_tracing = False
        trace_path_btn.name = "Trace path"


trace_path_btn.on_click(trace_path_toggle)

app = pn.Row(
    pn.Column(pn.Row(trace_path_btn), in_angle_slider, gconst_slider),
    live_plot,
)
app.servable()
