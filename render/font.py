import pygame

from settings import *


class Font:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont("monospace", 15, True)
        self.window = pygame.display.get_surface()

    # convert a string into a pygame.Surface
    def string_to_surface(self, text: str) -> pygame.Surface:
        _text = self.font.render(text, True, Color.WHITE)
        return pygame.Surface(_text.get_size())

    # overriding the font.render function to allow a blit in one line
    def render(self, text: str, antialias: bool, color: Color | str | tuple, pos: tuple[int, int]) -> pygame.Surface:
        _text = self.font.render(text, antialias, color)
        surface = pygame.Surface(
            _text.get_size(),
            pygame.SRCALPHA
        )
        surface.blit(_text, _text.get_rect())
        self.window.blit(surface, pos)

        return surface
