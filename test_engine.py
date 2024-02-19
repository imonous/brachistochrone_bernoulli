import pytest
import math
import random

from engine import LightRay


# computed using the online symbolab calculator
@pytest.mark.parametrize(
    "x, y, expected",
    [
        (0, 0.5, math.pi / 2),
        (0.5, 0.5, math.pi / 4),
        (0.75, 8, 1.47731),
        (-0.75, 8, math.pi - 1.47731),
        (-0.75, -8, 1.47731 - math.pi),
        (0.75, -8, -1.47731),
        (1.2, 1.3, 0.82537),
        (120, 1.3, 0.01083),
    ],
)
def test_get_angle_result(x, y, expected):
    ray = LightRay(x, y)
    assert ray.get_angle() == pytest.approx(expected, abs=1e-5)


@pytest.mark.parametrize("test_input", [(0, 0)])
def test_get_angle_fails(test_input):
    with pytest.raises(ValueError):
        LightRay(*test_input)


rand = lambda: random.uniform(1e-10, 1)


# Depends on test_get_angle!
@pytest.mark.parametrize(
    "angle, x, y",
    [(random.uniform(1e-50, 1e-10), rand(), rand()) for _ in range(10)]  # small angle
    + [
        (random.uniform(1e-10, math.pi / 2), rand(), rand()) for _ in range(10)
    ],  # any angle
)
def test_set_angle_result(angle, x, y):
    ray = LightRay(x, y)
    ray.set_angle(angle)
    assert angle == pytest.approx(ray.get_angle())


@pytest.mark.parametrize("angle", [0, math.pi / 2 + 1e-1, math.pi, -math.pi])
def test_set_angle_fail(angle):
    rand = lambda: random.uniform(1e-10, 1)
    ray = LightRay(rand(), rand())
    with pytest.raises(ValueError):
        ray.set_angle(angle)


# def test_get_other_angle() -> bool:
#     return True


# def test_propagate() -> bool:
#     return True


# def test_reflect() -> bool:
#     return True


# def test_refract() -> bool:
#     return True


# def test_can_refract() -> bool:
#     return True
