from abc import ABC, abstractmethod


class ClickEvent:
    def __init__(self, mouse_x, mouse_y):
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y


class Widget(ABC):
    width = 1
    height = 1

    @abstractmethod
    def build(self, parent) -> None:
        pass

    def on_clicked(self, event: ClickEvent):
        pass

    @abstractmethod
    def set_interactable(self, event: ClickEvent):
        pass

    @abstractmethod
    def delete(self, event: ClickEvent):
        pass
