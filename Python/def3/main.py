from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from struct import pack, unpack
from PyQt6 import QtCore
from os.path import exists
import ui

class Window:
    def __init__(self):
        self.app = QApplication([])
        self.window = QMainWindow()
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.ui.imageLabel_2.setScaledContents(True)
        self.connect()

    def set_file(self, file):
        self.ui.pathText.setText(file)
        pixmap = QPixmap(file)
        self.ui.imageLabel_2.setPixmap(
            pixmap.scaled(self.ui.imageLabel_2.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                          QtCore.Qt.TransformationMode.SmoothTransformation))

    def choose(self):
        file = QFileDialog.getOpenFileName(self.window, 'Open BMP file', filter='Image Files (*.bmp)')[0]
        self.set_file(file)

    def bright(self):
        bts = bytearray()
        with open(self.ui.pathText.text(), 'rb') as file:
            head_bytes = file.read(14)
            bts.extend(head_bytes)
            hdr = unpack('<HLHHL', head_bytes)
            inf_bytes = file.read(hdr[4]-14)
            bts.extend(inf_bytes)
            while (pix := file.read(3)) != b'':
                pixel = unpack('<BBB', pix)
                pixel = list(map(lambda x: min(255, x+20), pixel))
                bts.extend(pack('<BBB', pixel[0], pixel[1], pixel[2]))
        file = QFileDialog.getSaveFileName(self.window, 'Save to BMP file', filter='Image Files (*.bmp)')[0]
        try:
            with open(file, 'wb') as out_f:
                out_f.write(bts)
        except FileNotFoundError:
            pass


    def connect(self):
        self.ui.saveButton.clicked.connect(self.bright)
        self.ui.chooseButton.clicked.connect(self.choose)

    def run(self):
        self.window.show()
        self.app.exec()


if __name__ == "__main__":
    app = Window()
    app.run()

