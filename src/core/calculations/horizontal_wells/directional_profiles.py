from math import *
from abc import ABC, abstractmethod


class DirectionalProfile(ABC):
    """Абстрактный класс, описывающий направляющую часть профиля скважины"""

    _NAMES = ['H', 'A', 'a', 'a1', 'R1', 'R3', 'a3', 'R4']

    H: float # проектная глубина направляющей части профиля
    A: float # проектное смещение скважины на проектной глубине
    a: float # величина зенитного угла на проектной глубине (угол вхождения в пласт)
    a1: float # величина зенитного угла в конце 1-ого участка профиля
    R1: float # величина радиуса 1-ого участка
    R3: float # величина радиуса 3-ого участка
    a3: float # величина зенитного угла в конце 3-ого участка профиля
    R4: float # величина радиуса 4-ого участка

    def __init__(self, *args):
        self.__dict__.update(zip(self._NAMES, args))

    @property
    @abstractmethod
    def R(self):
        """Абстрактное свойство для расчёта радиуса кривизны"""
        raise NotImplementedError

    @property
    @abstractmethod
    def H_v(self):
        """Абстрактное свойство для расчёта длины вертикального участка"""
        raise NotImplementedError

    @property
    @abstractmethod
    def L(self):
        """Абстрактное свойство для расчёта длины участка стабилизации"""
        raise NotImplementedError

    @property
    @abstractmethod
    def intensities(self):
        """Абстрактное свойство для расчёта длины участка стабилизации"""
        raise NotImplementedError


class TwoInterval(DirectionalProfile):
    """Класс, описывающий двухинтервальную направляющую часть"""

    @property
    def R(self):
        return self.A / (1 - cos(radians(self.a)))

    @property
    def H_v(self):
        return self.H - self.R * sin(radians(self.a))

    @property
    def L(self):
        return super().L

    @property
    def depth(self):
        return [
            self.H_v,
            self.H
        ]

    @property
    def lengths_of_the_bores(self):
        return [
            self.H_v,
            self.H_v + (pi * self.R * self.a) / 180
        ]

    @property
    def lengths_of_the_intervals(self):
        return [
            self.H_v,
            self.lengths_of_the_bores[1] - self.lengths_of_the_bores[0]
        ]

    @property
    def dislocations(self):
        return [
            0,
            self.A
        ]

    @property
    def angles(self):
        return [
            0,
            self.a
        ]

    @property
    def intensities(self):
        return [
            0,
            57.3 / (self.R / 10)
        ]


class ThreeInterval(DirectionalProfile):
    """Класс, описывающий трёхинтервальную направляющую часть"""

    @property
    def R(self):
        return self.A - ((self.R1 * (1 - cos(radians(self.a1)))) / (cos(radians(self.a1)) - cos(radians(self.a))))

    @property
    def H_v(self):
        return self.H - self.R1 * sin(radians(self.a1)) - self.R * (sin(radians(self.a)) - sin(radians(self.a1)))

    @property
    def L(self):
        return super().L

    @property
    def depth(self):
        return [
            self.H_v,
            self.H_v + self.R1 * sin(radians(self.a1)),
            self.H
        ]

    @property
    def lengths_of_the_bores(self):
        return [
            self.H_v,
            self.H_v + (pi * self.R1 * self.a1) / 180,
            self.H_v + (pi * (self.R1 * self.a1 + self.R * (self.a - self.a1))) / 180
        ]

    @property
    def lengths_of_the_intervals(self):
        return [
            self.H_v,
            self.lengths_of_the_bores[1] - self.lengths_of_the_bores[0],
            self.lengths_of_the_bores[2] - self.lengths_of_the_bores[1]
        ]

    @property
    def dislocations(self):
        return [
            0,
            self.R1 * (1 - cos(radians(self.a1))),
            self.A
        ]

    @property
    def angles(self):
        return [
            0,
            self.a1,
            self.a
        ]

    @property
    def intensities(self):
        return [
            0,
            57.3 / (self.R1 / 10),
            57.3 / (self.R / 10)
        ]


class TanFourInterval(DirectionalProfile):
    """Класс, описывающий четырёхинтервальную тангенциальную направляющую часть с участком стабилизации"""

    @property
    def R(self):
        return super().R

    @property
    def H_v(self):
        return self.H - self.R1 * sin(radians(self.a1)) - self.R3 * self.W - self.L * cos(radians(self.a1))

    @property
    def L(self):
        return (self.A - self.R1 * (1 - cos(radians(self.a1))) - self.R3 * self.V) / sin(radians(self.a1))

    @property
    def W(self):
        return sin(self.a) - sin(self.a1)

    @property
    def V(self):
        return cos(self.a1) - cos(self.a)

    @property
    def dislocations(self):
        return [
            0,
            self.R1 * (1 - cos(radians(self.a1))),
            self.R1 * (1 - cos(radians(self.a1))) + self.L * sin(radians(self.a1)),
            self.A
        ]

    @property
    def angles(self):
        return [
            0,
            self.a1,
            self.a1,
            self.a
        ]

    @property
    def intensities(self):
        return [
            0,
            57.3 / (self.R1 / 10),
            0,
            57.3 / (self.R3 / 10)
        ]


