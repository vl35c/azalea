import math

from random import random


class Variance:
    def __init__(self):
        self.__total = 0

    def iterate(self) -> float:
        self.__total += (random() - 0.5) * 0.7
        return 20 * math.e ** (self.__total / 24)
