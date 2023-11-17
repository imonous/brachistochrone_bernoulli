import math


class LightMedium:
    def __init__(self, v):
        """Light medium in terms of velocity."""
        self.v = v

    def __repr__(self):
        return f"LightMedium(v={self.v:.2e})"


class BernoulliLightMedium(LightMedium):
    def __init__(self, y, g=9.8067):
        """
        A light medium from the Johann Bernoulli indirect method for the brachistochrone
        curve. It is meant to replicate gravity as a light ray passes through it.
        """
        self.g = g
        self.set_v(y)

    def set_v(self, y: float) -> None:
        """
        Set the velocity of the medium in accordance to:
                v = sqrt(-2 * g * y).
        """
        self.v = math.sqrt(-2 * self.g * y)


class LightRay:
    def __init__(self, x: float, y: float):
        """Light ray as a vector. Angles are in radians."""
        self.x, self.y = x, y

    def get_angle(self) -> float:
        """Get the angle of the vector."""
        return math.atan2(self.y, self.x)

    def set_angle(self, angle: float) -> None:
        """
        Set the angle of the vector in the range [-pi / 2, pi / 2]. If the sign of angle
        does not change, alter x. Otherwise, alter y and or x.
        """
        if math.copysign(angle, self.get_angle()) != angle:
            self.y = -self.y
        self.x = self.y / math.tan(angle)

    def get_other_angle(self) -> float:
        """
        Since Ray is a vector, to calculate its angle we imagine a right triangle. This
        function returns the other angle of that triangle.
        """
        angle = self.get_angle()
        return math.copysign(math.pi / 2 - abs(angle), angle)

    def propagate(self, medium1: type[LightMedium], medium2: type[LightMedium]) -> None:
        """Propagate the ray from medium1 to medium2."""
        if self.can_refract(medium1, medium2):
            return self._refract(medium1, medium2)
        return self.reflect()

    def reflect(self) -> None:
        """
        Reflect the ray (...specify...) using the Law of Reflection:
            alpha_1 = alpha_2.
        """
        self.y = -self.y

    def _refract(self, medium1: type[LightMedium], medium2: type[LightMedium]) -> None:
        """
        Refract the ray from medium1 to medium2 using the Law of Refraction:
            sin(alpha_1) / sin(alpha_2) = v1 / v2.
        The propagate method should be used directly instead of this, as light is not
        always able to refract.
        """
        alpha_1 = self.get_other_angle()
        v1, v2 = medium1.v, medium2.v
        w = v2 / v1 * math.sin(alpha_1)
        w = math.asin(w)
        alpha_2 = math.copysign(math.pi / 2 - abs(w), w)
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
        alpha_1 = self.get_other_angle()
        v1, v2 = medium1.v, medium2.v
        w = v2 / v1 * math.sin(alpha_1)
        if w == 0 or abs(w) > 1:  # no total internal reflectoin
            return False
        return True

    def __repr__(self):
        return f"LightRay(x={self.x:.2e}, y={self.y:.2e}, angle={self.get_angle():.2e})"
