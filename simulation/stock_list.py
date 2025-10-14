import csv
from typing import Any

from simulation.stock import Stock
from simulation.environment.company import Company


class StockList:
    def __init__(self):
        self.stock_list: list[Stock] = []

    def generate_stocks(self, count: int) -> None:
        self.stock_list = [Company.generate_stock() for _ in range(count)]

    def load_stocks(self, filename: str):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.add_stock(row['Name'], float(row['Share Value']), int(row['Total Shares']))

    def add_stock(self, name: str, share_value: float, total_shares: int) -> None:
        self.stock_list.append(Stock(name, "", "", share_value, total_shares))

    def stock_names(self) -> list[str]:
        return [stock.name for stock in self.stock_list]

    def select_stock(self, name: str) -> Any | None:
        for stock in self.stock_list:
            if stock.name == name:
                return stock
        return None

    def select_stocks(self, user_input: str) -> list[str]:
        if user_input == "":
            return []

        return [stock.name for stock in self.stock_list if user_input.lower() in stock.name.lower()][:4]