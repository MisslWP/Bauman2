from PyQt6.QtWidgets import QApplication, QMainWindow

import ui

class Window:
    def __init__(self):
        self.app = QApplication([])
        self.window = QMainWindow()
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.toOct = True
        self.connect()

    @staticmethod
    def oct_do_dec(oct_s: str) -> int:
        i = 0
        res = 0
        for c in reversed(oct_s.lstrip('-')):
            res += int(c) * (8 ** i)
            i += 1
        if '-' in oct_s:
            res *= -1
        return res

    @staticmethod
    def dec_to_oct(dec_n: int) -> str:
        sign = '-' if dec_n < 0 else ''
        d = abs(dec_n)
        s = ''
        while d > 0:
            d, m = divmod(d, 8)
            s = str(m) + s
        s = s if s != '' else '0'
        return sign + s

    def execute(self):
        def wrapped():
            v1 = Window.oct_do_dec(self.ui.num1.text())
            v2 = Window.oct_do_dec(self.ui.num2.text())
            self.ui.result.setText(Window.dec_to_oct(v1 + v2))
        return wrapped

    def connect(self):
        self.ui.pushButton.clicked.connect(self.execute())

    def run(self):
        self.window.show()
        self.app.exec()


if __name__ == "__main__":
    app = Window()
    app.run()