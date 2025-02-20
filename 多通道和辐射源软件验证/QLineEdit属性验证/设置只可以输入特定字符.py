import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QLabel
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator


class NumberOnlyLineEdit(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)

        self.setWindowTitle('QLineEdit with Numeric and Space Only')

        # 创建 QLineEdit
        self._line = QLineEdit(self)
        self._line.setPlaceholderText("Enter numbers and spaces only")

        # 创建正则表达式，用于限制输入
        regex = QRegularExpression("^[0-9 .]*$")
        validator = QRegularExpressionValidator(regex, self._line)

        # 设置 QLineEdit 的验证器
        self._line.setValidator(validator)
        self._line.setText("10.000 000 000")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NumberOnlyLineEdit()
    ex.show()
    sys.exit(app.exec_())
