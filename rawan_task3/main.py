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
import os
import glob
from pathlib import Path
from scipy.io import wavfile
from imagededup.methods import PHash
from imagededup.utils import plot_duplicates
from difflib import SequenceMatcher
class ApplicationWindow(QtWidgets.QMainWindow):

    music2: object

    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.pen=(145,0,145)
        #upload
        self.flag1=0
        self.mp3towav()
        self.spectrogramall()
        self.ui.actionLoad.triggered.connect(self.upload)
        self.hashingall()

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

    def mp3towav(self):
        pass
        # # files
        # lst = glob.glob("/home/menna/Songs/*.mp3")
        # print(lst)
        # for file in lst:
        #     # convert wav to mp3
        #     os.system(f"""ffmpeg -i {file} -acodec pcm_u8 -ar 22050 {file[:-4]}.wav""")
    def spectrogramall(self):
        pass
        # path = Path('/home/menna/Songs').glob('**/*.wav')
        #
        # wavs = [str(wavf) for wavf in path if wavf.is_file()]
        # wavs.sort()
        # number_of_files = len(wavs)
        # spk_ID = [wavs[i].split('/')[-1].lower() for i in range(number_of_files)]
        # for i in range(number_of_files):
        #     wavfile, freq = lr.load(wavs[i],duration=60.0)
        #     frequencies, times, spectrogram = signal.spectrogram(wavfile,freq)
        #     plt.pcolormesh(times, frequencies, np.log(spectrogram))
        #     plt.xlabel('time')
        #     plt.ylabel('freq')
        #     plt.savefig("/home/menna/DSP_Task3/songsspec/{}.png".format(spk_ID[i][:-4]), bbox_inches='tight', dpi=300, frameon='false')
    def playAudio(self, song):
        sd.play(song, self.freq)


    def upload(self):
        self.fileName = QFileDialog.getOpenFileName(None, "Load", "/home/menna/Songs","Track(*.wav)")
        #self.t1 = 20 * 1000  # Works in milliseconds
        #self.t2 = 60 * 1000
        # self.newAudio = AudioSegment.from_mp3(self.fileName[0])
        # self.newAudio.export('out.wav', format="wav")
        #self.newAudio = self.newAudio[: self.t2]

        self.wavefile2, self.freq = lr.load(self.fileName[0],duration=60.0)
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
        frequencies,times, spectrogram = signal.spectrogram(input, self.freq)
        plt.pcolormesh(times, frequencies, np.log(spectrogram))
        plt.ylabel('freq')
        plt.xlabel('time')
        plt.savefig('spectrogram.png', bbox_inches='tight', dpi=300, frameon='false')
        #plt.show()
        self.printhash()
    def hashingall(self):
        pass
        # phasher = PHash()
        # encodings = phasher.encode_images(image_dir='/home/menna/DSP_Task3/songsspece')
        # print(encodings)
        # with open('hash.txt', 'w') as f:
        #     for key, value in encodings.items():
        #         f.write('%s:%s\n' % (key, value))
        # duplicates = phasher.find_duplicates(encoding_map=encodings, scores=True)
        #print(duplicates)
        # a_file=open('hash.txt','w')
        # for row in duplicates:
        #     np.savetxt(a_file,row)
        # a_file.close()
        # plot_duplicates(image_dir='/home/menna/DSP_Task3/songsspece',
        #                                    duplicate_map=duplicates,
        #                                     filename='adele_million_years_ago_10.png')
    def printhash(self):
        data = dict()
        with open('hash.txt') as raw_data:
            for item in raw_data:
                if ':' in item:
                    key, value = item.split(':', 1)
                    data[key] = value
                else:
                    pass  # deal with bad lines of text here
        #print(data)
        phasher = PHash()
        encoding = phasher.encode_image(image_file='spectrogram.png')
        print(encoding)
        # duplicates = phasher.find_duplicates(encoding_map=data,max_distance_threshold=12, scores=True)

        #print(duplicates)
        for i,j in data.items():

            print(i,self.similar(encoding,j))

    # string similraity check


    def similar(self,a, b):
        return SequenceMatcher(None, a, b).ratio()


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
