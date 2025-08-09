from math import *
from abc import ABC, abstractmethod


class HorizontalProfile(ABC):
    """Абстрактный класс, описывающий горизонтальную часть профиля скважины"""

    _NAMES = ['H', 'A', 'a', 'S_l', 'T1', 'T2', 'R1']

    H: float # проектная глубина направляющей части профиля
    A: float # проектное смещение скважины на проектной глубине
    a: float # величина зенитного угла в начале горизонтального участка
    S_l: float # протяженность горизонтального участка по пласту
    T1: float # предельное смещение горизонтального участка в направлении вверх
    T2: float # предельное смещение горизонтального участка в направлении вниз
    R1: float # радиус кривизны 1-ого участка волнообразного профиля

    def __init__(self, *args):
        self.__dict__.update(zip(self._NAMES, args))

    @property
    @abstractmethod
    def H_h(self):
        """Абстрактное свойство для расчёта вертикальной проекции"""
        raise NotImplementedError

    @property
    @abstractmethod
    def A_h(self):
        """Абстрактное свойство для расчёта горизонтальной проекции"""
        raise NotImplementedError

    @property
    @abstractmethod
    def R_h(self):
        """Абстрактное свойство для расчета радиуса горизонтального участка"""
        raise NotImplementedError

    @property
    @abstractmethod
    def a_h(self):
        """Абстрактное свойство для расчета величины зенитного угла в конце горизонтального участка"""
        raise NotImplementedError
    
    @property
    @abstractmethod
    def L_h(self):
        """Абстрактное свойство для расчета длины горизонтального участка"""
        raise NotImplementedError


class Tangential(HorizontalProfile):
    """Класс, описывающий тангенциальный профиль"""

    @property
    def H_h(self):
        return self.S_l * cos(radians(self.a)) + self.H

    @property
    def A_h(self):
        return self.S_l * sin(radians(self.a)) + self.A
    
    @property
    def L_h(self):
        return super().L_h
    
    @property
    def R_h(self):
        return super().R_h

    @property
    def a_h(self):
        return super().a_h


class Descending(HorizontalProfile):
    """Класс, описывающий нисходящий профиль"""

    @property
    def R_h(self):
        return (self.S_l**2 + self.T2**2) / (2 * self.T2)

    @property
    def H_h(self):
        return self.S_l * cos(radians(self.a)) + self.T2 * sin(radians(self.a)) + self.H

    @property
    def A_h(self):
        return self.S_l * sin(radians(self.a)) - self.T2 * cos(radians(self.a)) + self.A

    @property
    def a_h(self):
        return self.a - degrees(asin(self.S_l / self.R_h))
    
    @property
    def L_h(self):
        return -pi / 180 * (self.a_h - self.a) * self.R_h


class Ascending(HorizontalProfile):
    """Класс, описывающий восходящий профиль"""

    @property
    def R_h(self):
        return ((self.S_l)**2 + (self.T1)**2) / (2 * self.T1)

    @property
    def H_h(self):
        return self.S_l * cos(radians(self.a)) - self.T1 * sin(radians(self.a)) + self.H

    @property
    def A_h(self):
        return self.S_l * sin(radians(self.a)) + self.T1 * cos(radians(self.a)) + self.A

    @property
    def a_h(self):
        return self.a + degrees(asin(self.S_l / self.R_h))
    
    @property
    def L_h(self):
        return pi / 180 * (self.a_h - self.a) * self.R_h


class Undulant(HorizontalProfile):
    """Класс, описывающий волнообразный профиль"""

    @property
    def R_h(self):
        K = self.S_l ** 2 + 2 * (self.R1 + self.T2) + self.T2 ** 2
        J = 8 * self.S_l ** 2 * self.R1 * self.T1 - 4 * self.S_l ** 2 * self.T1 ** 2 - K ** 2
        F = 4 * K * self.T2 + 8 * self.S_l ** 2 * self.T1
        return (-F + sqrt(F ** 2 + 16 * self.T2 ** 2 * J)) / (-8 * self.T2 ** 2)

    @property
    def H_h(self):
        return self.S_l * cos(self.a) + self.T2 * sin(self.a) + self.H

    @property
    def A_h(self):
        return self.S_l * sin(self.a) - self.T2 * cos(self.a) + self.A

    @property
    def a_h(self):
        return self.a - asin(sqrt(2 * self.R_h * (self.T1 + self.T2) - (self.T1 - self.T2) ** 2) / self.R_h)

    def L_h(self):
        return super().L_h