from PyQt5 import QtCore, QtGui
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QFileDialog
import pandas as pd
import wfdb, numpy as np
from scipy.io import wavfile
import pyaudio

class TimeGraph:
    
    def __init__(self, ui ,graph_widget):
        self.UI = ui
        self.graph_widget = graph_widget
        self.X_Points_Plotted = 0
        self.paused = False
        self.speed = 10
        self.X_Coordinates = []
        self.Y_Coordinates = []
        self.stopped = False

    def load_wav(self):
        File_Path, _ = QFileDialog.getOpenFileName(None, "Browse Signal", "", "All Files (*)")
        self.sample_rate, self.audio_data = wavfile.read(File_Path)

        self.X_Coordinates = np.arange(len(self.audio_data)) / self.sample_rate
        self.Y_Coordinates = self.audio_data
        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(File_Path)))
        self.plot_signal()

        # Set up the audio player with pyaudio
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,  # or paFloat32 depending on your data
                                  channels=1,
                                  rate=self.sample_rate,
                                  output=True)

    def load_ecg(self):
        File_Path, _ = QFileDialog.getOpenFileName(None, "Browse Signal", "", "All Files (*)")
        if File_Path:
            Record = wfdb.rdrecord(File_Path[:-4])
            self.Y_Coordinates = list(Record.p_signal[:, 0])
            self.X_Coordinates = list(np.arange(len(self.Y_Coordinates)))
            self.stopped = False
            self.plot_signal()
            
    def plot_signal(self):
        self.graph_widget.setLimits(xMin=0, xMax=float('inf'))
        self.data_line = self.graph_widget.plot(self.X_Coordinates[:1], self.Y_Coordinates[:1],pen="g")
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        self.player.play()

    def update_plot_data(self):
        if not self.paused and not self.stopped:    
            self.X_Points_Plotted += self.speed
            end_index = min(self.X_Points_Plotted, len(self.Y_Coordinates))

            self.data_line.setData(self.X_Coordinates[0 : self.X_Points_Plotted + 1], self.Y_Coordinates[0 : self.X_Points_Plotted + 1])
            if self.graph_widget == self.UI.ECG_Abnormalities_Input_Signal_Graph:
                self.graph_widget.getViewBox().setXRange(max(self.X_Coordinates[0: self.X_Points_Plotted + 1]) - 200, max(self.X_Coordinates[0: self.X_Points_Plotted + 1]))
            else:
                self.graph_widget.getViewBox().setXRange(max(self.X_Coordinates[0: self.X_Points_Plotted + 1]) - 1, max(self.X_Coordinates[0: self.X_Points_Plotted + 1]))
        
                start_byte = self.X_Points_Plotted * 2
                end_byte = end_index * 2
                self.stream.write(self.audio_data[start_byte:end_byte])

    def toggle_pause(self):
        self.paused = not self.paused
        icon = QtGui.QIcon()
        if not self.paused:
            icon.addPixmap(QtGui.QPixmap("Assets/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.UI.ECG_Abnormalities_Play_Pause_Button.setIcon(icon)
        else:
            icon.addPixmap(QtGui.QPixmap("Assets/play (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.UI.ECG_Abnormalities_Play_Pause_Button.setIcon(icon)

    def reset(self):
        self.X_Points_Plotted = 0

    def update_speed(self,slider):
        self.speed = 10*slider.value()

    def stop(self):
        self.stopped = True
        self.graph_widget.clear()
        self.graph_widget.getViewBox().setXRange(0,100)
        self.X_Points_Plotted = 0

    def zoomin(self):
        self.graph_widget.getViewBox().scaleBy((0.9, 0.9))

    def zoomout(self):
        self.graph_widget.getViewBox().scaleBy((1.1,1.1))


class FrequencyGraph:

    def __init__(self):
        pass




class Spectrogram:
    
    def __init__(self):
        pass
