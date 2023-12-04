import BaseMode, wfdb, numpy as np
from PyQt5.QtWidgets import QFileDialog

class UniformMode(BaseMode.BaseMode):

    def __init__(self, ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4, uismoothing, original_spectrogram_label, modified_spectrogram_label):
        super().__init__(ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4, uismoothing, original_spectrogram_label, modified_spectrogram_label)
        self.slider5 = ui.Uniform_Range_Frequency_Range_5_Slider
        self.slider6 = ui.Uniform_Range_Frequency_Range_6_Slider
        self.slider7 = ui.Uniform_Range_Frequency_Range_7_Slider
        self.slider8 = ui.Uniform_Range_Frequency_Range_8_Slider
        self.slider9 = ui.Uniform_Range_Frequency_Range_9_Slider
        self.slider10 = ui.Uniform_Range_Frequency_Range_10_Slider


    def modify_frequency(self, slider_value: int, slider: int):
        if slider == 1:
            super().modify_frequency(1050, 1150, slider_value)
        elif slider == 2:
            super().modify_frequency(1150, 1250, slider_value)
        elif slider == 3:
            super().modify_frequency(1250, 1350, slider_value)
        elif slider == 4:
            super().modify_frequency(1350, 1450, slider_value)
        elif slider == 5:
            super().modify_frequency(1450, 1550, slider_value)
        elif slider == 6:
            super().modify_frequency(1550, 1650, slider_value)
        elif slider == 7:
            super().modify_frequency(1650, 1750, slider_value)
        elif slider == 8:
            super().modify_frequency(1750, 1850, slider_value)
        elif slider == 9:
            super().modify_frequency(1850, 1950, slider_value)
        else:
            super().modify_frequency(1950, 2050, slider_value)

    def load_signal(self):
        self.change_pause_icon(self.ui.Uniform_Range_Play_Pause_Button)
        super().load_signal()

    def toggle_pause(self):
        super().toggle_pause()
        self.change_pause_icon(self.ui.Uniform_Range_Play_Pause_Button)

    def toggle_hide(self):
        super().toggle_hide()
        self.change_hide_icon(self.ui.Uniform_Range_Hide_Show_Spectrogram_Button)

    def plot_frequency_domain(self, smoothing_flag=0, minX=0, maxX=1000):
        super().plot_frequency_domain(minX=1090, maxX=2100)

class MusicalMode(BaseMode.BaseMode):

    def __init__(self, ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4, uismoothing, original_spectrogram_label, modified_spectrogram_label):
        super().__init__(ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4, uismoothing, original_spectrogram_label, modified_spectrogram_label)

    def modify_frequency(self, slider_value: int, slider: int):
        if slider == 1:
            super().modify_frequency(64, 125, slider_value)
        elif slider == 2:
            super().modify_frequency(125, 1000, slider_value)
        elif slider == 3:
            super().modify_frequency(1000, 2000, slider_value)
        else:
            super().modify_frequency(2000, 4000, slider_value)

    def load_signal(self):
        self.change_pause_icon(self.ui.Musical_Instruments_Play_Pause_Button)
        super().load_signal()

    def toggle_pause(self):
        super().toggle_pause()
        self.change_pause_icon(self.ui.Musical_Instruments_Play_Pause_Button)

    def toggle_hide(self):
        super().toggle_hide()
        self.change_hide_icon(self.ui.Musical_Instruments_Hide_Show_Spectrogram_Button)

    def plot_frequency_domain(self, smoothing_flag=0, minX=0, maxX=1000):
        super().plot_frequency_domain(minX=30, maxX=10000)

class AnimalMode(BaseMode.BaseMode):

    def __init__(self, ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4, uismoothing, original_spectrogram_label, modified_spectrogram_label):
        super().__init__(ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4, uismoothing, original_spectrogram_label, modified_spectrogram_label)

    def modify_frequency(self, slider_value: int, slider: int):
        if slider == 1:
            super().modify_frequency(64, 500, slider_value)
        elif slider == 2:
            super().modify_frequency(500, 1010, slider_value)
        elif slider == 3:
            super().modify_frequency(1010, 2010, slider_value)
        else:
            super().modify_frequency(2010, 8000, slider_value)

    def load_signal(self):
        self.change_pause_icon(self.ui.Animals_Sounds_Play_Pause_Button)
        super().load_signal()

    def toggle_pause(self):
        super().toggle_pause()
        self.change_pause_icon(self.ui.Animals_Sounds_Play_Pause_Button)

    def toggle_hide(self):
        super().toggle_hide()
        self.change_hide_icon(self.ui.Animals_Sounds_Hide_Show_Spectrogram_Button)

    def plot_frequency_domain(self, smoothing_flag=0, minX=0, maxX=1000):
        super().plot_frequency_domain(minX=60, maxX=4100)
