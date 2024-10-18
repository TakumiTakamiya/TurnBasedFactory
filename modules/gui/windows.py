import sys

from PyQt6.QtWidgets import QApplication

from modules.constants import MAIN_GRID_HEIGHT, MAIN_GRID_WIDTH

from .grid import Grid
from .widget.blank import BlankWidget


class MainWindow:
    "ゲームのメインウィンドウ"

    def __init__(self):
        super().__init__()

        qAp = QApplication(sys.argv)
        self.grid = Grid(width=MAIN_GRID_WIDTH, height=MAIN_GRID_HEIGHT)
        self.grid.show()
        self.grid.add_widget(BlankWidget(3, 2), 0, 0)
        self.grid.add_widget(BlankWidget(1, 2, color="#3a0a0a"), 4, 3)
        self.grid.show_overray(0, 0, 2, 2, "#21ee0013")
        qAp.exec()
