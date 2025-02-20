from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
)
from PyQt5.QtCore import Qt


class VirtualKeyboard(QDialog):
    def __init__(self, target_input=None, parent=None):
        super().__init__(parent)
        self.target_input = target_input  # 目标输入框
        self.setWindowTitle("虚拟键盘")
        self.setFixedSize(800, 300)  # 调整键盘窗口大小

        # 样式表美化
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #f8f8f8, stop:1 #e8e8e8);
                border: 1px solid #ccc;
                border-radius: 10px;
            }
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 10px;
                font-size: 16px;
                color: #333;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)

        # 主布局
        layout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()
        layout.addLayout(self.grid_layout)

        # 键盘按键定义
        self.keys = [
            "1 2 3 4 5 6 7 8 9 0 ← 清空".split(),
            "Q W E R T Y U I O P".split(),
            "A S D F G H J K L 回车".split(),
            "Z X C V B N M 空格 关闭".split(),
        ]

        # 创建键盘按钮
        for row_index, row_keys in enumerate(self.keys):
            for col_index, key in enumerate(row_keys):
                button = QPushButton(key)
                button.setFixedSize(60, 50)  # 按钮大小
                button.clicked.connect(lambda _, k=key: self.on_key_pressed(k))
                self.grid_layout.addWidget(button, row_index, col_index)

    def on_key_pressed(self, key):
        """
        按键点击事件处理逻辑
        """
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

        # 美化主窗口样式
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                font-size: 14px;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005fa1;
            }
            QPushButton:pressed {
                background-color: #003f74;
            }
            QLineEdit {
                font-size: 16px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """)

        # 显示虚拟键盘
        show_keyboard_button.clicked.connect(self.show_virtual_keyboard)

    def show_virtual_keyboard(self):
        """
        显示虚拟键盘
        """
        keyboard = VirtualKeyboard(self.input_field, self)
        keyboard.exec_()  # 模态显示


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
