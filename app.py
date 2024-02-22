import math
import time
import asyncio

import numpy as np
import pandas as pd
from colour import Color

import engine

import panel as pn
import holoviews as hv
from holoviews.streams import Pipe

pn.extension("floatpanel", design="material")

in_angle_slider = pn.widgets.FloatSlider(
    name="Initial ray angle (radians)",
    start=math.pi / 2.7,
    end=math.pi / 2.2,
    step=0.01,
    value=math.pi / 2.4,
)
gconst_slider = pn.widgets.FloatSlider(
    name="Gravitational Acceleration (m/s^2)", start=1, end=20, step=1, value=9.81
)

medium_height = 1e-1
N_mediums = 50  # max ray angle = 1.43
gradient = list(
    Color("#34cceb").range_to(Color("#d334eb"), N_mediums)
)  # cyan to violet

colored_container = hv.Overlay(
    [
        hv.HSpan(h * medium_height, h * medium_height - medium_height).opts(
            color=gradient[abs(h)].get_hex(), alpha=0.3
        )
        for h in range(0, -N_mediums, -1)
    ]
)

pipe = Pipe(data=pd.DataFrame({"x": [], "y": []}))
live_plot = colored_container * hv.DynamicMap(hv.Curve, streams=[pipe]).opts(
    width=1000, height=600, color="#f0dd13", alpha=1, ylim=(-5, 0)
)
live_data = hv.DynamicMap(hv.Table, streams=[pipe]).opts(height=800)

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
            await asyncio.sleep(0.2)
            pipe.send(bkc_data.points)

    else:
        is_tracing = False
        trace_path_btn.name = "Trace path"


trace_path_btn.on_click(trace_path_toggle)

# data_gather_modal = pn.layout.FloatPanel(
#     pn.pane.DataFrame(data_to_gather, width=400),
#     name="Basic FloatPanel",
#     margin=20,
#     visible=False,
# )


# async def gather_data(event):
#     data_gather_modal.visible = True


gather_data_btn = pn.widgets.Button(name="Gather data", button_type="primary")
# gather_data_btn.on_click(gather_data)

app = pn.template.VanillaTemplate(
    title="The Brachistochrone via Bernoulli's Indirect Method",
    sidebar=[
        in_angle_slider,
        gconst_slider,
        pn.layout.Divider(),
        pn.Row(trace_path_btn, gather_data_btn),
    ],
)
app.main.append(
    pn.Column(
        pn.Row(live_plot, live_data),
    )
)
# app.main.append(data_gather_modal)
app.servable()
