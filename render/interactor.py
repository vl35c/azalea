import pygame

from render.font import Font


class Interactor:
    def __init__(self, x: int, y: int, width: int, height: int, radius: int, text_color: str, bg_color: str,
                 text:str = None, func = lambda: None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.radius = radius
        self.text_color = text_color
        self.bg_color = bg_color # background color
        self.text = text
        self._func = func

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

    # calls interactors functions
    def func(self) -> ():
        return self._func()

    # calculate position to center text in button
    def _centered_text(self, text_object: str) -> tuple[int, int]:
        text_object = self.font.string_to_surface(text_object)

        x = self.x + (self.width - text_object.get_width()) // 2
        y = self.y + (self.height - text_object.get_height()) // 2

        return x, y

    # draw buttons
    def draw(self) -> None:
        pygame.draw.rect(self.window, self.bg_color, self.rect, 0, self.radius)

    # render text on button
    def render(self) -> None:
        self.font.render(self.text, True, self.text_color, self._centered_text(self.text))

    # draws and renders in 1 call
    def display(self) -> None:
        self.draw()
        self.render()
