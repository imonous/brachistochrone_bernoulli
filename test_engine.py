import pytest
import math
import random

from engine import BernoulliRay, LightMedium


@pytest.fixture
def rand_xy():
    """To be used for vector lenghth. Mix small and large values."""
    xs = lambda: random.uniform(1e-10, 1)  # small
    xl = lambda: random.uniform(1e3, 1e9)  # large
    return [xs() if random.randint(0, 1) else xl() for _ in range(2)]


# used https://www.symbolab.com/solver/vector-angle-calculator
@pytest.mark.parametrize(
    "x, y, expected",
    [
        (0, 0.5, math.pi / 2),
        (0.5, 0.5, math.pi / 4),
        (0.75, 8, 1.47731),
        (1.2, 1.3, 0.82537),
        (120, 1.3, 0.01083),
    ],
)
def test_angle_getter_result(x, y, expected):
    r = BernoulliRay(x, y)
    assert r.angle == pytest.approx(expected, abs=1e-5)


@pytest.mark.parametrize(
    "test_input",
    [
        (0, 0),
        (-0.75, 8),
        (-0.75, -8),
        (0.75, -8),
    ],
)
def test_angle_getter_fails(test_input):
    with pytest.raises(ValueError):
        BernoulliRay(*test_input)


# depends on engine.angle getter
@pytest.mark.parametrize(
    "angle",
    [random.uniform(1e-50, 1e-10) for _ in range(10)]  # small angle
    + [random.uniform(1e-10, math.pi / 2) for _ in range(10)],  # any angle
)
def test_angle_setter_result(rand_xy, angle):
    r = BernoulliRay(*rand_xy)
    r.angle = angle
    assert angle == pytest.approx(r.angle)


@pytest.mark.parametrize("angle", [0, math.pi / 2 + 1e-1, math.pi, -math.pi])
def test_angle_setter_fails(rand_xy, angle):
    r = BernoulliRay(*rand_xy)
    with pytest.raises(ValueError):
        r.angle = angle


# too simple of a function to test
def test_get_incidence():
    assert True


# depends on engine.LightMedum, engine.set_angle, engine.get_angle
# used https://www.omnicalculator.com/physics/snells-law
@pytest.mark.parametrize(
    "n1, n2, incidence, expected",
    [
        # n1 >= n2
        (1.000293, 1.000293, 0.7853981633974483, 0.785398),
        (1.333, 1.000293, 0.7853981633974483, 1.229427),
        (2.419, 1, 0.1, 0.2439083),
        (1.36, 1.49, 0.0005, 0.000456376),
        (1.36, 1.49, 1.5, 1.144408),
        # n1 <= n2
        (1, 1.000293, 0.7853981633974483, 0.785105),
        (1.333, 2.419, 0.7853981633974483, 0.400256),
        (1.333, 2.419, 0.5235987755982988, 0.279138),
        (1.52, 2.419, 1.5, 0.67742),
        (1.000293, 2.419, 1.5, 0.425174),
    ],
)
def test_propagate_refract_results(rand_xy, n1, n2, incidence, expected):
    v1, v2 = LightMedium.n_to_v(n1), LightMedium.n_to_v(n2)
    m1, m2 = LightMedium(v1), LightMedium(v2)
    r = BernoulliRay(*rand_xy)
    r.angle = math.pi / 2 - incidence  # set incidence angle
    r.propagate(m1, m2)
    assert pytest.approx(r.angle) == expected


# depends on engine.LightMedum, engine.set_angle
# used https://www.omnicalculator.com/physics/snells-law
@pytest.mark.parametrize(
    "n1, n2, incidence, expected",
    # n1 > n2 must follow
    [
        (2.419, 1.333, 1, True),
        # fail cases (n1 <= n2)
        (1, 1.000293, 0.7853981633974483, False),
        (1.333, 2.419, 0.7853981633974483, False),
        (1.333, 2.419, 0.5235987755982988, False),
        (1.52, 2.419, 1.5, False),
        (1.000293, 2.419, 1.5, False),
    ],
)
def test_propagate_reflect_results(rand_xy, n1, n2, incidence, expected):
    v1, v2 = LightMedium.n_to_v(n1), LightMedium.n_to_v(n2)
    m1, m2 = LightMedium(v1), LightMedium(v2)
    r = BernoulliRay(*rand_xy)
    r.angle = math.pi / 2 - incidence
    r.propagate(m1, m2)
    assert r.reflected == expected


# should feature no fail cases
def test_propagate_fail():
    assert True
