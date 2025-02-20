from PyQt5.QtWidgets import QApplication, QDoubleSpinBox, QWidget, QVBoxLayout

app = QApplication([])

window = QWidget()
layout = QVBoxLayout()

line_edit = QDoubleSpinBox()
line_edit.setValue(1)
line_edit.setProperty("type", 1)  # 设置自定义属性1
line_edit.setProperty("unit", "GHz")  # 设置自定义属性2

print(type(line_edit.property('type')))
print(line_edit.property('unit'))

layout.addWidget(line_edit)
window.setLayout(layout)
window.show()
app.exec_()
