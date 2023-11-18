import BaseMode, wfdb, numpy as np
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtGui

class UniformMode(BaseMode.BaseMode):

    def __init__(self, ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4):
        super().__init__(ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4)

    def modify_frequency(self, value: int):
        pass

    def toggle_pause(self):
        # Why the whole function is not written in BaseMode?
        super().toggle_pause()
        self.change_pause_icon(self.ui.Uniform_Range_Play_Pause_Button)

    def toggle_hide(self):
        super().toggle_hide()
        self.change_hide_icon(self.ui.Uniform_Range_Hide_Show_Spectrogram_Button)



class MusicalMode(BaseMode.BaseMode):

    def __init__(self, ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4):
        super().__init__(ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4)

    def modify_frequency(self, slider_value: int, slider: int):
        if slider == 1:
            super().modify_frequency(64, 500, slider_value)
        elif slider == 2:
            super().modify_frequency(250, 1000, slider_value)
        elif slider == 3:
            super().modify_frequency(1000, 2000, slider_value)
        else:
            super().modify_frequency(2000, 8000, slider_value)

    def toggle_pause(self):
        super().toggle_pause()
        self.change_pause_icon(self.ui.Musical_Instruments_Play_Pause_Button)

    def toggle_hide(self):
        super().toggle_hide()
        self.change_hide_icon(self.ui.Musical_Instruments_Hide_Show_Spectrogram_Button)

class AnimalMode(BaseMode.BaseMode):

    def __init__(self, ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4):
        super().__init__(ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4)

    def modify_frequency(self, slider: int):
        pass

    def toggle_pause(self):
        super().toggle_pause()
        self.change_pause_icon(self.ui.Animals_Sounds_Play_Pause_Button)

    def toggle_hide(self):
        super().toggle_hide()
        self.change_hide_icon(self.ui.Animals_Sounds_Hide_Show_Spectrogram_Button)

class ECGMode(BaseMode.BaseMode):

    def __init__(self, ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4):
        super().__init__(ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4)
    
    def modify_frequency(self, value: int):
        pass

    def load_signal(self):
        self.input_graph.clear()
        File_Path, _ = QFileDialog.getOpenFileName(None, "Browse Signal", "", "All Files (*)")
        if File_Path:
            Record = wfdb.rdrecord(File_Path[:-4])
            self.time_domain_Y_coordinates = list(Record.p_signal[:, 0])
            self.time_domain_X_coordinates = list(np.arange(len(self.time_domain_Y_coordinates)))
            self.stopped = False
            self.plot_signal()

    def update_plot_data(self):
        if not self.paused and not self.stopped:
            self.X_Points_Plotted += self.speed
            self.data_line.setData(self.time_domain_X_coordinates[0 : self.X_Points_Plotted + 1], 
                                self.time_domain_Y_coordinates[0 : self.X_Points_Plotted + 1])
            
            self.input_graph.getViewBox().setXRange(max(self.time_domain_X_coordinates[0: self.X_Points_Plotted + 1]) - 200, 
                                                    max(self.time_domain_X_coordinates[0: self.X_Points_Plotted + 1]))
        
    def toggle_pause(self):
        self.paused = not self.paused
        self.change_pause_icon(self.ui.ECG_Abnormalities_Hide_Show_Spectrogram_Button)

    def reset(self):
        self.X_Points_Plotted = 0

    def update_speed(self,slider):
        self.speed = 10 * slider.value()

    def stop(self):
        self.stopped = True
        self.input_graph.clear()
        self.input_graph.getViewBox().setXRange(0,100)
        self.X_Points_Plotted = 0

    def toggle_hide(self):
        super().toggle_hide()
        self.change_hide_icon(self.ui.ECG_Abnormalities_Play_Pause_Button)