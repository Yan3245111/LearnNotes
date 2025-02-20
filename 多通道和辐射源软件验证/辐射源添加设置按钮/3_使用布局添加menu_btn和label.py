from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QLabel, QMenu, QVBoxLayout
from PyQt5.QtCore import Qt
import sys


class Title(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__()
        self.setParent(parent)
        # self.setGeometry(200, 200, 800, 600)
        self.resize(800, 20)

        # 创建主垂直布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # 设置主布局的边距为 0

        # 创建水平布局
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)  # 设置水平布局的边距为 0

        # 添加 QLabel
        label = QLabel("This is a label")
        h_layout.addWidget(label)

        # 创建一个按钮来触发 QMenu
        btn_menu = QPushButton("设置")
        menu = QMenu(self)

        # 在 QMenu 中添加一些动作
        action1 = menu.addAction("Option 1")
        action2 = menu.addAction("Option 2")
        action3 = menu.addAction("Option 3")

        # 设置按钮的菜单
        btn_menu.setMenu(menu)

        # 将按钮添加到布局中
        h_layout.addWidget(btn_menu)

        # 添加另一个 QPushButton
        btn = QPushButton("Click Me")
        h_layout.addWidget(btn)

        # 将水平布局添加到主垂直布局中
        main_layout.addLayout(h_layout)

        # 确保布局的伸展是正确的
        main_layout.addStretch(1)

        # 设置主窗口的布局
        self.setLayout(main_layout)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        title = Title(self)

        # 隐藏默认标题栏
        self.setWindowFlags(Qt.FramelessWindowHint)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
