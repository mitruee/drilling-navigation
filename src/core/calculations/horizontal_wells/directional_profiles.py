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
    def H(self):
        """Абстрактное свойство для расчёта длины вертикального участка"""
        raise NotImplementedError

    @property
    @abstractmethod
    def L(self):
        """Абстрактное свойство для расчёта длины участка стабилизации"""
        raise NotImplementedError



class TwoInterval(DirectionalProfile):
    """Класс, описывающий двухинтервальную направляющую часть"""

    @property
    def R(self):
        return self.A / (1 - cos(self.a))

    @property
    def H_v(self):
        return self.H - self.R * sin(self.a)

    @property
    def L(self):
        return super().L



class ThreeInterval(DirectionalProfile):
    """Класс, описывающий трёхинтервальную направляющую часть"""

    @property
    def R(self):
        return self.A - ((self.R1 * (1 - cos(self.a1))) / (cos(self.a1) - cos(self.a)))

    @property
    def H_v(self):
        return self.H - self.R1 * sin(self.a1) - self.R * (sin(self.a) - sin(self.a1))

    @property
    def L(self):
        return super().L



class TanFourInterval(DirectionalProfile):
    """Класс, описывающий четырёхинтервальную направляющую часть с участком стабилизации"""

    @property
    def R(self):
        return super().R

    @property
    def H_v(self):
        W1 = sin(self.a) - sin(self.a1)
        return self.H - self.R1 * sin(self.a1) - self.R3 * W1 - self.L * cos(self.a1)

    @property
    def L(self):
        V = cos(self.a) - cos(self.a1)
        return (self.A - self.R1 * (1 - cos(self.a1)) - self.R3 * V) / sin(self.a)



class TanFiveInterval(DirectionalProfile):
    """Класс, описывающий пятиинтервальную направляющую часть с участком стабилизации"""

    @property
    def R(self):
        return super().R

    @property
    def H_v(self):
        W2, W3 = sin(self.a3) - sin(self.a1), sin(self.a) - sin(self.a3)
        return self.H - self.R1 * sin(self.a1) - self.R3 * W2  - self.L * cos(self.a3) - self.R4 * W3

    @property
    def L(self):
        V2, V3 = cos(self.a1) - cos(self.a3), cos(self.a3) - cos(self.a)
        return (self.A - self.R1 * (1 - cos(self.a1)) - self.R3 * V2 - self.R4 * V3) / sin(self.a1)



class FiveInterval(DirectionalProfile):
    """Класс, описывающий пятиинтервальную направляющую часть"""

    @property
    def R(self):
        V4, V5 = cos(self.a1) - cos(self.a3), cos(self.a3) - cos(self.a1)
        return (self.A - (1 - cos(self.a1)) * self.R1 * V4) / V5

    @property
    def H_v(self):
        W4, W5 = sin(self.a3) - sin(self.a1), sin(self.a) - sin(self.a3)
        return self.H - self.R1 * sin(self.a1) - self.R3 * W4 - self.R * W5

    @property
    def L(self):
        return super().L