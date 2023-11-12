from PyQt5 import QtCore, QtGui
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QFileDialog
import pyqtgraph as pg
import wfdb, numpy as np
from scipy.io import wavfile
import bisect


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
        self.graph_widget.clear()
        File_Path, _ = QFileDialog.getOpenFileName(None, "Browse Signal", "", "All Files (*)")
        
        self.sample_rate, self.audio_data = wavfile.read(File_Path)

        self.X_Coordinates = np.arange(len(self.audio_data)) / self.sample_rate
        self.Y_Coordinates = self.audio_data
        
        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(File_Path)))

        self.plot_signal()

    def load_ecg(self):
        self.graph_widget.clear()
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
            if self.graph_widget == self.UI.ECG_Abnormalities_Original_Signal_PlotWidget:
                self.graph_widget.getViewBox().setXRange(max(self.X_Coordinates[0: self.X_Points_Plotted + 1]) - 200, max(self.X_Coordinates[0: self.X_Points_Plotted + 1]))
                self.X_Points_Plotted += self.speed
                self.data_line.setData(self.X_Coordinates[0 : self.X_Points_Plotted + 1], self.Y_Coordinates[0 : self.X_Points_Plotted + 1])

            else:
                sound_position = self.player.position()
                sound_duration = self.player.duration()
                progress = sound_position / sound_duration

                target_x = int(progress * max(self.X_Coordinates))
                target_index = bisect.bisect_left(self.X_Coordinates, target_x)

                self.graph_widget.getViewBox().setXRange(target_x - 4, target_x)
                self.data_line.setData(self.X_Coordinates[:target_index], self.Y_Coordinates[:target_index])

    def toggle_pause(self):
        self.paused = not self.paused
        icon = QtGui.QIcon()
        if not self.paused:
            self.player.play()
            icon.addPixmap(QtGui.QPixmap("Assets/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.UI.Musical_Instruments_Play_Pause_Button.setIcon(icon)
        else:
            self.player.pause()
            icon.addPixmap(QtGui.QPixmap("Assets/play (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.UI.Musical_Instruments_Play_Pause_Button.setIcon(icon)

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
    
    def __init__(self, graph_widget, timegraph):
        self.spectrogram_widget = graph_widget
        self.timegraph = timegraph
        self.image_item = pg.ImageItem()
        self.spectrogram_widget.addItem(self.image_item)


    def plot_spectrogram(self):
        pass
        # sample_rate = 44100  # Sample rate in Hz
        # duration = 100  # Duration in seconds
        # freq = 44000  # Frequency in Hz
        # t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        # audio_data = np.sin(2 * np.pi * freq * t)

        # f, t, Sxx = signal.spectrogram(audio_data, fs=sample_rate)
        # self.image_item.setImage(Sxx)


