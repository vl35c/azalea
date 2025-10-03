from simulation.stock import Stock


class Buyer:
    def __init__(self) -> None:
        self.stocks: list[Stock] = []

    def buy_stock(self, stock: Stock) -> None:
        self.stocks.append(stock)
