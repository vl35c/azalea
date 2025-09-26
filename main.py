import sys
import pygame

from settings import *
from stock import Stock
from graph import Graph


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
            Button(20, 540, 60, 40, "crimson", lambda: self.stock.change_value(1)),
            Button(100, 540, 60, 40, "cadetblue4", lambda: self.stock.change_value(-1)),
            Button(180, 540, 60, 40, "aquamarine4", self.tick)
        ]

        self.graph = Graph(20, 100, 760, 200)

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

            pygame.font.init()
            my_font = pygame.font.SysFont("monospace", 15, True)
            text_surface = my_font.render(f'Day: {self.day}', True, (255, 255, 255))
            self.window.blit(text_surface, (0,0))

            text_surface = my_font.render(f'Stock Price: {self.stock.share_value}', True, (255, 255, 255))
            self.window.blit(text_surface, (100, 0))



            for button in self.buttons:
                pygame.draw.rect(self.window, button.color, button.rect)

            text_surface = my_font.render('inc', True, (255, 255, 255))
            self.window.blit(text_surface, (30, 550))

            text_surface = my_font.render('dec', True, (255, 255, 255))
            self.window.blit(text_surface, (110, 550))

            text_surface = my_font.render('tick', True, (255, 255, 255))
            self.window.blit(text_surface, (190, 550))

            self.graph.draw(self.day, self.stock.historic_price)
            #self.draw_chart()

            pygame.display.flip()


if __name__ == '__main__':
    main = Main()
    main.run()
