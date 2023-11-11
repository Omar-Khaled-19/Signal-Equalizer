from PyQt5 import QtCore, QtGui
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QFileDialog
import pandas as pd
import pyqtgraph as pg
import wfdb, numpy as np
from scipy.io import wavfile
import pyaudio
from scipy import signal
from scipy.signal.windows import get_window
from scipy.signal.windows import boxcar
import math

class TimeGraph:

    def __init__(self,graph_widget):
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
                                  channels=1, rate=self.sample_rate, output=True)

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
            if self.graph_widget == self.UI.ECG_Abnormalities_Original_Signal_PlotWidget:
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

    def __init__(self, ui, freq_widget, input_widget, smoothing_widget):
        self.input_graph = input_widget
        self.ui_window = ui
        self.freq_graph = freq_widget
        self.smoothing_graph = smoothing_widget
        self.current_smoothing = None
        #self.sampling_rate = input_widget.sample_rate
        self.x_coordinates = 0


    def smoothing_window(self):
        # Check which radio button is selected
        if self.ui_window.Smoothing_Window_Hamming_Radio_Button.isChecked():
            # Generate Hamming window
            hamming_window = get_window('hamming', self.ui_window.Smoothing_Window_Frequency_Slider.value())
            # Scale the Hamming window to the desired amplitude
            scaled_hamming_window = self.ui_window.Smoothing_Window_Amplitude_Slider.value() * hamming_window / np.max(hamming_window)
            return (scaled_hamming_window)

        elif self.ui_window.Smoothing_Window_Hanning_Radio_Button.isChecked():
            # Generate Hanning window
            hanning_window = get_window('hann', self.ui_window.Smoothing_Window_Frequency_Slider.value())
            # Scale the Hanning window to the desired amplitude
            scaled_hanning_window = self.ui_window.Smoothing_Window_Amplitude_Slider.value() * hanning_window / np.max(hanning_window)
            return (scaled_hanning_window)

        elif self.ui_window.Smoothing_Window_Rectangle_Radio_Button.isChecked():
            # generate and adjust the height as desired
            rectangle_window = boxcar(self.ui_window.Smoothing_Window_Frequency_Slider.value()) * self.ui_window.Smoothing_Window_Amplitude_Slider.value()
            return (rectangle_window)

        elif self.ui_window.Smoothing_Window_Gaussian_Radio_Button.isChecked():
            std_dev = self.ui_window.Smoothing_Window_Frequency_Slider.value() / (2 * math.sqrt(2 * math.log(2)))
            gaussian_window = get_window(('gaussian', std_dev), self.ui_window.Smoothing_Window_Frequency_Slider.value()) * self.ui_window.Smoothing_Window_Amplitude_Slider.value()
            return (gaussian_window)

    def plot_smoothing(self):
        self.current_smoothing = self.smoothing_window()
        self.smoothing_graph.clear()
        self.smoothing_graph.plot(self.current_smoothing)

    def plot_frequency_domain(self):
        # fft_result = np.fft.fft(signal)
        # frequencies = np.fft.fftfreq(len(fft_result), 1/sampling_rate)
        # self.freq_graph.plot.plot(frequencies, np.abs(fft_result))
        self.x_coordinates = self.input_graph.X_Coordinates
        signal = self.input_graph.Y_Coordinates
        signal = np.array(signal)
        dt = self.x_coordinates[1] - self.x_coordinates[0]
        # if dt is None:
        #     dt = 1
        #     t = np.arange(0, signal.shape[-1])
        # else: #mosta7el teb2a b none f m4 needed awy, arga3laha ba3den
        t = np.arange(0, signal.shape[-1]) * dt

        if signal.shape[0] % 2 != 0:
            t = t[0:-1]
            signal = signal[0:-1]

        fft_result = np.fft.fft(signal) / t.shape[0]  # Divided by size t for coherent magnitude
        freq = np.fft.fftfreq(t.shape[0], d=dt)

        # Plot analytic signal - right half of the frequency axis is needed only...
        first_neg_index = np.argmax(freq < 0)
        freq_axis_pos = freq[0:first_neg_index]
        sig_fft_pos = 2 * fft_result[0:first_neg_index]  # *2 because of the magnitude of the analytic signal
        self.freq_graph.plot(freq_axis_pos, np.abs(sig_fft_pos))

class Spectrogram:
    
    def __init__(self, graph_widget, timegraph):
        # Instead of passing common elements more than one, how about all graphs in the same tab inherit from the tab the basic attributes??
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


