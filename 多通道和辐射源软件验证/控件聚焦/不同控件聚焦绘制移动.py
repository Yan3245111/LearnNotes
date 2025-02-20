from PyQt5.QtWidgets import QApplication, QLineEdit, QSpinBox, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt


# 定义一个类封装 QLineEdit 控件
class MyLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setPlaceholderText("请输入文本")


# 定义一个类封装 QSpinBox 控件
class MySpinBox(QSpinBox):
    def __init__(self):
        super().__init__()
        self.setRange(0, 100)

    def keyPressEvent(self, event):
        # 检查是否按下了上下方向键
        if event.key() in (Qt.Key_Up, Qt.Key_Down):
            # 将事件交给父级窗口处理，而不是 QSpinBox 处理
            self.parentWidget().keyPressEvent(event)
        else:
            # 否则调用默认事件处理
            super().keyPressEvent(event)


# 主窗口类，包含两个控件并处理聚焦
class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle("不同控件聚焦示例")

        # 创建自定义控件的实例
        self.line_edit = MyLineEdit()
        self.spin_box = MySpinBox()

        # 使用 QSS 设置样式
        self.setStyleSheet("""
            QLineEdit, QSpinBox {
                border: 2px solid gray;
                padding: 5px;
                border-radius: 5px;
            }
            QLineEdit:focus, QSpinBox:focus {
                border: 2px solid #0078d7;  /* 聚焦时的边框颜色 */
            }
        """)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.line_edit)
        layout.addWidget(self.spin_box)
        self.setLayout(layout)

    def keyPressEvent(self, event):
        # 获取当前聚焦的控件
        focused_widget = self.focusWidget()

        # 检查聚焦控件并打印控件信息
        if focused_widget == self.line_edit:
            print("聚焦在文本框")
        elif focused_widget == self.spin_box:
            print("聚焦在数字框")

        # 处理方向键移动聚焦
        if event.key() == Qt.Key_Down:
            if focused_widget == self.line_edit:
                self.spin_box.setFocus()
            elif focused_widget == self.spin_box:
                self.line_edit.setFocus()

        elif event.key() == Qt.Key_Up:
            if focused_widget == self.spin_box:
                self.line_edit.setFocus()
            elif focused_widget == self.line_edit:
                self.spin_box.setFocus()


# 创建应用程序实例并运行
app = QApplication([])
window = MyApp()
window.show()
app.exec_()
