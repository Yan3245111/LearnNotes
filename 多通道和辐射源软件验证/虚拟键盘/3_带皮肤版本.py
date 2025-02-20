from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5 import QtGui


class VirtualKeyboard(QDialog):
    def __init__(self, target_input=None, parent=None):
        super().__init__(parent)
        self.target_input = target_input  # 目标输入框
        self.setWindowTitle("虚拟键盘")
        self.setFixedSize(1050, 480)  # 调整键盘窗口大小

        # 样式表美化
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 10px;
                background-image: url('suolong.jpg');
            }
            QPushButton {
                background-color: #ffffff;
                border: 2px solid #bbb;
                border-radius: 5px;
                font-size: 18px;
                color: #333;
                min-width: 60px;
                min-height: 60px;
                padding: 0;
                text-align: center;
                box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);
                background-color: rgba(76, 175, 80, 0.8)
            }
            QPushButton:pressed {
                background-color: rgba(76, 175, 80, 0.2);
                box-shadow: inset 2px 2px 6px rgba(0, 0, 0, 0.2);
            }
            QPushButton:hover {
                background-color: rgba(76, 175, 80, 0.4);
            }
        """)

        # 主布局
        layout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()
        layout.addLayout(self.grid_layout)

        # 真实键盘按键定义（包括方向键）
        self.keys = [
            # 第一行
            ["Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"],
            # 第二行
            ["~", "`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "delete"],
            # 第三行
            ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\", "|"],
            # 第四行
            ["caps lock", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "enter"],
            # 第五行
            ["shift", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "shift"],
            # 第六行
            ["ctrl", "fn", "alt", "space", "alt", "ctrl", "↑", "↓", "←", "→"],
        ]

        # 创建键盘按钮
        for row_index, row_keys in enumerate(self.keys):
            for col_index, key in enumerate(row_keys):
                button = QPushButton(key)
                button.setFixedSize(60, 60)  # 按钮大小
                button.clicked.connect(lambda _, k=key: self.on_key_pressed(k))
                self.grid_layout.addWidget(button, row_index, col_index)

        # 调整行列间距
        self.grid_layout.setHorizontalSpacing(10)  # 列间距
        self.grid_layout.setVerticalSpacing(10)    # 行间距

        # 调整行和列的比例（例如，空格键宽度加大）
        self.grid_layout.setColumnStretch(14, 2)  # 将最后一列（Space）宽度加大

    def on_key_pressed(self, key):
        """
        按键点击事件处理逻辑
        """
        if self.target_input is None:
            return

        if key == "delete":  # 删除最后一个字符
            self.target_input.backspace()
        elif key == "清空":  # 清空输入框
            self.target_input.clear()
        elif key == "Enter":  # 插入换行
            self.target_input.insert("\n")
        elif key == "Space":  # 插入空格
            self.target_input.insert(" ")
        elif key == "Shift" or key == "Ctrl" or key == "Alt" or key == "Fn" or key == "Tab" or key == "CapsLock":
            pass  # 这些是控制按键，不在输入框中插入字符
        elif key == "↑":  # 向上箭头
            pass  # 可以添加自定义操作
        elif key == "↓":  # 向下箭头
            pass  # 可以添加自定义操作
        elif key == "←":  # 向左箭头
            pass  # 可以添加自定义操作
        elif key == "→":  # 向右箭头
            pass  # 可以添加自定义操作
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
