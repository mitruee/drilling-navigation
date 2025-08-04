from math import *
from abc import ABC, abstractmethod


class HorizontalProfile(ABC):
    """Абстрактный класс, описывающий горизонтальную часть профиля скважины"""

    _NAMES = ['H', 'A', 'a', 'S_l', 'T1', 'T1']

    H: float # проектная глубина направляющей части профиля
    A: float # проектное смещение скважины на проектной глубине
    a: float # величина зенитного угла в начале горизонтального участка
    S_l: float # протяженность горизонтального участка по пласту
    T1: float # предельные отклонения оси горизонтального участка в поперечном направлении
    T2: float # <<<------>>>

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


class Tagential(HorizontalProfile):
    """Класс, описывающий тангенциальный профиль"""

    @property
    def H_h(self):
        return self.S_l * cos(self.a) + self.H

    @property
    def A_h(self):
        return self.S_l * sin(self.a) + self.H


class Descending(HorizontalProfile):
    """Класс, описывающий нисходящий профиль"""

    @property
    def R_h(self):
        return (self.S_l**2 + self.T2**2) / 2 * self.T2

    @property
    def H_h(self):
        return self.S_l * cos(self.a) - self.T2 * sin(self.a) + self.H

    @property
    def A_h(self):
        return self.S_l * sin(self.a) - self.T2 * cos(self.a) + self.A

    @property
    def a_h(self):
        return self.a - asin(self.S_l / self.R_h)


class Ascending(HorizontalProfile):
    """Класс, описывающий восходящий профиль"""

    @property
    def R_h(self):
        return (self.S_l**2 + self.T1**2) / 2 * self.T1

    @property
    def H_h(self):
        return self.S_l * cos(self.a) + self.T1 * sin(self.a) + self.H

    @property
    def A_h(self):
        return self.S_l * sin(self.a) + self.T1 * cos(self.a) + self.A

    @property
    def a_h(self):
        return self.a + asin(self.S_l / self.R_h)

# class Undulant(HorizontalProfile):
    """Класс, описывающий волнообразный профиль"""