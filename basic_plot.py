import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from scipy.signal import butter, lfilter, freqz
from plotly.offline import plot

# Parameters for the sine waves
sampling_rate = 1000  # Samples per second
duration = 1.0        # Duration in seconds
t = np.linspace(0, duration, int(sampling_rate * duration))  # Time vector

# Generate sine waves
freqs = [30, 60, 120]  # Frequencies of the sine waves in Hz
sine_waves = [np.sin(2 * np.pi * f * t) for f in freqs]  # List of sine waves

# Create subplot for the sine waves
fig = make_subplots(rows=8, cols=2, subplot_titles=[
    "Original Sine Waves", "Noisy Signals", "Bode Plot (Magnitude)", 
    "Bode Plot (Phase)", "FFT Spectrum", "Filtered Signals"],
    vertical_spacing=0.05)

# Plot the original sine waves
for i, wave in enumerate(sine_waves):
    fig.add_trace(go.Scatter(x=t, y=wave, mode='lines', name=f'{freqs[i]}Hz (Clean)'),
                  row=1, col=1)

# Add random noise and plot noisy signals
noise = [wave + np.random.normal(0, 0.5, len(t)) for wave in sine_waves]  # Noisy signals
for i, noisy_wave in enumerate(noise):
    fig.add_trace(go.Scatter(x=t, y=noisy_wave, mode='lines', name=f'{freqs[i]}Hz (Noisy)',
                             line=dict(color='red', width=1, dash='dot')),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=t, y=sine_waves[i], mode='lines', name=f'{freqs[i]}Hz (Original)',
                             line=dict(color='blue', width=2)),
                  row=2, col=1)

# Bode plot (magnitude and phase)
# Use a Butterworth filter as an example to show frequency response
b, a = butter(4, [20 / (sampling_rate / 2), 150 / (sampling_rate / 2)], btype='band')
w, h = freqz(b, a, worN=8000)
fig.add_trace(go.Scatter(x=w * sampling_rate / (2 * np.pi), y=20 * np.log10(abs(h)),
                         mode='lines', name='Magnitude Response'),
              row=3, col=1)
fig.add_trace(go.Scatter(x=w * sampling_rate / (2 * np.pi), y=np.angle(h),
                         mode='lines', name='Phase Response'),
              row=4, col=1)

# FFT of noisy signals to identify active frequencies
fft_results = [np.fft.fft(noisy_wave) for noisy_wave in noise]
fft_freq = np.fft.fftfreq(len(t), 1 / sampling_rate)
for i, fft_wave in enumerate(fft_results):
    fig.add_trace(go.Scatter(x=fft_freq, y=abs(fft_wave), mode='lines', name=f'{freqs[i]}Hz FFT'),
                  row=5, col=1)

# Filter the noisy signals using a bandpass filter
def bandpass_filter(data, lowcut, highcut, fs, order=4):
    """Applies a Butterworth bandpass filter to the input data."""
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    y = lfilter(b, a, data)
    return y

filtered_signals = [bandpass_filter(noisy_wave, 20, 150, sampling_rate) for noisy_wave in noise]

# Plot the filtered signals
for i, filtered_wave in enumerate(filtered_signals):
    fig.add_trace(go.Scatter(x=t, y=filtered_wave, mode='lines', name=f'{freqs[i]}Hz (Filtered)',
                             line=dict(color='green', width=2)),
                  row=6, col=1)

# Update layout
fig.update_layout(height=2000, width=1000, title_text="Sine Waves, Noise, and Filtering Example")

# Show plot in browser
plot(fig)
