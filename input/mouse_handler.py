import pygame

from typing import Any


class MouseHandler:
    def __init__(self):
        self.obj: Any = None  # mouse's clicked object
        self.pos: tuple = ()

    @property
    def x(self) -> int:
        return self.pos[0]

    @property
    def y(self) -> int:
        return self.pos[1]

    # for allowing mouse to know what object it was initially held on
    def click(self, obj: Any) -> None:
        self.obj = obj
        self.pos = pygame.mouse.get_pos()

    # release held object
    def release(self) -> None:
        self.obj = None
        self.pos = ()