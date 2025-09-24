import sys
import pygame

from settings import *


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

        self.buttons = [
            Button(100, 100, 100, 100, "red", lambda: print("I am red")),
            Button(300, 100, 100, 100, "blue", lambda: print("I am blue"))
        ]

    def handle_mouse(self) -> None:
        mx, my = pygame.mouse.get_pos()

        for button in self.buttons:
            if button.rect.collidepoint(mx, my):
                button.func()


    def run(self):
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

            pygame.display.flip()



if __name__ == '__main__':
    main = Main()
    main.run()
