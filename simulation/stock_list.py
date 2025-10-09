from typing import Any
import csv

from simulation.stock import Stock

class StockList:
    def __init__(self):
        self.stock_list: [Stock] = []


    def load_stocks(self, filename: str):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.add_stock(row['Name'], float(row['Share Value']), int(row['Total Shares']))

    def add_stock(self, name: str, share_value: float, total_shares: int) -> None:
        self.stock_list.append(Stock(name, share_value, total_shares))

    def stock_names(self) -> [str]:
        return [s.name for s in self.stock_list]

    def select_stock(self, name: str) -> Any | None:
        for s in self.stock_list:
            if s.name == name:
                return s
        return None