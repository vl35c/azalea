import sys
import pygame

from settings import *
from simulation.stock import Stock
from render.graph import Graph
from render.font import Font
from render.button import Button


class StockData:
    def __init__(self, day: int, s: Stock):
        self.day = day
        self.stock = s


class Main:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Stock Sim")

        self.stock = Stock("FTSE100", 20, 1000)
        self.day = 0

        self.buttons = [
            Button(20, 540, 60, 40, Color.RED, text="inc",
                   func=lambda: self.stock.change_value(1)),
            Button(100, 540, 60, 40, Color.BLUE, text="dec",
                   func=lambda: self.stock.change_value(-1)),
            Button(180, 540, 60, 40, Color.AQUAMARINE, text="tick",
                   func=self.tick)
        ]

        self.graph = Graph(GRAPH_X, 100, GRAPH_WIDTH, 200)

        self.stock_data = StockData(self.day, self.stock)

        self.font = Font()

    def tick(self):
        self.stock.update_price_record(self.day)
        self.day += 1
        self.stock_data.day += 1

    def handle_mouse(self) -> None:
        mx, my = pygame.mouse.get_pos()

        for button in self.buttons:
            if button.rect.collidepoint(mx, my):
                button.func()
                break

    def run(self) -> None:
        while True:
            self.window.fill(Color.BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse()

            self.font.render(f'Day: {self.day}', True, (255, 255, 255), (0, 0))
            self.font.render(f'Stock Price: {self.stock.share_value}', True, (255, 255, 255), (100, 0))

            for button in self.buttons:
                button.draw()
                button.render()

            self.graph.draw(self.stock_data)

            pygame.display.flip()


if __name__ == '__main__':
    main = Main()
    main.run()
