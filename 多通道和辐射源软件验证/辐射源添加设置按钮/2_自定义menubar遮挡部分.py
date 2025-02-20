from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QWidget, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: black; color: white")
        self.showMaximized()
        screen_h, screen_w = self.screen().size().height(), self.screen().size().width()
        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏标题栏
        print(screen_h, screen_w)

        self._widget = QWidget(self)
        self._widget.resize(screen_w, 100)

        self._logo_label = QLabel(self._widget)
        self._logo_label.resize(200, 30)
        self._logo_label.move(10, 0)
        self._logo_label.setText("Radsim 中科睿信 FSY18A-4")

        self._menu = QMenuBar(self._widget)
        set_menu = self._menu.addMenu("设置")
        self._menu.move(500, 3)

        self._min_btn = QPushButton("━", self._widget)
        self._min_btn.resize(30, 30)
        self._min_btn.move(700, 0)
        self._max_btn = QPushButton("▢", self._widget)
        self._max_btn.resize(30, 30)
        self._max_btn.move(725, 0)
        self._close_btn = QPushButton("X", self._widget)
        self._close_btn.resize(30, 30)
        self._close_btn.move(750, 0)

        for btn in (self._min_btn, self._max_btn, self._close_btn):
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("border: none; color: white;")

        self._min_btn.clicked.connect(self.showMinimized)
        self._max_btn.clicked.connect(self._show_max_mized)
        self._close_btn.clicked.connect(self.close)

    def _show_max_mized(self):
        if self.window().isFullScreen():
            # self.window().showNormal()
            self.showMaximized()
            self._max_btn.setText("▢")
        else:
            # self.window().showMaximized()
            self.window().showFullScreen()
            self._max_btn.setText("❐")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
