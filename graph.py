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
        pygame.draw.rect(self.window, Color.WHITE, self.rect, 0, 6)
        self.candle(stock_data)

    def candle(self, stock_data) -> None:
        for d in range(stock_data.day):
            top = self.map(
                stock_data.stock.stock_floor,
                stock_data.stock.stock_ceiling,
                self.y + self.height,
                self.y,
                stock_data.stock.historic_price[d].value
            )
            bottom = self.map(
                stock_data.stock.stock_floor,
                stock_data.stock.stock_ceiling,
                self.y + self.height,
                self.y,
                stock_data.stock.historic_price[d - 1].value
            )
            color = Color.GREEN

            if bottom < top:
                top, bottom = bottom, top
                color = Color.RED

            rect = pygame.Rect(GRAPH_X + d * 10, top, 8, bottom - top)

            high = self.map(
                stock_data.stock.stock_floor,
                stock_data.stock.stock_ceiling,
                self.y + self.height,
                self.y,
                stock_data.stock.historic_price[d].high
            )
            low = self.map(
                stock_data.stock.stock_floor,
                stock_data.stock.stock_ceiling,
                self.y + self.height,
                self.y,
                stock_data.stock.historic_price[d].low
            )

            high = (GRAPH_X + d * 10 + 3, high)
            low = (GRAPH_X + d * 10 + 3, low)

            pygame.draw.rect(self.window, color, rect)
            pygame.draw.line(self.window, color, high, low, 2)

    @staticmethod
    def map(min_value: int, max_value: int, min_y: int, max_y: int, value: int) -> int:
        height = max_y - min_y  # height of the graph
        diff = max_value - min_value  # difference in stock price

        unit = abs(int(height / diff))  # how big 1 unit should be

        position = min_y - (value - min_value) * unit  # mapped position to graph

        return position
