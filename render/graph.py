import pygame

from settings import *
from render.font import Font
from render.renderer import Renderer


class Graph:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.window = pygame.display.get_surface()
        self.font = Font()
        self.renderer = Renderer()

    @staticmethod
    def __offset_tuple(t1: tuple, t2: tuple) -> tuple:
        return t1[0] + t2[0], t1[1] + t2[1]

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, stock_data) -> None:
        self.renderer.hold(lambda: self.draw_base(), 0)
        self.hover(stock_data)
        self.renderer.hold(lambda: self.draw_data(stock_data), 2)

        self.renderer.call()

    def draw_base(self) -> None:
        pygame.draw.rect(self.window, Color.WHITE, self.rect, 0, GRAPH_CORNER_ROUNDING)

    def draw_data(self, stock_data) -> None:
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
                stock_data.stock.historic_price[d].close_v
            )
            # opening price
            bottom = self.map(
                stock_data.stock.bound.floor,
                stock_data.stock.bound.ceiling,
                self.y + self.height,
                self.y,
                stock_data.stock.historic_price[d - 1].close_v
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

    # draws a background behind a candle to indicate which one is hovered
    def highlight_candle(self, position: int) -> None:
        x = GRAPH_X + position * CANDLE_SPACING
        y = GRAPH_Y
        width = CANDLE_WIDTH
        height = GRAPH_HEIGHT

        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.window, Color.LIGHT_GREY, rect, 0, GRAPH_CORNER_ROUNDING)

    def candle_data(self, day: int, stock_data) -> None:
        opening_price = stock_data.stock.historic_price[day].open_v
        closing_price = stock_data.stock.historic_price[day].close_v
        day_low = stock_data.stock.historic_price[day].low
        day_high = stock_data.stock.historic_price[day].high

        close_percentage = (closing_price - opening_price) / closing_price * 100
        low_percentage = (day_low - opening_price) / day_low * 100
        high_percentage = (day_high - opening_price) / day_high * 100

        origin = self.__offset_tuple(pygame.mouse.get_pos(), (16, 10))
        rect = pygame.Rect(*origin, 200, 80)
        pygame.draw.rect(self.window, Color.LIGHT_BLACK, rect, 0, GRAPH_CORNER_ROUNDING)

        self.font.render(f"{'Open:':<6} ${opening_price:.2f}", True, Color.WHITE,
                         self.__offset_tuple(origin, (4, 0)))
        self.font.render(f"{'Close:':<6} ${closing_price:.2f}  {close_percentage:.1f}%", True, Color.WHITE,
                         self.__offset_tuple(origin, (4, 20)))
        self.font.render(f"{'High:':<6} ${day_high:.2f}  {high_percentage:.1f}%", True, Color.WHITE,
                         self.__offset_tuple(origin, (4, 40)))
        self.font.render(f"{'Low:':<6} ${day_low:.2f}  {low_percentage:.1f}%", True, Color.WHITE,
                         self.__offset_tuple(origin, (4, 60)))

    def hover(self, stock_data) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if not self.rect.collidepoint(mouse_x, mouse_y):
            return

        # map mouse so that top corner of graph is (0,0)
        x, y = mouse_x - GRAPH_X, mouse_y - GRAPH_Y
        candle = x // CANDLE_SPACING

        if candle >= stock_data.day:
            return

        self.renderer.hold(lambda: self.highlight_candle(candle), 1)
        self.renderer.hold(lambda: self.candle_data(candle, stock_data), 3)

    @staticmethod
    def map(min_value: int, max_value: int, min_y: int, max_y: int, value: int) -> int:
        height = max_y - min_y  # height of the graph
        diff = max_value - min_value  # difference in stock price
        unit = abs(height / diff)  # how big 1 unit should be
        position = min_y - (value - min_value) * unit  # mapped position to graph

        return int(position)

    @staticmethod
    def __candle_color(top: int, bottom: int) -> str:
        if top < bottom:
            return Color.GREEN
        elif top > bottom:
            return Color.RED
        else:
            return Color.GREY
