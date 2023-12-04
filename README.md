# Signal Equalizer

Welcome to Signal Equalizer, a Python desktop application for signal processing with four different modes: Uniform Range, Musical Instruments, Animal Sounds, and ECG Signals. This application allows users to load signals, visualize them dynamically, analyze their frequencies in the Fourier domain, and manipulate the signal using sliders for frequency components.

## Features

- **Four Modes:**
  1. **Uniform Range:** Manipulate signals in a uniform frequency range with 10 sliders.
  2. **Musical Instruments:** Analyze and modify musical instrument signals with 4 sliders.
  3. **Animal Sounds:** Adjust frequency components of animal sounds using 4 sliders.
  4. **ECG Signals:** Process ECG signals with 4 sliders for arrhythmia components.

- **Signal Visualization:**
  - Dynamically plot the input signal.
  - Display Fourier domain representation of the signal.
  - Visualize the output signal after inverse Fourier transformation.

- **Frequency Manipulation:**
  - Use sliders to remove or amplify specific frequency components.
  - Choose from various smoothing windows: Hanning, Hamming, Rectangular, or Gaussian.

## Libraries Used

- PyQt5
- pyqtgraph
- numpy
- bisect
- librosa
- scipy
- soundfile
- os
- abc

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Omar-Khaled-19/Signal-Equalizer.git
   ```

2. **Install dependencies:**
   ```bash
   pip install PyQt5 pyqtgraph numpy librosa scipy soundfile
   ```

3. **Run the application:**
   ```bash
   python Signal_Equaliser.py
   ```

## Usage

1. Launch the application.
2. Choose the desired mode from the menu.
3. Load a signal file.
4. Explore and manipulate the signal using sliders.
5. Choose a smoothing window for frequency modification.
6. Visualize the signal, Fourier domain, and modified signal.

## Contributions

Contributions are welcome! If you have any ideas or improvements, feel free to open an issue or create a pull request.

## Acknowledgments

- Special thanks to the developers of PyQt5, pyqtgraph, and other libraries used in this project.

Happy signal processing! 🎛️🎶
