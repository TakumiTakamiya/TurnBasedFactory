from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget

from modules.constants import GRID_SIZE

from ..widget import Widget


class BlankWidget(Widget):
    def __init__(self, width=1, height=1, color="#fd9644"):
        self.color = color
        self.width = width
        self.height = height
        self._interactable = False

    def build(self, parent) -> None:
        self.widget = QWidget(parent=parent)
        self._interactable = True
        self.widget.setStyleSheet(
            f"""
            QWidget {{
                background-color: {self.color};
                border: 4px ridge {self.color};
            }}
            """
        )
        self.widget.setGeometry(
            0,
            0,
            GRID_SIZE * self.width,
            GRID_SIZE * self.height,
        )

    def set_interactable(self, interactable):
        if self._interactable != interactable:
            self.widget.setAttribute(
                Qt.WidgetAttribute.WA_TransparentForMouseEvents, not interactable
            )
            self._interactable = interactable


class EmptyWidget(BlankWidget):
    def __init__(self):
        super().__init__(color="#2c3e50")
