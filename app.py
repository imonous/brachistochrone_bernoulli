import panel as pn
import engine

pn.extension(design="material")

ITERATIONS = 300000
MEDIUM_HEIGHT = 0.5
points = engine.trace_light(ITERATIONS, MEDIUM_HEIGHT)
plot = engine.plot(points, MEDIUM_HEIGHT, "./data/plot.png")

app = pn.panel(plot)
app.servable()
