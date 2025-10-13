from typing import Callable

from settings import *
from render.interactor import Interactor
from render.button import Button


class TextInput(Interactor):
    def __init__(self, x: int, y: int, width: int, height: int, radius: int, text_color: str, bg_color: str, placeholder: str,
                 on_input_list_update: Callable[[str], list[str]], button_func: Callable[[str], None]):
        # when the user types in the input box, calls this function to return a new list of recommended options
        super().__init__(x, y, width, height, radius, text_color, bg_color, text="")

        self.on_input_list_update = on_input_list_update
        self.placeholder = placeholder
        self.active = False
        self.button_func = button_func

        self.__buttons = []

    def activate(self):
        self.active = True

    def deactivate(self):
        self.text = ""
        self.active = False
        self.__buttons = []

    def on_type(self, character: str):
        self.text += character
        option_list = self.on_input_list_update(self.text)
        self.__buttons = []
        start_y = self.y + self.height + 5

        # double lambda function to get around for-loop and lambda functions not getting along
        button_functions = lambda val: lambda: self.button_func(val)
        for i, option in enumerate(option_list):
            self.__buttons.append(Button(self.x, start_y + 40 * i, self.width, 40, 0, self.text_color,
                                  self.bg_color, text=option, func=button_functions(option)))
        return self.__buttons

    def remove_char(self):
        self.text = self.text[:-1]

    def __offset_text(self, text_object: str) -> tuple[int, int]:
        text_object = self.font.string_to_surface(text_object)

        x = self.x + 5  # offset by 5 to the right
        y = self.y + (self.height - text_object.get_height()) / 2  # center vertically

        return x, y

    def render(self) -> None:
        if not self.active:
            self.font.render(self.placeholder, True, Color.GREY, self.__offset_text(self.text))
            return

        self.font.render(self.text, True, self.text_color, self.__offset_text(self.text))