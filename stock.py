from settings import *


class Stock:
    def __init__(self, name: str, share_value: float, total_shares: int):
        self.name = name
        self.share_value = share_value
        self.total_shares = total_shares
        self.historic_price: dict[int: ShareData] = {-1: ShareData.from_value(share_value)}  # key: date, value: (closing, low, high)

        self.bound: ShareData = ShareData.from_high_low(int(share_value / 2), int(share_value * 2))

        self.current_day: ShareData = ShareData.from_value(share_value)

        self.all_time: ShareData = ShareData.from_value(share_value)

    # changes a stocks value
    def change_value(self, value: float) -> None:
        self.share_value += value

        if self.share_value < 0:
            self.share_value = 0

        self.current_day.greater_swap(self.share_value) # sets current_day.high to share_value if share_value is greater
        self.current_day.lesser_swap(self.share_value)

        self.all_time.greater_swap(self.current_day.high)
        self.all_time.lesser_swap(self.current_day.low)

    def update_price_record(self, date: int) -> None:
        self.historic_price[date] = ShareData.from_full(self.share_value, self.current_day.low, self.current_day.high)

        self.current_day.low = self.share_value
        self.current_day.high = self.share_value

        self.bound.ceiling = int(self.all_time.high * HIGH_FACTOR)
        self.bound.floor = int(self.all_time.low * LOW_FACTOR)


class ShareData:
    def __init__(self, value: float, low: float, high: float):
        self.value = value
        self.low = low
        self.high = high
        self.ceiling: float = high
        self.floor: float = low

    @classmethod
    def from_value(cls, value: float):
        return cls(value, value, value)

    @classmethod
    def from_full(cls, value: float, low: float, high: float):
        return cls(value, low, high)

    @classmethod
    def from_high_low(cls, low: float, high: float):
        return cls(-1, low, high)


    def greater_swap(self, other: float) -> None:
        if self.high < other:
            self.high = other

    def lesser_swap(self, other: float) -> None:
        if self.low > other:
            self.low = other