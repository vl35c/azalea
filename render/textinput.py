import pygame
from typing import Callable

from render.interactor import Interactor
from render.renderer import Renderer
from settings import *

class TextInput(Interactor):
    def __init__(self, x: int, y: int, width: int, height: int, text_color: str, bg_color: str, placeholder: str,
                 on_input_list_update: Callable[[str], list[str]]):
        # when the user types in the input box, calls this function to return a new list of recommended options
        super().__init__(x, y, width, height, text_color, bg_color, text="")
        self.on_input_list_update = on_input_list_update
        self.placeholder = placeholder
        self.active = False

    def on_activate(self):
        self.active = True
        print("activated")

    def on_deactivate(self):
        self.active = False
        print("deactivated")

    def on_type(self, character: str):
        self.text += character
        self.on_input_list_update(self.text)