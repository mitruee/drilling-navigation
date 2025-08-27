from math import *
from abc import ABC, abstractmethod


class InclinedProfile(ABC):
    """Абстрактный класс, описывающий профиль наклонной скважины"""

    _NAMES = ['H', 'A', 'H_v', 'R1', 'a1', 'R2']

    H: float # проектная глубина направляющей части профиля (глубина горизонтального участка)
    A: float # проектное смещение скважины на проектной глубине
    H_v: float # длина вертикального участка
    R1: float # радиус кривизны 2-го участка
    a1: float # начальный зенитный угол
    R2: float # радиус кривизны 3-го участка

    @property
    @abstractmethod
    def a(self):
        """Абстрактное свойство для расчета конечного зенитного угла"""
        return NotImplementedError

    @property
    @abstractmethod
    def L(self):
        """Абстрактное свойство для расчета длины участка стабилизации"""
        return NotImplementedError


class TangentialThreeInterval(InclinedProfile):
    """
    Класс, описывающий профиль трехинтервальной тангенциальной скважины
    """

    @property
    def a(self):
        return 2 * atan(radians((self.H - sqrt(self.H**2 - self.A * (2 * self.R1 - self.A))) / (2 * self.R1 - self.A)))

    @property
    def L(self):
        return (self.A - self.R1 * (1 - cos(radians(self.a)))) / sin(radians(self.a))


class TangentialFourInterval(InclinedProfile):
    """
    Класс, описывающий профиль четырехинтервальной тангенциальной скважины
    """

    @property
    def a(self):
        B = self.R1 * (1 - cos(radians(self.a1))) + (self.H - self.H_v - self.R1 * sin(radians(self.a1))) * tan(
            radians(self.a1))
        M = (self.H - self.H_v - self.R1 * sin(radians(self.a1))) + (self.A - B) * sin(radians(self.a1))
        T = (self.A - B) * cos(radians(self.a1))
        return self.a1 + acos((self.R2 * (self.R2 - T) + M * sqrt(M**2 + T**2 - 2 * T * self.R2)) / ((self.R2 - T)**2 +
                                                                                                     M**2))

    @property
    def L(self):
        return super().L


class SShaped(InclinedProfile):
    """
    Класс, описывающий профиль S-образной скважины
    """

    @property
    def a(self):
        B = self.R1 * (1 - cos(radians(self.a1))) + (self.H - self.H_v - self.R1 * sin(radians(self.a1))) * tan(
            radians(self.a1))
        Q = sqrt(2 * self.R2 * abs(self.A - B) * cos(radians(self.a1)) - (self.A - B)**2 * cos(radians(self.a1))**2)
        return self.a1 - atan(Q / sqrt(self.R2**2 - Q**2))

    @property
    def L(self):
        B = self.R1 * (1 - cos(radians(self.a1))) + (self.H - self.H_v - self.R1 * sin(radians(self.a1))) * tan(
            radians(self.a1))
        C = (self.H - self.H_v - self.R1 * sin(radians(self.a1))) / cos(radians(self.a1)) - abs(self.A - B) * sin(
            radians(self.a1))
        Q = sqrt(2 * self.R2 * abs(self.A - B) * cos(radians(self.a1)) - (self.A - B)**2 * cos(radians(self.a1))**2)
        return C - Q


class JShaped(InclinedProfile):
    """
    Класс, описывающий профиль J-образной скважины
    """

    @property
    def a(self):
        B = (self.R1 * (1 - cos(radians(self.a1))) + (self.H - self.H_v - self.R1 * sin(radians(self.a1))) *
             tan(radians(self.a1)))
        Q = sqrt(2 * self.R2 * abs(self.A - B) * cos(radians(self.a1)) - (self.A - B)**2 * cos(radians(self.a1))**2)
        return self.a1 + atan(Q / sqrt(self.R2**2 - Q**2))

    @property
    def L(self):
        B = (self.R1 * (1 - cos(radians(self.a1))) + (self.H - self.H_v - self.R1 * sin(radians(self.a1))) *
             tan(radians(self.a1)))
        C = ((self.H - self.H_v - self.R1 * sin(radians(self.a1))) / cos(radians(self.a1)) + abs(self.A - B) *
             sin(radians(self.a1)))
        Q = sqrt(2 * self.R2 * abs(self.A - B) * cos(radians(self.a1)) - (self.A - B)**2 * cos(radians(self.a1))**2)
        return C - Q