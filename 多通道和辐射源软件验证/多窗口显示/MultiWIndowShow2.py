import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from Gui.UI.UIMain import Ui_MainWindow
from Gui.UI.UISet import Ui_Set
from Gui.UI.UISignal import Ui_Signal


class UiSet(QMainWindow):

    def __init__(self, parent):
        super().__init__()
        self._ui = Ui_Signal()
        self._ui.setupUi(self)
        self.setParent(parent)


class UiMain:

    def __init__(self, ui: Ui_MainWindow):
        self._ui = ui


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self._ui_set = UiSet(self)
        self._ui_set.move(500, 500)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec_()
