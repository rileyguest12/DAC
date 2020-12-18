'''
Author: Riley Guest
Scope:  OTDR Calculator
Function:   To calculate length of a fiber optic cable and calculate loss in db/km.'
'''
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QPixmap
import numpy as np


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Fiber Calculations")
        self.setFixedSize(self.sizeHint())

        self.picture = QtWidgets.QLabel()
        self.picture.setPixmap(QPixmap("foro_desktop_icon.png"))

        self.fiber_length = QtWidgets.QLabel('0.0')
        self.fiber_length.setStyleSheet('font-size:12pt;font:bold')

        self.fiber_length_label = QtWidgets.QLabel("Fiber Length (m): ")
        self.fiber_length_label.setStyleSheet('font-size:12pt;font:bold')

        self.delta_pulse_label = QtWidgets.QLabel("Delta t (s): ")
        self.delta_pulse_label.setStyleSheet('font-size:12pt;font:bold')

        self.delta_pulse_input = QtWidgets.QLineEdit()
        self.delta_pulse_input.setStyleSheet('font-size:12pt;font:bold')

        self.power_in_label = QtWidgets.QLabel('Power In (W): ')
        self.power_in_label.setStyleSheet('font-size:12pt;font:bold')

        self.power_in_input = QtWidgets.QLineEdit()
        self.power_in_input.setStyleSheet('font-size:12pt;font:bold')

        self.power_out_label = QtWidgets.QLabel('Power Out (W): ')
        self.power_out_label.setStyleSheet('font-size:12pt;font:bold')

        self.power_out_input = QtWidgets.QLineEdit()
        self.power_out_input.setStyleSheet('font-size:12pt;font:bold')

        self.loss_label = QtWidgets.QLabel("Loss (db/km): ")
        self.loss_label.setStyleSheet('font-size:12pt;font:bold')

        self.loss = QtWidgets.QLabel('0.0')
        self.loss.setStyleSheet('font-size:12pt;font:bold')

        self.est_length_label = QtWidgets.QLabel('Estimated Length (km): ')
        self.est_length_label.setStyleSheet('font-size:12pt;font:bold')

        self.est_length_input = QtWidgets.QLineEdit()
        self.est_length_input.setStyleSheet('font-size:12pt;font:bold')

        self.calculatelength_button = QtWidgets.QPushButton('Calculate Length')
        self.calculatelength_button.setStyleSheet('font-size:12pt;font:bold')
        self.calculatelength_button.clicked.connect(self.calculatelength)

        self.calculateloss_button = QtWidgets.QPushButton('Calculate Loss')
        self.calculateloss_button.setStyleSheet('font-size:12pt;font:bold')
        self.calculateloss_button.clicked.connect(self.calculateloss)

        self.close_button = QtWidgets.QPushButton('Close')
        self.close_button.setStyleSheet('font-size:12pt;font:bold')
        self.close_button.clicked.connect(self.close)

        self.otdrcalculator = QtWidgets.QLabel('OTDR Calculator')
        self.otdrcalculator .setStyleSheet('font-size:16pt;font:bold')

        self.fiberlosscalculator = QtWidgets.QLabel('Fiber Loss Calculator')
        self.fiberlosscalculator .setStyleSheet('font-size:16pt;font:bold')

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QGridLayout(central_widget)

        '''addWidget (self, QWidget, row, column, rowSpan, columnSpan, Qt.Alignment alignment = 0)'''
        layout.addWidget(self.picture, 0, 2, 1, 1)
        layout.addWidget(self.otdrcalculator, 1, 0, 1, 2)
        layout.addWidget(self.fiberlosscalculator, 1, 5, 1, 1)
        layout.addWidget(self.delta_pulse_label, 2, 0, 1, 1)
        layout.addWidget(self.delta_pulse_input, 2, 1, 1, 1)
        layout.addWidget(self.fiber_length_label, 3, 0, 1, 1)
        layout.addWidget(self.fiber_length, 3, 1, 1, 2)
        layout.addWidget(self.est_length_label, 2, 5, 1, 1)
        layout.addWidget(self.est_length_input, 2, 6, 1, 2)
        layout.addWidget(self.power_in_label, 3, 5, 1, 1)
        layout.addWidget(self.power_in_input, 3, 6, 1, 2)
        layout.addWidget(self.power_out_label, 4, 5, 1, 1)
        layout.addWidget(self.power_out_input, 4, 6, 1, 2)
        layout.addWidget(self.loss_label, 5, 5, 1, 1)
        layout.addWidget(self.loss, 5, 6, 1, 2)
        layout.addWidget(self.calculatelength_button, 6, 0, 1, 1)
        layout.addWidget(self.calculateloss_button, 6, 5, 2, 1)
        layout.addWidget(self.close_button, 8, 2, 1, 2)

    @QtCore.pyqtSlot()
    def calculateloss(self):
        if len(self.power_in_input.text()) == 0 or len(self.power_out_input.text()) == 0 \
                or len(self.est_length_input.text()) == 0:
            self.powerinputWarning()

        else:
            power_in = float(self.power_in_input.text())
            power_out = float(self.power_out_input.text())
            est_length = float(self.est_length_input.text())
            loss = float((10*np.log10(power_out/power_in))/est_length)
            self.loss.setText((str(round(loss, 2))))

    @QtCore.pyqtSlot()
    def calculatelength(self):
        if len (self.delta_pulse_input.text()) == 0:
            self.deltainputWarning()
        else:
            delta = float(self.delta_pulse_input.text())
            n = 1.4546
            speed_of_light = 3e8
            speed_in_medium = speed_of_light/n
            length = round(speed_in_medium * (delta/2), 2)
            fiber_length = str(length)
            self.fiber_length.setText(fiber_length)

    @QtCore.pyqtSlot(bool)
    def close(self):
        sys.exit()

    @QtCore.pyqtSlot()
    def deltainputWarning(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Please fill in the time between pulses.")
        msg.setInformativeText("Any questions contact:\nriley.guest@foroenergy.com")
        msg.setWindowTitle("General Information")
        msg.setDetailedText("Please make sure all the necessary requirements are filled.")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)  # | QtWidgets.QMessageBox.Cancel)
        msg.exec()

    @QtCore.pyqtSlot()
    def powerinputWarning(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Please fill in the the power in and power out requirements.")
        msg.setInformativeText("Any questions contact:\nriley.guest@foroenergy.com")
        msg.setWindowTitle("General Information")
        msg.setDetailedText("Please make sure all the necessary requirements are filled.")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)  # | QtWidgets.QMessageBox.Cancel)
        msg.exec()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('foro_window_icon.ico'))  # made on the website https://icoconvert.com/
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
