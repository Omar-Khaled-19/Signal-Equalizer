import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import fft, ifft
from IPython.display import Audio

# Load the original audio file
sample_rate, audio_data = wavfile.read('original_sound.wav')

# Extract the time-domain signal
time = np.arange(len(audio_data)) / sample_rate

# Plot the original signal in the time domain
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.plot(time, audio_data)
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.title('Original Signal')

# Perform the Fourier transform on the signal
frequency_domain_signal = fft.fft(audio_data)

# Compute the magnitudes of the frequency components
magnitudes = np.abs(frequency_domain_signal)

# Determine the corresponding frequencies
frequencies = fft.fftfreq(len(audio_data), 1/sample_rate)

# Find the indices corresponding to the frequency range to remove
min_freq = 2
max_freq = 19
indices_to_remove = np.where((frequencies >= min_freq) & (frequencies <= max_freq))

# Set the magnitudes of the specified frequencies to zero
magnitudes[indices_to_remove] = 0

# Perform the inverse Fourier transform to obtain the modified signal
modified_signal = ifft.ifft(magnitudes)

# Plot the modified signal in the time domain
plt.subplot(1, 2, 2)
plt.plot(time, modified_signal.real)
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.title('Modified Signal')

# Save the modified signal as a new audio file
wavfile.write('modified_sound.wav', sample_rate, modified_signal.real.astype(np.int16))

# Play the modified signal
Audio('modified_sound.wav')