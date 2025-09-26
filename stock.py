class Stock:
    def __init__(self, name: str, share_value: float, total_shares: int):
        self.name = name
        self.share_value = share_value
        self.total_shares = total_shares
        self.historic_price: dict[int: DayShare] = {-1: DayShare(share_value, share_value, share_value)}  # key: date, value: (closing, low, high)

        self.stock_floor: int = int(share_value / 2)
        self.stock_ceiling: int = int(share_value * 2)

        self.current_high_day: float = share_value
        self.current_low_day: float = share_value

        self.all_time_high_day: float = share_value
        self.all_time_low_day: float = share_value

    # changes a stocks value
    def change_value(self, value: float):
        self.share_value += value

        if self.share_value > self.current_high_day: self.current_high_day = self.share_value
        elif self.share_value < self.current_low_day: self.current_low_day = self.share_value

        if self.current_high_day > self.all_time_high_day: self.all_time_high_day = self.current_high_day
        elif self.current_low_day > self.all_time_low_day: self.all_time_low_day = self.current_low_day

    def update_historic_price(self, date: int):
        self.historic_price[date] = DayShare(self.share_value, self.current_low_day, self.current_high_day)

        self.current_low_day = self.share_value
        self.current_high_day = self.share_value


class DayShare:
    def __init__(self, value: float, low: float, high: float):
        self.value = value
        self.low = low
        self.high = high