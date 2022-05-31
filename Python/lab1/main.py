from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

import re
import ui

decRegex = re.compile(r'^([0-9]+)?(.[0-9]+)?$')
octRegex = re.compile(r'^([0-7]+)?(.[0-7]+)?$')


class Window:
    def __init__(self):
        self.app = QApplication([])
        self.window = QMainWindow()
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.toOct = True
        self.connect()

    def oct_to_dec(self, oct: str):
        if oct == '':
            return ''
        head, tail = '', ''
        if oct[0] == '.':
            tail = oct
        elif not '.' in oct:
            head = oct
        else:
            head, tail = oct.split('.', 2)
        res = 0
        power = 0
        for c in reversed(head):
            res += int(c) * (8 ** power)
            power += 1
        power = -1
        for c in tail:
            res += int(c) * (8 ** power)
            power -= 1

        return str(res)

    def dec_to_oct(self, dec: str):
        if dec == '':
            return ''
        head, tail = '', ''
        if dec[0] == '.':
            tail = dec
        elif not '.' in dec:
            head = dec
        else:
            head, tail = dec.split('.', 2)
        res = ''
        if head != '':
            d, m = divmod(int(head), 8)
            res += str(m)
            while d > 0:
                d, m = divmod(d, 8)
                res += str(m)
            res = res[::-1]
        if tail != '':
            res += '.'
            tail = float('.' + tail)
            for _ in range(self.ui.precisionSpin.value()):
                tail *= 8
                if tail == 1:
                    continue
                d, tail = divmod(tail, 8)
                res += str(int(d))
                if tail == 0:
                    break
        return res

    def add_char(self, c: str):
        def wrapper():
            if self.toOct:
                self.ui.base10Text.insert(c)
            else:
                self.ui.base8Text.insert(c)

        return wrapper

    def connect(self):
        self.ui.buttonChange.clicked.connect(self.swap_direction)
        self.ui.actionChange_direction.triggered.connect(self.swap_direction)
        self.ui.actionInput.triggered.connect(self.ui.base10Text.clear)
        self.ui.actionOutput.triggered.connect(self.ui.base8Text.clear)
        self.ui.actionInput_Output.triggered.connect(self.ui.buttonClear.click)
        self.ui.actionAbout.triggered.connect(self.aboutMessage)
        self.ui.buttonTranslate.clicked.connect(self.translate)
        self.ui.actionTranslate.triggered.connect(self.ui.buttonTranslate.click)
        self.ui.button0.clicked.connect(self.add_char('0'))
        self.ui.button1.clicked.connect(self.add_char('1'))
        self.ui.button2.clicked.connect(self.add_char('2'))
        self.ui.button3.clicked.connect(self.add_char('3'))
        self.ui.button4.clicked.connect(self.add_char('4'))
        self.ui.button5.clicked.connect(self.add_char('5'))
        self.ui.button6.clicked.connect(self.add_char('6'))
        self.ui.button7.clicked.connect(self.add_char('7'))
        self.ui.button8.clicked.connect(self.add_char('8'))
        self.ui.button9.clicked.connect(self.add_char('9'))
        self.ui.buttonPoint.clicked.connect(self.add_char('.'))

    def aboutMessage(self):
        Window.show_message_box('About that program',
                                'Author: UncleDrema ( Дремин Кирилл ИУ7-26Б ) \n'
                                'This program is designed to convert numbers from decimal to octal and back.')

    @staticmethod
    def show_message_box(title: str, msg: str, warning: bool = False):
        box = QMessageBox()
        box.setWindowTitle(title)
        box.setText(msg)
        if warning:
            box.setIcon(QMessageBox.Icon.Warning)
        else:
            box.setIcon(QMessageBox.Icon.Information)
        box.exec()

    def translate(self):
        if self.toOct:
            if decRegex.fullmatch(self.ui.base10Text.text()):
                self.ui.base8Text.setText(self.dec_to_oct(self.ui.base10Text.text()))
            else:
                Window.show_message_box('Incorrect input',
                                        'Input field contains incorrect symbols for base 10', True)
        else:
            if octRegex.fullmatch(self.ui.base8Text.text()):
                self.ui.base10Text.setText(self.oct_to_dec(self.ui.base8Text.text()))
            else:
                Window.show_message_box('Incorrect input',
                                        'Input field contains incorrect symbols for base 8', True)

    def run(self):
        self.window.show()
        self.app.exec()

    def swap_direction(self):
        self.toOct = not self.toOct
        if self.toOct:
            self.ui.directionLabel.setText('→')
            self.ui.button8.setEnabled(True)
            self.ui.button9.setEnabled(True)
        else:
            self.ui.directionLabel.setText('←')
            self.ui.button8.setEnabled(False)
            self.ui.button9.setEnabled(False)


if __name__ == "__main__":
    app = Window()
    app.run()
