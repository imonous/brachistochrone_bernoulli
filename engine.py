import math
import holoviews as hv
import numpy as np

# hv.extension("bokeh")


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


class BernoulliLightMedium(LightMedium):
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
        self.v = math.sqrt(-2 * self.g * y)


class LightRay:
    def __init__(self, x: float, y: float) -> None:
        """Light ray as a vector in the 1st cartesian quadrant. Angles are in radians."""
        if (x, y) == (0, 0):
            raise ValueError("LightRay cannot be a null vector.")
        if x < 0 or y < 0:
            raise ValueError("LightRay must be in the first (cartesian) quadrant.")
        self._x, self._y = x, y
        self.reflected = False

    # TODO x, y = 0, 0?
    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        if value < 0:
            raise ValueError("LightRay.x < 0 is invalid.")
        self._x = value

    @property
    def y(self) -> float:
        return -1 * self._y if self.reflected else self._y

    @y.setter
    def y(self, value: float) -> None:
        if value < 0:
            raise ValueError(
                "LightRay.y < 0 is invalid. Use LightRay.reflected attribute."
            )
        self._y = value

    def get_angle(self) -> float:
        """Get the angle of the vector."""
        return math.atan2(self.y, self.x)

    def set_angle(self, angle: float) -> None:
        """
        Set the angle of the vector in the range [-pi / 2, pi / 2]. If the sign of angle
        does not change, alter x. Otherwise, alter y and or x.

        Angle is calculated in terms of tan(y/x).
        """
        if angle > math.pi / 2 or angle <= 0:
            raise ValueError("Angle outside of the domain.")
        # if math.copysign(angle, self.get_angle()) != angle:
        #     self.y = -self.y
        self.x = self.y / math.tan(angle)

    def get_other_angle(self) -> float:
        """
        Since Ray is a vector, to calculate its angle we imagine a right triangle. This
        function returns the other angle of that triangle.
        """
        angle = self.get_angle()
        return math.pi / 2 - angle
        # return math.copysign(math.pi / 2 - abs(angle), angle)

    def propagate(self, medium1: type[LightMedium], medium2: type[LightMedium]) -> None:
        """
        Propagate the ray from medium1 to medium2.

        Determine whether light can refract using the Law of Refraction:
            sin(alpha_1) / sin(alpha_2) = v1 / v2,
            alpha_2 = arcsin(v2 / v1 * sin(alpha_1)).
        If out of domain return False, otherwise True.

        Reflect the ray using the Law of Reflection:
            alpha_1 = alpha_2.

        Refract the ray from medium1 to medium2 using the Law of Refraction:
            sin(alpha_1) / sin(alpha_2) = v1 / v2.
        The propagate method should be used directly instead of this, as light is not
        always able to refract.

        Assume reflection under critical angle.

        Can only reflect once. Total internal reflection occurs when v2 > v1.
        """
        alpha_1 = self.get_other_angle()
        v1, v2 = medium1.v, medium2.v
        w = (v2 / v1) * math.sin(alpha_1)
        if w == 0:
            raise ValueError("Ege case #1!")
        if abs(w) >= 1 and v2 <= v1:
            raise ValueError("Edge case #2!")
        elif abs(w) >= 1 and v2 > v1:
            self.reflected = True
            # self.y = -self.y
        else:  # refract
            w = math.asin(w)
            # alpha_2 = math.copysign(math.pi / 2 - abs(w), w)
            # self.set_angle(alpha_2)
            self.set_angle(w)

    def __repr__(self) -> str:
        return f"LightRay(x={self.x:.2e}, y={self.y:.2e}, angle={self.get_angle():.2e})"


class ConstructBrachistochrone:
    def __init__(self):
        """Construct the Brachistochrone curve."""
        pass

    def step(self):
        """Step forward."""
        pass


# def trace_light(
#     iterations: int, medium_height: float, init_angle: float
# ) -> list[tuple[float, float]]:
#     ray = LightRay(x=0, y=-medium_height)
#     ray.set_angle(init_angle)
#     x, y = 0, ray.y
#     points = [(0, 0), (ray.x, ray.y)]
#     m1, m2 = BernoulliLightMedium(0), BernoulliLightMedium(0)
#     for _ in range(iterations):
#         if y + ray.y >= 0:
#             break
#         m1.set_v(y)
#         m2.set_v(y + ray.y)
#         ray.propagate(m1, m2)
#         x += ray.x
#         y += ray.y
#         points.append((x, y))
#     return points


# def plot(
#     points: list[tuple[float, float]], medium_height: float, file_path=None, save=False
# ) -> hv.core.layout.Layout:
#     alim = np.max(np.abs(np.array(points)))
#     # lines = hv.HLines(-np.arange(0, alim, medium_height)).opts(
#     #     color="lightgray", line_width=1
#     # )

#     pad = 1e-1
#     xlim = (-alim * pad, alim + alim * pad)
#     ylim = (-alim - alim * pad, alim * pad)
#     curve = hv.Curve(points).opts(xlim=xlim, ylim=ylim, height=650, width=650)

#     # res = lines * curve
#     res = curve
#     if save:
#         # show(hv.render(res))
#         hv.save(res, file_path, fmt="png")
#     return res
