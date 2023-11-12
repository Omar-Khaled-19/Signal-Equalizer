from abc import ABC, abstractmethod # Used  to declare abstract class and pure virtual functions
from PyQt5 import QtCore, QtGui
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QFileDialog
import numpy as np
from scipy.io import wavfile
import bisect


class BaseMode(ABC):
    def __init__(self, ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4):
        self.ui = ui
        self.input_graph = input_time_graph
        self.output_graph = output_time_graph
        self.frequency_graph = frequency_graph
        self.input_spectrogram = input_spectro
        self.output_spectrogram = output_spectro
        self.time_domain_X_coordinates = []
        self.time_domain_Y_coordinates = []
        self.slider1 = slider1
        self.slider2 = slider2
        self.slider3 = slider3
        self.slider4 = slider4

        self.X_Points_Plotted = 0
        self.paused = False
        self.speed = 10
        self.stopped = False
        self.player = QMediaPlayer()

    @abstractmethod
    def modify_frequency(self, value: int):
        pass
    
    def load_signal(self):
        self.input_graph.clear()
        File_Path, _ = QFileDialog.getOpenFileName(None, "Browse Signal", "", "All Files (*)")
        
        self.sample_rate, self.audio_data = wavfile.read(File_Path)

        self.time_domain_X_coordinates = np.arange(len(self.audio_data)) / self.sample_rate
        self.time_domain_Y_coordinates = self.audio_data
        
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(File_Path)))
        self.stopped = False
        self.plot_signal()
           
    def plot_signal(self):
        self.input_graph.setLimits(xMin=0, xMax=float('inf'))
        self.data_line = self.input_graph.plot(self.time_domain_X_coordinates[:1], self.time_domain_Y_coordinates[:1],pen="g")
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        self.player.play()

    def update_plot_data(self):
        if not self.paused and not self.stopped:             
            sound_position = self.player.position()
            sound_duration = self.player.duration()
            progress = sound_position / sound_duration

            if progress == 1:
                self.stopped = True

            target_x = int(progress * max(self.time_domain_X_coordinates))
            target_index = bisect.bisect_left(self.time_domain_X_coordinates, target_x)

            self.input_graph.getViewBox().setXRange(target_x - 4, target_x)
            self.data_line.setData(self.time_domain_X_coordinates[:target_index], self.time_domain_Y_coordinates[:target_index])

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.player.pause()
        else:
            if not self.stopped:
                self.player.play()

    def reset(self):
        self.stopped = False
        self.player.stop()
        self.player.setPosition(0)
        self.player.play()

    def update_speed(self,slider):
        pass

    def stop(self):
        self.player.stop()
        self.stopped = True
        self.input_graph.clear()
        self.input_graph.getViewBox().setXRange(0,4)

    def zoomin(self):
        self.input_graph.getViewBox().scaleBy((0.9, 0.9))

    def zoomout(self):
        self.input_graph.getViewBox().scaleBy((1.1,1.1))
