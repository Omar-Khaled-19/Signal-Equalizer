import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sounddevice as sd

# Parameters
duration = 5  # Duration of the signal in seconds
sample_rate = 44100  # Sample rate (number of samples per second)
frequency = 440  # Frequency of the signal in Hz

# Generate the signal
t = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)
signal = np.sin(2 * np.pi * frequency * t)

# Initialize the figure and plot
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_xlim(0, duration)
ax.set_ylim(-1, 1)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Amplitude')

# Callback function for updating the line
def update_line(frame):
    line.set_data(t[:frame], signal[:frame])
    return line,

# Initialize the audio stream
stream = sd.OutputStream(samplerate=sample_rate, channels=1)

# Callback function for playing audio
def play_audio(outdata, frames, time, status):
    if frames:
        outdata[:, 0] = signal[:frames]

# Start the animation
ani = FuncAnimation(fig, update_line, frames=len(t), interval=10, blit=True)

# Start playing the audio
with stream:
 # Start the audio playback with the callback function
    sd.play(callback=play_audio, channels=1, samplerate=sample_rate)

# Show the plot
plt.show()