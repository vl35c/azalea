import random
from typing import Self

from simulation.environment.company import Company
from simulation.stock_list import StockList


class Event:
    default_sectors_effect = {s:1 for s in Company.sectors}
    default_countries_effect = {c:1 for c in Company.countries}

    def __init__(self, event_id: int, date: int, time: int, description: str,
                 sectors_effect: dict[str, float], countries_effect: dict[str, float]):
        self.event_id = event_id
        self.date = date
        self.time = time
        self.description = description
        self.sectors_effect = sectors_effect
        self.countries_effect = countries_effect

    def update_stock_prices(self, stock_list: StockList) -> None:
        for stock in stock_list.stock_list:
            for sector in Company.sectors:
                if stock.sector == sector:
                    stock.change_value(self.sectors_effect[sector])

            for country in Company.countries:
                if stock.country == country:
                    stock.change_value(self.countries_effect[country])

    @staticmethod
    def change_effects(effect_dict: dict[str, float], names: list[str], values: list[float]) -> dict[str, float]:
        for name, value in zip(names, values):
            if name in effect_dict:
                effect_dict[name] = value
        return effect_dict

    @staticmethod
    def change_effects_default(effect_type: str, names: list[str], values: list[float]) -> dict[str, float]:
        effect_dict = Event.default_sectors_effect if effect_type == 'sectors' else Event.default_countries_effect
        return Event.change_effects(effect_dict, names, values)

    @classmethod
    def generate_random_w_desc(cls, desc: str) -> Self:
        countries_effected = list(set(random.sample(Company.countries, random.randint(1, len(Company.countries)))))
        sectors_effected = list(set(random.sample(Company.sectors, random.randint(1, len(Company.sectors)))))
        countries_random_values = [random.uniform(-0.9,1.1) for _ in range(len(countries_effected))]
        sectors_random_values = [random.uniform(-0.9, 1.1) for _ in range(len(sectors_effected))]
        return cls(random.randint(0, 100000), random.randint(1, 30), random.randint(1, 24), desc,)





class Events:
    def __init__(self):
        # dictionary of Day : (Dict Time : Event)
        self.events: dict[int, dict[int, Event]] = {}

    def generate_random_events(self, date: int) -> None:
        event_desc = [
            'SOUTH KOREA GOES TO WAR WITH SOUTH AFRICA OVER SOUTH DISPUTE',
            'AGI OFFICIALLY SCRAPPED',
            'DONALD TRUMP JR JR JR BECOMES NEW PRESIDENT',
            'DONALD TRUMP JR JR JR INTRODUCES MORE TARIFFS',

