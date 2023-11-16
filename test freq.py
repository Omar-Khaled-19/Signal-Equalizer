import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

def plot_signal_time_frequency(file_path):
    # Load the WAV file
    sampling_rate, signal = wavfile.read(file_path)

    # Plot in time domain
    plt.subplot(2, 1, 1)
    plt.plot(np.arange(len(signal)) / sampling_rate, signal)
    plt.title('Time Domain Signal')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    # Plot in frequency domain
    plt.subplot(2, 1, 2)
    fft_result = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(len(fft_result), 1 / sampling_rate)
    plt.plot(frequencies, np.abs(fft_result))
    plt.title('Frequency Domain Representation')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')

    plt.tight_layout()
    plt.show()

# Example usage
wav_file_path = r"C:\Users\Ahmed Taha\Desktop\Signal-Equalizer\data.wav"

plot_signal_time_frequency(wav_file_path)
