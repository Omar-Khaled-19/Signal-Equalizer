# Imports
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib
matplotlib.use('QT5Agg')
class MplCanvas(Canvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)

    def plot_spectrogram(self, signal, fs):
        self.ax.cla()
        self.ax.specgram(signal, Fs=fs, cmap='viridis')
        self.ax.set_xlabel('Time [s]')
        self.ax.set_ylabel('Frequency [Hz]')
        self.ax.set_title('Spectrogram')
        self.draw()

    def clear_spectrogram(self):
        self.ax.cla()

class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QtWidgets.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
