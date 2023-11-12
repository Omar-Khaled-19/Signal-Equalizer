import BaseMode
from PyQt5.QtWidgets import QFileDialog
import wfdb, numpy as np
from PyQt5 import QtGui

class UniformMode(BaseMode.BaseMode):

    def __init__(self, ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4):
        super().__init__(ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4)

    def modify_frequency(self, value: int):
        pass

    def toggle_pause(self):
        super().toggle_pause()
        icon = QtGui.QIcon()
        if not self.paused:
            icon.addPixmap(QtGui.QPixmap("Assets/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.Uniform_Range_Play_Pause_Button.setIcon(icon)
        else:
            icon.addPixmap(QtGui.QPixmap("Assets/play (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.Uniform_Range_Play_Pause_Button.setIcon(icon)



class MusicalMode(BaseMode.BaseMode):

    def __init__(self, ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4):
        super().__init__(ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4)

    def modify_frequency(self, value: int):
        pass

    def toggle_pause(self):
        super().toggle_pause()
        icon = QtGui.QIcon()
        if not self.paused:
            icon.addPixmap(QtGui.QPixmap("Assets/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.Musical_Instruments_Play_Pause_Button.setIcon(icon)
        else:
            icon.addPixmap(QtGui.QPixmap("Assets/play (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.Musical_Instruments_Play_Pause_Button.setIcon(icon)


class AnimalMode(BaseMode.BaseMode):

    def __init__(self, ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4):
        super().__init__(ui, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4)

    def modify_frequency(self, value: int):
        pass

    def toggle_pause(self):
        super().toggle_pause()
        icon = QtGui.QIcon()
        if not self.paused:
            icon.addPixmap(QtGui.QPixmap("Assets/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.Animals_Sounds_Play_Pause_Button.setIcon(icon)
        else:
            icon.addPixmap(QtGui.QPixmap("Assets/play (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.Animals_Sounds_Play_Pause_Button.setIcon(icon)

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
        super().toggle_pause()
        icon = QtGui.QIcon()
        if not self.paused:
            icon.addPixmap(QtGui.QPixmap("Assets/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.ECG_Abnormalities_Play_Pause_Button.setIcon(icon)
        else:
            icon.addPixmap(QtGui.QPixmap("Assets/play (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.ECG_Abnormalities_Play_Pause_Button.setIcon(icon)

