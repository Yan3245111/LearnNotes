from PyQt5.QtWidgets import QApplication, QLineEdit, QSpinBox, QWidget
from PyQt5.QtCore import Qt
from PyQt5 import QtGui


class OneLineEdit(QLineEdit):

    def __init__(self, parent: QWidget, width: int, height: int, pos_x: int, pos_y: int):
        super().__init__()
        self._is_edit = False

        self.setParent(parent)
        self.setReadOnly(True)

        self.resize(width, height)
        self.move(pos_x, pos_y)
        self.setPlaceholderText("输入文本")
        # STYLE SHEET
        self.setStyleSheet("""
            QLineEdit{
                border: 2px solid gray;
                padding: 5px;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border: 2px solid #0078d7;  /* 聚焦时的边框颜色 */
            }
        """)
        
    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() in [Qt.Key_Up, Qt.Key_Down] and not self._is_edit:
            self.parentWidget().keyPressEvent(a0)
            self.setReadOnly(True)
        else:
            if a0.key() in [Qt.Key_Enter, Qt.Key_Return]:
                self.setReadOnly(self._is_edit)
                self._is_edit = not self._is_edit
            elif not self._is_edit:
                self.setReadOnly(False)
                self._is_edit = True
            super().keyPressEvent(a0)

    def set_edit_state(self, is_edit: bool):
        self.setReadOnly(not is_edit)
        self._is_edit = is_edit

    def get_is_edit(self) -> bool:
        return self._is_edit


class OneSpinBox(QSpinBox):

    def __init__(self, parent: QWidget, width: int, height: int, pos_x: int, pos_y: int):
        super().__init__()
        self._is_edit = False
        
        self.setParent(parent)
        self.setReadOnly(True)

        self.resize(width, height)
        self.move(pos_x, pos_y)
        self.setStyleSheet("""
            QSpinBox {
                border: 2px solid gray;
                padding: 5px;
                border-radius: 5px;
            }
            QSpinBox:focus {
                border: 2px solid #0078d7;  /* 聚焦时的边框颜色 */
            }
        """)
        
    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() in [Qt.Key_Up, Qt.Key_Down] and not self._is_edit:
            self.parentWidget().keyPressEvent(a0)
            self.setReadOnly(True)
        else:
            if a0.key() in [Qt.Key_Enter, Qt.Key_Return]:
                self.setReadOnly(self._is_edit)
                self._is_edit = not self._is_edit
            else:
                self.setReadOnly(False)
                self._is_edit = True
            super().keyPressEvent(a0)

    def set_edit_state(self, is_edit: bool):
        self.setReadOnly(not is_edit)
        self._is_edit = is_edit

    def get_is_edit(self) -> bool:
        return self._is_edit


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self._one_line = OneLineEdit(parent=self, width=200, height=30, pos_x=20, pos_y=20)
        self._one_spinbox = OneSpinBox(parent=self, width=200, height=30, pos_x=20, pos_y=120)

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        focused_widget = self.focusWidget()
        if focused_widget == self._one_line and self._one_line.get_is_edit():
            print("聚焦在文本框")
            return
        elif focused_widget == self._one_spinbox and self._one_spinbox.get_is_edit():
            print("聚焦在数字框")
            return

        if a0.key() == Qt.Key_Down:
            self._one_line.set_edit_state(is_edit=False)
            self._one_line.set_edit_state(is_edit=False)
            if focused_widget == self._one_line:
                self._one_spinbox.setFocus()
            elif focused_widget == self._one_spinbox:
                self._one_line.setFocus()
        elif a0.key() == Qt.Key_Up:
            self._one_line.set_edit_state(is_edit=False)
            self._one_line.set_edit_state(is_edit=False)
            if focused_widget == self._one_line:
                self._one_spinbox.setFocus()
            elif focused_widget == self._one_spinbox:
                self._one_line.setFocus()


if __name__ == '__main__':
    app = QApplication([])
    win = App()
    win.show()
    app.exec_()
