from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QHBoxLayout, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon

# 备注：qt无法直接在mainwindow栏里添加menubar，所以要自己重新写menubar


class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.setStyleSheet("background-color: #3c3f41; color: white;")

        # 左侧标题
        self.title = QLabel("Custom Window", self)
        self.title.setStyleSheet("color: white;")

        # 最小化、最大化、关闭按钮
        self.min_button = QPushButton("━", self)
        self.max_button = QPushButton("▢", self)
        self.close_button = QPushButton("✕", self)

        # 设置按钮
        self.settings_button = QPushButton("⚙", self)
        self.settings_button.setToolTip("设置")

        # 去除按钮的默认边框
        for btn in (self.min_button, self.max_button, self.close_button, self.settings_button):
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("border: none; color: white;")

        # 布局管理
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.addWidget(self.title)
        layout.addStretch(1)
        layout.addWidget(self.settings_button)
        layout.addWidget(self.min_button)
        layout.addWidget(self.max_button)
        layout.addWidget(self.close_button)

        # 按钮事件
        self.min_button.clicked.connect(parent.showMinimized)
        self.max_button.clicked.connect(self.toggle_max_restore)
        self.close_button.clicked.connect(parent.close)
        self.settings_button.clicked.connect(parent.open_settings)

    def toggle_max_restore(self):
        if self.window().isMaximized():
            self.window().showNormal()
            self.max_button.setText("▢")
        else:
            self.window().showMaximized()
            self.max_button.setText("❐")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.old_pos)
        self.window().move(self.window().x() + delta.x(), self.window().y() + delta.y())
        self.old_pos = event.globalPos()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)

        # 隐藏默认标题栏
        self.setWindowFlags(Qt.FramelessWindowHint)

        # 自定义标题栏
        self.title_bar = CustomTitleBar(self)
        self.setCentralWidget(QWidget())
        layout = QVBoxLayout(self.centralWidget())
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.title_bar)
        layout.addStretch(1)

        self.settings_window = None

    def open_settings(self):
        # 打开设置窗口
        if self.settings_window is None or not self.settings_window.isVisible():
            self.settings_window = QWidget()
            self.settings_window.setWindowTitle("Settings")
            self.settings_window.setGeometry(200, 200, 300, 200)
            layout = QVBoxLayout(self.settings_window)
            layout.addWidget(QLabel("这里是设置界面"))
        self.settings_window.show()


if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()
