import pygame

from settings import *
from render.font import Font


class Button:
    def __init__(self, x, y, width, height, color, text=None, func=lambda: None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.func = func

        self.window = pygame.display.get_surface()
        self.font = Font()

    # creates a tuple containing the position of the top left corner
    @property
    def pos(self) -> tuple[int, int]:
        return self.x, self.y

    # creates a pygame.Rect encompassing the button
    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    # calls buttons functions
    def func(self) -> ():
        return self.func()

    # calculate position to center text in button
    def __centred_text(self, text_object: str) -> tuple[int, int]:
        text_object = self.font.string_to_surface(text_object)

        x = self.x + (self.width - text_object.get_width()) / 2
        y = self.y + (self.height - text_object.get_height()) / 2

        return x, y

    # draw buttons
    def draw(self) -> None:
        pygame.draw.rect(self.window, self.color, self.rect, 0, 8)

    # render text on button
    def render(self) -> None:
        self.font.render(self.text, True, Color.WHITE, self.__centred_text(self.text))