class ECGMode(BaseMode.BaseMode):

    def __init__(self, ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4, uismoothing, original_spectrogram_label, modified_spectrogram_label):
        self.duration = None
        super().__init__(ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4, uismoothing, original_spectrogram_label, modified_spectrogram_label)
        self.is_sound = False
    def modify_frequency(self, slider_value: int, slider: int):
        if slider == 1:
            super().modify_frequency(0, 60, slider_value) # P54 rec2
        elif slider == 2:
            super().modify_frequency(95, 105, slider_value) # P88 rec3
        elif slider == 3:
            super().modify_frequency(140, 160, slider_value) #P68 rec2
        else:
            super().modify_frequency(198, 202, slider_value) #P24 rec2  Bonus: P11 rec1 (248- 250 Hz)

    def load_signal(self):
        self.input_graph.clear()
        self.frequency_graph.clear()
        self.output_graph.clear()
        self.X_Points_Plotted = 0
        self.change_pause_icon(self.ui.ECG_Abnormalities_Play_Pause_Button)
        self.File_Path, _ = QFileDialog.getOpenFileName(None, "Browse Signal", "", "All Files (*)")
        if self.File_Path:
            record_data, record_fields = wfdb.rdsamp(self.File_Path[:-4], channels=[1])
            self.sample_rate = record_fields['fs']
            self.duration = record_fields['sig_len'] / self.sample_rate  # Duration in seconds
            self.time_domain_Y_coordinates = list(record_data[:, 0])
            self.time_domain_signal_modified = self.time_domain_Y_coordinates.copy()
            self.time_domain_X_coordinates = np.linspace(0, self.duration, len(self.time_domain_Y_coordinates), endpoint=False)
            self.stopped = False
            self.plot_signals()

    def update_plot_data(self):
        if not self.paused and not self.stopped:
            self.X_Points_Plotted += 50
            self.data_line_in.setData(self.time_domain_X_coordinates[0 : self.X_Points_Plotted + 1], self.time_domain_Y_coordinates[0 : self.X_Points_Plotted + 1])
            self.data_line_out.setData(self.time_domain_X_coordinates[0: self.X_Points_Plotted + 1], self.time_domain_signal_modified[0: self.X_Points_Plotted + 1].real)

            self.input_graph.getViewBox().setXRange(max(self.time_domain_X_coordinates[0: self.X_Points_Plotted + 1]) - 5, max(self.time_domain_X_coordinates[0: self.X_Points_Plotted + 1]))
            self.output_graph.getViewBox().setXRange(max(self.time_domain_X_coordinates[0: self.X_Points_Plotted + 1]) - 5, max(self.time_domain_X_coordinates[0: self.X_Points_Plotted + 1]))
            self.frequency_graph.getViewBox().setYRange(0,2000)

            if not self.hidden:
                self.input_spectrogram.canvas.plot_spectrogram(self.time_domain_Y_coordinates[:self.X_Points_Plotted + 1],self.sample_rate)
                self.output_spectrogram.canvas.plot_spectrogram(self.time_domain_signal_modified[:self.X_Points_Plotted + 1],self.sample_rate)

    def toggle_pause(self):
        self.paused = not self.paused
        self.change_pause_icon(self.ui.ECG_Abnormalities_Play_Pause_Button)

    def reset(self):
        self.X_Points_Plotted = 0

    def update_speed(self,slider):
        self.speed = 100 * slider.value()

    def stop(self):
        self.stopped = True
        self.input_graph.clear()
        self.input_graph.getViewBox().setXRange(0,100)
        self.X_Points_Plotted = 0

    def toggle_hide(self):
        super().toggle_hide()
        self.change_hide_icon(self.ui.ECG_Abnormalities_Hide_Show_Spectrogram_Button)

    def calculate_frequency_domain(self):
        fft_result = np.fft.fft(self.time_domain_Y_coordinates)
        self.freq_domain_X_coordinates = np.fft.fftfreq(len(self.time_domain_Y_coordinates), d=1 / self.sample_rate)  # Frequency values corresponding to the FFT result
        self.freq_domain_Y_coordinates = np.abs(fft_result)
        self.phases = np.angle(fft_result)
        self.modified_freq_domain_Y_coordinates = self.freq_domain_Y_coordinates.copy()
        self.plot_frequency_domain()

    def plot_frequency_domain(self, smoothing_flag=0, minX=0, maxX=1000):
        super().plot_frequency_domain(minX=0, maxX=250)