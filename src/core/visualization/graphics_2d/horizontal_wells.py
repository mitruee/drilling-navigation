from src.core.calculations.horizontal_wells.directional_profiles import *
from src.core.calculations.horizontal_wells.horizontal_profiles import *
from functools import singledispatchmethod
import matplotlib.pyplot as plt
import numpy as np


class DirectionalProfilesGraphic:
    def __init__(self, direction_profile, horizontal_profile):

        if not isinstance(direction_profile, DirectionalProfile):
            raise TypeError(f"Unsupported profile type: {type(direction_profile)}")
        if not isinstance(horizontal_profile, HorizontalProfile):
            raise TypeError(f"Unsupported profile type: {type(horizontal_profile)}")

        self.direction_profile, self.horizontal_profile = direction_profile, horizontal_profile

        x = [0.0] + direction_profile.dislocations + horizontal_profile.dislocations
        y = [0.0] + list(map(lambda depth: -depth, direction_profile.depths + horizontal_profile.depths))

        self.x, self.y = x, y

        coordinates = list(zip(np.repeat(x, 2), np.repeat(y, 2)))[1:-1]

        self.pairs_of_points = [[coordinates[i], coordinates[i + 1]] for i in range(0, len(coordinates) - 1, 2)]
        self.radii = direction_profile.radii + horizontal_profile.radii
        self.fig, self.ax = plt.subplots(figsize=(6, 6))

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

        # center_x = -radius * cos(pi - angle_b2 - angle_y) + x1
        # center_y = -radius * cos(pi - angle_b1 - angle_y) - y2
        # circle = lambda x: center_y + (radius ** 2 - (x - center_x) ** 2) ** 0.5

        # self.ax.scatter(center_x, center_y)

        x = np.linspace(x1, x2, 100)
        y = circle(x)

        self.ax.plot(x, y)

    def draw_straight(self, start_point, end_point):
        x1, y1 = start_point
        x2, y2 = end_point
        self.ax.plot([x1, x2], [y1, y2])

    def draw_part(self, start_point, end_point, radius):
        if not radius:
            self.draw_straight(start_point, end_point)
        else:
            self.draw_arc(start_point, end_point, radius)

    def draw(self):
        for i in range(len(self.pairs_of_points)):
            self.draw_part(*self.pairs_of_points[i], self.radii[i])

        self.ax.set_xlim(-self.direction_profile.H - 500, self.direction_profile.H + 500)
        self.ax.set_ylim(-self.direction_profile.H - 500, 0)
        self.ax.axis('equal')

        plt.tight_layout()
        plt.show()


# profile = DirectionalProfilesGraphic(TwoInterval(1600, 400, 90))
# profile = DirectionalProfilesGraphic(ThreeInterval(1600, 400, 30, 40, 400))
profile = DirectionalProfilesGraphic(TangentialFourInterval(1678, 900, 40, 30, 382, 1900), Ascending(1678, 900, 70, 100, 20))
print(profile.horizontal_profile.__dict__)
profile.draw()