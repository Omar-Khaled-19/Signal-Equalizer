from abc import ABC, abstractmethod # Used  to declare abstract class and pure virtual functions
from PyQt5 import QtCore, QtGui
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QFileDialog
import numpy as np, bisect, math, librosa, sounddevice as sd, soundfile as sf
from scipy.signal.windows import get_window
from scipy.signal.windows import boxcar
from scipy.io import wavfile
import pyqtgraph as pg

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
        self.phases = []
        self.current_smoothing = 0

        self.X_Points_Plotted = 0
        self.paused = False
        self.stopped = False
        self.hidden = False
        self.speed = 10
        self.player = QMediaPlayer()
        self.sample_rate = 44100
        self.min_range = 0
        self.max_range = 0

        self.input_graph.setXLink(self.output_graph)
        self.input_graph.setYLink(self.output_graph)
        self.first_time_flag = True # This checks if the signal is loaded for the first time

    @abstractmethod
    def modify_frequency(self, min_freq: int, max_freq: int, factor: int):
        self.min_range = min_freq
        self.max_range = max_freq
        smoothing_factor = factor / 5.0
        self.modified_freq_domain_Y_coordinates[(self.freq_domain_X_coordinates >= min_freq) & (self.freq_domain_X_coordinates <= max_freq)] = self.freq_domain_Y_coordinates.copy()[(self.freq_domain_X_coordinates >= min_freq) & (self.freq_domain_X_coordinates <= max_freq)]
        
        # self.modified_freq_domain_Y_coordinates = list(np.array(self.modified_freq_domain_Y_coordinates[min_freq:max_freq + 1]) * self.smoothing_window() * smoothing_factor)
        self.modified_freq_domain_Y_coordinates[(self.freq_domain_X_coordinates >= min_freq) & (self.freq_domain_X_coordinates <= max_freq)] *= smoothing_factor
        self.plot_frequency_domain(1)
        self.plot_smoothing(max_freq - min_freq, factor)
    
    def load_signal(self):
        self.input_graph.clear()
        File_Path, _ = QFileDialog.getOpenFileName(None, "Browse Signal", "", "All Files (*)")
        # TODO for OMAR KHALED: Revise Plotting given we changed the library that reads the wav file,
        #   although both return the same thing
        """
        Both soundfile sf.read() and librosa.load() return the same 2 parameters when reading a .wav file.
        Below I will leave this part from the documentation of Both Libraries
        Returns 2 things:	
        ============= Soundfile Documentation for sf.read() ===================================
            1-) audiodata (numpy.ndarray or type(out)) – A two-dimensional (frames x channels) NumPy array is returned. 
            If the sound file has only one channel, a one-dimensional array is returned. 
            Use always_2d=True to return a two-dimensional array anyway.
            2-)  samplerate (int) – The sample rate of the audio file.
             ============= Librosa Documentation for librosa.load() ===================================
            Returns 2 things:
                1-) ynp.ndarray [shape=(n,) or (…, n)]
                audio time series. Multi-channel is supported.
                
                2-) srnumber > 0 [scalar]
                sampling rate of y
            =====================================================================================
        """
        # audio_data, self.sample_rate = librosa.load(File_Path)
        self.time_domain_Y_coordinates, self.sample_rate = sf.read(File_Path)
        self.time_domain_X_coordinates = np.arange(len(self.time_domain_Y_coordinates)) / self.sample_rate
        sd.play(self.time_domain_Y_coordinates, self.sample_rate) # Here shines the power of sounddevice, it plays the sound given numpy array
        # self.player.setMedia(QMediaContent(QUrl.fromLocalFile(File_Path)))
        # self.player.setMedia(QMediaContent(QUrl.fromLocalFile('modified_signal.wav')))
        self.stopped = False
        self.plot_signals()
           
    def plot_signals(self):
        self.input_graph.setLimits(xMin=0, xMax=float('inf'))
        self.output_graph.setLimits(xMin = 0 ,xMax = float('inf') )
        
        self.data_line_in = self.input_graph.plot(self.time_domain_X_coordinates[:1], self.time_domain_Y_coordinates[:1],pen="g")
        self.data_line_out = self.output_graph.plot(self.time_domain_X_coordinates[:1], self.time_domain_signal_modified[:1],pen="b")
        #TODO: change this setting, after calculating the actual time domain from the fourier inverse not taking a copy from origin
        self.time_domain_signal_modified = self.time_domain_Y_coordinates.copy()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        # self.player.play()
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
        self.input_graph.clear()
        self.input_graph.getViewBox().setXRange(0,4)
        self.output_graph.clear()
        self.output_graph.getViewBox().setXRange(0,4)
        self.first_time_flag = True

    def zoomin(self):
        self.input_graph.getViewBox().scaleBy((0.9, 0.9))

    def zoomout(self):
        self.input_graph.getViewBox().scaleBy((1.1,1.1))

    def smoothing_window(self, width, height):
        # Check which radio button is selected
        if self.ui.Smoothing_Window_Hamming_Radio_Button.isChecked():
            # Generate Hamming window
            hamming_window = get_window('hamming', width)
            # Scale the Hamming window to the desired amplitude
            scaled_hamming_window = height * hamming_window / np.max(hamming_window)
            return scaled_hamming_window

        elif self.ui.Smoothing_Window_Hanning_Radio_Button.isChecked():
            # Generate Hanning window
            hanning_window = get_window('hann', width)
            # Scale the Hanning window to the desired amplitude
            scaled_hanning_window = height * hanning_window / np.max(hanning_window)
            return scaled_hanning_window

        elif self.ui.Smoothing_Window_Rectangle_Radio_Button.isChecked():
            # generate and adjust the height as desired
            rectangle_window = boxcar(width) * height
            return rectangle_window

        elif self.ui.Smoothing_Window_Gaussian_Radio_Button.isChecked():
            std_dev = width / (2 * math.sqrt(2 * math.log(2)))
            gaussian_window = get_window(('gaussian', std_dev), width) * height
            return gaussian_window

    def plot_smoothing(self, width : int, height : int):
        self.current_smoothing = self.smoothing_window(width, height)
        self.ui.Smoothing_Window_PlotWidget.clear()
        self.ui.Smoothing_Window_PlotWidget.plot(self.current_smoothing)
        
    def apply_selector(self):
        # Create a smoothing window box
        smoothing_window = pg.LinearRegionItem()
        smoothing_window.setRegion([self.min_range, self.max_range])
        self.frequency_graph.addItem(smoothing_window)

    def plot_frequency_domain(self, smoothing_flag=0):
        self.frequency_graph.clear()
        if smoothing_flag == 1:
            self.apply_selector()  
        self.frequency_graph.setLimits(xMin = 0, xMax = max(self.freq_domain_X_coordinates))
        self.frequency_graph.setLimits(yMin = min(self.modified_freq_domain_Y_coordinates), yMax = max(self.modified_freq_domain_Y_coordinates))
        self.frequency_graph.setYRange(min(self.modified_freq_domain_Y_coordinates), max(self.modified_freq_domain_Y_coordinates))
        self.frequency_graph.plot(self.freq_domain_X_coordinates, self.modified_freq_domain_Y_coordinates)
        
        #TODO: the transperent box need to be plotted in the ui class and then change it in width from sliders value. commented until fix
            #self.frequency_graph.gca().add_patch(self.frequency_graph.Rectangle((0, 0), 5, 2, edgecolor='r', facecolor='none', alpha=1))
            
        # Inverse Fourier transform to go back to the time domain
        self.time_domain_signal_modified = np.fft.ifft(self.modified_freq_domain_Y_coordinates * np.exp(1j * self.phases))
        #self.time_domain_signal_modified = np.real(self.time_domain_signal_modified)
        self.output_graph.setLimits(xMin = 0, xMax = max(self.freq_domain_X_coordinates))
        
        #TODO: check the limits again after fixing the plot in the output graph
            #self.output_graph.setLimits(yMin = min(self.time_domain_signal_modified), yMax = max(self.time_domain_signal_modified))
            
        self.output_graph.getViewBox().setYRange(-0.4, 0.4)
        #self.plot_output(self.time_domain_X_coordinates[:1], self.time_domain_signal_modified[:1])
        
        #TODO: need an update. this line convert the modified signal into wav file,
        # also try to change the datatype into hexa to check if the saxaphone sound is fixed or not
        wavfile.write('modified_signal.wav', self.sample_rate, self.time_domain_signal_modified.astype(np.float32))
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile('modified_signal.wav')))
        #self.player.play()
        
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
        self.hidden = not self.hidden
        self.input_spectrogram.canvas.toggle_spectrogram()
        self.output_spectrogram.canvas.toggle_spectrogram()

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
