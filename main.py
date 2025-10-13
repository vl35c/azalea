import sys
import pygame

from settings import *
from simulation.stock import Stock
from simulation.stock_list import StockList
from render.graph import Graph
from render.font import Font
from render.button import Button
from input.mouse_handler import MouseHandler
from render.textinput import TextInput


class StockData:
    def __init__(self, day: int, stock: Stock):
        self.day = day
        self.stock = stock


class Main:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Azalea")
        logo = pygame.image.load("assets/images/azalea-logo.png")
        pygame.display.set_icon(logo)

        # background
        self.background = pygame.image.load("assets/images/azalea-logo-dark.png").convert_alpha()
        self.background.set_alpha(30)
        self.background = pygame.transform.smoothscale_by(self.background, 0.75)

        # stocks
        self.stock_list = StockList()
        self.stock_list.load_stocks("assets/data/stocks.csv")
        self.stock = self.stock_list.select_stock("NASDAQ")
        self.day = 0
        self.stock_data = StockData(self.day, self.stock)

        # buttons
        self.buttons = [
            Button(20, 540, 60, 40, Color.WHITE, Color.AQUAMARINE, text="tick",
                   func=self.tick)
        ]
        self.text_inputs_buttons = []

        self.text_inputs = [
            TextInput((SCREEN_WIDTH // 2 - 100), 10, 200, 40, Color.BLACK, Color.LIGHT_GREY,
                      "Search Stock", self.stock_list.select_stocks, self.change_stock)
        ]

        # graph
        self.mouse = MouseHandler()
        self.graph = Graph(GRAPH_X, GRAPH_Y, GRAPH_WIDTH, GRAPH_HEIGHT, self.mouse)

        # misc.
        self.font = Font()

    def tick(self) -> None:
        for stock in self.stock_list.stock_list:
            for i in range(24):  # 24 ticks to update it 24 times in 1 day
                change = stock.variance.iterate()  # iterate each stock's price
                stock.set_value(change)

            stock.update_price_record(self.day)

        self.day += 1
        self.stock_data.day += 1

    def handle_mouse(self) -> None:
        mx, my = pygame.mouse.get_pos()

        for button in self.buttons + self.text_inputs_buttons:
            if button.rect.collidepoint(mx, my):
                button.func()
                break
        else:
            if self.graph.rect.collidepoint(mx, my):
                self.mouse.click(self.graph)

        for text_input in self.text_inputs:
            clicked_on = text_input.rect.collidepoint(mx, my)

            if not text_input.active and clicked_on:
                text_input.activate()
            elif text_input.active and not clicked_on:
                text_input.deactivate()

    def handle_key_press(self, event) -> None:
        if (text_input := self.find_active_text_input()) is None:
            return

        if event.key == pygame.K_BACKSPACE:
            text_input.remove_char()

        if event.unicode.isalpha() or event.unicode.isnumeric():
            letter = event.unicode
            self.text_inputs_buttons = text_input.on_type(letter)

    def find_active_text_input(self) -> TextInput | None:
        for text_input in self.text_inputs:
            if text_input.active:
                return text_input
        return None

    def change_stock(self, stock: str) -> None:
        if (stock_str_arr := self.stock_list.select_stocks(stock)) is not None:
            stock = self.stock_list.select_stock(stock_str_arr[0])
            self.stock = stock
            self.stock_data.stock = stock

    def run(self) -> None:
        while True:
            self.window.fill(Color.BLACK)
            self.window.blit(self.background,
                             (
                                 (SCREEN_WIDTH - self.background.get_width()) / 2,
                                 (SCREEN_HEIGHT - self.background.get_height()) / 2)
                             )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # mouse clicked
                        self.handle_mouse()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse.release()
                if event.type == pygame.KEYDOWN:
                    self.handle_key_press(event)

            if pygame.mouse.get_pressed()[0]:
                if self.mouse.obj == self.graph:
                    self.graph.handle_held(self.stock_data)

            self.font.render(
                f'Day: {self.day}',
                True,
                (255, 255, 255),
                (0, 0)
            )
            self.font.render(
                f'{self.stock.name}: ${self.stock.share_value:.2f}',
                True,
                (255, 255, 255),
                (100, 0)
            )

            for button in self.buttons:
                button.draw()
                button.render()

            for text_input in self.text_inputs:
                text_input.draw()
                text_input.render()

            self.graph.draw(self.stock_data)

            for button in self.text_inputs_buttons:
                button.draw()
                button.render()

            pygame.display.flip()


if __name__ == '__main__':
    main = Main()
    main.run()
