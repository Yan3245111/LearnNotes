# http://192.168.50.250/login
#
#
# 1-更改为自动获取IP
# 2-http://192.168.50.250/login
# 3-登录 密码123456

# oa 密码：8fd44cd1bb0ce517839d

from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QPushButton
import sys


class ComboBoxTest(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self._box = QComboBox(self)
        self._box.addItems(["1", "2"])

        if "3" in [self._box.itemText(i) for i in range(self._box.count())]:
            print(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ComboBoxTest()
    win.show()
    app.exec_()
