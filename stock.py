class Stock:
    def __init__(self, name: str, share_value: float, total_shares: int):
        self.name = name
        self.share_value = share_value
        self.total_shares = total_shares
        self.historic_price: dict[int: float] = {}  # key: date, value: price

    # changes a stocks value
    def change_value(self, value: float):
        self.share_value += value
        print(f'Stock Value: {self.share_value}')  # DEBUG

    def update_historic_price(self, date: int):
        self.historic_price[date] = self.share_value
        print(f'Stock History: {self.historic_price}')
