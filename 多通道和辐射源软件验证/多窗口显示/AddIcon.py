from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys

from Gui.UI.UIMain import Ui_MainWindow
from Gui.UI.UISet import Ui_Set


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self._ui_main = Ui_MainWindow()
        self._ui_main.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # BTN
        self._ui_main.btn_close.setIcon(QIcon("ICONS/win_close.png"))
        self._ui_main.btn_min.setIcon(QIcon("ICONS/win_min.png"))
        self._ui_main.btn_max.setIcon(QIcon("ICONS/win_max.png"))
        self._ui_main.btn_set.setIcon(QIcon("ICONS/3.png"))
        # BTN_EVENT
        self._ui_main.btn_close.clicked.connect(self.close)
        self._ui_main.btn_min.clicked.connect(self.showMinimized)
        self._ui_main.btn_max.clicked.connect(self._set_win_max_event)
        self._ui_main.btn_set.clicked.connect(self._show_set_window)

    def _set_win_max_event(self):
        if self.isMaximized():
            self.showFullScreen()
        else:
            self.showMaximized()

    def _show_set_window(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec_()
