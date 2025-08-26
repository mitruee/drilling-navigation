from math import *
from abc import ABC, abstractmethod


class DirectionalProfile(ABC):
    """Абстрактный класс, описывающий направляющую часть профиля скважины"""

    _NAMES = ['H', 'A', 'a', 'a1', 'R1', 'R3', 'a3', 'R4']

    H: float # проектная глубина направляющей части профиля
    A: float # проектное смещение скважины на проектной глубине
    a: float # величина зенитного угла на проектной глубине (угол вхождения в пласт)
    a1: float # начальный зенитный угол
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
    def radii(self):
        """Абстрактное свойство для получения массива радиусов"""
        raise NotImplementedError

    @property
    @abstractmethod
    def depths(self):
        """Абстрактное свойство для расчёта глубин по участкам"""
        raise NotImplementedError

    @property
    @abstractmethod
    def lengths_of_the_bores(self):
        """Абстрактное свойство для расчёта длин стволов по участкам"""
        return NotImplementedError

    @property
    @abstractmethod
    def lengths_of_the_intervals(self):
        """Абстрактное свойство для расчёта длин участков"""
        return NotImplementedError

    @property
    @abstractmethod
    def dislocations(self):
        """Абстрактное свойства для расчёта смещения по участкам"""
        return NotImplementedError

    @property
    @abstractmethod
    def angles(self):
        """Абстрактное свойство для расчёта зенитных углов по участкам"""
        return NotImplementedError

    @property
    @abstractmethod
    def intensities(self):
        """Абстрактное свойство для расчёта интенсивности искривления участков"""
        raise NotImplementedError


class TwoInterval(DirectionalProfile):
    """
    Класс, описывающий двухинтервальную направляющую часть.
    Параметры, необходимые для расчёта свойств объекта:
    :параметр H: float, H > 0, проектная глубина направляющей части профиля;
    :параметр A: float, A >= 0, проектное смещение скважины на проектной глубине;
    :параметр a: float, 0 <= a <= 90, угол вхождения в пласт (градусы);
    """

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
    def radii(self):
        return [
            0.0,
            self.R
        ]

    @property
    def depths(self):
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
            0.0,
            self.A
        ]

    @property
    def angles(self):
        return [
            0.0,
            self.a
        ]

    @property
    def intensities(self):
        return [
            0.0,
            57.3 / (self.R / 10)
        ]


class ThreeInterval(DirectionalProfile):
    """
    Класс, описывающий трёхинтервальную направляющую часть
    Параметры, необходимые для расчёта свойств объекта:
    :параметр H: float, H > 0, проектная глубина направляющей части профиля;
    :параметр A: float, A >= 0, проектное смещение скважины на проектной глубине;
    :параметр a: float, 0 <= a <= 90, угол вхождения в пласт (градусы);
    :параметр a1: float, 0 <= a <= 90, начальный зенитный угол;
    """

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
    def radii(self):
        return [
            0.0,
            self.R1,
            self.R
        ]

    @property
    def depths(self):
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
            0.0,
            self.R1 * (1 - cos(radians(self.a1))),
            self.A
        ]

    @property
    def angles(self):
        return [
            0.0,
            self.a1,
            self.a
        ]

    @property
    def intensities(self):
        return [
            0.0,
            57.3 / (self.R1 / 10),
            57.3 / (self.R / 10)
        ]


class TangentialFourInterval(DirectionalProfile):
    """
    Класс, описывающий четырёхинтервальную направляющую часть с участком стабилизации.
    Параметры, необходимые для расчёта свойств объекта:
    :параметр H: float, H > 0, проектная глубина направляющей части профиля;
    :параметр A: float, A > 0, проектное смещение скважины на проектной глубине;
    :параметр a: float, 0 <= a <= 90, угол вхождения в пласт (градусы);
    :параметр a1: float, 0 <= a <= 90, начальный зенитный угол;
    :параметр R1: float, R1 > 0, величина радиуса 1-ого участка;
    :параметр R3: float, R3 > 0, величина радиуса 3-ого участка;
    """

    @property
    def R(self):
        return super().R

    @property
    def H_v(self):
        W = sin(self.a) - sin(self.a1)
        return self.H - self.R1 * sin(radians(self.a1)) - self.R3 * W - self.L * cos(radians(self.a1))

    @property
    def L(self):
        V = cos(self.a1) - cos(self.a)
        return (self.A - self.R1 * (1 - cos(radians(self.a1))) - self.R3 * V) / sin(radians(self.a1))

    @property
    def radii(self):
        return [
            0.0,
            self.R1,
            0.0,
            self.R3
        ]

    @property
    def depths(self):
        return [
            self.H_v,
            self.H_v + self.R1 * sin(radians(self.a1)),
            self.H_v + self.R1 * sin(radians(self.a1)) + self.L * cos(radians(self.a1)),
            self.H
        ]

    @property
    def lengths_of_the_bores(self):
        return [
            self.H_v,
            self.H_v + (pi * self.R1 * self.a1) / 180,
            self.H_v + self.L + (pi * (self.R1 * self.a1)) / 180,
            self.H_v + self.L + (pi * (self.R1 * self.a1 + self.R3 * (self.a - self.a1))) / 180
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
            0.0,
            self.R1 * (1 - cos(radians(self.a1))),
            self.R1 * (1 - cos(radians(self.a1))) + self.L * sin(radians(self.a1)),
            self.A
        ]

    @property
    def angles(self):
        return [
            0.0,
            self.a1,
            self.a1,
            self.a
        ]

    @property
    def intensities(self):
        return [
            0.0,
            57.3 / (self.R1 / 10),
            0.0,
            57.3 / (self.R3 / 10)
        ]


