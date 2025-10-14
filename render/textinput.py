import pygame

from typing import Callable

from settings import *
from render.interactor import Interactor
from render.button import Button
from input.keyboard_handler import KeyboardHandler


class TextInput(Interactor):
    def __init__(self, x: int, y: int, width: int, height: int, radius: int, text_color: str, bg_color: str, placeholder: str,
                 input_func: Callable[[str], list[str]], button_func: Callable[[str], None]):
        super().__init__(x, y, width, height, radius, text_color, bg_color, text="")

        # when the user types in the input box, calls this function to return a new list of recommended options
        self.input_func = input_func
        self.placeholder = placeholder
        self.active = False
        self.button_func = button_func

        self.__buttons = []

        self.keyboard = None

    def set_keyboard_handler(self, keyboard: KeyboardHandler) -> None:
        self.keyboard = keyboard
        self.keyboard.add_child(self)

    def activate(self) -> None:
        self.active = True

    def deactivate(self) -> None:
        self.text = ""
        self.active = False
        self.__buttons = []

    def key_down(self, event) -> None:
        if event.key == pygame.K_BACKSPACE:
            self.remove_char()
        else:
            self.text += event.unicode

        self.on_type()

    def on_type(self) -> None:
        option_list = self.input_func(self.text)
        self.__buttons = []
        y = self.y + self.height + 5

        # double lambda function to get around for-loop and lambda functions not getting along
        button_functions = lambda val: lambda: self.button_func(val)
        for i, option in enumerate(option_list):
            self.__buttons.append(Button(self.x, y + 40 * i, self.width, 40, 0, self.text_color,
                                  self.bg_color, text=option, func=button_functions(option)))

    def get_buttons(self) -> list[Button]:
        return self.__buttons

    def remove_char(self) -> None:
        self.text = self.text[:-1]

    def __offset_text(self, text_object: str) -> tuple[int, int]:
        text_object = self.font.string_to_surface(text_object)

        x = self.x + 5  # offset by 5 to the right
        y = self.y + (self.height - text_object.get_height()) / 2  # center vertically

        return x, y

    def render(self) -> None:
        if not self.active:
            self.font.render(self.placeholder, True, Color.GREY, self._centered_text(self.placeholder))
            return

        self.font.render(self.text, True, self.text_color, self.__offset_text(self.text))
