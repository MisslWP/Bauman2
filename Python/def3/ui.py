# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.chooseButton = QtWidgets.QPushButton(self.centralwidget)
        self.chooseButton.setGeometry(QtCore.QRect(20, 10, 171, 34))
        self.chooseButton.setObjectName("chooseButton")
        self.imageLabelText = QtWidgets.QLabel(self.centralwidget)
        self.imageLabelText.setGeometry(QtCore.QRect(220, 460, 351, 41))
        font = QtGui.QFont()
        font.setFamily("Hack")
        font.setPointSize(20)
        font.setItalic(False)
        self.imageLabelText.setFont(font)
        self.imageLabelText.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.imageLabelText.setObjectName("imageLabelText")
        self.pathText = QtWidgets.QLineEdit(self.centralwidget)
        self.pathText.setGeometry(QtCore.QRect(200, 10, 591, 31))
        self.pathText.setObjectName("pathText")
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(20, 520, 781, 31))
        self.saveButton.setObjectName("saveButton")
        self.imageLabel_2 = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel_2.setGeometry(QtCore.QRect(48, 80, 731, 349))
        self.imageLabel_2.setText("")
        self.imageLabel_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.imageLabel_2.setObjectName("imageLabel_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.chooseButton.setText(_translate("MainWindow", "Choose file"))
        self.imageLabelText.setText(_translate("MainWindow", "Your image"))
        self.saveButton.setText(_translate("MainWindow", "Make brighter and save as"))
