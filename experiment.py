import engine


if __name__ == "__main__":
    ITERATIONS = 300000
    MEDIUM_HEIGHT = 0.5
    points = engine.trace_light(ITERATIONS, MEDIUM_HEIGHT)
    engine.plot(points, MEDIUM_HEIGHT, "./data/plot.png")
