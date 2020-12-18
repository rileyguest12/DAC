'''
Developer: Riley Guest
Scope:  SQL Data Acquisition
Function:   To fetch data from SQL database with pressing one button, visual + overlay data.
'''
import pyodbc
import pandas as pd
import os
import glob
from PyQt5 import QtCore, QtWidgets, QtSerialPort, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets
import matplotlib.pyplot as plt
plt.style.use('dark_background')
import sys

'''Setup of the UI'''
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Foro Energy DaC SQL Plotting")
        self.setFixedSize(self.sizeHint())
        self.picture = QtWidgets.QLabel()
        self.picture.setPixmap(QPixmap("logo1.png"))
        self.plotButton = QtWidgets.QPushButton("Plot Run ID 1")
        self.plotButton.setStyleSheet('font-size:10pt;font:bold')
        self.plotButton.clicked.connect(self.SQLSinglePlot1)
        self.plotButton2 = QtWidgets.QPushButton("Plot Run ID 2")
        self.plotButton2.setStyleSheet('font-size:10pt;font:bold')
        self.plotButton2.clicked.connect(self.SQLSinglePlot2)
        self.plotButton3 = QtWidgets.QPushButton("Overlay Both Run ID's")
        self.plotButton3.setStyleSheet('font-size:10pt;font:bold')
        self.plotButton3.clicked.connect(self.SQLOverlayPlot)
        self.plotButton4 = QtWidgets.QPushButton("Plot NA Run ID 1")
        self.plotButton4.setStyleSheet('font-size:10pt;font:bold')
        # self.plotButton4.clicked.connect(self.NA)
        self.closeButton = QtWidgets.QPushButton("Close")
        self.closeButton.setStyleSheet('font-size:10pt;font:bold')
        self.closeButton.clicked.connect(self.quit)
        self.runLabel = QtWidgets.QLabel("Run ID 1: ")
        self.runLabel.setStyleSheet("font-size:10pt; font:bold")
        self.runLabel2 = QtWidgets.QLabel("Run ID 2: ")
        self.runLabel2.setStyleSheet("font-size:10pt; font:bold")
        self.NARunLabel =QtWidgets.QLabel("NA Run ID: ")
        self.NARunLabel.setStyleSheet("font-size:10pt; font:bold")
        self.NARunLabel2 =QtWidgets.QLabel("NA Run ID: ")
        self.NARunLabel2.setStyleSheet("font-size:10pt; font:bold")
        self.NARunID = QtWidgets.QLineEdit()
        self.NARunID.setStyleSheet('font-size:10pt;font:bold')
        self.NARunID2 = QtWidgets.QLineEdit()
        self.NARunID2.setStyleSheet('font-size:10pt;font:bold')
        self.runID = QtWidgets.QLineEdit()
        self.runID.setStyleSheet('font-size:10pt;font:bold')
        self.runID2 = QtWidgets.QLineEdit()
        self.runID2.setStyleSheet('font-size:10pt;font:bold')
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QFormLayout(central_widget)
        row0 = QtWidgets.QHBoxLayout()
        row0.addWidget(self.NARunLabel)
        row0.addWidget(self.NARunID)
        row0.addWidget(self.NARunLabel2)
        row0.addWidget(self.NARunID2)
        row1 = QtWidgets.QHBoxLayout()
        row1.addWidget(self.runLabel)
        row1.addWidget(self.runID)
        row1.addWidget(self.runLabel2)
        row1.addWidget(self.runID2)
        row2 = QtWidgets.QHBoxLayout()
        row2.addWidget(self.plotButton)
        row2.addWidget(self.plotButton2)
        row3 = QtWidgets.QHBoxLayout()
        row3.addWidget(self.plotButton3)
        row4 = QtWidgets.QHBoxLayout()
        row4.addWidget(self.closeButton)
        row5 = QtWidgets.QHBoxLayout()
        row5.addWidget(self.plotButton4)
        layout.addRow(self.picture)
        layout.addRow(row1)
        layout.addRow(row2)
        layout.addRow(row3)
        # layout.addRow(row0)
        # layout.addRow(row5)
        layout.addRow(row4)

    @QtCore.pyqtSlot()
    def SQLSinglePlot1(self):


        server = 'insert server name here'
        database = 'insert db name here'
        username = 'insert username here'
        password = 'use password'
        driver = '{SQL Server}'     # Driver you need to connect to the database
        port = 'insert port here'
        cnn = pyodbc.connect()

        run = self.runID.text()
        runid = str(run)

        DHCTemp = cnn.cursor()
        DHCTemp = DHCTemp.execute('Select DHCTemp from RunData where RunID = '+runid)
        DHCTemp = DHCTemp.fetchall()

        DHCLight = cnn.cursor()
        DHCLight = DHCLight.execute('Select DHCLight from RunData where RunID = '+runid)
        DHCLight = DHCLight.fetchall()

        LaserPower = cnn.cursor()
        LaserPower = LaserPower.execute('Select LaserPower from RunData where RunID = '+runid)
        LaserPower = LaserPower.fetchall()

        ElapsedTime = cnn.cursor()
        ElapsedTime = ElapsedTime.execute('Select ElapsedTime from RunData where RunID = '+runid)
        ElapsedTime = ElapsedTime.fetchall()

        CutRate = cnn.cursor()
        CutRate = CutRate.execute('Select CutRate from RunData where RunID = ' + runid)
        CutRate = CutRate.fetchall()

        CHTemp = cnn.cursor()
        CHTemp = CHTemp.execute('Select CHTemp from RunData where RunID = ' + runid)
        CHTemp = CHTemp.fetchall()

        CHLight = cnn.cursor()
        CHLight = CHLight.execute('Select CHLight from RunData where RunID = ' + runid)
        CHLight = CHLight.fetchall()

        if len(ElapsedTime) == 0:# and len(DHCLight) and len(LaserPower) < 5:
            self.NoDataWarning1()

        else:
            fig, ax1 = plt.subplots(figsize=(13, 5))
            ax1.set_xlabel('Run Time', fontsize=12)
            ax1.set_ylabel('Temperature (C)\nLight Level (%)', fontsize=12)
            ax1.plot(ElapsedTime, DHCTemp, color='Red', label='DHC Temp')
            ax1.plot(ElapsedTime, DHCLight, color='Blue', label='DHC Light')
            ax1.plot(ElapsedTime, CHTemp, color='Orange', label='CH Temp')
            ax1.plot(ElapsedTime, CHLight, color='Cyan', label='CH Light')
            ax1.set_ylim(ymin=0)

            ax2 = ax1.twinx()
            ax2.set_ylabel('Laser Power (kW)\n&\nCut Rate (rev/hr)', fontsize=12)
            ax2.set_ylim(ymin=0, ymax=20)
            ax2.plot(ElapsedTime, CutRate, color='lime', label='Cut Rate (rev/hr)')
            ax2.plot(ElapsedTime, LaserPower, color='Purple', label='Laser Power')
            plt.title('DHC Connector and DaC V2 Data\nRun ID: '+runid, fontsize=12)
            ax1.legend(loc=2)
            ax2.legend(loc=1)

            plt.grid(True, color='gray')
            plt.show()

    @QtCore.pyqtSlot()
    def SQLSinglePlot2(self):

        server = 'insert server name here'
        database = 'insert db name here'
        username = 'insert username here'
        password = 'use password'
        driver = '{SQL Server}'  # Driver you need to connect to the database
        port = 'insert port here'
        cnn = pyodbc.connect()

        run2 = self.runID2.text()
        runid2 = str(run2)

        DHCTemp2 = cnn.cursor()
        DHCTemp2 = DHCTemp2.execute('Select DHCTemp from RunData where RunID = '+runid2)
        DHCTemp2 = DHCTemp2.fetchall()

        DHCLight2 = cnn.cursor()
        DHCLight2 = DHCLight2.execute('Select DHCLight from RunData where RunID = '+runid2)
        DHCLight2 = DHCLight2.fetchall()

        LaserPower2 = cnn.cursor()
        LaserPower2 = LaserPower2.execute('Select LaserPower from RunData where RunID = '+runid2)
        LaserPower2 = LaserPower2.fetchall()

        CutRate2 = cnn.cursor()
        CutRate2 = CutRate2.execute('Select CutRate from RunData where RunID = ' + runid2)
        CutRate2 = CutRate2.fetchall()

        CHTemp2 = cnn.cursor()
        CHTemp2 = CHTemp2.execute('Select CHTemp from RunData where RunID = ' + runid2)
        CHTemp2 = CHTemp2.fetchall()

        CHLight2 = cnn.cursor()
        CHLight2 = CHLight2.execute('Select CHLight from RunData where RunID = ' + runid2)
        CHLight2 = CHLight2.fetchall()

        ElapsedTime2 = cnn.cursor()
        ElapsedTime2 = ElapsedTime2.execute('Select ElapsedTime from RunData where RunID = '+runid2)
        ElapsedTime2 = ElapsedTime2.fetchall()

        if len(ElapsedTime2) == 0:# and len(DHCLight) and len(LaserPower) < 5:
            self.NoDataWarning2()
        else:

            fig, ax1 = plt.subplots(figsize=(13, 5))
            ax1.set_xlabel('Run Time', fontsize=12)
            ax1.set_ylabel('Temperature (C)\nLight Level (%)', fontsize=12)
            ax1.plot(ElapsedTime2, DHCTemp2, color='Orange', label='DHC Temp')
            ax1.plot(ElapsedTime2, DHCLight2, color='Cyan', label='DHC Light')
            ax1.plot(ElapsedTime2, CHTemp2, color='darkorange', label='CH Temp')
            ax1.plot(ElapsedTime2, CHLight2, color='lightseagreen', label='CH Light')
            ax1.set_ylim(ymin=0)
            ax2 = ax1.twinx()
            ax2.set_ylabel('Laser Power (kW)', fontsize=12)
            ax2.set_ylim(ymin=0, ymax=20)
            ax2.plot(ElapsedTime2, CutRate2, color='springgreen', label='Cut Rate (rev/hr)')
            ax2.plot(ElapsedTime2, LaserPower2, color='magenta', label='Laser Power')
            plt.title('DHC Connector and DaC V2 Data\nRun ID: '+runid2, fontsize=12)
            ax1.legend(loc=2)
            ax2.legend(loc=1)
            plt.grid(True, color='gray')
            plt.show()

    @QtCore.pyqtSlot()
    def SQLOverlayPlot(self):

        if len(self.runID.text()) == 0 or len(self.runID2.text()) == 0:
            self.runIDWarning()

        else:
            server = 'insert server name here'
            database = 'insert db name here'
            username = 'insert username here'
            password = 'use password'
            driver = '{SQL Server}'  # Driver you need to connect to the database
            port = 'insert port here'
            cnn = pyodbc.connect()

            run = self.runID.text()
            runid = str(run)

            DHCTemp = cnn.cursor()
            DHCTemp = DHCTemp.execute('Select DHCTemp from RunData where RunID = ' + runid)
            DHCTemp = DHCTemp.fetchall()

            DHCLight = cnn.cursor()
            DHCLight = DHCLight.execute('Select DHCLight from RunData where RunID = ' + runid)
            DHCLight = DHCLight.fetchall()

            LaserPower = cnn.cursor()
            LaserPower = LaserPower.execute('Select LaserPower from RunData where RunID = ' + runid)
            LaserPower = LaserPower.fetchall()

            ElapsedTime = cnn.cursor()
            ElapsedTime = ElapsedTime.execute('Select ElapsedTime from RunData where RunID = ' + runid)
            ElapsedTime = ElapsedTime.fetchall()

            run2 = self.runID2.text()
            runid2 = str(run2)

            DHCTemp2 = cnn.cursor()
            DHCTemp2 = DHCTemp2.execute('Select DHCTemp from RunData where RunID = ' + runid2)
            DHCTemp2 = DHCTemp2.fetchall()

            DHCLight2 = cnn.cursor()
            DHCLight2 = DHCLight2.execute('Select DHCLight from RunData where RunID = ' + runid2)
            DHCLight2 = DHCLight2.fetchall()

            LaserPower2 = cnn.cursor()
            LaserPower2 = LaserPower2.execute('Select LaserPower from RunData where RunID = ' + runid2)
            LaserPower2 = LaserPower2.fetchall()

            ElapsedTime2 = cnn.cursor()
            ElapsedTime2 = ElapsedTime2.execute('Select ElapsedTime from RunData where RunID = ' + runid2)
            ElapsedTime2 = ElapsedTime2.fetchall()

            if len(ElapsedTime) == 0:
                self.NoDataWarning1()
            elif len(ElapsedTime2) == 0:  # and len(DHCLight) and len(LaserPower) < 5:
                self.NoDataWarning2()
            else:
                fig, ax1 = plt.subplots(figsize=(13, 5))
                ax1.set_xlabel('Run Time', fontsize=12)
                ax1.set_ylabel('Temperature (C)\nLight Level (%)', fontsize=12)
                ax1.plot(DHCTemp, color='Red', label='DHC Temp-'+runid)
                ax1.plot(DHCTemp2, color='Orange', label='DHC Temp-'+runid2)
                ax1.plot(DHCLight, color='Blue', label='DHC Light-'+runid)
                ax1.plot(DHCLight2, color='Cyan', label='DHC Light-'+runid2)
                ax1.set_ylim(ymin=0)
                ax2 = ax1.twinx()
                ax2.set_ylabel('Laser Power (kW)', fontsize=12)
                ax2.set_ylim(ymin=0, ymax=20)
                ax2.plot(LaserPower, color='Purple', label='Laser Power-'+runid)
                ax2.plot(LaserPower2, color='magenta', label='Laser Power-'+runid2)
                plt.title("DHC Connector and DaC V2 Data Overlay;\nRun ID's in Legend", fontsize=12)
                ax1.legend(loc=2)
                ax2.legend(loc=1)
                plt.grid(True, color='gray')
                plt.show()

    @QtCore.pyqtSlot(bool)
    def quit(self):
        sys.exit()

    @QtCore.pyqtSlot()
    def runIDWarning(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Please make sure both Run ID are entered.")
        msg.setInformativeText("Any questions contact:\nriley.guest@foroenergy.com")
        msg.setWindowTitle("Stop! Enter Run ID!")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)  # | QtWidgets.QMessageBox.Cancel)
        msg.exec()

    @QtCore.pyqtSlot()
    def NoDataWarning1(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Please enter a valid Run ID 1, there is no data available.")
        msg.setInformativeText("Any questions contact:\nriley.guest@foroenergy.com")
        msg.setWindowTitle("Stop! Enter valid Run ID!")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)  # | QtWidgets.QMessageBox.Cancel)
        msg.exec()

    @QtCore.pyqtSlot()
    def NoDataWarning2(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Please enter a valid Run ID 2, there is no data available.")
        msg.setInformativeText("Any questions contact:\nriley.guest@foroenergy.com")
        msg.setWindowTitle("Stop! Enter valid Run ID!")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)  # | QtWidgets.QMessageBox.Cancel)
        msg.exec()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('foro_window_icon.ico'))  # made on the website https://icoconvert.com/
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())