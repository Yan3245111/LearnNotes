from PyQt5.QtWidgets import QApplication, QLineEdit, QSpinBox, QWidget
from PyQt5.QtCore import Qt
from PyQt5 import QtGui


# 注意：谁隐藏需要把谁的点击focus事件也隐藏掉

def singleton(cls):

    instance = dict()

    def _singleton(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    _singleton: type(cls)
    return _singleton


@singleton
class Group(list):

    def __init__(self):
        super().__init__()

    def add_widget(self, widget):
        if widget not in self:
            self.append(widget)

    def remove_widget(self, widget):
        if widget in self:
            self.remove(widget)

    def get_next_widget(self, cur_widget):
        next_widget = None
        for idx, one_w in enumerate(self):
            if cur_widget == one_w:
                next_idx = idx + 1
                if next_idx == len(self):
                    next_idx = 0
                while not self[next_idx].isVisible():
                    next_idx += 1
                    if next_idx == len(self):
                        next_idx = 0
                next_widget = self[next_idx]
                break
        return next_widget

    def get_last_widget(self, cur_widget):
        last_widget = None
        for idx, one_w in enumerate(self):
            if cur_widget == one_w:
                last_idx = idx - 1
                if last_idx == -1:
                    last_idx = len(self) - 1
                while not self[last_idx].isVisible():
                    last_idx -= 1
                    if last_idx == -1:
                        last_idx = len(self) - 1
                last_widget = self[last_idx]
                break
        return last_widget


class OneLineEdit(QLineEdit):

    def __init__(self, parent: QWidget, w: int, h: int, x: int, y: int, is_add_group: bool = True):
        super().__init__()
        self._is_edit = False
        self._group = Group()
        if is_add_group:
            self._group.add_widget(self)
        else:
            self.clearFocus()
        # INIT
        self.setReadOnly(True)
        self.setParent(parent)
        self.resize(w, h)
        self.move(x, y)

    def set_visible(self, visible: bool):
        self.setVisible(visible)

    def get_visible(self) -> bool:
        return self.isVisible()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() in [Qt.Key_Up, Qt.Key_Down] and not self._is_edit:
            self.parentWidget().keyPressEvent(a0)
            self.setReadOnly(True)
        else:
            if a0.key() in [Qt.Key_Enter, Qt.Key_Return]:
                self.setReadOnly(self._is_edit)
                self._is_edit = not self._is_edit
            else:
                if not self._is_edit:
                    self.clear()
                self.setReadOnly(False)
                self._is_edit = True
            super().keyPressEvent(a0)

    def set_edit_state(self, is_edit: bool):
        self.setReadOnly(not is_edit)
        self._is_edit = is_edit

    def get_is_edit(self) -> bool:
        return self._is_edit


class OneSpinBox(QSpinBox):

    def __init__(self, parent: QWidget, w: int, h: int, x: int, y: int, is_add_group: bool = True):
        super().__init__()
        self._is_edit = False
        self._group = Group()
        if is_add_group:
            self._group.add_widget(self)
        # INIT
        self.setReadOnly(True)
        self.setParent(parent)
        self.resize(w, h)
        self.move(x, y)

    def set_visible(self, visible: bool):
        self.setVisible(visible=visible)

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() in [Qt.Key_Up, Qt.Key_Down] and not self._is_edit:
            self.parentWidget().keyPressEvent(a0)
            self.setReadOnly(True)
        else:
            if a0.key() in [Qt.Key_Enter, Qt.Key_Return]:
                self.setReadOnly(self._is_edit)
                self._is_edit = not self._is_edit
            else:
                if not self._is_edit:
                    self.clear()
                self.setReadOnly(False)
                self._is_edit = True
            super().keyPressEvent(a0)

    def set_edit_state(self, is_edit: bool):
        self.setReadOnly(not is_edit)
        self._is_edit = is_edit

    def get_is_edit(self) -> bool:
        return self._is_edit


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self._one_line = OneLineEdit(parent=self, w=200, h=30, x=20, y=20)
        self._one_line2 = OneLineEdit(parent=self, w=200, h=30, x=20, y=70, is_add_group=False)
        self._one_spinbox = OneSpinBox(parent=self, w=200, h=30, x=20, y=120)
        self._group = Group()
        # self._one_line.setVisible(False)
        self._one_spinbox.setFocus()

        self.setStyleSheet("""
            QSpinBox, QLineEdit {
                border: 2px solid gray;
                padding: 5px;
                border-radius: 5px;
            }
            QSpinBox:focus, QLineEdit:focus {
                border: 2px solid #0078d7;  /* 聚焦时的边框颜色 */
            }
        """)

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        focused_widget = self.focusWidget()
        if focused_widget in self._group and focused_widget.get_is_edit():
            return
        if a0.key() == Qt.Key_Down:
            next_widget = self._group.get_next_widget(cur_widget=focused_widget)
            focused_widget.set_edit_state(False)
            next_widget.setFocus()
        elif a0.key() == Qt.Key_Up:
            last_widget = self._group.get_last_widget(cur_widget=focused_widget)
            focused_widget.set_edit_state(False)
            last_widget.setFocus()


if __name__ == '__main__':
    app = QApplication([])
    win = Window()
    win.show()
    app.exec_()
