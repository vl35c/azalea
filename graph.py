import pygame


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
        pygame.draw.rect(self.window, "white", self.rect)
        self.candle(stock_data)

    def candle(self, stock_data) -> None:
        for d in range(stock_data.day):
            top = self.map(
                stock_data.stock.stock_floor,
                stock_data.stock.stock_ceiling,
                self.y + self.height,
                self.y,
                stock_data.stock.historic_price[d][0]
            )
            bottom = self.map(
                stock_data.stock.stock_floor,
                stock_data.stock.stock_ceiling,
                self.y + self.height,
                self.y,
                stock_data.stock.historic_price[d - 1][0]
            )
            color = "green"

            if bottom < top:
                top, bottom = bottom, top
                color = "red"

            rect = pygame.Rect(20 + d * 10, top, 8, bottom - top)

            pygame.draw.rect(self.window, color, rect)

    @staticmethod
    def map(min_value: int, max_value: int, min_y: int, max_y: int, value: int) -> int:
        height = max_y - min_y  # height of the graph
        diff = max_value - min_value  # difference in stock price

        unit = abs(int(height / diff))  # how big 1 unit should be

        position = min_y - (value - min_value) * unit  # mapped position to graph

        return position