from src.core.calculations.horizontal_wells.directional_profiles import *
from src.core.calculations.horizontal_wells.horizontal_profiles import *
import matplotlib.pyplot as plt
import numpy as np


class ProfileGraphic(ABC):
    @abstractmethod
    def __init__(self, profile, axes, start_point=(0.0, 0.0)):
        axes.set_xlim(-profile.H - 500, profile.H + 500)
        axes.set_ylim(-profile.H - 500, 0)
        axes.axis('equal')

        self.profile, self.axes = profile, axes

        x0, y0 = start_point
        x = [x0] + profile.dislocations
        y = [y0] + list(map(lambda depth: -depth, profile.depths))

        coordinates = list(zip(np.repeat(x, 2), np.repeat(y, 2)))[1:-1]

        self.pairs_of_points = [[coordinates[i], coordinates[i + 1]] for i in range(0, len(coordinates) - 1, 2)]
        self.radii = profile.radii

    def draw_straight(self, start_point, end_point):
        x1, y1 = start_point
        x2, y2 = end_point
        self.axes.plot([x1, x2], [y1, y2])

    @abstractmethod
    def draw_arc(self, start_point, end_point, radius):
        raise NotImplementedError

    def draw(self):
        for i in range(len(self.pairs_of_points)):
            if not self.radii[i]:
                self.draw_straight(*self.pairs_of_points[i])
            else:
                self.draw_arc(*self.pairs_of_points[i], self.radii[i])


class DirectionalProfilesGraphic(ProfileGraphic):
    def __init__(self, direction_profile, axes):
        if not isinstance(direction_profile, DirectionalProfile):
            raise TypeError(f"Unsupported profile type: {type(direction_profile)}")
        super().__init__(direction_profile, axes)

    def draw_arc(self, start_point, end_point, radius):
        x1, y1 = start_point
        x2, y2 = end_point

        y1, y2 = -y1, -y2

        angle_b1 = atan((x2 - x1) / (y2 - y1))
        angle_b2 = atan((y2 - y1) / (x2 - x1))
        angle_y = acos(sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) / (2 * radius))

        center_x = radius * sin(pi - angle_b1 - angle_y) + x1
        center_y = radius * sin(pi - angle_b2 - angle_y) - y2
        circle = lambda x: center_y - (radius ** 2 - (x - center_x) ** 2) ** 0.5

        x = np.linspace(x1, x2, 100)
        y = circle(x)

        self.axes.plot(x, y)


class HorizontalProfilesGraphic(ProfileGraphic):
    def __init__(self, horizontal_profile, axes):
        if not isinstance(horizontal_profile, HorizontalProfile):
            raise TypeError(f"Unsupported profile type: {type(horizontal_profile)}")
        super().__init__(horizontal_profile, axes, start_point=(horizontal_profile.A, -horizontal_profile.H))

    def draw_arc(self, start_point, end_point, radius):
        x1, y1 = start_point
        x2, y2 = end_point

        y1, y2 = -y1, -y2

        angle_b1 = atan((x2 - x1) / (y2 - y1))
        angle_b2 = atan((y2 - y1) / (x2 - x1))
        angle_y = acos(sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) / (2 * radius))

        if isinstance(self.profile, Ascending):
            center_x = radius * sin(pi - angle_b1 - angle_y) + x1
            center_y = radius * sin(pi - angle_b2 - angle_y) - y2
            circle = lambda x: center_y - (radius ** 2 - (x - center_x) ** 2) ** 0.5

        if isinstance(self.profile, Descending):
            center_x = -radius * cos(pi - angle_b2 - angle_y) + x1
            center_y = -radius * cos(pi - angle_b1 - angle_y) - y2
            circle = lambda x: center_y + (radius ** 2 - (x - center_x) ** 2) ** 0.5

        x = np.linspace(x1, x2, 100)
        y = circle(x)

        self.axes.plot(x, y)


fig1, axes1 = plt.subplots(figsize=(6, 6))

directional_profile = DirectionalProfilesGraphic(TangentialFourInterval(1678, 900, 40, 30, 382, 1900), axes1)
horizontal_profile = HorizontalProfilesGraphic(Descending(1678, 900, 70, 100, 20), axes1)

directional_profile.draw()
horizontal_profile.draw()
plt.show()

fig2, axes2 = plt.subplots(figsize=(6, 6))

directional_profile = DirectionalProfilesGraphic(ThreeInterval(1600, 400, 30, 40, 400), axes2)
horizontal_profile = HorizontalProfilesGraphic(Descending(1600, 400, 70, 100, 20), axes2)

directional_profile.draw()
horizontal_profile.draw()
plt.show()