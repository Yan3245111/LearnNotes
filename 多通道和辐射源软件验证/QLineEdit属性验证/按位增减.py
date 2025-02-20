from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import sys


freq_digit = [9, 6, 3, 0]

unit_digit = {0: [9, 6, 3, 0], 1: [1], 2: [9, 6, 3, 0]}


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self._line = QLineEdit(self)
        self._line.move(100, 100)
        self._line.setText("0.0")  # test dBm

    def increase(self):
        text = self._line.text()
        value, str_value = self.text_to_value(text=text)
        print(value, str_value)
        # 有小数点的地方会错，因为0.5 去除完以后变成5了，其实是2位
        cursor_pos = self._line.cursorPosition()
        value_len = len(str_value)
        step_len = 0
        for i, char in enumerate(text):
            if char.isdigit() or char == "-":
                if (i + 1) == cursor_pos:
                    break
                step_len += 1
        if step_len >= value_len:
            return value
        value = value + 10 ** (value_len - step_len - 1)
        new_text = self.value_to_text(value=value, unit=0, param_type=1)
        self._line.setText(new_text)
        self._line.setCursorPosition(cursor_pos + (len(new_text) - len(text)))

    def decrease(self):
        text = self._line.text()
        value, str_value = self.text_to_value(text=text)
        cursor_pos = self._line.cursorPosition()
        value_len = len(str_value)
        step_len = 0
        for i, char in enumerate(text):
            if char.isdigit() or char == "-":
                if (i + 1) == cursor_pos:
                    break
                step_len += 1
        if step_len >= value_len:
            return value
        value = value - 10 ** (value_len - step_len - 1)
        if value < -200:
            value = -200
        new_text = self.value_to_text(value=value, unit=0, param_type=1)
        self._line.setText(new_text)
        self._line.setCursorPosition(cursor_pos + (len(new_text) - len(text)))

    @staticmethod
    def value_to_text(value: int, unit: int, param_type: int) -> str:
        is_negative = True if value < 0 else False
        value = abs(value)
        v_len = len(str(value))
        if v_len <= unit_digit[param_type][unit]:
            number_str = str(value).zfill(unit_digit[param_type][unit] + 1)
        else:
            number_str = str(value)
        front_part = number_str[:-unit_digit[param_type][unit]]
        back_part = number_str[-unit_digit[param_type][unit]:]
        formatted_back = " ".join([back_part[max(i - 3, 0):i] for i in range(len(back_part), 0, -3)][::-1])
        formatted_front = " ".join([front_part[max(i - 3, 0):i] for i in range(len(front_part), 0, -3)][::-1])
        res = formatted_back
        if front_part:
            res = f"{formatted_front}.{formatted_back}".strip()
        if is_negative:
            res = '-' + res
        return res

    @staticmethod
    def text_to_value(text: str, unit: int, param_type: int) -> tuple:
        res = text.replace(" ", "")
        value = float(res) * 10
        return int(value), res.replace(".", "")

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == Qt.Key_Down:
            self.decrease()
        elif a0.key() == Qt.Key_Up:
            self.increase()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec_()
