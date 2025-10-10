import pygame

from settings import *
from render.font import Font
from render.renderer import Renderer
from input.mouse_handler import MouseHandler


class Graph:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.window = pygame.display.get_surface()
        self.font = Font()
        self.renderer = Renderer()

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    # add tuples
    @staticmethod
    def __add_tuples(t1: tuple, t2: tuple) -> tuple[int, int]:
        return t1[0] + t2[0], t1[1] + t2[1]

    # return candle color based on graph position
    @staticmethod
    def __candle_color(top: int, bottom: int) -> str:
        if top < bottom:
            return Color.GREEN
        elif top > bottom:
            return Color.RED
        else:
            return Color.GREY

    # returns column (candle) of graph
    @staticmethod
    def __get_column(x: int) -> int:
        x -= GRAPH_X  # adjust x so that left edge of graph is coordinate (0,_)
        return x // CANDLE_SPACING

    @staticmethod
    def __clamp(min_value: int, max_value: int, value: int) -> int:
        return max(min_value, min(max_value, value))

    # linearly interpolate between 2 values
    @staticmethod
    def map(min_value: int, max_value: int, min_y: int, max_y: int, value: int) -> int:
        height = max_y - min_y  # height of the graph
        diff = max_value - min_value  # difference in stock price
        unit = abs(height / diff)  # how big 1 unit should be
        position = min_y - (value - min_value) * unit  # mapped position to graph

        return int(position)

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
                stock_data.stock.historic_price[d].open_v
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
    def highlight_candle(self, start_position: int, end_position: int=-1) -> None:
        x = GRAPH_X + start_position * CANDLE_SPACING
        y = GRAPH_Y
        height = GRAPH_HEIGHT
        if end_position == -1:
            width = CANDLE_WIDTH
        else:
            end_position = self.__clamp(0, GRAPH_WIDTH // CANDLE_SPACING, end_position)
            width = (end_position - start_position) * CANDLE_SPACING

        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.window, Color.LIGHT_GREY, rect, 0, GRAPH_CORNER_ROUNDING)

    # shows pricing data when hovering on candle
    def candle_data(self, day: int, stock_data) -> None:
        day_offset = day + max(stock_data.day - GRAPH_WIDTH // CANDLE_SPACING, 0)

        opening_price = stock_data.stock.historic_price[day_offset].open_v
        closing_price = stock_data.stock.historic_price[day_offset].close_v
        day_low = stock_data.stock.historic_price[day_offset].low
        day_high = stock_data.stock.historic_price[day_offset].high

        close_percentage = (closing_price - opening_price) / closing_price * 100
        low_percentage = (day_low - opening_price) / day_low * 100
        high_percentage = (day_high - opening_price) / day_high * 100

        mouse_x, mouse_y = pygame.mouse.get_pos()
        origin = self.__add_tuples((mouse_x, mouse_y), (16 if mouse_x < SCREEN_WIDTH - 300 else -216, 10))
        rect = pygame.Rect(*origin, 200, 80)
        pygame.draw.rect(self.window, Color.LIGHT_BLACK, rect, 0, GRAPH_CORNER_ROUNDING)

        self.font.render(f"{'Open:':<6} ${opening_price:.2f}",
                         True, Color.WHITE, self.__add_tuples(origin, (4, 0)))
        self.font.render(f"{'Close:':<6} ${closing_price:.2f}  {close_percentage:.1f}%",
                         True, Color.WHITE, self.__add_tuples(origin, (4, 20)))
        self.font.render(f"{'High:':<6} ${day_high:.2f}  {high_percentage:.1f}%",
                         True, Color.WHITE, self.__add_tuples(origin, (4, 40)))
        self.font.render(f"{'Low:':<6} ${day_low:.2f}  {low_percentage:.1f}%",
                         True, Color.WHITE, self.__add_tuples(origin, (4, 60)))

    def hover(self, stock_data) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if not self.rect.collidepoint(mouse_x, mouse_y):
            return

        column = self.__get_column(mouse_x)

        # if viewing column which for data does not exist, error will occur
        if column >= stock_data.day:
            return

        # render on different layers, need candles rendered between these 2, hence z layers
        self.renderer.hold(lambda: self.highlight_candle(column), 1)
        self.renderer.hold(lambda: self.candle_data(column, stock_data), 3)

    def handle_held(self, mouse: MouseHandler):
        c1 = self.__get_column(mouse.x)  # initial column
        c2 = self.__get_column(pygame.mouse.get_pos()[0])  # current column
        c2 = c2 + 1 if c2 > c1 else c2  # if end is bigger than start, cover hovered column as well

        self.renderer.hold(lambda: self.highlight_candle(c1, c2), 1)
