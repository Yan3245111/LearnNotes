from PyQt5.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle("键盘控制聚焦示例")

        # 创建两个文本框控件
        self.line_edit1 = QLineEdit(self)
        self.line_edit1.setPlaceholderText("请输入文本框 1")

        self.line_edit2 = QLineEdit(self)
        self.line_edit2.setPlaceholderText("请输入文本框 2")

        # 使用 QSS 设置样式，聚焦时的边框样式会自动应用到获得焦点的控件
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid gray;
                padding: 5px;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border: 2px solid #0078d7;  /* 聚焦时的边框颜色 */
            }
        """)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.line_edit1)
        layout.addWidget(self.line_edit2)
        self.setLayout(layout)

    def keyPressEvent(self, event):
        # 获取多个聚焦框的聚焦信息
        focused_widget = self.focusWidget()
        # 检查聚焦控件并打印控件信息
        if focused_widget == self.line_edit1:
            print("聚焦在文本框 1")
        elif focused_widget == self.line_edit2:
            print("聚焦在文本框 2")

        # 获取当前的焦点控件
        focused_widget = self.focusWidget()
        # 按下向下方向键
        if event.key() == Qt.Key_Down:
            if focused_widget == self.line_edit1:
                self.line_edit2.setFocus()
            elif focused_widget == self.line_edit2:
                self.line_edit1.setFocus()

        # 按下向上方向键
        elif event.key() == Qt.Key_Up:
            if focused_widget == self.line_edit2:
                self.line_edit1.setFocus()
            elif focused_widget == self.line_edit1:
                self.line_edit2.setFocus()


if __name__ == '__main__':
    # 创建应用程序实例并运行
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec_()
