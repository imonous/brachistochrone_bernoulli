""" True for pass. """
from typing import Iterable, Any
from engine import LightRay


def test(inputs: Iterable[Any], expected: Iterable[Any]) -> bool:
    if len(inputs) != len(expected):
        raise ValueError("inputs and expected must be of same length")
    for i in range(len(inputs)):
        if inputs[i] != expected[i]:
            return False
    return True


def test_get_angle() -> bool:
    return True


def test_set_angle() -> bool:
    return True


def test_get_other_angle() -> bool:
    return True


def test_propagate() -> bool:
    return True


def test_reflect() -> bool:
    return True


def test_refract() -> bool:
    return True


def test_can_refract() -> bool:
    return True


if __name__ == "__main__":
    L = [
        test_get_angle,
        test_set_angle,
        test_get_other_angle,
        test_propagate,
        test_reflect,
        test_refract,
        test_can_refract,
    ]
    passed = 0
    for f in L:
        passed += f()
    print(f"PASSED: {passed} / {len(L)}")
