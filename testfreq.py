import sys
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtGui, QtCore

# Generate sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create PyQtGraph application
app = QtWidgets.QApplication([])
win = QtWidgets.QMainWindow()
central_widget = QtWidgets.QWidget()
win.setCentralWidget(central_widget)
grid_layout = QtWidgets.QGridLayout(central_widget)

# Create the frame and grid layout
frame_17 = QtWidgets.QFrame()
frame_17.setFrameShape(QtWidgets.QFrame.StyledPanel)
frame_17.setFrameShadow(QtWidgets.QFrame.Raised)
frame_17.setObjectName("frame_17")
grid_layout_26 = QtWidgets.QGridLayout(frame_17)
grid_layout_26.setObjectName("gridLayout_26")

# Create the plot widget
Animals_Sounds_Frequency_Domain_PlotWidget = pg.PlotWidget()
Animals_Sounds_Frequency_Domain_PlotWidget.setMinimumSize(QtCore.QSize(1231, 130))
Animals_Sounds_Frequency_Domain_PlotWidget.setObjectName("Animals_Sounds_Frequency_Domain_PlotWidget")
grid_layout_26.addWidget(Animals_Sounds_Frequency_Domain_PlotWidget, 0, 0, 1, 1)

# Plot the original signal
curve = Animals_Sounds_Frequency_Domain_PlotWidget.plot(x, y, pen='b')

# Create a smoothing window box
smoothing_window = pg.LinearRegionItem()
smoothing_window.setRegion([x.min(), x.max()])
Animals_Sounds_Frequency_Domain_PlotWidget.addItem(smoothing_window)

# Create a filtered signal plot
filtered_curve = Animals_Sounds_Frequency_Domain_PlotWidget.plot(pen='r')

# Define update function
def update():
    # Get the region of the smoothing window
    xmin, xmax = smoothing_window.getRegion()
    
    # Apply smoothing to the signal within the window
    filtered_y = np.copy(y)
    filtered_y[(x < xmin) | (x > xmax)] = 0.0
    
    # Update the filtered signal plot
    filtered_curve.setData(x, filtered_y)

# Connect the update function to the region change signal of the smoothing window
smoothing_window.sigRegionChanged.connect(update)

# Add the frame to the grid layout
grid_layout.addWidget(frame_17)

# Set the main window properties
win.setWindowTitle("Signal with Smoothing Window")
win.resize(800, 600)

# Start the PyQtGraph application
if __name__ == '__main__':
    update()
    win.show()
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        QtWidgets.QApplication.instance().exec_()