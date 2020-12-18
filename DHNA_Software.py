"""
    Author: Riley Guest
    Scope: User Interface for data analysis on the xxx project

"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QIcon
from DHNA_functions import close, directory_warning, thorLabs, LBP2, fiberlength_warning
import time
import glob
import os
import numpy
import matplotlib.pyplot as plt

day = time.strftime("%b_%d_%Y", time.localtime())
# time = time.strftime("%H:%M:%S", time.localtime())
fname = time.strftime("%H%M%S", time.localtime())


class Ui_MainWindow(object):

    def pspc(self):
        if len(self.fiberlength.text()) == 0:
            fiberlength_warning()
        else:
            files = glob.glob(r"PostSplicePowerCorrelation\*.txt")
            if not files:
                return directory_warning()
            else:
                mostRecent = max(files, key=os.path.getctime)
                file = open(mostRecent)
                # print(mostRecent)
                lines = file.readlines()[2:]
                split = []
                trans = []
                for line in lines:
                    sp = (line.split()[3])
                    sp = float(sp)
                    tr = (line.split()[4])
                    tr = float(tr)
                    split.append(sp)
                    trans.append(tr)
                    corr = tr / sp
                split_average = numpy.average(sp)
                trans_average1 = numpy.max(tr)
                # plt.figure(1, figsize=(10, 6))
                plt.plot(split, label='Post Split Power')
                plt.plot(trans, label='Post Transmitted Power')
                plt.xlabel("Data/Steps")
                plt.ylabel("Laser Power (mW)")

            files = glob.glob(r"InitialPowerCorrelation\*.txt")
            if not files:
                return directory_warning()
            else:
                mostRecent = max(files, key=os.path.getctime)
                file = open(mostRecent)
                # print(mostRecent)
                lines = file.readlines()[2:]
                split = []
                trans = []
                for line in lines:
                    sp = (line.split()[3])
                    sp = float(sp)
                    tr = (line.split()[4])
                    tr = float(tr)
                    split.append(sp)
                    trans.append(tr)
                split_average = numpy.average(sp)
                trans_average2 = numpy.max(tr)
                fiber_length = float(self.fiberlength.text())
                loss = round((10 * numpy.log(trans_average2 / trans_average1)) / fiber_length, 3)
                plt.plot(split, label='Initial Split Power')
                plt.plot(trans, label='Initial Transmitted Power')
                plt.title("Post Splice Power Correlation " + day + "\nFiber Length (km): " + str(fiber_length) +"\nLoss: " + str(loss) + " db/km")
                plt.legend(loc=0)
                plt.savefig(r"Plots\PC_" + fname + ".png")
                plt.show()

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.picture = QtWidgets.QLabel(self.centralwidget)
        self.picture.setPixmap(QPixmap("logo1.png"))
        self.picture.move(200, 25)

        self.fiberlength = QtWidgets.QLineEdit(self.centralwidget)
        self.fiberlength.setGeometry(QtCore.QRect(20, 300, 200, 21))

        self.thorlabsSoftware = QtWidgets.QPushButton(self.centralwidget)
        self.thorlabsSoftware.setGeometry(QtCore.QRect(20, 350, 200, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.thorlabsSoftware.setFont(font)
        self.thorlabsSoftware.setObjectName("pushButton")
        self.thorlabsSoftware.clicked.connect(thorLabs)

        self.postspliceAnalysis = QtWidgets.QPushButton(self.centralwidget)
        self.postspliceAnalysis.setGeometry(QtCore.QRect(20, 400, 200, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.postspliceAnalysis.setFont(font)
        self.postspliceAnalysis.setObjectName("pushButton_2")
        self.postspliceAnalysis.clicked.connect(self.pspc)

        self.newportSoftware = QtWidgets.QPushButton(self.centralwidget)
        self.newportSoftware.setGeometry(QtCore.QRect(20, 450, 200, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.newportSoftware.setFont(font)
        self.newportSoftware.setObjectName("pushButton_3")
        self.newportSoftware.clicked.connect(LBP2)

        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setGeometry(QtCore.QRect(20, 500, 200, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.closeButton.setFont(font)
        self.closeButton.setObjectName("pushButton_4")
        self.closeButton.clicked.connect(close)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 190, 611, 31))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        MainWindow.setCentralWidget(self.centralwidget)         # setting
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)       # setting statusbar widget
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)                          # allowing retranslateUi to be inside of "MainWindow"
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):                        # retranslateUi function to set text on all widgets
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DHNA Tool Software"))
        self.thorlabsSoftware.setText(_translate("MainWindow", "Thor Labs Power Meter"))
        self.postspliceAnalysis.setText(_translate("MainWindow", "Post Splice Power Analysis"))
        self.newportSoftware.setText(_translate("MainWindow", "Newport LBP2 Software"))
        self.label.setText(_translate("MainWindow", "Downhole Numerical Aperture Analyzer"))
        self.fiberlength.setPlaceholderText(_translate("MainWindow", "Enter fiber length in km"))
        self.closeButton.setText(_translate("MainWindow", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    app.setWindowIcon(QtGui.QIcon('foro_window_icon.ico'))  # made on the website https://icoconvert.com/
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

