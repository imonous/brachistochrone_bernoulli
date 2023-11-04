from engine import BernoulliLightMedium, LightRay
import holoviews as hv

hv.extension("bokeh")


def trace_light(iterations: int, medium_height: float) -> list[tuple[float, float]]:
    ray = LightRay(x=1e-10, y=-medium_height)  # update init x
    print(ray)
    x, y = 0, -1e-10  # update init y
    points = [(x, y)]
    m1, m2 = BernoulliLightMedium(0), BernoulliLightMedium(0)
    for i in range(iterations):
        m1.set_v(abs(y))
        m2.set_v(abs(y + ray.y))
        ray.propagate(m1, m2)
        x += ray.x
        y += ray.y
        points.append((x, y))
        # print(m1, m2, ray)
    return points


def plot(
    points: list[tuple[float, float]], file_path: str, save=True
) -> hv.core.layout.Layout:
    res = hv.Curve(points)
    if save:
        hv.save(res, file_path, fmt="png")
    return res


if __name__ == "__main__":
    ITERATIONS = 3
    MEDIUM_HEIGHT = 1e-5
    points = trace_light(ITERATIONS, MEDIUM_HEIGHT)
    plot(points, "./data/plot.png")
