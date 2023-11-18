from abc import ABC, abstractmethod # Used  to declare abstract class and pure virtual functions
from PyQt5 import QtCore, QtGui
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QFileDialog
import numpy as np, bisect, math, librosa
from scipy.signal.windows import get_window
from scipy.signal.windows import boxcar
from mplwidget import MplCanvas,MplWidget

# Proposed Modifications = 4
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
        self.freq_domain_X_coordinates = []
        self.freq_domain_Y_coordinates = []
        self.modified_freq_domain_Y_coordinates = []
        self.time_domain_signal_modified = []
        self.slider1 = slider1
        self.slider2 = slider2
        self.slider3 = slider3
        self.slider4 = slider4

        self.X_Points_Plotted = 0
        self.paused = False
        self.stopped = False
        self.hidden = False
        self.speed = 10
        self.player = QMediaPlayer()

    @abstractmethod
    def modify_frequency(self, min_freq: int, max_freq: int, factor: int):
        smoothing_factor = factor / 5.0
        self.modified_freq_domain_Y_coordinates = self.freq_domain_Y_coordinates.copy()
        self.modified_freq_domain_Y_coordinates[(self.freq_domain_X_coordinates >= min_freq) & (self.freq_domain_X_coordinates <= max_freq)] *= smoothing_factor
        self.plot_frequency_domain()
    
    def load_signal(self):
        self.input_graph.clear()
        File_Path, _ = QFileDialog.getOpenFileName(None, "Browse Signal", "", "All Files (*)")
        # Can it be audio_data, sample_rate = librosa.load(File_Path)
        self.audio_data, self.sample_rate = librosa.load(File_Path)

        self.time_domain_X_coordinates = np.arange(len(self.audio_data)) / self.sample_rate
        self.time_domain_Y_coordinates = self.audio_data
        
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(File_Path)))
        self.stopped = False
        # Change play button to pause
        self.plot_signal()
           
    def plot_signal(self):
        self.input_graph.setLimits(xMin=0, xMax=float('inf'))
        self.data_line = self.input_graph.plot(self.time_domain_X_coordinates[:1], self.time_domain_Y_coordinates[:1],pen="g")
        self.time_domain_signal_modified = self.time_domain_Y_coordinates.copy()
        self.data_line_out = self.output_graph.plot(self.time_domain_X_coordinates[:1], self.time_domain_signal_modified[:1],pen="g")
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        self.player.play()
        self.calculate_frequency_domain()
        
    def plot_output(self, Xcoordinates, Ycoordinates):
        self.reset()
        self.output_graph.setYRange(min(self.modified_freq_domain_Y_coordinates), max(self.modified_freq_domain_Y_coordinates))
        self.output_graph.clear()
        self.output_graph.plot(Xcoordinates, Ycoordinates)


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
            self.data_line.setData(self.time_domain_X_coordinates[:target_index], self.time_domain_Y_coordinates[:target_index])
            self.data_line_out.setData(self.time_domain_X_coordinates[:target_index], self.time_domain_signal_modified[:target_index])

            if not self.hidden:
                self.input_spectrogram.canvas.plot_spectrogram(self.time_domain_Y_coordinates[:target_index],self.sample_rate)


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
        self.input_graph.clear()
        self.input_graph.getViewBox().setXRange(0,4)

    def zoomin(self):
        self.input_graph.getViewBox().scaleBy((0.9, 0.9))

    def zoomout(self):
        self.input_graph.getViewBox().scaleBy((1.1,1.1))

    def smoothing_window(self):
        # Check which radio button is selected
        if self.ui.Smoothing_Window_Hamming_Radio_Button.isChecked():
            # Generate Hamming window
            hamming_window = get_window('hamming', self.ui.Smoothing_Window_Frequency_Slider.value())
            # Scale the Hamming window to the desired amplitude
            scaled_hamming_window = self.ui.Smoothing_Window_Amplitude_Slider.value() * hamming_window / np.max(hamming_window)
            return scaled_hamming_window

        elif self.ui.Smoothing_Window_Hanning_Radio_Button.isChecked():
            # Generate Hanning window
            hanning_window = get_window('hann', self.ui.Smoothing_Window_Frequency_Slider.value())
            # Scale the Hanning window to the desired amplitude
            scaled_hanning_window = self.ui.Smoothing_Window_Amplitude_Slider.value() * hanning_window / np.max(hanning_window)
            return scaled_hanning_window

        elif self.ui.Smoothing_Window_Rectangle_Radio_Button.isChecked():
            # generate and adjust the height as desired
            rectangle_window = boxcar(self.ui.Smoothing_Window_Frequency_Slider.value()) * self.ui.Smoothing_Window_Amplitude_Slider.value()
            return rectangle_window

        elif self.ui.Smoothing_Window_Gaussian_Radio_Button.isChecked():
            std_dev = self.ui.Smoothing_Window_Frequency_Slider.value() / (2 * math.sqrt(2 * math.log(2)))
            gaussian_window = get_window(('gaussian', std_dev), self.ui.Smoothing_Window_Frequency_Slider.value()) * self.ui.Smoothing_Window_Amplitude_Slider.value()
            return gaussian_window

    def plot_smoothing(self):
        # Can it be current_smoothing = self.smoothing_window()
        self.current_smoothing = self.smoothing_window()
        self.ui.Smoothing_Window_PlotWidget.clear()
        self.ui.Smoothing_Window_PlotWidget.plot(self.current_smoothing)

    def plot_frequency_domain(self):
        self.frequency_graph.clear()
        self.frequency_graph.setLimits(xMin = 0, xMax = max(self.freq_domain_X_coordinates))
        self.frequency_graph.setLimits(yMin = min(self.modified_freq_domain_Y_coordinates), yMax = max(self.modified_freq_domain_Y_coordinates))
        self.frequency_graph.setYRange(min(self.modified_freq_domain_Y_coordinates), max(self.modified_freq_domain_Y_coordinates))
        self.frequency_graph.plot(self.freq_domain_X_coordinates, self.modified_freq_domain_Y_coordinates)
        # Inverse Fourier transform to go back to the time domain
        self.time_domain_signal_modified = np.fft.ifft(self.modified_freq_domain_Y_coordinates)
        self.time_domain_signal_modified = np.real(self.time_domain_signal_modified)
        self.output_graph.setLimits(xMin = 0, xMax = max(self.freq_domain_X_coordinates))
        self.output_graph.setLimits(yMin = min(self.time_domain_signal_modified), yMax = max(self.time_domain_signal_modified))
        self.plot_output(self.time_domain_X_coordinates[:1], self.time_domain_signal_modified[:1])
        


    def calculate_frequency_domain(self):
        dt = self.time_domain_X_coordinates[1] - self.time_domain_X_coordinates[0]
        fft_result = np.fft.fft(self.time_domain_Y_coordinates)
        frequencies = np.fft.fftfreq(len(fft_result), dt)
        self.freq_domain_X_coordinates = frequencies
        self.freq_domain_Y_coordinates = np.abs(fft_result)
        self.modified_freq_domain_Y_coordinates = self.freq_domain_Y_coordinates.copy()
        self.plot_frequency_domain()


    def toggle_hide(self):
        self.hidden = not self.hidden
        self.input_spectrogram.canvas.clear_spectrogram()

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
