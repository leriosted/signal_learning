"""
Complex Wave Generation with Automatic Transfer Function Calculation
12 Jan 25
T Lerios
"""

import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly.offline import plot

# Parameters for signals
duration = 6  # Duration in seconds
sampling_rate = 1000  # Samples per second
t = np.linspace(0, duration, int(sampling_rate * duration))

# Signal parameters
freqs = [3, 6, 12]  # Frequencies in Hz
exponential_rates = [0.5, -0.5, 0]  # Exponential growth/decay rates (positive, negative, zero)

# Generate complex waves
waves = [
    np.exp(exponential_rates[i] * t) * np.sin(2 * np.pi * freqs[i] * t)
    for i in range(3)
]

# Compute FFT for each signal
fft_results = [np.fft.fft(wave) for wave in waves]
frequencies = np.fft.fftfreq(len(t), d=1 / sampling_rate)  # Frequency vector

# Compute amplitude and phase for the positive frequencies only
positive_freq_idx = frequencies > 0  # Ignore zero and negative frequencies
amplitude = [2 * np.abs(fft[positive_freq_idx]) / len(t) for fft in fft_results]
phase = [np.angle(fft[positive_freq_idx], deg=True) for fft in fft_results]
frequencies = frequencies[positive_freq_idx]

# Convert amplitude to decibels
amplitude_db = [20 * np.log10(amp) for amp in amplitude]

# Create subplot structure
fig = make_subplots(
    rows=6, cols=1,
    subplot_titles=[
        "Signal 1: Exponentially Increasing", "Signal 2: Exponentially Decreasing", "Signal 3: Constant",
        "All Signals", "Bode Plot: Amplitude (dB)", "Bode Plot: Phase (Degrees)"
    ],
    vertical_spacing=0.11,
    shared_xaxes=True
)

colors = ['blue', 'green', 'red']

# Plot the individual signals
for i, (wave, color) in enumerate(zip(waves, colors)):
    fig.add_trace(go.Scatter(x=t, y=wave, mode='lines', name=f'Signal {i + 1}', line=dict(color=color)),
                  row=i + 1, col=1)

# Plot combined signals
for wave, color in zip(waves, colors):
    fig.add_trace(go.Scatter(x=t, y=wave, mode='lines', name='Combined Signals', line=dict(color=color)),
                  row=4, col=1)

# Add Bode plot - amplitude (dB)
for i, (amp_db, color) in enumerate(zip(amplitude_db, colors)):
    fig.add_trace(go.Scatter(x=frequencies, y=amp_db, mode='lines', name=f'Amplitude (dB) Signal {i + 1}', line=dict(color=color)),
                  row=5, col=1)

# Add Bode plot - phase (degrees)
for i, (ph, color) in enumerate(zip(phase, colors)):
    fig.add_trace(go.Scatter(x=frequencies, y=ph, mode='lines', name=f'Phase (Degrees) Signal {i + 1}', line=dict(color=color)),
                  row=6, col=1)

# Automatically compute and display transfer functions
transfer_functions = []
for i, (freq, rate) in enumerate(zip(freqs, exponential_rates)):
    omega = 2 * np.pi * freq
    if rate == 0:
        tf_freq_domain = f"H(s) = {omega:.2f} / (s + {omega:.2f})"
        tf_time_domain = f"H(t) = A sin(2π{freq}t)"
    else:
        tf_freq_domain = f"H(s) = {omega:.2f} / (s {'+' if rate > 0 else '-'} {abs(rate):.2f})"
        tf_time_domain = f"H(t) = A e^({'+' if rate > 0 else '-'}{abs(rate):.2f}t) sin(2π{freq}t)"
    tf_output_input = f"Y(s)/X(s) = {omega:.2f} / (s {'+' if rate > 0 else '-'} {abs(rate):.2f})"
    transfer_functions.append({
        "freq": freq,
        "time_domain": tf_time_domain,
        "freq_domain": tf_freq_domain,
        "output_input": tf_output_input
    })

# Add transfer function annotations off to the side
for i, tf in enumerate(transfer_functions):
    fig.add_annotation(
        x=1.05, y=0.5, xref='paper', yref=f'y{i + 1}',
        text=(
            f"<b>Signal {i + 1}</b><br>"
            f"Time: {tf['time_domain']}<br>"
            f"Freq: {tf['freq_domain']}<br>"
            f"Output/Input: {tf['output_input']}"
        ),
        showarrow=False, font=dict(size=12, color=colors[i]), align="left"
    )

# Update x-axis to logarithmic scale for Bode plots
fig.update_xaxes(type='log', title_text='Frequency (Hz)', row=5, col=1)
fig.update_xaxes(type='log', title_text='Frequency (Hz)', row=6, col=1)

# Update y-axis labels
fig.update_yaxes(title_text='Amplitude (dB)', row=5, col=1)
fig.update_yaxes(title_text='Phase (Degrees)', row=6, col=1)

# Show the plot
plot(fig)
