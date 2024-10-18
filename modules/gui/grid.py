from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QWidget

from modules.constants import GRID_SIZE

from .widget.blank.blank import EmptyWidget
from .widget.widget import Widget


class Grid(QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.setWindowTitle("Basic Grid Layout")
        self.setMinimumSize(width * GRID_SIZE, height * GRID_SIZE)
        self.setMaximumSize(width * GRID_SIZE, height * GRID_SIZE)

        self.grid_width = width
        self.grid_height = height

        # グリッド上のウィジェット
        self._widgets: list[list[Widget]] = [
            [EmptyWidget() for _ in range(width)] for _ in range(height)
        ]
        for row in self._widgets:
            for widget in row:
                widget.build(self)

        # 移動関係
        # オーバーレイ
        self._overray = QWidget(parent=self)
        self._overray.hide()
        # オブジェクト
        self.movingWidget: Widget | None = None
        self.movingWidgetDelta: tuple[int, int] = (0, 0)
        self.set_edit_mode(True)

    def getGridPos(self, mouse_x, mouse_y):
        grid_x = mouse_x // GRID_SIZE
        grid_y = mouse_y // GRID_SIZE
        if grid_x < 0:
            grid_x = 0
        if grid_y < 0:
            grid_y = 0
        if grid_x >= self.grid_width:
            grid_x = self.grid_width - 1
        if grid_y >= self.grid_height:
            grid_y = self.grid_height - 1
        return grid_x, grid_y

    def getMovingWidgetGridPos(self, mouse_x, mouse_y):
        grid_x = (mouse_x + self.movingWidgetDelta[0]) // GRID_SIZE
        grid_y = (mouse_y + self.movingWidgetDelta[1]) // GRID_SIZE
        if grid_x < 0:
            grid_x = 0
        if grid_y < 0:
            grid_y = 0
        if grid_x + self.movingWidget.width >= self.grid_width:
            grid_x = self.grid_width - self.movingWidget.width
        if grid_y + self.movingWidget.height >= self.grid_height:
            grid_y = self.grid_height - self.movingWidget.height
        print(f"GMWP: {grid_x},{grid_y}")
        return grid_x, grid_y

    def mouseMoveEvent(self, a0: QMouseEvent | None) -> None:
        "移動時の処理"
        print(id(a0))
        super().mouseMoveEvent(a0)

        if self.movingWidget is None:
            return

        # マウスのグリッド位置の取得
        mouse_pos = a0.pos()
        grid_x, grid_y = self.getMovingWidgetGridPos(mouse_pos.x(), mouse_pos.y())

        self._overray.setGeometry(
            GRID_SIZE * grid_x,
            GRID_SIZE * grid_y,
            GRID_SIZE * self.movingWidget.width,
            GRID_SIZE * self.movingWidget.height,
        )
        self.update()

    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        super().mousePressEvent(a0)
        if self._edit_mode:
            if self.movingWidget is None:
                mouse_pos = a0.pos()
                grid_x, grid_y = self.getGridPos(mouse_pos.x(), mouse_pos.y())
                if self._widgets[grid_x][grid_y] is None:
                    return
                self.movingWidget = self._widgets[grid_x][grid_y]
                self.remove_widget(self.movingWidget)
            else:
                # マウスのグリッド位置の取得
                mouse_pos = a0.pos()
                grid_x, grid_y = self.getMovingWidgetGridPos(
                    mouse_pos.x(), mouse_pos.y()
                )

                if self.check_space(
                    grid_x, grid_y, self.movingWidget.width, self.movingWidget.height
                ):
                    self.add_widget(self.movingWidget, grid_x, grid_y)
                    self.movingWidget = None
        else:
            # 子ウィジェット上のクリック
            pass

    def remove_widget(self, widget: Widget):
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if id(self._widgets[i][j]) == id(widget):
                    self._widgets[i][j].delete()
                    self._widgets[i][j] = EmptyWidget()
        self.update()

    def add_widget(self, widget: Widget, x, y):
        new_widget = QWidget(parent=self)
        new_widget.setGeometry(
            GRID_SIZE * x,
            GRID_SIZE * y,
            GRID_SIZE * widget.width,
            GRID_SIZE * widget.height,
        )
        widget.build(new_widget)
        self.movingWidget = widget
        new_widget.show()
        for i in range(y, y + widget.height):
            for j in range(x, x + widget.width):
                self._widgets[i][j] = widget
        self.update()

    def show_overray(self, x, y, w, h, color):
        self._overray.setStyleSheet(
            f"""
            QWidget {{
                background-color: {color};
            }}
            """
        )
        self._overray.setGeometry(
            GRID_SIZE * x, GRID_SIZE * y, GRID_SIZE * w, GRID_SIZE * h
        )
        self._overray.raise_()
        self._overray.show()
        self.update()

    def check_space(self, x, y, width, height):
        for i in range(y, y + height):
            for j in range(x, x + width):
                if self._widgets[i][j] is not None:
                    return False
        return True

    def set_edit_mode(self, mode):
        self._edit_mode = mode
        for row in self._widgets_data:
            for widget in row:
                if widget is not None:
                    widget.set_interactable(not mode)
