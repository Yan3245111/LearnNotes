from PyQt5.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QWidget


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle("聚焦边框示例")

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


if __name__ == '__main__':
    # 创建应用程序实例并运行
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec_()
