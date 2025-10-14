from typing import Any


class KeyboardHandler:
    def __init__(self):
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    @staticmethod
    def key_down_with_child(event, child: Any):
        if event.key > 1000:
            return
        child.key_down(event)
