import numpy as np

class Interval:
    def __init__(self, lower, upper):
        if lower > upper:
            raise ValueError("Lower bound cannot be greater than upper bound.")
        self.lower = lower
        self.upper = upper

    def __repr__(self):
        return f"[{self.lower}, {self.upper}]"

    # Средняя точка интервала
    def mid(self):
        return (self.lower + self.upper) / 2

    # Ширина интервала
    def width(self):
        return self.upper - self.lower

    # Сложение интервалов
    def __add__(self, other):
        if isinstance(other, Interval):
            return Interval(self.lower + other.lower, self.upper + other.upper)
        return Interval(self.lower + other, self.upper + other)

    # Вычитание интервалов
    def __sub__(self, other):
        if isinstance(other, Interval):
            return Interval(self.lower - other.upper, self.upper - other.lower)
        return Interval(self.lower - other, self.upper - other)

    # Умножение интервалов
    def __mul__(self, other):
        if isinstance(other, Interval):
            products = np.array([
                self.lower * other.lower,
                self.lower * other.upper,
                self.upper * other.lower,
                self.upper * other.upper
            ])
            return Interval(np.min(products), np.max(products))
        return Interval(self.lower * other, self.upper * other)

    # Деление интервалов
    def __truediv__(self, other):
        if isinstance(other, Interval):
            # if other.lower <= 0 <= other.upper:
            #     raise ZeroDivisionError("Interval includes zero, cannot divide.")
            divisions = np.array([
                self.lower / other.lower,
                self.lower / other.upper,
                self.upper / other.lower,
                self.upper / other.upper
            ])
            return Interval(np.min(divisions), np.max(divisions))
        return Interval(self.lower / other, self.upper / other)

    # Принадлежность числа интервалу
    def __contains__(self, value):
        return self.lower <= value <= self.upper

    # Пересечение интервалов
    def __and__(self, other):
        new_lower = max(self.lower, other.lower)
        new_upper = min(self.upper, other.upper)
        if new_lower > new_upper:
            return Interval(0, 0)  # Возвращаем пустой интервал
        return Interval(new_lower, new_upper)

    # Объединение интервалов
    def __or__(self, other):
        return Interval(min(self.lower, other.lower), max(self.upper, other.upper))
