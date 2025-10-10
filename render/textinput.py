import pygame
from typing import Callable
from render.renderer import Renderer

class TextInput:
    def __init__(self, x: int, y: int, width: int, height: int, b_color: str,
                 placeholder: str, on_input_list_update: Callable[[str], list[str]]):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.b_color = b_color
        self.placeholder = placeholder

        # when the user types in the input box, calls this function to return a new list of recommended options
        self.on_input_list_update = on_input_list_update