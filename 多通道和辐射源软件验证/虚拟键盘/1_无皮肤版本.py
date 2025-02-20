from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QGridLayout, QPushButton, QLineEdit


class VirtualKeyboard(QDialog):
    def __init__(self, target_input=None, parent=None):
        super().__init__(parent)
        self.target_input = target_input  # 目标输入框
        self.setWindowTitle("虚拟键盘")
        self.setFixedSize(400, 200)
        self.setStyleSheet("background-color: lightgray;")

        # 创建键盘布局
        layout = QVBoxLayout(self)
        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)

        # 键盘按钮
        self.keys = [
            "1 2 3 4 5 6 7 8 9 0 ← 清空".split(),
            "Q W E R T Y U I O P [ ]".split(),
            "A S D F G H J K L ; ' 回车".split(),
            "Z X C V B N M , . / 空格 关闭".split(),
        ]
        for row_index, row_keys in enumerate(self.keys):
            for col_index, key in enumerate(row_keys):
                button = QPushButton(key)
                button.setFixedSize(50, 50)
                button.clicked.connect(lambda _, k=key: self.on_key_pressed(k))
                grid_layout.addWidget(button, row_index, col_index)

    def on_key_pressed(self, key):
        if self.target_input is None:
            return
        if key == "←":  # 删除最后一个字符
            self.target_input.backspace()
        elif key == "清空":  # 清空输入框
            self.target_input.clear()
        elif key == "回车":  # 插入换行
            self.target_input.insert("\n")
        elif key == "空格":  # 插入空格
            self.target_input.insert(" ")
        elif key == "关闭":  # 关闭虚拟键盘
            self.close()
        else:  # 其他字符插入到输入框
            self.target_input.insert(key)


class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("主窗口")
        self.setFixedSize(400, 200)

        # 主窗口布局
        layout = QVBoxLayout(self)
        self.input_field = QLineEdit(self)
        show_keyboard_button = QPushButton("显示虚拟键盘")

        layout.addWidget(self.input_field)
        layout.addWidget(show_keyboard_button)

        # 显示虚拟键盘
        show_keyboard_button.clicked.connect(self.show_virtual_keyboard)

    def show_virtual_keyboard(self):
        keyboard = VirtualKeyboard(self.input_field, self)
        keyboard.exec_()  # 模态显示


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
