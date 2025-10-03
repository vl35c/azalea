import pygame

from settings import *


class Graph:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.window = pygame.display.get_surface()

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, stock_data) -> None:
        pygame.draw.rect(self.window, Color.WHITE, self.rect, 0, GRAPH_CORNER_ROUNDING)
        self.candle(stock_data)

    def candle(self, stock_data) -> None:
        max_candles = int(GRAPH_WIDTH / CANDLE_SPACING)
        offset = stock_data.day - max_candles if stock_data.day > max_candles else 0

        for d in range(min(stock_data.day, max_candles)):
            d += offset
            # closing price
            top = self.map(
                stock_data.stock.bound.floor,
                stock_data.stock.bound.ceiling,
                self.y + self.height,
                self.y,
                stock_data.stock.historic_price[d].value
            )
            # opening price
            bottom = self.map(
                stock_data.stock.bound.floor,
                stock_data.stock.bound.ceiling,
                self.y + self.height,
                self.y,
                stock_data.stock.historic_price[d - 1].value
            )

            # green for increase, red for decrease, grey for no change
            color = self.__candle_color(top, bottom)
            # top > bottom in terms of screen position -> higher y value on screen = lower value
            if top > bottom:
                top, bottom = bottom, top

            # daily high
            high = self.map(
                stock_data.stock.bound.floor,
                stock_data.stock.bound.ceiling,
                self.y + self.height,
                self.y,
                stock_data.stock.historic_price[d].high
            )
            # daily low
            low = self.map(
                stock_data.stock.bound.floor,
                stock_data.stock.bound.ceiling,
                self.y + self.height,
                self.y,
                stock_data.stock.historic_price[d].low
            )

            # remove offset for placing on graph
            d -= offset

            rect = pygame.Rect(GRAPH_X + d * CANDLE_SPACING, top, CANDLE_WIDTH, bottom - top)
            high = (GRAPH_X + d * CANDLE_SPACING + (CANDLE_WIDTH - 2) / 2, high)
            low = (GRAPH_X + d * CANDLE_SPACING + (CANDLE_WIDTH - 2) / 2, low)

            pygame.draw.rect(self.window, color, rect)
            pygame.draw.line(self.window, color, high, low, CANDLE_LINE_WIDTH)

    @staticmethod
    def map(min_value: int, max_value: int, min_y: int, max_y: int, value: int) -> int:
        height = max_y - min_y  # height of the graph
        diff = max_value - min_value  # difference in stock price
        unit = abs(height / diff)  # how big 1 unit should be
        position = min_y - (value - min_value) * unit  # mapped position to graph

        return position

    @staticmethod
    def __candle_color(top: int, bottom: int) -> Color:
        if top < bottom:
            return Color.GREEN
        elif top > bottom:
            return Color.RED
        else:
            return Color.GREY
