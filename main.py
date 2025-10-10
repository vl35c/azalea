import sys
import pygame

from settings import *
from simulation.stock import Stock
from simulation.variance import Variance
from render.graph import Graph
from render.font import Font
from render.button import Button
from input.mouse_handler import MouseHandler


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
        self.stock = Stock("FTSE100", 20, 1000)
        self.day = 0
        self.stock_data = StockData(self.day, self.stock)

        # buttons
        self.buttons = [
            Button(20, 540, 60, 40, Color.AQUAMARINE, text="tick",
                   func=self.tick),
            Button(100, 540, 60, 40, Color.RED, text="week",
                   func=lambda: [self.tick() for _ in range(7)])
        ]

        # graph
        self.graph = Graph(GRAPH_X, GRAPH_Y, GRAPH_WIDTH, GRAPH_HEIGHT)

        # misc.
        self.font = Font()
        self.variance = Variance()
        self.mouse = MouseHandler()

    def tick(self) -> None:
        for i in range(24):  # iterate 24 times in 1 day to get daily highs and lows
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
        else:
            if self.graph.rect.collidepoint(mx, my):
                self.mouse.click(self.graph)

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

            if pygame.mouse.get_pressed()[0]:
                if self.mouse.obj == self.graph:
                    self.graph.handle_held(self.mouse)

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

            self.graph.draw(self.stock_data)

            pygame.display.flip()


if __name__ == '__main__':
    main = Main()
    main.run()
