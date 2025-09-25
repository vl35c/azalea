class Stock:
    def __init__(self, name: str, share_value: float, total_shares: int):
        self.name = name
        self.share_value = share_value
        self.total_shares = total_shares
        self.historic_price: dict[int: float] = {-1: share_value}  # key: date, value: price

        self.stock_floor = int(share_value / 2)
        self.stock_ceiling = share_value * 2

    # changes a stocks value
    def change_value(self, value: float):
        self.share_value += value

    def update_historic_price(self, date: int):
        self.historic_price[date] = self.share_value
