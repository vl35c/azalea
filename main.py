import sys
import pygame

from settings import *
from simulation.stock import Stock
from simulation.variance import Variance
from render.graph import Graph
from render.font import Font
from render.button import Button


class StockData:
    def __init__(self, day: int, stock: Stock):
        self.day = day
        self.stock = stock


class Main:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Stock Sim")

        self.stock = Stock("FTSE100", 20, 1000)
        self.day = 0

        self.buttons = [
            Button(20, 540, 60, 40, Color.AQUAMARINE, text="tick",
                   func=self.tick)
        ]

        self.graph = Graph(GRAPH_X, GRAPH_Y, GRAPH_WIDTH, GRAPH_HEIGHT)

        self.stock_data = StockData(self.day, self.stock)

        self.font = Font()
        self.variance = Variance()

    def tick(self) -> None:
        for i in range(24):
            change = self.variance.iterate()
            self.stock.set_value(change)

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
            self.font.render(f'{self.stock.name}: ${self.stock.share_value:.2f}', True, (255, 255, 255), (100, 0))

            for button in self.buttons:
                button.draw()
                button.render()

            self.graph.draw(self.stock_data)

            pygame.display.flip()


if __name__ == '__main__':
    main = Main()
    main.run()
