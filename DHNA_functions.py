"""
    Author: Riley Guest
    Company: FORO Energy
    Scope: User Interface for data analysis

"""
import matplotlib
import matplotlib.pyplot as plt
plt.style.use('seaborn')
plt.grid(True)
import numpy
import scipy as sp
import pandas as pd
import subprocess
import glob
from PyQt5 import *
import os
import sys
import time
from datetime import datetime

day = time.strftime("%b_%d_%Y", time.localtime())
# time = time.strftime("%H:%M:%S", time.localtime())
fname = time.strftime("%H%M%S", time.localtime())
fiber_length = .15 # in km

def pspc():
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
            corr = tr/sp
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
        loss = round((10*numpy.log(trans_average2/trans_average1))/fiber_length, 3)
        plt.plot(split, label='Initial Split Power')
        plt.plot(trans, label='Initial Transmitted Power')
        plt.title("Post Splice Power Correlation "+day+"\nLoss: "+str(loss)+"db/km")
        plt.legend(loc=0)
        plt.savefig(r"Plots\PC_"+fname+".png")


def close():
    sys.exit()


def directory_warning():
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText("Directory is empty.\nPlease make sure the files that need to be analyzed are in the correct place.")
    msg.setInformativeText("Any questions contact:\nriley.guest@foroenergy.com")
    msg.setWindowTitle("Error!")
    msg.setDetailedText("Please make sure all the necessary directories have files in them for proper analysis.")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)  # | QtWidgets.QMessageBox.Cancel)
    msg.exec()

def fiberlength_warning():
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText("Please fill in the fiber length (in km) in the line provided.")
    msg.setInformativeText("Any questions contact:\nriley.guest@foroenergy.com")
    msg.setWindowTitle("Error!")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)  # | QtWidgets.QMessageBox.Cancel)
    msg.exec()

def software_warning():
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText("This software isn't detected on your system.\nPress okay to begin installer.")
    msg.setInformativeText("Any questions contact:\nriley.guest@foroenergy.com")
    msg.setWindowTitle("Error!")
    msg.setDetailedText("Please make sure all the necessary directories have files in them for proper analysis.")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)  # | QtWidgets.QMessageBox.Cancel)
    msg.exec()

def thorLabs():
    tlSoftware = r"Thorlabs\PowerMeters\MultiPowerMeter\THO Multi Power Meter.exe"
    tlInstaller = r"ThorlabsPowerMeter_1.0.2\setup.exe"
    if not tlSoftware:
        software_warning()
        subprocess.Popen(tlInstaller)
    else:
        subprocess.Popen(tlSoftware)


def LBP2():
    newportSoftware = r"Newport\LBP2 Series\Spiricon.Version5.exe"
    newportInstaller = r"Newport LBP HR USB 2.0 rev.1.14.zip\Newport LBP HR USB 2.0 rev.1.14\Setup.exe"
    if not newportSoftware:
        software_warning()
        subprocess.Popen(newportInstaller)
    else:
        subprocess.Popen(newportSoftware)


