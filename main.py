import sys
import pygame

from settings import *
from stock import Stock


class Button:
    def __init__(self, x, y, width, height, color, func=lambda: None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.func = func

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def func(self) -> ():
        return self.func()


class Main:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Stock Sim")

        self.stock = Stock("FTSE100", 20, 1000)
        self.day = 0

        self.buttons = [
            Button(20, 540, 60, 40, "red", lambda: self.stock.change_value(1)),
            Button(100, 540, 60, 40, "blue", lambda: self.stock.change_value(-1)),
            Button(180, 540, 60, 40, "green", self.tick)
        ]

    def tick(self):
        self.stock.update_historic_price(self.day)
        self.day += 1

    def draw_chart(self):
        for day in range(self.day):
            change = self.stock.historic_price[day][0] - self.stock.historic_price[day - 1][0]

            height = change / (self.stock.stock_ceiling - self.stock.stock_floor) * 200
            width = 8
            x = 20 + day * 10
            y = self.stock.historic_price[day - 1][0] / (self.stock.stock_ceiling - self.stock.stock_floor) * 200 + 100
            color = "green"

            if change < 0:
                color = "red"
                height *= -1
                y -= height

            pygame.draw.rect(
                self.window,
                color,
                (x, y, width, height))

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

            for button in self.buttons:
                pygame.draw.rect(self.window, button.color, button.rect)

            self.draw_chart()

            pygame.display.flip()


if __name__ == '__main__':
    main = Main()
    main.run()
