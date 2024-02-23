import math
import asyncio
import time

import io

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
    name="Gravitational Acceleration (m/s^2)", start=1, end=100, step=1, value=9.81
)

medium_height = 1e-1
N_mediums = 50  # max ray angle = 1.43
gradient = list(
    Color("#34cceb").range_to(Color("#d334eb"), N_mediums)
)  # cyan to violet

colored_container = hv.Overlay(
    [
        hv.HSpan(h * medium_height, h * medium_height - medium_height).opts(
            color=gradient[abs(h)].get_hex(), alpha=0.2, line_alpha=0.1
        )
        for h in range(0, -N_mediums, -1)
    ]
)

pipe = Pipe(data=pd.DataFrame({"x, m": [], "y, m": [], "Medium velocity, m/s": []}))
live_plot = colored_container * hv.DynamicMap(hv.Curve, streams=[pipe]).opts(
    width=800,
    height=600,
    color="#ffd700",
    alpha=1,
    ylim=(-5, 0),
    xlim=(0, 8),
    line_width=2,
)
live_data = hv.DynamicMap(hv.Table, streams=[pipe]).opts(height=600)
is_tracing = False


async def stop_trace():
    global is_tracing
    is_tracing = False
    in_angle_slider.disabled = False
    gconst_slider.disabled = False
    trace_path_btn.button_type = "success"
    trace_path_btn.name = "Trace path"


async def start_trace():
    global is_tracing
    is_tracing = True
    in_angle_slider.disabled = True
    gconst_slider.disabled = True
    trace_path_btn.button_type = "danger"
    trace_path_btn.name = "Stop trace"

    bkc_data = engine.ConstructBrachistochrone(
        init_angle=in_angle_slider.value, g=gconst_slider.value
    )
    while bkc_data.step() and is_tracing:
        await asyncio.sleep(0.05)
        pipe.send(bkc_data.data)
    return await stop_trace()


async def trace_path_toggle(event):
    global is_tracing
    if not is_tracing:
        return await start_trace()
    return await stop_trace()


trace_path_btn = pn.widgets.Button(name="Trace path", button_type="success", height=48)
trace_path_btn.on_click(trace_path_toggle)


def export_data():
    export_data_btn.loading = True
    filefy = lambda x: str(round(x, 2)).replace(
        ".", "-"
    )  # convert a float to a str with - for .
    export_data_btn.filename = (
        f"angle{filefy(in_angle_slider.value)}_g{filefy(gconst_slider.value)}.csv"
    )
    file = io.BytesIO()
    pipe.data.to_csv(file, index=False)
    file.seek(0)
    time.sleep(0.2)  # fake sleep for UX; asyncio fails
    export_data_btn.loading = False
    return file


export_data_btn = pn.widgets.FileDownload(
    label="Export data",
    button_type="default",
    callback=export_data,
    filename="data.csv",
    height=48,
)

notice = pn.pane.Str(
    "Note: you will be unable to adjust the<br>parameters whilst tracing!",
    width=10,
)


app = pn.template.VanillaTemplate(
    title="The Brachistochrone via Bernoulli's Indirect Method",
    sidebar=[
        in_angle_slider,
        gconst_slider,
        pn.layout.Divider(),
        pn.Row(trace_path_btn, export_data_btn),
        pn.layout.Divider(),
        notice,
    ],
    main=[
        pn.Column(
            pn.Row(live_plot, live_data),
        )
    ],
)
app.servable()
