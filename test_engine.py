import pytest
import math
import random

from engine import LightRay, LightMedium


# used https://www.symbolab.com/solver/vector-angle-calculator
# TODO: add more cases
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


# depends on engine.get_angle
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
    rand = lambda: random.uniform(1e-10, 1)  # TODO: does not work!
    ray = LightRay(rand(), rand())
    with pytest.raises(ValueError):
        ray.set_angle(angle)


# def test_get_other_angle() -> bool:
#     return True


# def test_propagate() -> bool:
#     return True


# def test_reflect() -> bool:
#     return True


c = 299792458  # m / s


def n_to_v(n):
    """
    Convert refractive index to velocity.
            n = c / v,
            v = c / n.
    """
    return c / n


# depends on engine.LightMedum, n_to_v, engine.set_angle, engine.get_other_angle
# used https://www.omnicalculator.com/physics/snells-law
#   for (1, 2, 3, 4, 5)
# used https://www.allaboutcircuits.com/tools/snells-law-calculator-snells-law-equation/
#   for ()
# used https://www.translatorscafe.com/unit-converter/de-DE/calculator/snell-law/
#   for ()
@pytest.mark.parametrize(
    "n1, n2, angle, expected",
    [
        # n1 >= n2
        (1.000293, 1.000293, 0.7853981633974483, 0.785398),
        (1.333, 1.000293, 0.7853981633974483, 1.229427),
        # n1 <= n2
        # (1, 1.000293, 0.7853981633974483, 0.785105),
        # (1.229427, 2.419, 0.7853981633974483, 0.7853981633974483),
        # (1.229427, 2.419, 0.5235987755982988, 0.279138),
    ],
)
def test_refract_results(n1, n2, angle, expected):
    r = LightRay(1, 1)
    r.set_angle(angle)
    m1, m2 = LightMedium(n_to_v(n1)), LightMedium(n_to_v(n2))
    r._refract(m1, m2)
    assert pytest.approx(r.get_other_angle(), abs=1e-3) == expected


# def test_can_refract() -> bool:
#     return True
