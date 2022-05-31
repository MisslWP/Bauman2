from PyQt6.QtGui import QPixmap

import bmp_utils
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from os.path import exists
from PyQt6 import QtCore
import ui


class Window:
    def __init__(self):
        self.app = QApplication([])
        self.window = QMainWindow()
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.ui.imageLabel.setScaledContents(True)
        self.connect()

    def choose(self):
        self.ui.textToSave.clear()
        file = QFileDialog.getOpenFileName(self.window, 'Open BMP file', filter='Image Files (*.bmp)')[0]
        self.ui.pathText.setText(file)
        pixmap = QPixmap(file)
        self.ui.imageLabel.setPixmap(pixmap.scaled(self.ui.imageLabel.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))
        if exists(file):
            self.ui.textToSave.setText(bmp_utils.text_from_file(file))

    def validate_text(self) -> bool:
        try:
            self.ui.textToSave.toPlainText().encode('ascii')
        except UnicodeEncodeError:
            return False
        return True

    def save(self):
        if self.validate_text():
            file = QFileDialog.getSaveFileName(self.window, 'Save to BMP file', filter='Image Files (*.bmp)')[0]
            if not exists(self.ui.pathText.text()):
                Window.show_message_box('Error', 'Chosen file does not exist!', True)
                return
            try:
                bmp_utils.save_with_text(self.ui.pathText.text(), file, self.ui.textToSave.toPlainText())
            except ValueError:
                Window.show_message_box('Error', 'Inputted text is too large!', True)
            except FileNotFoundError:
                pass
        else:
            Window.show_message_box('Error', 'Inputted text can not be encoded to ASCII', True)

    def connect(self):
        self.ui.actionAbout.triggered.connect(self.aboutMessage)
        self.ui.chooseButton.clicked.connect(self.choose)
        self.ui.actionChoose.triggered.connect(self.ui.chooseButton.click)
        self.ui.saveButton.clicked.connect(self.save)
        self.ui.actionSave.triggered.connect(self.ui.saveButton.click)

    def aboutMessage(self):
        Window.show_message_box('About that program',
                                'Author: UncleDrema ( Дремин Кирилл ИУ7-26Б ) \n'
                                'This program is to read and hide information in images.')

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

    def run(self):
        self.window.show()
        self.app.exec()


if __name__ == "__main__":
    app = Window()
    app.run()
