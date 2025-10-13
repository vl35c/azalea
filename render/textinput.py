import pygame
from typing import Callable

from render.interactor import Interactor
from render.button import Button
from settings import *

class TextInput(Interactor):
    def __init__(self, x: int, y: int, width: int, height: int, text_color: str, bg_color: str, placeholder: str,
                 on_input_list_update: Callable[[str], list[str]], button_func: Callable[[str], None]):
        # when the user types in the input box, calls this function to return a new list of recommended options
        super().__init__(x, y, width, height, text_color, bg_color, text="")
        self.on_input_list_update = on_input_list_update
        self.placeholder = placeholder
        self.active = False
        self.button_func = button_func

    def on_activate(self):
        self.active = True
        print("activated")

    def on_deactivate(self):
        self.active = False
        print("deactivated")

    def on_type(self, character: str):
        self.text += character

        option_list = self.on_input_list_update(self.text)

        buttons = []

        start_y = self.y + self.height + 5

        for i,option in enumerate(option_list):
            buttons.append(Button(self.x, start_y + (40*i), self.width, 40, self.text_color, self.bg_color, text=option, func=lambda : self.button_func(option)))

        return buttons



    def remove_char(self):
        self.text = self.text[:-1]
        print(self.text, self.on_input_list_update(self.text))

    def __centred_text(self, text_object: str) -> tuple[int, int]:
        text_object = self.font.string_to_surface(text_object)

        x = self.x + 5
        y = self.y + (self.height - text_object.get_height()) / 2

        return x, y

    def render(self) -> None:
        self.font.render(self.text, True, self.text_color, self.__centred_text(self.text))