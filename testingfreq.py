import numpy as np
import wave
import pyaudio
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


def write_wav_file(filename, data, sample_rate):
    output_path = 'C:\\Users\\Ahmed Taha\\Desktop\\' + filename
    with wave.open(output_path, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes (16 bits) per sample
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(data.tobytes())


def read_wav_file(filename):
    with wave.open(filename, 'rb') as wav_file:
        num_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        sample_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()
        raw_data = wav_file.readframes(num_frames)

    data = np.frombuffer(raw_data, dtype=np.int16)

    return data, sample_rate



def modify_frequency_domain(data, factor):
    spectrum = np.fft.fft(data)
    spectrum *= factor
    modified_data = np.fft.ifft(spectrum).real.astype(np.int16)
    return modified_data


# Generate a sine wave signal
duration = 5  # seconds
sample_rate = 44100  # Hz
frequency = 440  # Hz
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
signal = np.sin(2 * np.pi * frequency * t)

# Write the initial signal to a WAV file
write_wav_file('original.wav', signal, sample_rate)

# Play the initial signal using QMediaPlayer
player = QMediaPlayer()
media_content = QMediaContent(QUrl.fromLocalFile('original.wav'))
player.setMedia(media_content)
player.play()

# Modify the signal in the frequency domain
modified_signal = modify_frequency_domain(signal, 2.0)  # Example modification: doubling the signal amplitude

# Write the modified signal to the same WAV file
write_wav_file('original2.wav', modified_signal, sample_rate)

# Play the modified signal using QMediaPlayer
modified_media_content = QMediaContent(QUrl.fromLocalFile('original.wav'))
player.setMedia(modified_media_content)
player.play()

# Wait for the playback to finish
while player.state() == QMediaPlayer.PlayingState:
    pass

# Clean up
player.stop()