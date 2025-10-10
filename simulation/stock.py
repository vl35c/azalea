from settings import *
from typing import Self
from simulation.variance import Variance

class Stock:
    def __init__(self, name: str, share_value: float, total_shares: int):
        self.name = name
        self.share_value = share_value
        self.total_shares = total_shares
        # key: date, value: (closing, low, high)
        # also uses day -1 to start simulation with a value
        self.historic_price: dict[int: ShareData] = {}
        # bound stores the ceiling and floor values for the graph to contain the values
        self.bound: ShareData = ShareData.from_high_low(int(share_value / 2), int(share_value * 2))
        # current day stores the daily highs and lows
        self.current_day: ShareData = ShareData.from_value(share_value)
        # all time stores the all-time highs and lows
        self.all_time: ShareData = ShareData.from_value(share_value)
        self.variance: Variance = Variance(share_value)

    def store_value_data(self) -> None:
        self.current_day.greater_swap(self.share_value)
        self.current_day.lesser_swap(self.share_value)

        self.all_time.greater_swap(self.current_day.high)
        self.all_time.lesser_swap(self.current_day.low)

    # changes a stocks value
    def change_value(self, value: float) -> None:
        self.share_value *= value
        self.share_value = max(self.share_value, 0.01)

        self.store_value_data()

    # sets a stocks value
    def set_value(self, value: float) -> None:
        self.share_value = value
        self.share_value = max(self.share_value, 0.01)

        self.store_value_data()

    def update_price_record(self, date: int) -> None:
        self.historic_price[date] = ShareData.from_full(
            self.current_day.open_v,
            self.share_value,  # share value when updating day becomes closing value
            self.current_day.low,
            self.current_day.high
        )

        self.current_day.open_v = self.share_value
        self.current_day.low = self.share_value
        self.current_day.high = self.share_value

        self.bound.ceiling = int(self.all_time.high * HIGH_FACTOR)
        self.bound.floor = int(self.all_time.low * LOW_FACTOR)


class ShareData:
    def __init__(self, open_v: float, close_v: float, high: float, low: float):
        self.open_v = open_v  # open_v is opening value
        self.close_v = close_v  # close_v is closing value
        self.high = high
        self.low = low
        self.ceiling = high
        self.floor = low

    @classmethod
    def from_value(cls, value: float) -> Self:
        return cls(value, value, value, value)

    @classmethod
    def from_full(cls, open_v: float, close_v: float, high: float, low: float) -> Self:
        return cls(open_v, close_v, low, high)

    @classmethod
    def from_v_h_l(cls, value: float, high: float, low: float) -> Self:
        return cls(value, value, high, low)

    @classmethod
    def from_high_low(cls, low: float, high: float) -> Self:
        return cls(-1, -1, low, high)

    # evaluate and swap if greater
    def greater_swap(self, value: float) -> None:
        if value > self.high:
            self.high = value

    # evaluate and swap if less
    def lesser_swap(self, value: float) -> None:
        if value < self.low:
            self.low = value
