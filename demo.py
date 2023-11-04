import math
import numpy as np
from sys import float_info


class LightMedium:
    def __init__(self, v):
        """Light medium in terms of velocity."""
        self.v = v


class BernoulliLightMedium(LightMedium):
    def __init__(self, v, g=9.8067):
        """
        A light medium from the Johann Bernoulli indirect method for the brachistochrone
        curve. It is meant to replicate gravity as a light ray passes through it.
        """
        pass

    # def v(self, y):
    #     return (2 * self.g * y) ** 0.5


class LightRay:
    def __init__(self, x: float, y: float):
        """Light ray as a vector."""
        self.x, self.y = x, y

    def get_angle(self) -> float:
        """Get the angle of the vector."""
        return math.atan(self.y / self.x)

    def set_angle(self, angle: float) -> None:
        """Set the angle of the vector."""
        self.x = self.y / math.tan(angle)

    def get_other_angle(self) -> float:
        """
        Since Ray is a vector, to calculate its angle we imagine a right triangle. This
        function returns the other angle of that triangle.
        """
        angle = self.get_angle()
        return math.copysign(np.pi / 2 - abs(angle), angle)

    def propagate(self, medium1: type[LightMedium], medium2: type[LightMedium]) -> None:
        """Propagate the ray from medium1 to medium2."""
        if self.can_refract(medium1, medium2):
            return self._refract(medium1, medium2)
        return self.reflect()

    def reflect(self) -> None:
        """
        Reflect the ray (off a ... surface) using the Law of Reflection:
            alpha_1 = alpha_2.
        """
        alpha_1 = self.get_other_angle()
        alpha_w = -alpha_1
        alpha_2 = math.copysign(np.pi / 2 - abs(alpha_w), alpha_2)
        self.set_angle(alpha_2)

    def _refract(self, medium1: type[LightMedium], medium2: type[LightMedium]) -> None:
        """
        Refract the ray from medium1 to medium2 using the Law of Refraction:
            sin(alpha_1) / sin(alpha_2) = v1 / v2.
        The propagate method should be used directly instead of this, as light is not
        always able to refract.
        """
        alpha_1 = self.get_angle()
        v1, v2 = medium1.v, medium2.v
        w = v2 / v1 * math.sin(alpha_1)
        alpha_2 = math.asin(w)
        self.set_angle(alpha_2)

    def can_refract(
        self, medium1: type[LightMedium], medium2: type[LightMedium]
    ) -> bool:
        """
        Determine whether light can refract using the Law of Refraction:
            sin(alpha_1) / sin(alpha_2) = v1 / v2,
            alpha_2 = arcsin(v2 / v1 * sin(alpha_1)).
        If out of domain return False, otherwise True.
        """
        alpha_1 = self.get_angle()
        v1, v2 = medium1.v, medium2.v
        w = v2 / v1 * math.sin(alpha_1)
        if abs(w) > 1:
            return False
        return True


if __name__ == "__main__":
    pass
