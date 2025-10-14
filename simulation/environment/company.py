import random
import string
from settings import *
'''
Sectors:
- Tech
- Finance
- Health
- Industrial
- Defense
- Mining

Countries:
- UK
- USA
- CHINA
- RUSSIA
- GERMANY
- ITALY
- JAPAN
- SOUTH KOREA
- SOUTH AFRICA
- BRAZIL
- SAUDI ARABIA
'''

from simulation.stock import Stock


class Company:
    countries = [
        "UK",
        "USA",
        "CHINA",
        "RUSSIA",
        "GERMANY",
        "ITALY",
        "JAPAN",
        "SOUTH KOREA",
        "SOUTH AFRICA",
        "BRAZIL",
        "SAUDI ARABIA"
    ]

    sectors = [
        "Tech",
        "Finance",
        "Health",
        "Industrial",
        "Defense",
        "Mining"
    ]

    @staticmethod
    def generate_stock() -> Stock:
        return Stock(
            Company.__generate_random_name(),
            random.choice(Company.countries),
            random.choice(Company.sectors),
            1 + random.random() * 59,
            random.randint(1, 100) * 100
        )

    @staticmethod
    def __generate_random_name():
        name = random.choice(string.ascii_uppercase)
        for i in range(random.randint(2, 4)):
            name += Company.__pick_next_char(name[-1])
        return name

    @staticmethod
    def __pick_next_char(prev_char: str):
        table = ALPHA_TABLE[prev_char]
        letters = string.ascii_uppercase
        position = random.random() * sum(table)  # generate a random number in the distribution of characters

        char_dict = {i: (letters[i], table[i]) for i in range(len(ALPHA_TABLE))}
        
        while position > (m := max([v[1] for v in char_dict.values()])):  # loop until found position of number
            position -= m

            char_dict.pop(max(char_dict, key=lambda k: char_dict[k][1]))  # remove letter starting from most common

        return sorted(char_dict.values(), key=lambda x: x[1], reverse=True)[0][0]  # return most populous character left

