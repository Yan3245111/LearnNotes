from PyQt5.QtWidgets import QApplication, QDoubleSpinBox, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt


class CustomDoubleSpinBox(QDoubleSpinBox):
    def __init__(self):
        super().__init__()
        self.setDecimals(2)  # 设置小数位数为2
        self.setSingleStep(1.0)  # 默认步长
        self.setValue(0.0)  # 初始值

    def stepBy(self, steps):
        cursor_position = self.lineEdit().cursorPosition()
        text = self.text()

        # 获取小数点位置
        dot_position = text.find('.')

        # 计算步长：根据光标从最后一位右向左，分别调整个位、十分位、百分位
        if dot_position == -1 or cursor_position <= dot_position:  # 在整数部分
            print(f"pos={cursor_position}, dot={dot_position}, text={text}")
            step = 10 ** (len(text[:dot_position]) - cursor_position)
        else:  # 在小数部分
            step = 10 ** (dot_position - cursor_position + 1)

        # print(f"steps={steps}, step={step}")
        # 调整值并设置回 spinbox
        self.setValue(self.value() + steps * step)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.stepBy(1)  # 向上增加
        elif event.key() == Qt.Key_Down:
            self.stepBy(-1)  # 向下减少
        else:
            super().keyPressEvent(event)  # 其他按键按默认处理


app = QApplication([])
window = QWidget()
layout = QVBoxLayout()

double_spin_box = CustomDoubleSpinBox()
layout.addWidget(double_spin_box)

window.setLayout(layout)
window.show()
app.exec_()
