import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Matplotlib Rectangle in PyQtGraph")
        self.setGeometry(100, 100, 800, 600)

        # Create a PyQtGraph plot widget
        self.plot_widget = pg.PlotWidget(self)
        self.setCentralWidget(self.plot_widget)

        # Generate some random data for the plot
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        # Plot the data using PyQtGraph
        self.plot_widget.plot(x, y)

        # Create a Matplotlib figure and axes
        self.fig, self.ax = plt.subplots()

        # Draw a rectangle using Matplotlib
        rect = Rectangle((2, -0.5), 3, 1, facecolor='red', alpha=0.5)
        self.ax.add_patch(rect)

        # Get the Matplotlib figure canvas and initialize it
        self.canvas = self.fig.canvas
        self.canvas.draw()

        # Convert the Matplotlib canvas to a PyQtGraph widget
        self.matplotlib_widget = self.canvas.native

        # Set the position and size of the Matplotlib widget within the PyQtGraph plot widget
        self.matplotlib_widget.setGeometry(100, 100, 200, 150)

        # Add the Matplotlib widget to the PyQtGraph plot widget
        self.plot_widget.addItem(self.matplotlib_widget)

        # Disable the interaction on the Matplotlib widget to prevent conflicts with PyQtGraph
        self.matplotlib_widget.setFlag(Qt.ItemIsMovable, False)
        self.matplotlib_widget.setFlag(Qt.ItemIsSelectable, False)
        self.matplotlib_widget.setFlag(Qt.ItemIsFocusable, False)

 # Draw a transparent box above the frequency domain
    box_width = frq[-1] / 4
    box_height = max(abs(fft_signal)) / 4
    plt.gca().add_patch(plt.Rectangle((0, 0), box_width, box_height, edgecolor='r', facecolor='none', alpha=1))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())