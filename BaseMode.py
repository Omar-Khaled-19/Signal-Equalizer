from abc import ABC, abstractmethod # Used  to declare abstract class and pure virtual functions
from PyQt5 import QtCore, QtGui
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QFileDialog
import numpy as np, bisect, librosa, soundfile as sf
from scipy.signal.windows import get_window
from scipy.signal.windows import boxcar
import pyqtgraph as pg
import os

class BaseMode(ABC):
    def __init__(self, ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4, ui_smoothing, Original_Spectrogram_Label, Modified_Spectrogram_Label):
        self.ui = ui
        self.input_graph = input_time_graph
        self.output_graph = output_time_graph
        self.frequency_graph = frequency_graph
        self.input_spectrogram = input_spectro
        self.output_spectrogram = output_spectro
        self.time_domain_X_coordinates = []
        self.time_domain_Y_coordinates = []
        self.freq_domain_X_coordinates = []
        self.freq_domain_Y_coordinates = []
        self.modified_freq_domain_Y_coordinates = []
        self.time_domain_signal_modified = []
        self.slider1 = slider1
        self.slider2 = slider2
        self.slider3 = slider3
        self.slider4 = slider4
        self.phases = []
        self.current_smoothing = 0
        self.uiSmoothing = ui_smoothing
        self.X_Points_Plotted = 0
        self.paused = False
        self.stopped = False
        self.hidden = False
        self.player = QMediaPlayer()
        self.sample_rate = 44100
        self.min_range = 0
        self.max_range = 0
        self.c = 0
        self.output_sound = False
        self.input_graph.setXLink(self.output_graph)
        self.input_graph.setYLink(self.output_graph)
        self.File_Path = None
        self.Original_Spectrogram_Label = Original_Spectrogram_Label
        self.Modified_Spectrogram_Label = Modified_Spectrogram_Label
       
    @abstractmethod
    def modify_frequency(self, min_freq: int, max_freq: int, factor: int):
        self.min_range = min_freq
        self.max_range = max_freq
        smoothing_factor = factor / 5.0
        self.current_smoothing = self.smoothing_window(len(self.modified_freq_domain_Y_coordinates[(self.freq_domain_X_coordinates >= min_freq) & (self.freq_domain_X_coordinates <= max_freq)]), smoothing_factor)
        self.modified_freq_domain_Y_coordinates[(self.freq_domain_X_coordinates >= min_freq) & (self.freq_domain_X_coordinates <= max_freq)] = self.freq_domain_Y_coordinates.copy()[(self.freq_domain_X_coordinates >= min_freq) & (self.freq_domain_X_coordinates <= max_freq)]

        self.modified_freq_domain_Y_coordinates[(self.freq_domain_X_coordinates >= min_freq) & (self.freq_domain_X_coordinates <= max_freq)] *= self.current_smoothing
        self.modified_freq_domain_Y_coordinates[(self.freq_domain_X_coordinates <= -min_freq) & (self.freq_domain_X_coordinates >= -max_freq)] *= self.current_smoothing
        self.plot_frequency_domain(smoothing_flag=1)

    def load_signal(self):
        self.clear_graphs()
        self.File_Path, _ = QFileDialog.getOpenFileName(None, "Browse Signal", "", "All Files (*)")
        self.time_domain_Y_coordinates, self.sample_rate = librosa.load(self.File_Path)
        self.time_domain_X_coordinates = np.arange(len(self.time_domain_Y_coordinates)) / self.sample_rate
        self.time_domain_signal_modified = self.time_domain_Y_coordinates.copy()

        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.File_Path)))
        self.player.play()

        self.stopped = False
        self.plot_signals()
           
    def plot_signals(self):
        self.input_graph.setLimits(xMin=0, xMax=float('inf'))
        self.output_graph.setLimits(xMin = 0 ,xMax = float('inf') )
        self.data_line_in = self.input_graph.plot(self.time_domain_X_coordinates[:1], self.time_domain_Y_coordinates[:1],pen="g")
        self.data_line_out = self.output_graph.plot(self.time_domain_X_coordinates[:1], self.time_domain_signal_modified[:1],pen="b")

        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        self.calculate_frequency_domain()

    def update_plot_data(self):
        if not self.paused and not self.stopped:             
            sound_position = self.player.position()
            sound_duration = self.player.duration()
            try:
                progress = sound_position / sound_duration
            except ZeroDivisionError:
                progress = 0

            if progress == 1:
                self.stopped = True

            target_x = int(progress * max(self.time_domain_X_coordinates))
            target_index = bisect.bisect_left(self.time_domain_X_coordinates, target_x)

            self.input_graph.getViewBox().setXRange(target_x - 4, target_x)
            self.output_graph.getViewBox().setXRange(target_x - 4, target_x)
            self.data_line_in.setData(self.time_domain_X_coordinates[:target_index], self.time_domain_Y_coordinates[:target_index])
            self.data_line_out.setData(self.time_domain_X_coordinates[:target_index], self.time_domain_signal_modified[:target_index].real)

            if not self.hidden:
                self.input_spectrogram.canvas.plot_spectrogram(self.time_domain_Y_coordinates[:target_index],self.sample_rate)
                self.output_spectrogram.canvas.plot_spectrogram(self.time_domain_signal_modified[:target_index],self.sample_rate)

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

    def update_speed(self, slider):
        self.player.setPlaybackRate(slider.value())

    def stop(self):
        self.player.stop()
        self.stopped = True
        self.clear_graphs()

    def zoomin(self):
        self.input_graph.getViewBox().scaleBy((0.9, 0.9))

    def zoomout(self):
        self.input_graph.getViewBox().scaleBy((1.1,1.1))

    def smoothing_window(self, width= 100 , height = 10):
        self.uiSmoothing.Std_Dev_slider.setEnabled(False)
        # Check which radio button is selected and choose the proper window
        if self.uiSmoothing.Smoothing_Window_Hamming_Radio_Button.isChecked():
            window = get_window('hamming', width)
        elif self.uiSmoothing.Smoothing_Window_Hanning_Radio_Button.isChecked():
            window = get_window('hann', width)
        elif self.uiSmoothing.Smoothing_Window_Rectangle_Radio_Button.isChecked():
            window = boxcar(width) * height
            return window
        elif self.uiSmoothing.Smoothing_Window_Gaussian_Radio_Button.isChecked():
            self.uiSmoothing.Std_Dev_slider.setEnabled(True)
            window = get_window(('gaussian', 6), 100) * 10
            return window
        else:
            return None
        scaled_window = height * window / np.max(window)
        return scaled_window
 
    def plot_smoothing(self, slider_value = None):
        if slider_value is not None and self.uiSmoothing.Smoothing_Window_Gaussian_Radio_Button.isChecked():
            self.current_smoothing = get_window(('gaussian', slider_value), 100) * 10
        else:
            self.current_smoothing = self.smoothing_window(100, 10)
        self.uiSmoothing.Smoothing_Window_PlotWidget_2.clear()
        self.uiSmoothing.Smoothing_Window_PlotWidget_2.plot(self.current_smoothing)

    def apply_selector(self):
        # Create a smoothing window box
        selector = pg.LinearRegionItem()
        selector.setRegion([self.min_range, self.max_range])
        selector.setMovable(False)
        self.frequency_graph.addItem(selector)

    def plot_frequency_domain(self, smoothing_flag=1, minX = 0, maxX = 1000):
        self.frequency_graph.clear()
        if smoothing_flag == 1:
            self.apply_selector()
        self.frequency_graph.setLimits(xMin = minX, xMax = maxX)
        self.frequency_graph.setLimits(yMin = min(self.modified_freq_domain_Y_coordinates), yMax = max(self.modified_freq_domain_Y_coordinates))
        self.frequency_graph.setYRange(min(self.modified_freq_domain_Y_coordinates), max(self.modified_freq_domain_Y_coordinates))
        self.frequency_graph.plot(self.freq_domain_X_coordinates, self.modified_freq_domain_Y_coordinates)

        # Inverse Fourier transform to go back to the time domain
        self.time_domain_signal_modified = np.fft.ifft(self.modified_freq_domain_Y_coordinates * np.exp(1j * self.phases))
        self.output_graph.setLimits(xMin = 0, xMax = max(self.freq_domain_X_coordinates))

        self.output_graph.getViewBox().setYRange(-0.4, 0.4)

        self.c += 1
        self.audio_file = f"temp_audio{self.c}.wav"
        if self.c != 1:
            os.remove(f"temp_audio{self.c-1}.wav")

        real_signal = np.real(self.time_domain_signal_modified)
        sf.write(self.audio_file, real_signal.astype(np.float32), self.sample_rate)

        if self.output_sound:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.audio_file)))
            self.player.play()

    def calculate_frequency_domain(self):
        dt = self.time_domain_X_coordinates[1] - self.time_domain_X_coordinates[0]
        fft_result = np.fft.fft(self.time_domain_Y_coordinates)
        frequencies = np.fft.fftfreq(len(fft_result), dt)
        self.freq_domain_X_coordinates = frequencies
        self.freq_domain_Y_coordinates = np.abs(fft_result)
        self.phases = np.angle(fft_result)
        self.modified_freq_domain_Y_coordinates = self.freq_domain_Y_coordinates.copy()
        self.plot_frequency_domain()

    def toggle_hide(self):
        self.input_spectrogram.setVisible(self.hidden)
        self.Original_Spectrogram_Label.setVisible(self.hidden)
        self.output_spectrogram.setVisible(self.hidden)
        self.Modified_Spectrogram_Label.setVisible(self.hidden)
        self.hidden = not self.hidden

    def toggle_sound(self,radio):
        Original = {self.ui.Uniform_Range_Original_Signal_Sound_Radio_Button, self.ui.Musical_Instruments_Original_Signal_Sound_Radio_Button,
                    self.ui.Animals_Sounds_Original_Signal_Sound_Radio_Button}

        if radio in Original:
            self.output_sound = False
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.File_Path)))
            self.player.play()
        else:
            self.output_sound = True
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.audio_file)))
            self.player.play()

        if self.stopped:
            self.reset()

    def change_pause_icon(self,button):
        icon = QtGui.QIcon()
        if not self.paused:
            icon.addPixmap(QtGui.QPixmap("Assets/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            button.setIcon(icon)
        else:
            icon.addPixmap(QtGui.QPixmap("Assets/play (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            button.setIcon(icon)

    def change_hide_icon(self,button):
        _translate = QtCore.QCoreApplication.translate
        icon = QtGui.QIcon()
        if not self.hidden:
            icon.addPixmap(QtGui.QPixmap("Assets/invisible.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            button.setIcon(icon)
            button.setText(_translate("Form", "   Hide Spectrogram"))
        else:
            icon.addPixmap(QtGui.QPixmap("Assets/eye.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            button.setIcon(icon)  
            button.setText(_translate("Form", "   Show Spectrogram"))  

    def clear_graphs(self):
        self.input_graph.clear()
        self.frequency_graph.clear()
        self.output_graph.clear()
        self.input_graph.getViewBox().setXRange(0, 4)
        self.output_graph.getViewBox().setXRange(0, 4)
        self.frequency_graph.getViewBox().setXRange(0, 4)