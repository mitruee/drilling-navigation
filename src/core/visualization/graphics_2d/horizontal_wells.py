from src.core.calculations.horizontal_wells.directional_profiles import *
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import numpy as np
from functools import singledispatchmethod


class DirectionalProfilesGraphics:
    @singledispatchmethod
    def __init__(self, obj):
        raise TypeError

    @__init__.register
    def _from_correct(self, obj: DirectionalProfile):
        self.obj = obj
        self.depths = [0] + list(map(lambda x: -x, obj.depth))
        self.dislocations = [0] + obj.dislocations
        self.coordinates = tuple(zip(self.dislocations, self.depths))

    @staticmethod
    def draw_arc(H, A, H_v, R):
        angle_b1 = atan(A / (H - H_v))
        angle_b2 = atan((H - H_v) / A)
        angle_y = acos(sqrt(A ** 2 + (H - H_v) ** 2) / (2 * R))

        center_x = R * sin(pi - angle_b1 - angle_y)
        center_y = R * sin(pi - angle_b2 - angle_y) - H

        arc = Arc(
            (-center_x, center_y),
            width=center_x * 2,
            height=-center_x * 2,
            angle=0,
            theta1=0,
            theta2=-well.a,
            linewidth=2,
            color='red'
        )

    @staticmethod
    def draw_vertical(coordinates):
        x1, y1 = coordinates[0]
        x2, y2 = coordinates[1]
        plt.plot([x1, x2], [y1, y2])



well = DirectionalProfilesGraphics(TwoInterval(1600, 400, 90))
print(well.coordinates)





# depths = [0] + list(map(lambda x: -x, well.depth))
# dislocations = [0] + well.dislocations
#
# print(depths)
# print(dislocations)
#

#
#     ax.add_patch(arc)
#     ax.set_xlim(-1000, 1000)
#     ax.set_ylim(-2000, 0)
#     ax.set_aspect('equal')
#
#
# fig, ax = plt.subplots(figsize=(6, 6))
#
# plt.plot(dislocations[:2], depths[:2])
# plt.scatter(well.H - well.H_v, -well.H_v, color='red')
# plt.scatter(dislocations[-1], depths[-1])
# plt.scatter(-dislocations[-1], depths[-1])
#
# draw_arc(well.H, well.A, well.H_v, well.R)
#
# print(sin(pi/2 - radians(well.a)) * well.R)
# print(well.R, well.A)
#
#
# plt.show()