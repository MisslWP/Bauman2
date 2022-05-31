from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import ui
from root_finder import RootFinder, RootData
import numpy as np


class MplCanvas(FigureCanvasQTAgg):

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        print(event.pos())

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Window:
    def __init__(self):
        self.n_max = 15
        self.f = 'sin(10*x)'
        self.eps = 0.001
        self.h = 0.25
        self.b = 5
        self.a = -5
        self.app = QApplication([])
        self.window = QMainWindow()
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self.window)
        sc = MplCanvas(self, width=20, height=10, dpi=100)
        self.plot = sc
        self.ui.graphLayout.addWidget(sc)

        self.connect()

    def run(self):
        self.window.show()
        self.app.exec()

    def loadData(self):
        try:
            self.a = float(self.ui.inputA.text())
            self.b = float(self.ui.inputB.text())
            self.h = float(self.ui.inputH.text())
            self.eps = float(self.ui.inputEps.text())
            self.f = self.ui.inputFunc.text()
            self.n_max = self.ui.inputNMax.value()
            return True
        except ValueError:
            return False

    def aboutMessage(self):
        Window.show_message_box('About that program',
                                'Author: UncleDrema ( Дремин Кирилл ИУ7-26Б ) \n'
                                'This program is designed to find roots of any functions using Steffenser method.')

    def connect(self):
        self.ui.calcButton.clicked.connect(self.on_clicked)
        self.ui.calcAction.triggered.connect(self.on_clicked)
        self.ui.aboutAction.triggered.connect(self.aboutMessage)

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

    def on_clicked(self):
        if not self.loadData():
            Window.show_message_box('Ошибка', 'Введённые данные не являются валидными', warning=True)
            return
        table = self.ui.rootTable
        for i in range(table.rowCount() - 1, -1, -1):
            table.removeRow(i)
        rf = RootFinder(self.a, self.b, self.h, self.n_max, self.eps, self.f)
        root_data = rf.roots
        for i, data in enumerate(root_data):
            table.insertRow(i)
            table.setItem(i, 0, QTableWidgetItem(f'[{data.a};{data.b}]'))
            table.setItem(i, 1, QTableWidgetItem(str(data.x)))
            table.setItem(i, 2, QTableWidgetItem(f'{data.f_x:.1e}'))
            table.setItem(i, 3, QTableWidgetItem(str(data.iters)))
            table.setItem(i, 4, QTableWidgetItem(str(data.err_code)))
        self.ui.graphLayout.removeWidget(self.plot)
        sc = MplCanvas(self, width=20, height=10, dpi=100)
        self.plot = sc
        rf.plot(self.plot)
        self.ui.graphLayout.addWidget(self.plot)


if __name__ == "__main__":
    window = Window()
    window.run()
