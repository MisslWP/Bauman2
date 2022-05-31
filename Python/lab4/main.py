"""
Решение планиметрической задачи (дано мн-во точек - найти треугольник макс. площади)
Точки вводить как коориднатно так и на картинке и вводить тыкая на экран:
вводить точки, окружности, треугольник, прямые
добавить список объектов
"""
from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import QMessageBox, QApplication, QMainWindow, QTableWidgetItem
import ui
from graph import Point, Circle, Triangle, Line, GraphicsManager
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


def get_or_else(x, y):
    return x if x is not None else y


class MplCanvas(FigureCanvasQTAgg):

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.callback(event)

    def __init__(self, width=5, height=4, dpi=100, callback=lambda x: x):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        self.callback = callback


class Window:
    def __init__(self):
        self.app = QApplication([])
        self.window = QMainWindow()
        self.ui = ui.Ui_Planimetr()
        self.ui.setupUi(self.window)
        self.window.setFixedSize(800, 600)
        self.plot = None
        self.x_start = 100
        self.y_start = 30
        self.x_end = 711
        self.y_end = 220
        self.x_diff = self.x_end - self.x_start
        self.y_diff = self.y_end - self.y_start
        self.connect()
        self.points = []
        self.xlim = (-300, 300)
        self.ylim = (-100, 100)
        self.selected_type = 0
        self.types_dict = {
            0: Point,
            1: Line,
            2: Triangle,
            3: Circle
        }
        self.gm = GraphicsManager(self.xlim, self.ylim)
        self.gm.temp_points = self.points
        self.ui.xlim_low.setValue(self.xlim[0])
        self.ui.xlim_high.setValue(self.xlim[1])
        self.ui.ylim_low.setValue(self.ylim[0])
        self.ui.ylim_high.setValue(self.ylim[1])
        self.redraw()

    def on_change_type(self, index: int):
        self.selected_type = index
        self.cancel_selection()

    def cancel_selection(self):
        self.points.clear()
        self.update_status()
        self.redraw()

    def refill_table(self):
        table = self.ui.elementsTable
        for i in range(table.rowCount() - 1, -1, -1):
            table.removeRow(i)
        obj_type = self.types_dict[self.selected_type]
        type_name = obj_type.__name__
        objects = self.gm.objects[obj_type]
        for i, o in enumerate(objects):
            table.insertRow(i)
            table.setItem(i, 0, QTableWidgetItem(type_name))
            table.setItem(i, 1, QTableWidgetItem(repr(o)))

    def redraw(self):
        if self.plot is not None:
            self.ui.graphLayout.removeWidget(self.plot)
        self.plot = MplCanvas(callback=self.process_click)
        self.gm.draw(self.plot.axes)
        self.ui.graphLayout.addWidget(self.plot)
        self.refill_table()

    def process_click(self, event):
        pos = event.pos()
        x, y = pos.x(), pos.y()  # 500 230
        if (self.x_start <= x <= self.x_end) and (self.y_start <= y <= self.y_end):
            # x_diff = 600
            # y_diff = 200
            x -= self.x_start  # 500 - 100 = 400
            y -= self.y_start  # 230 - 30 = 200
            x_lim_start, x_lim_end = self.xlim  # -200, 200
            y_lim_start, y_lim_end = self.ylim  # 0, 100
            x_lim_diff = x_lim_end - x_lim_start  # 400
            y_lim_diff = y_lim_end - y_lim_start  # 100
            x = x * x_lim_diff / self.x_diff + x_lim_start  # 400 * 400 / 600 = 400 * 2/3 ?= 266
            y = y * y_lim_diff / self.y_diff + y_lim_start  # 200 * 100 / 200 = 100
            self.on_clicked_point(x, -y + self.ylim[0] + self.ylim[1])

    def update_status(self):
        if self.selected_type == 0:
            self.ui.statusLabel.setText('Нажмите, чтобы поставить точку')
            self.ui.x2_in.setDisabled(True)
            self.ui.x2_label.setDisabled(True)
            self.ui.y2_in.setDisabled(True)
            self.ui.y2_label.setDisabled(True)
            self.ui.x3_in.setDisabled(True)
            self.ui.x3_label.setDisabled(True)
            self.ui.y3_in.setDisabled(True)
            self.ui.y3_label.setDisabled(True)
        elif self.selected_type == 1 or self.selected_type == 3:
            self.ui.statusLabel.setText(f'Выбрано точек: {len(self.points)}/2')
            self.ui.x2_in.setEnabled(True)
            self.ui.x2_label.setEnabled(True)
            self.ui.y2_in.setEnabled(True)
            self.ui.y2_label.setEnabled(True)
            self.ui.x3_in.setDisabled(True)
            self.ui.x3_label.setDisabled(True)
            self.ui.y3_in.setDisabled(True)
            self.ui.y3_label.setDisabled(True)
        elif self.selected_type == 2:
            self.ui.statusLabel.setText(f'Выбрано точек: {len(self.points)}/3')
            self.ui.x2_in.setEnabled(True)
            self.ui.x2_label.setEnabled(True)
            self.ui.y2_in.setEnabled(True)
            self.ui.y2_label.setEnabled(True)
            self.ui.x3_in.setEnabled(True)
            self.ui.x3_label.setEnabled(True)
            self.ui.y3_in.setEnabled(True)
            self.ui.y3_label.setEnabled(True)

    def on_clicked_point(self, x, y):
        match self.selected_type:
            case 0:
                self.gm.objects[Point].append(Point(x, y))
            case 1:
                if len(self.points) == 1:
                    x2, y2 = self.points[0].x, self.points[0].y
                    self.gm.objects[Line].append(Line(x, y, x2, y2))
                    self.points.clear()
                else:
                    self.points.append(Point(x, y))
            case 2:
                if len(self.points) == 2:
                    x2, y2 = self.points[0].x, self.points[0].y
                    x3, y3 = self.points[1].x, self.points[1].y
                    self.gm.objects[Triangle].append(Triangle(x, y, x2, y2, x3, y3))
                    self.points.clear()
                else:
                    self.points.append(Point(x, y))
            case 3:
                if len(self.points) == 1:
                    x2, y2 = self.points[0].x, self.points[0].y
                    self.gm.objects[Circle].append(Circle(x2, y2, x, y))
                    self.points.clear()
                else:
                    self.points.append(Point(x, y))

        self.update_status()
        self.redraw()

    def run(self):
        self.window.show()
        self.app.exec()

    def aboutMessage(self):
        Window.show_message_box('About that program',
                                'Author: UncleDrema ( Дремин Кирилл ИУ7-26Б ) \n'
                                'This program is designed to solve planimetric issues.')

    def connect(self):
        self.ui.primitiveTypeBox.currentIndexChanged.connect(self.on_change_type)
        self.ui.xlim_low.valueChanged.connect(lambda x: self.set_limits(xlim_low=x))
        self.ui.xlim_high.valueChanged.connect(lambda x: self.set_limits(xlim_high=x))
        self.ui.ylim_low.valueChanged.connect(lambda x: self.set_limits(ylim_low=x))
        self.ui.ylim_high.valueChanged.connect(lambda x: self.set_limits(ylim_high=x))
        self.ui.clearAllButton.clicked.connect(self.clearAll)
        self.ui.clearCurrentButton.clicked.connect(self.clearCurrent)
        self.ui.clearAllAction.triggered.connect(self.clearAll)
        self.ui.clearAllAction.setShortcut(QKeySequence('Shift+Delete'))
        self.ui.clearCurrentAction.triggered.connect(self.clearCurrent)
        self.ui.clearCurrentAction.setShortcut(QKeySequence('Delete'))
        self.ui.cancelPointsAction.triggered.connect(self.cancel_selection)
        self.ui.cancelPointsAction.setShortcut(QKeySequence('Esc'))
        self.ui.addButton.clicked.connect(self.add_object)
        self.ui.actionAbout.triggered.connect(self.aboutMessage)
        self.ui.solveButton.clicked.connect(self.solve)

    def solve(self):
        radius = self.ui.radius.value()
        self.gm.solve(radius)
        self.redraw()

    def add_object(self):
        x1 = x2 = x3 = y1 = y2 = y3 = 0
        match self.selected_type:
            case 0:
                try:
                    x1 = float(self.ui.x1_in.text())
                    y1 = float(self.ui.y1_in.text())
                except ValueError:
                    Window.show_message_box('Некорректный ввод', 'Введённые вами данные некорректны!', True)
                    return
                self.gm.objects[Point].append(Point(x1, y1))
            case 1:
                try:
                    x1 = float(self.ui.x1_in.text())
                    y1 = float(self.ui.y1_in.text())
                    x2 = float(self.ui.x2_in.text())
                    y2 = float(self.ui.y2_in.text())
                except ValueError:
                    Window.show_message_box('Некорректный ввод', 'Введённые вами данные некорректны!', True)
                    return
                self.gm.objects[Line].append(Line(x1, y1, x2, y2))
            case 2:
                try:
                    x1 = float(self.ui.x1_in.text())
                    y1 = float(self.ui.y1_in.text())
                    x2 = float(self.ui.x2_in.text())
                    y2 = float(self.ui.y2_in.text())
                    x3 = float(self.ui.x3_in.text())
                    y3 = float(self.ui.y3_in.text())
                except ValueError:
                    Window.show_message_box('Некорректный ввод', 'Введённые вами данные некорректны!', True)
                    return
                self.gm.objects[Triangle].append(Triangle(x1, y1, x2, y2, x3, y3))
            case 3:
                try:
                    x1 = float(self.ui.x1_in.text())
                    y1 = float(self.ui.y1_in.text())
                    x2 = float(self.ui.x2_in.text())
                    y2 = float(self.ui.y2_in.text())
                except ValueError:
                    Window.show_message_box('Некорректный ввод', 'Введённые вами данные некорректны!', True)
                    return
                self.gm.objects[Circle].append(Circle(x1, y1, x2, y2))
        self.redraw()

    def clearAll(self):
        for o in self.gm.objects:
            self.gm.objects[o].clear()
        self.redraw()

    def clearCurrent(self):
        selected_index = self.ui.elementsTable.currentRow()
        if selected_index == -1:
            return
        objects = []
        match self.selected_type:
            case 0:
                objects = self.gm.objects[Point]
            case 1:
                objects = self.gm.objects[Line]
            case 2:
                objects = self.gm.objects[Triangle]
            case 3:
                objects = self.gm.objects[Circle]
        del objects[selected_index]
        self.redraw()

    def set_limits(self, xlim_low=None, xlim_high=None, ylim_low=None, ylim_high=None):
        self.xlim = (get_or_else(xlim_low, self.xlim[0]), get_or_else(xlim_high, self.xlim[1]))
        self.ylim = (get_or_else(ylim_low, self.ylim[0]), get_or_else(ylim_high, self.ylim[1]))
        self.gm.set_limits(self.xlim, self.ylim)
        self.redraw()

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


if __name__ == "__main__":
    window = Window()
    window.run()
