import panel as pn
import math
import engine

pn.extension(design="material")

ITERATIONS = 300000
MEDIUM_HEIGHT = 0.5

points = engine.trace_light(ITERATIONS, MEDIUM_HEIGHT, -math.pi / 3)
plot = engine.plot(points, MEDIUM_HEIGHT)
# bokeh_pane = pn.pane.Bokeh(plot)

angle_slider = pn.widgets.FloatSlider(
    name="Angle", start=0.5, end=89.5, step=0.5, value=45
)

app = pn.Row(angle_slider, plot)
app.servable()
