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
        font = QtGui.QFont()
        font.setFamily("Hack")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pathText = QtWidgets.QLineEdit(self.centralwidget)
        self.pathText.setGeometry(QtCore.QRect(200, 70, 591, 31))
        self.pathText.setObjectName("pathText")
        self.headerLabel = QtWidgets.QLabel(self.centralwidget)
        self.headerLabel.setGeometry(QtCore.QRect(210, 0, 351, 41))
        font = QtGui.QFont()
        font.setFamily("Hack")
        font.setPointSize(20)
        font.setItalic(False)
        self.headerLabel.setFont(font)
        self.headerLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.headerLabel.setObjectName("headerLabel")
        self.chooseButton = QtWidgets.QPushButton(self.centralwidget)
        self.chooseButton.setGeometry(QtCore.QRect(10, 70, 171, 34))
        self.chooseButton.setObjectName("chooseButton")
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(10, 520, 781, 31))
        self.saveButton.setObjectName("saveButton")
        self.textToSave = QtWidgets.QTextEdit(self.centralwidget)
        self.textToSave.setGeometry(QtCore.QRect(10, 110, 371, 361))
        self.textToSave.setObjectName("textToSave")
        self.textLabel = QtWidgets.QLabel(self.centralwidget)
        self.textLabel.setGeometry(QtCore.QRect(10, 470, 351, 41))
        font = QtGui.QFont()
        font.setFamily("Hack")
        font.setPointSize(20)
        font.setItalic(False)
        self.textLabel.setFont(font)
        self.textLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.textLabel.setObjectName("textLabel")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(390, 110, 401, 351))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.imageLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.imageLayout.setContentsMargins(0, 0, 0, 0)
        self.imageLayout.setObjectName("imageLayout")
        self.imageLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.imageLabel.setText("")
        self.imageLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.imageLabel.setObjectName("imageLabel")
        self.imageLayout.addWidget(self.imageLabel)
        self.imageLabelText = QtWidgets.QLabel(self.centralwidget)
        self.imageLabelText.setGeometry(QtCore.QRect(410, 470, 351, 41))
        font = QtGui.QFont()
        font.setFamily("Hack")
        font.setPointSize(20)
        font.setItalic(False)
        self.imageLabelText.setFont(font)
        self.imageLabelText.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.imageLabelText.setObjectName("imageLabelText")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 29))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionChoose = QtGui.QAction(MainWindow)
        self.actionChoose.setObjectName("actionChoose")
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuHelp.addAction(self.actionAbout)
        self.menuFile.addAction(self.actionChoose)
        self.menuFile.addAction(self.actionSave)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Image Cypher 9000"))
        self.headerLabel.setText(_translate("MainWindow", "Image Cypher 9000"))
        self.chooseButton.setText(_translate("MainWindow", "Choose file"))
        self.saveButton.setText(_translate("MainWindow", "Save as"))
        self.textLabel.setText(_translate("MainWindow", "Your text"))
        self.imageLabelText.setText(_translate("MainWindow", "Your image"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionChoose.setText(_translate("MainWindow", "Choose file"))
        self.actionSave.setText(_translate("MainWindow", "Save as"))