class TanFiveInterval(DirectionalProfile):
    """Класс, описывающий пятиинтервальную направляющую часть с участком стабилизации"""

    @property
    def R(self):
        return super().R

    @property
    def H_v(self):
        return self.H - self.R1 * sin(radians(self.a1)) - self.R3 * self.W2  - self.L * cos(radians(self.a1)) - self.R4 * self.W3

    @property
    def L(self):
        return (self.A - self.R1 * (1 - cos(radians(self.a1))) - self.R3 * self.V2 - self.R4 * self.V3) / sin(radians(self.a1))

    @property
    def W2(self):
        return sin(radians(self.a3)) - sin(radians(self.a1))

    @property
    def W3(self):
        return sin(radians(self.a)) - sin(radians(self.a3))

    @property
    def V2(self):
        return cos(radians(self.a1)) - cos(radians(self.a3))

    @property
    def V3(self):
        return cos(radians(self.a3)) - cos(radians(self.a))

    @property
    def depths(self):
        return [
            self.H_v,
            self.H_v + self.R1 * sin(radians(self.a1)),
            self.H_v + self.R1 * sin(radians(self.a1)) + self.L * cos(radians(self.a1)),
            self.H_v + self.R1 * sin(radians(self.a1)) + self.L * cos(radians(self.a1)) + self.R3 * self.W2,
            self.H
        ]

    @property
    def lengths_of_the_bores(self):
        return [
            self.H_v,
            self.H_v + (pi * self.R1 * self.a1) / 180,
            self.H_v + self.L + (pi * (self.R1 * self.a1)) / 180,
            self.H_v + self.L + (pi * (self.R1 * self.a1 + self.R3 * (self.a3 - self.a1))) / 180,
            self.H_v + self.L + (pi * (self.R1 * self.a1 + self.R3 * (self.a3 - self.a1) + self.R4 * (self.a - self.a3))) / 180,
        ]

    @property
    def lengths_of_the_intervals(self):
        return [
            self.H_v,
            self.lengths_of_the_bores[1] - self.lengths_of_the_bores[0],
            self.lengths_of_the_bores[2] - self.lengths_of_the_bores[1],
            self.lengths_of_the_bores[3] - self.lengths_of_the_bores[2],
            self.lengths_of_the_bores[4] - self.lengths_of_the_bores[3]
        ]

    @property
    def dislocations(self):
        return [
            0,
            self.R1 * (1 - cos(radians(self.a1))),
            self.R1 * (1 - cos(radians(self.a1))) + self.L * sin(radians(self.a1)),
            self.R1 * (1 - cos(radians(self.a1))) + self.L * sin(radians(self.a1)) + self.R3 * (cos(radians(self.a1)) - cos(radians(self.a3))),
            self.A
        ]

    @property
    def angles(self):
        return [
            0,
            self.a1,
            0,
            self.a3,
            self.a
        ]

    @property
    def intensities(self):
        return [
            0,
            57.3 / (self.R1 / 10),
            0,
            57.3 / (self.R3 / 10),
            57.3 / (self.R4 / 10)
        ]


class FourInterval(DirectionalProfile):
    """Класс, описывающий четырехинтервальную направляющую часть"""

    @property
    def R(self):
        return (self.A - self.R1 * (1 - cos(radians(self.a1))) - self.R3 * self.V4) / self.V5

    @property
    def H_v(self):
        return self.H - self.R1 * sin(radians(self.a1)) - self.R3 * self.W4 - self.R * self.W5

    @property
    def L(self):
        return super().L

    @property
    def W4(self):
        return sin(radians(self.a3)) - sin(radians(self.a1))

    @property
    def W5(self):
        return sin(radians(self.a)) - sin(radians(self.a3))

    @property
    def V4(self):
        return cos(radians(self.a1)) - cos(radians(self.a3))

    @property
    def V5(self):
        return cos(radians(self.a3)) - cos(radians(self.a))

    @property
    def depths(self):
        return [
            self.H_v,
            self.H_v + self.R1 * sin(radians(self.a1)),
            self.H_v + self.R1 * sin(radians(self.a1)) + self.R3 * self.W4,
            self.H
        ]

    @property
    def lengths_of_the_bores(self):
        return [
            self.H_v,
            self.H_v + (pi * self.R1 * self.a1) / 180,
            self.H_v + (pi * (self.R1 * self.a1 + self.R3 * (self.a3 - self.a1))) / 180,
            self.H_v + (pi * (self.R1 * self.a1 + self.R3 * (self.a3 - self.a1) + self.R * (self.a - self.a3))) / 180,
        ]

    @property
    def lengths_of_the_intervals(self):
        return [
            self.H_v,
            self.lengths_of_the_bores[1] - self.lengths_of_the_bores[0],
            self.lengths_of_the_bores[2] - self.lengths_of_the_bores[1],
            self.lengths_of_the_bores[3] - self.lengths_of_the_bores[2]
        ]

    @property
    def dislocations(self):
        return [
            0,
            self.R1 * (1 - cos(radians(self.a1))),
            self.R1 * (1 - cos(radians(self.a1))) + self.R3 * (cos(radians(self.a1)) - cos(radians(self.a3))),
            self.A
        ]

    @property
    def angles(self):
        return [
            0,
            self.a1,
            self.a3,
            self.a
        ]

    @property
    def intensities(self):
        return [
            0,
            57.3 / (self.R1 / 10),
            57.3 / (self.R3 / 10),
            57.3 / (self.R / 10)
        ]