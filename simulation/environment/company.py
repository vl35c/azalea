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
        "CANADA",
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
        if prev_char in CONSONANTS:
            if random.random() < 0.8:
                return random.choice(VOWELS)
            else:
                return random.choice(CONSONANTS)
        else:
            if random.random() < 0.25:
                return random.choice(VOWELS)
            else:
                return random.choice(CONSONANTS)


