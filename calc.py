import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QKeyEvent
from math import sqrt, pow


class CustomButton(QPushButton):
    def __init__(self, title, role):
        super().__init__(title)
        self.role = role
        self.initUI()

    def initUI(self):
        self.setFont(QFont('Arial', 14))
        self.setFixedSize(55, 55)
        self.setCursor(Qt.PointingHandCursor)
        css = "QPushButton { background-color: #555; color: #DDD; border-radius: 27px; }"
        css_hover = "QPushButton:hover { background-color: #686868; }"
        css_pressed = "QPushButton:pressed { background-color: #3A3A3A; }"

        if self.role in ('op', 'func'):
            css = "QPushButton { background-color: #777; color: #FFF; border-radius: 27px; }"
        elif self.role == 'equal':
            css = "QPushButton { background-color: #0F0; color: #000; border-radius: 27px; }"
        elif self.role == 'clear':
            css = "QPushButton { background-color: #F00; color: #FFF; border-radius: 27px; }"

        self.setStyleSheet(f"{css} {css_hover} {css_pressed}")


class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Калькулятор')
        self.setFixedSize(300, 400)
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('free-icon-calculator-342344.png'))
        widget = QWidget(self)
        self.setCentralWidget(widget)
        vbox_layout = QVBoxLayout(widget)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        self.setPalette(palette)

        self.input_field = QLineEdit()
        self.input_field.setAlignment(Qt.AlignRight)
        self.input_field.setFont(QFont('Arial', 18))
        self.input_field.setStyleSheet("""
            QLineEdit {
                color: #00FF00;
                padding: 10px;
                border-radius: 10px;
                background-color: #000000;
            }
        """)
        vbox_layout.addWidget(self.input_field)

        buttons = [
            ('C', 'clear'), ('√', 'func'), ('^', 'func'), ('/', 'op'),
            ('7', 'num'), ('8', 'num'), ('9', 'num'), ('*', 'op'),
            ('4', 'num'), ('5', 'num'), ('6', 'num'), ('-', 'op'),
            ('1', 'num'), ('2', 'num'), ('3', 'num'), ('+', 'op'),
            ('(', 'num'), ('0', 'num'), (')', 'num'), ('=', 'equal')
        ]

        grid_layout = QGridLayout()

        positions = [(i, j) for i in range(5) for j in range(4)]
        for position, (text, role) in zip(positions, buttons):
            button = CustomButton(text, role)
            button.clicked.connect(self.on_button_clicked)
            grid_layout.addWidget(button, *position)

        vbox_layout.addLayout(grid_layout)

    def on_button_clicked(self):
        button = self.sender()
        button_text = button.text()

        if button_text == 'C':
            self.input_field.clear()
        elif button_text == '=':
            self.calculate_result()
        elif button_text in {'√', '^'}:
            self.input_field.setText(self.input_field.text() + button_text)
        else:
            self.input_field.setText(self.input_field.text() + button_text)

    def calculate_result(self):
        try:
            expression = self.input_field.text().replace('^', '**')
            result = str(eval(expression, {"__builtins__": {}}, {"sqrt": sqrt, "pow": pow}))
            self.input_field.setText(result)
        except Exception as e:
            self.input_field.setText("Error")

    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            key = event.key()
            text = self.input_field.text()
            if key == Qt.Key_Escape:
                self.input_field.clear()
            elif key in (Qt.Key_Enter, Qt.Key_Return):
                self.calculate_result()
            elif key == Qt.Key_Backspace:
                self.input_field.setText(text[:-1])
            else:
                char = event.text()
                if char in '0123456789+-*/().√^':
                    self.input_field.setText(text + char)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc_app = CalculatorApp()
    calc_app.show()
    sys.exit(app.exec_())
