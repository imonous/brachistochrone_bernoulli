import math
import holoviews as hv
import numpy as np


class LightMedium:
    def __init__(self, v: float) -> None:
        """Light medium in terms of velocity."""
        self.v = v

    @staticmethod
    def n_to_v(n):
        """
        Convert refractive index to velocity.
            n = c / v,
            v = c / n.
        """
        c = 299792458  # m / s
        return c / n

    def __repr__(self) -> str:
        return f"LightMedium(v={self.v:.2e})"


class BernoulliMedium(LightMedium):
    def __init__(self, y: float, g: float = 9.8067) -> None:
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
        self.v = math.sqrt(-2 * g * y)


class BernoulliRay:
    def __init__(self, y: float, angle: float) -> None:
        """Light ray as a vector in the 1st cartesian quadrant. Angles are in radians.
        Specifically made for the experiment."""
        # if (x, y) == (0, 0):
        #     raise ValueError("BernoulliRay cannot be a null vector.")
        self.reflected = False
        self.y = y
        self.angle = angle

    # TODO x, y = 0, 0?
    @property
    def x(self) -> float:
        """Basic x getter."""
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        """Set x in the positive domain."""
        if value < 0:
            raise ValueError("BernoulliRay.x < 0 is invalid.")
        self._x = value

    @property
    def y(self) -> float:
        """Negate y if reflected."""
        return -self._y if self.reflected else self._y

    @y.setter
    def y(self, value: float) -> None:
        """Set y in the positive domain."""
        if value < 0:
            raise ValueError(
                "Bernoulli.y < 0 is invalid. Use Bernoulli.reflected attribute."
            )
        self._y = value

    @property
    def angle(self) -> float:
        """Get the angle of the vector. Caching would add unnecessary complexity."""
        return math.atan2(abs(self.y), self.x)

    @angle.setter
    def angle(self, value: float) -> None:
        """
        Set the angle of the vector in the range (0, pi / 2). Angle is calculated in
        terms of tan(y/x). Keep y, alter x.
        """
        if value >= math.pi / 2 or value <= 0:
            raise ValueError("Angle outside of the domain.")
        self.x = abs(self.y) / math.tan(value)

    def get_incidence(self) -> float:
        """
        Since Ray is a vector, to calculate its angle we imagine a right triangle. This
        function returns the other angle of that triangle. It can be imagines as the
        incidence angle.
        """
        return math.pi / 2 - self.angle

    def propagate(self, medium1: type[LightMedium], medium2: type[LightMedium]) -> None:
        """
        Propagate the ray from medium1 to medium2. Assume reflection under critical
        angle. Can only reflect once. Total internal reflection occurs when v2 > v1.

        Determine whether light can refract using the Law of Refraction:
            sin(alpha_1) / sin(alpha_2) = v1 / v2,
            alpha_2 = arcsin(v2 / v1 * sin(alpha_1)).
        If out of domain reflect using the Law of Reflection:
            alpha_1 = alpha_2.
            sin(alpha_1) / sin(alpha_2) = v1 / v2.
        """
        alpha_1 = self.get_incidence()
        v1, v2 = medium1.v, medium2.v
        alpha_2 = (v2 / v1) * math.sin(alpha_1)
        if alpha_2 >= 1 and v2 > v1:  # reflect
            self.reflected = True
        else:  # refract
            self.angle = math.pi / 2 - math.asin(alpha_2)

    def __repr__(self) -> str:
        return f"LightRay(x={self.x:.2e}, y={self.y:.2e}, angle={self.angle:.2e})"


class ConstructBrachistochrone:
    def __init__(
        self, init_angle: float, step_height: float = 1e-1, g: float = 9.8067
    ) -> None:
        """Construct the Brachistochrone curve. Altered cutoff points for velocity."""
        self.ray = BernoulliRay(step_height, init_angle)
        self.x, self.y = self.ray.x, -self.ray.y
        self.points = [(0, 0), (self.x, self.y)]

        self.step_height = step_height
        self.g = g

    def step(self) -> bool:
        """Step forward. Returns False when next steps are finished."""
        try:
            m1 = BernoulliMedium(self.y, g=self.g)
            m2 = BernoulliMedium(self.y - self.ray.y, g=self.g)
            self.ray.propagate(m1, m2)
        except ValueError:
            return False

        self.x += self.ray.x
        self.y -= self.ray.y
        self.points.append((self.x, self.y))

        return True