class TangentialFiveInterval(DirectionalProfile):
    """
    Класс, описывающий пятиинтервальную направляющую часть с участком стабилизации.
    Параметры, необходимые для расчёта свойств объекта:
    :параметр H: float, H > 0, проектная глубина направляющей части профиля;
    :параметр A: float, A > 0, проектное смещение скважины на проектной глубине;
    :параметр a: float, 0 <= a <= 90, угол вхождения в пласт (градусы);
    :параметр a1: float, 0 <= a1 <= 90, начальный зенитный угол;
    :параметр R1: float, R1 > 0, величина радиуса 1-ого участка;
    :параметр R3: float, R3 > 0, величина радиуса 3-ого участка;
    :параметр а3: float, 0 <= a3 <= 90, зенитный угол в конце 3-ого участка;
    :параметр R4: float, R4 > 0, величина радиуса;
    """

    @property
    def R(self):
        return super().R

    @property
    def H_v(self):
        W2, W3 = sin(radians(self.a3)) - sin(radians(self.a1)), sin(radians(self.a)) - sin(radians(self.a3))
        return self.H - self.R1 * sin(radians(self.a1)) - self.R3 * W2  - self.L * cos(radians(self.a1)) - self.R4 * W3

    @property
    def L(self):
        V2, V3 = cos(radians(self.a1)) - cos(radians(self.a3)), cos(radians(self.a3)) - cos(radians(self.a))
        return (self.A - self.R1 * (1 - cos(radians(self.a1))) - self.R3 * V2 - self.R4 * V3) / sin(radians(self.a1))

    @property
    def radii(self):
        return [
            0.0,
            self.R1,
            0.0,
            self.R3,
            self.R4
        ]

    @property
    def depths(self):
        W2 = sin(radians(self.a3)) - sin(radians(self.a1))
        return [
            self.H_v,
            self.H_v + self.R1 * sin(radians(self.a1)),
            self.H_v + self.R1 * sin(radians(self.a1)) + self.L * cos(radians(self.a1)),
            self.H_v + self.R1 * sin(radians(self.a1)) + self.L * cos(radians(self.a1)) + self.R3 * W2,
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
            0.0,
            self.R1 * (1 - cos(radians(self.a1))),
            self.R1 * (1 - cos(radians(self.a1))) + self.L * sin(radians(self.a1)),
            self.R1 * (1 - cos(radians(self.a1))) + self.L * sin(radians(self.a1)) + self.R3 * (cos(radians(self.a1)) - cos(radians(self.a3))),
            self.A
        ]

    @property
    def angles(self):
        return [
            0.0,
            self.a1,
            self.a1,
            self.a3,
            self.a
        ]

    @property
    def intensities(self):
        return [
            0.0,
            57.3 / (self.R1 / 10),
            0.0,
            57.3 / (self.R3 / 10),
            57.3 / (self.R4 / 10)
        ]


class FourInterval(DirectionalProfile):
    """
    Класс, описывающий четырехинтервальную направляющую часть.
    Параметры, необходимые для расчёта свойств объекта:
    :параметр H: float, H > 0, проектная глубина направляющей части профиля;
    :параметр A: float, A > 0, проектное смещение скважины на проектной глубине;
    :параметр a: float, 0 <= a <= 90, угол вхождения в пласт (градусы);
    :параметр a1: float, 0 <= a1 <= 90, начальный зенитный угол;
    :параметр R1: float, R1 > 0, величина радиуса 1-ого участка;
    :параметр R3: float, R3 > 0, величина радиуса 2-ого участка (!!!);
    :параметр а3: float, 0 <= a3 <= 90, зенитный угол в конце 3-ого участка;
    """

    @property
    def R(self):
        V4, V5 = cos(radians(self.a1)) - cos(radians(self.a3)), cos(radians(self.a3)) - cos(radians(self.a))
        return (self.A - self.R1 * (1 - cos(radians(self.a1))) - self.R3 * V4) / V5

    @property
    def H_v(self):
        W4, W5 = sin(radians(self.a3)) - sin(radians(self.a1)), sin(radians(self.a)) - sin(radians(self.a3))
        return self.H - self.R1 * sin(radians(self.a1)) - self.R3 * W4 - self.R * W5

    @property
    def L(self):
        return super().L

    @property
    def radii(self):
        return [
            0.0,
            self.R1,
            self.R3,
            self.R
        ]

    @property
    def depths(self):
        W4 = sin(radians(self.a3)) - sin(radians(self.a1))
        return [
            self.H_v,
            self.H_v + self.R1 * sin(radians(self.a1)),
            self.H_v + self.R1 * sin(radians(self.a1)) + self.R3 * W4,
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
            0.0,
            self.R1 * (1 - cos(radians(self.a1))),
            self.R1 * (1 - cos(radians(self.a1))) + self.R3 * (cos(radians(self.a1)) - cos(radians(self.a3))),
            self.A
        ]

    @property
    def angles(self):
        return [
            0.0,
            self.a1,
            self.a3,
            self.a
        ]

    @property
    def intensities(self):
        return [
            0.0,
            57.3 / (self.R1 / 10),
            57.3 / (self.R3 / 10),
            57.3 / (self.R / 10)
        ]