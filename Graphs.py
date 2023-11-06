from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog
import pandas as pd
import wfdb, numpy as np

class TimeGraph:
    
    def __init__(self, ui ,graph_widget):
        self.UI = ui
        self.graph_widget = graph_widget
        self.X_Points_Plotted = 0
        self.paused = False
        self.speed = 1
        self.X_Coordinates = []
        self.Y_Coordinates = []

    def load_csv(self):
        File_Path, _ = QFileDialog.getOpenFileName(None, "Browse Signal", "", "All Files (*)")
        if File_Path:
            Coordinates_List = ["x", "y"]
            Signal = pd.read_csv(File_Path, usecols=Coordinates_List)
            self.X_Coordinates = Signal["x"]
            self.Y_Coordinates = Signal["y"]
            self.plot_signal()

    def load_ecg(self):
        File_Path, _ = QFileDialog.getOpenFileName(None, "Browse Signal", "", "All Files (*)")
        if File_Path:
            Record = wfdb.rdrecord(File_Path[:-4])
            self.Y_Coordinates = list(Record.p_signal[:1000, 0])
            self.X_Coordinates = list(np.arange(len(self.Y_Coordinates)))
            self.plot_signal()
            self.UI.ECG_Abnormalities_Signal_Speed_Slider.setValue(1)

    def plot_signal(self):
        self.graph_widget.setLimits(xMin=0, xMax=float('inf'))
        self.data_line = self.graph_widget.plot(self.X_Coordinates[:1], self.Y_Coordinates[:1],pen="g")
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        if not self.paused:    
            self.X_Points_Plotted += self.speed
            self.data_line.setData(self.X_Coordinates[0 : self.X_Points_Plotted + 1], self.Y_Coordinates[0 : self.X_Points_Plotted + 1])
            self.graph_widget.getViewBox().setXRange(max(self.X_Coordinates[0: self.X_Points_Plotted + 1]) - 100, max(self.X_Coordinates[0: self.X_Points_Plotted + 1]))
        
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

    def update_speed(self):
        self.speed = self.UI.ECG_Abnormalities_Signal_Speed_Slider.value()

    def stop(self):
        self.graph_widget.clear()


class FrequencyGraph:

    def __init__(self):
        pass




class Spectrogram:
    
    def __init__(self):
        pass
