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
from imagededup.methods import PHash,DHash,WHash,AHash
from imagededup.utils import plot_duplicates
from difflib import SequenceMatcher
import operator
class ApplicationWindow(QtWidgets.QMainWindow):

    music2: object

    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.pen=(145,0,145)

        #convert
        self.mp3towav()
        self.spectrogram_hashall()

        # upload
        self.flag1 = 0
        self.ui.actionLoad.triggered.connect(self.upload)
        #play
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
        self.ui.compare.clicked.connect(self.compare)
    def mp3towav(self):
        pass
        # # files
        # lst = glob.glob("/home/menna/Songs/*.mp3")
        # print(lst)
        # for file in lst:
        #     # convert wav to mp3
        #     os.system(f"""ffmpeg -i {file} -acodec pcm_u8 -ar 22050 {file[:-4]}.wav""")
    #we used this fn at first to generate spectrogram images
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
    #then we used this fn o generate sepectrogram as arrays ans phash them
    def spectrogram_hashall(self):
        pass
        # phasher = PHash()
        # path = Path('/home/menna/Songs').glob('**/*.wav')
        # data = dict()
        # wavs = [str(wavf) for wavf in path if wavf.is_file()]
        # wavs.sort()
        # number_of_files = len(wavs)
        # spk_ID = [wavs[i].split('/')[-1].lower() for i in range(number_of_files)]
        # for i in range(number_of_files):
        #     wavfile, freq = lr.load(wavs[i],duration=60.0)
        #     spectrogram=lr.amplitude_to_db(np.abs(lr.stft(wavfile)), ref=np.max)
        #     encoding = phasher.encode_image(image_array=spectrogram)
        #     data[spk_ID[i][:-4]] = encoding
        # with open('arrayhash.txt', 'w') as f:
        #     for key, value in data.items():
        #         f.write('%s:%s\n' % (key, value))



    def playAudio(self, song):
        sd.play(song, self.freq)


    def upload(self):
        self.fileName = QFileDialog.getOpenFileName(None, "Load", "/home/menna/Songs","Track(*.wav)")
        print(self.fileName)
        self.wavefile2, self.freq = lr.load(self.fileName[0],duration=60.0)
        self.time = np.arange(0, len(self.wavefile2)) / self.freq
        if self.flag1 == 0:
            self.music1=self.wavefile2
            self.flag1 =1
        else:
            self.music2=self.wavefile2
            self.flag1 = 0

    def ratio(self):
        self.ratio1 = float(float(self.ui.slider1.value()) / 100.0)
        print("Music1ratio=",self.ratio1)
        self.ratio2 = float(1-self.ratio1)
        print("Music2ratio=", self.ratio2)

    def mix(self):
        self.result = self.ratio1 * self.music1 + self.ratio2 * self.music2
        self.Spectrogram(self.result)


    def Spectrogram(self,input):
        self.spectrogram=lr.amplitude_to_db(np.abs(lr.stft(input)), ref=np.max)
        ###used this code to generate spec image to make sure that its the same as the original ones
        # frequencies,times, self.spectrogram = signal.spectrogram(input, self.freq)
        # plt.pcolormesh(times, frequencies, np.log(self.spectrogram))
        # plt.ylabel('freq')
        # plt.xlabel('time')
        # plt.savefig('spectrogram.png', bbox_inches='tight', dpi=300, frameon='false')
        #plt.show()

    def compare(self):
        if self.ui.Hash.isChecked():
            self.hash()
        elif self.ui.MainFeatures.isChecked():
            self.mainfeatureSelect(self.spectrogram, self.freq, mode="spectralCentroid")
        elif self.ui.Both.isChecked():
            pass
    def hash(self):
    #to read the hash file
        data = dict()
        with open('arrayhash.txt') as raw_data:
            for item in raw_data:
                if ':' in item:
                    key, value = item.split(':', 1)
                    data[key] = value
                else:
                    pass  # deal with bad lines of text here

        #hash the spec of the new song
        phasher = PHash()
        encoding1 = phasher.encode_image(image_array=self.spectrogram)
        #compare btw the hashes
        for i,j in data.items():
            data[i] = str(self.similar(encoding1,j))
        #ordering the results
        sorted_d = dict(sorted(data.items(), key=operator.itemgetter(1), reverse=True))
        y=1
        #showing the results
        for i,j in sorted_d.items():
            if y==11:
                break
            else:
                self.ui.comparisontable.setItem(y, 0, QTableWidgetItem(i))
                self.ui.comparisontable.setItem(y, 1, QTableWidgetItem(j))
            y=y+1

    def similar(self,a, b):
        return SequenceMatcher(None, a, b).ratio()

    def mainfeatureSelect(self,spectogram, freq, mode):
        if mode == "spectralCentroid":
            # spectral_cenroids
            featureExtraction = lr.feature.spectral_centroid(S=spectogram, sr=freq)
        elif mode == "spectralRolloff":
            # spectral_rolloff
            featureExtraction = lr.feature.spectral_rolloff(S=S, sr=freq)
            # print(np.mean(featureExtraction))
        elif mode == "mfccs":
            # mfccs
            featureExtraction = lr.feature.mfcc(S=spectrogram, sr=freq)
            # print(np.mean(featureExtraction.shape))
        featureExtraction.tostring()
        # Pitch Tracing
        # pitches, magnitudes = lr.piptrack(y=wavefile, sr=freq, fmin=150, fmax=800)
        # print(pitches)


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
