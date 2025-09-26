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

    def draw(self, day: int, prices: dict[int: tuple[float]]) -> None:
        pygame.draw.rect(self.window, "white", self.rect)
        self.candle(day, prices)

    def candle(self, day: int, prices: dict[int: tuple[float]]) -> None:
        for d in range(day):
            top = self.map(10, 40, self.y + self.height, self.y, prices[d][0])
            bottom = self.map(10, 40, self.y + self.height, self.y, prices[d - 1][0])
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