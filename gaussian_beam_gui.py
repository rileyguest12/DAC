import sys
import PyQt5
import matplotlib
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import constants
plt.style.use('seaborn')
plt.tight_layout()

class Window(QDialog):              # Calling the class "window" using QDialog

    def setupUi(self, MainWindow):              # Start of the function "setupUi" with self and MainWindow as a variable

        MainWindow.setObjectName("MainWindow")  # Naming the MainWindow object "MainWindow
        MainWindow.resize(400, 400)         # Ability to resize the MainWindow

        self.centralwidget = QtWidgets.QWidget(MainWindow)  # Creating 'central widget' as a QtWidget from Qwidget
        self.centralwidget.setObjectName("centralwidget")   # Naming the centralwidget object "centralwidget"

    def __init__(self, parent=None):   # Defining the init class function, this is where all the design will be put in
        super(Window, self).__init__(parent)        # Super as Window and init as a parent
        self.setWindowTitle("Gaussian Beam")
        self.figure = plt.figure(figsize=(15, 15))      # Using the figure function to declare 'self.figure' as
        plt.grid(True)                                                        # The plot figure
        plt.legend(loc=0)
        plt.title("Gaussian Laser Beam")
        self.canvas = FigureCanvas(self.figure)     # This is the Canvas Widget that displays the `figure`
        self.canvas.resize(12,15)               # It takes the `figure` instance as a parameter to __init__

        self.toolbar = NavigationToolbar(self.canvas, self)     # This is the Navigation widget,
                                                                # Takes the Canvas widget and a parent
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)
        self.button.setDefault(False)
        self.button.setAutoDefault(True)

        self.close = QPushButton('Close')
        self.close.clicked.connect(self.end)

        self.title = QLabel("\tGaussian Laser Beam Model")
        self.title.setStyleSheet("font-size: 18pt; font: bold")

        self.dive = QLabel()
        self.dive.setText("Divergence (half angle) :")
        self.dive.setStyleSheet('font:bold')

        self.focal_length = QLabel()
        self.focal_length.setText("Lens Focal Length (m) :")
        self.focal_length.setStyleSheet('font:bold')

        self.wavelength = QLabel()
        self.wavelength.setText("Wavelength (nm) :")
        self.wavelength.setStyleSheet('font:bold')

        self.diveinput = QLineEdit()
        self.diveinput.setPlaceholderText("Divergence in radians")

        self.focal_lengthinput = QLineEdit()
        self.focal_lengthinput.setPlaceholderText("Focal length of lens in meters")

        self.wavelength_input = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.dive)
        layout.addWidget(self.diveinput)
        layout.addWidget(self.focal_length)
        layout.addWidget(self.focal_lengthinput)
        layout.addWidget(self.wavelength)
        layout.addWidget(self.wavelength_input)
        layout.addWidget(self.button)
        layout.addWidget(self.close)
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)
        self.setLayout(layout)

    def plot(self):
        if len(self.diveinput.text()) == 0 or len(self.focal_lengthinput.text()) == 0 or \
                len(self.wavelength_input.text()) == 0 or float(self.diveinput.text()) < 0 or \
                float(self.focal_lengthinput.text()) < 0 or float(self.wavelength_input.text()) < 0:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Error!\nPlease Check All Inputs.")
            msg.setWindowTitle("Error!")
            msg.setDetailedText("Please make sure all the necessary categories are filled for proper calculations.")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)  # | QtWidgets.QMessageBox.Cancel)
            msg.exec()

        else:
            self.figure.clf()
            divergence = float(self.diveinput.text())
            fl = float(self.focal_lengthinput.text())
            wavelength = float(self.wavelength_input.text()) * 1e-9
            pi = 3.14159
            waist = fl * divergence
            zR = pi * waist**2 / wavelength
            z = np.arange(2*-zR, 2*zR, zR/100)
            wz = waist * np.sqrt(1+(z/zR)**2)
            confocal_parameter = zR * 2
            ax = self.figure.add_subplot(111)
            plt.title('Gaussian Laser Beam')
            plt.xlabel('Z')
            plt.ylabel("Beam Width")
            ax.plot(z, wz, color='red', label='Laser Beam', alpha=.3)
            ax.plot(z, -wz, color='red', alpha=0.3)
            plt.axvline(zR, ymin=.225, ymax=.775, linewidth=3, color='black', label="Confocal Parameter | " +str(round(confocal_parameter,9)))
            plt.axvline(-zR, ymin=.225, ymax=.775,linewidth=3,color='black')
            plt.axvline(0, ymin=.30, ymax=.70, color='blue', label="Beam Waist | " +str(round(waist, 9)))
            plt.fill_between(z, wz, -wz, color='red', alpha=0.3)
            plt.legend(loc=0)
            # plt.grid(True)
            self.canvas.draw()  # Refresh canvas

    def end(self):
        quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setWindowIcon(QtGui.QIcon('foro_window_icon.ico'))  # made on the website https://icoconvert.com/
    main = Window()
    main.show()
    sys.exit(app.exec_())
