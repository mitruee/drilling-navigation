from src.core.visualization.graphics_2d import TwoInterval, ThreeInterval, TangentialFourInterval, TangentialFiveInterval, FourInterval, Tangential, Descending, Ascending, Undulant, DirectionalProfile, HorizontalProfile
import numpy as np
from abc import ABC, abstractmethod
from math import *


class ProfileGraphic(ABC):
    """Абстрактный класс, описывающий график профиля скважины"""

    @abstractmethod
    def __init__(self, profile, axes, start_point=(0.0, 0.0)):
        axes.axis('equal')
        axes.set_xlim(-profile.A * 2, profile.A * 2)
        axes.set_ylim(-profile.H - 500, 0)
        axes.grid(True, alpha=0.3)

        self.profile, self.axes = profile, axes

        x0, y0 = start_point
        x = [x0] + profile.dislocations
        y = [y0] + list(map(lambda depth: -depth, profile.depths))

        self.x, self.y = x, y

        coordinates = list(zip(np.repeat(x, 2), np.repeat(y, 2)))[1:-1]

        self.pairs_of_points = [[coordinates[i], coordinates[i + 1]] for i in range(0, len(coordinates) - 1, 2)]
        self.radii = profile.radii

    def draw_straight(self, start_point, end_point, linewidth):
        """Метод для построения прямых участков профиля скважины"""

        x1, y1 = start_point
        x2, y2 = end_point

        if x1 == x2:
            label = 'Вертикальный участок'
        else:
            label = 'Участок стабилизации'

        self.axes.plot([x1, x2], [y1, y2], label=label, linewidth=linewidth)

    @abstractmethod
    def draw_arc(self, start_point, end_point, radius, linewidth):
        """Абстрактное метод для построения кривых участков профиля скважины"""
        raise NotImplementedError

    def draw(self):
        """Метод для добавления участков профиля скважины на график"""

        for i in range(len(self.pairs_of_points)):
            if not self.radii[i]:
                self.draw_straight(*self.pairs_of_points[i], linewidth=2.3)
            else:
                self.draw_arc(*self.pairs_of_points[i], self.radii[i], linewidth=2.4)

        self.axes.legend(loc='lower left', fontsize=9)


class DirectionalProfilesGraphic(ProfileGraphic):
    """Класс, описывающий график направляющей части профиля скважины"""

    def __init__(self, direction_profile, axes):
        if not isinstance(direction_profile, DirectionalProfile):
            raise TypeError(f"Unsupported profile type: {type(direction_profile)}")
        super().__init__(direction_profile, axes)

    def draw_arc(self, start_point, end_point, radius, linewidth):

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

        if center_y < -y2:
            label = 'Стабилизация зенитного угла'
        else:
            label = 'Набор зенитного угла'

        self.axes.plot(x, y, label=label, linewidth=linewidth)


class HorizontalProfilesGraphic(ProfileGraphic):
    """Класс, описывающий график горизонтальной части профиля скважины"""

    def __init__(self, horizontal_profile, axes):
        if not isinstance(horizontal_profile, HorizontalProfile):
            raise TypeError(f"Unsupported profile type: {type(horizontal_profile)}")
        super().__init__(horizontal_profile, axes, start_point=(horizontal_profile.A, -horizontal_profile.H))

    def draw_arc(self, start_point, end_point, radius, linewidth):
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

            label = 'Горизонтальный участок (восходящий)'

        if isinstance(self.profile, Descending):
            center_x = -radius * cos(pi - angle_b2 - angle_y) + x1
            center_y = -radius * cos(pi - angle_b1 - angle_y) - y2
            circle = lambda x: center_y + (radius ** 2 - (x - center_x) ** 2) ** 0.5

            label = 'Горизонтальный участок (нисходящий)'

        if isinstance(self.profile, Undulant):

            #Код

            label = 'Горизонтальный участок (Волнообразный)'

        x = np.linspace(x1, x2, 100)
        y = circle(x)

        self.axes.plot(x, y, label=label, linewidth=linewidth)