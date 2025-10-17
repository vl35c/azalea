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
        print(self.sectors_effect)
        print(self.countries_effect)
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
    def add_missing_sectors(sectors_effect: dict[str, float]) -> dict[str, float]:
        for sector in Company.sectors:
            if sector not in sectors_effect:
                sectors_effect[sector] = 1.0
        return sectors_effect

    @staticmethod
    def add_missing_countries(countries_effect: dict[str, float]) -> dict[str, float]:
        for country in Company.countries:
            if country not in countries_effect:
                countries_effect[country] = 1.0
        return countries_effect

    @staticmethod
    def change_effects_default(effect_type: str, names: list[str], values: list[float]) -> dict[str, float]:
        effect_dict = Event.default_sectors_effect if effect_type == 'sectors' else Event.default_countries_effect
        return Event.change_effects(effect_dict, names, values)

    @classmethod
    def generate_random_w_desc(cls, desc: str) -> Self:
        countries_affected = list(set(random.sample(Company.countries, random.randint(1, len(Company.countries)))))
        sectors_affected = list(set(random.sample(Company.sectors, random.randint(1, len(Company.sectors)))))
        countries_random = {country: random.uniform(0.8,1.2) for country in countries_affected}
        sectors_random = {sector: random.uniform(0.8, 1.2) for sector in sectors_affected}
        full_countries = Event.add_missing_countries(countries_random)
        full_sectors = Event.add_missing_sectors(sectors_random)

        return cls(random.randint(0, 100000), random.randint(1, 30), random.randint(1, 24),
                   desc, full_sectors, full_countries
        )





class Events:
    def __init__(self):
        # dictionary of Day : (Dict Time : Event)
        self.events: dict[int, dict[int, list[Event]]] = {}

    def generate_random_events(self) -> None:
        event_descs = [
            'SOUTH KOREA GOES TO WAR WITH SOUTH AFRICA OVER SOUTH DISPUTE',
            'AGI OFFICIALLY SCRAPPED',
            'DONALD TRUMP JR JR JR BECOMES NEW PRESIDENT',
            'DONALD TRUMP JR JR JR INTRODUCES MORE TARIFFS',
            'METEOR HITS SOUTH SUDAN',
            'MONACO FINDS LARGEST OIL RESERVE UNDER PARKING LOT',
            'VIETNAM CHANGES OFFICIAL LANGUAGE TO KAZAKH',
            'BODY FOUND IN GERMAN CHANCELLOR WINE CELLAR'
        ]

        for event_desc in event_descs:
            temp_event = Event.generate_random_w_desc(event_desc)
            try:
                self.events[temp_event.date][temp_event.time].append(temp_event)
            except KeyError:
                try:
                    self.events[temp_event.date][temp_event.time] = [temp_event]
                except KeyError:
                    self.events[temp_event.date] = {}
                    self.events[temp_event.date][temp_event.time] = [temp_event]
