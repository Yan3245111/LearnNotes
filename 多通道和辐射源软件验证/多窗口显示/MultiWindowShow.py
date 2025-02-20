from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QObject

from Gui.UI.UIMain import Ui_MainWindow
from Gui.UI.UISet import Ui_Set


class ParentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = Ui_MainWindow()
        self._main.setupUi(self)  # 设置父窗口界面

        # 创建子窗口实例
        self.child_window = ChildWindow(self)  # 传递父窗口作为子窗口的父类


class ChildWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self._ui = Ui_Set()
        self._ui.setupUi(self)  # 设置子窗口界面
        self.setParent(parent)  # 设置父窗口为父类
        self.move(500, 500)

    def change_background_color(self):
        self.setStyleSheet("background-color: lightblue;")


class Hello(QObject):

    def __init__(self):
        super().__init__()
        self.parent = ParentWindow()
        self.child = ChildWindow(self.parent)

    def show(self):
        self.parent.show()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # 创建并显示父窗口
    # parent_window = ParentWindow()
    # parent_window.show()
    hello = Hello()
    hello.show()

    sys.exit(app.exec_())
