import math

from random import random


class Variance:
    def __init__(self, stock_price: float):
        self.__total = 0
        self.__stock_price: float = stock_price

    def iterate(self) -> float:
        self.__total += (random() - 0.5) * 0.7
        return self.__stock_price * math.e ** (self.__total / 24)
