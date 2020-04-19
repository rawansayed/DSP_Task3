import sys
import sounddevice as sd
from sounddevice import play
from pydub import AudioSegment
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog,QTableWidget,QTableWidgetItem
                             ,QApplication, QCheckBox, QApplication, QHBoxLayout, QWidget,QMessageBox)
import pyqtgraph as pg
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from pyqtgraph import PlotWidget, plot
import librosa as lr
from Task4 import Ui_MainWindow

class ApplicationWindow(QtWidgets.QMainWindow):

    music2: object

    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.pen=(145,0,145)
        #upload
        self.flag1=0
        self.ui.actionLoad.triggered.connect(self.upload)
        #play
        # self.ui.play1.clicked.connect(lambda: self.playAudio(self.music1))
        # self.ui.play2.clicked.connect(lambda: self.playAudio(self.music2))
        self.ui.play3.clicked.connect(lambda: self.playAudio(self.result))
        #slider ratio
        self.ui.slider1.setMaximum(100)
        self.ui.slider1.setMinimum(0)
        self.ui.slider1.setValue(100)
        self.ui.slider1.setSingleStep(1)
        self.ui.slider1.valueChanged.connect(self.ratio)
        #mix
        self.ui.mix.clicked.connect(self.mix)
        #comparison
        self.ui.comparisontable.setColumnCount(2)
        self.ui.comparisontable.setRowCount(10)
        self.ui.comparisontable.setItem(0,0,QTableWidgetItem("Song 1"))
        self.ui.comparisontable.setItem(0,1, QTableWidgetItem("Similarity Check"))

    def playAudio(self, song):
        sd.play(song, self.freq)


    def upload(self):
        self.fileName = QFileDialog.getOpenFileName(None, "Load", "D:/BIOMEDICAL ENGINEERING/3rd/2nd semester/dsp/tasks/sbe309-2020-task2-team__12","Track(*.wav)")
        self.t1 = 20 * 1000  # Works in milliseconds
        self.t2 = 60 * 1000
        self.newAudio = AudioSegment.from_wav(self.fileName[0])
        self.newAudio = self.newAudio[self.t1: self.t2]
        self.newAudio.export('out.wav', format="wav")
        self.wavefile2, self.freq = lr.load('out.wav')
        self.time = np.arange(0, len(self.wavefile2)) / self.freq
        # print(time)
        if self.flag1 == 0:
            self.music1=self.wavefile2
            # self.ui.music1.plot(self.time, self.wavefile2,pen=self.pen)
            self.flag1 =1
        else:
            self.music2=self.wavefile2
            # self.ui.music2.plot(self.time, self.wavefile2,pen=self.pen)
            self.flag1 = 0

    def ratio(self):
        self.ratio1 = float(float(self.ui.slider1.value()) / 100.0)
        print("Music1ratio=",self.ratio1)
        self.ratio2 = float(1-self.ratio1)
        print("Music2ratio=", self.ratio2)

    def mix(self):
        self.result = self.ratio1 * self.music1 + self.ratio2 * self.music2
        print(self.result)
        self.spectrogram(self.result)
        # self.ui.music2.clear()
        # self.ui.music2.plot(self.time, self.result)

    def spectrogram(self,input):
        fig = plt.gcf()
        frequencies,times, spectrogram = signal.spectrogram(input, self.freq/2)
        plt.pcolormesh(times, frequencies, np.log(spectrogram))
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.savefig('spectrogram.png')
        plt.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()
