import numpy as np
import plotly.graph_objects as go
from scipy.integrate import quad
from scipy.fft import fft, fftfreq
import webbrowser
import os

# Function to compute Laplace Transform
# Here, we assume f(t) = e^(-t) * u(t), where u(t) is the unit step function
def laplace_transform(s_values):
    results = []
    for s in s_values:
        integral, _ = quad(lambda t: np.exp(-t) * np.exp(-s * t), 0, np.inf)
        results.append(np.real(integral))  # Taking real part
    return np.array(results)

# Parameters
t = np.linspace(0, 10, 1000)  # Time domain
f_t = np.exp(-t)  # Example function: e^(-t)

# Fourier Transform using FFT
N = len(t)
dt = t[1] - t[0]
frequencies = fftfreq(N, dt)
F_w = fft(f_t)

# Laplace Transform
s_real = np.linspace(0, 10, 100)
L_s = laplace_transform(s_real)

# Create subplots
fig = go.Figure()

# Plotting Fourier Transform
fig.add_trace(go.Scatter(x=frequencies, y=np.abs(F_w), mode='lines', name='Fourier Transform'))
fig.update_layout(
    title="Fourier Transform",
    xaxis_title="Frequency",
    yaxis_title="Magnitude",
    height=600
)

# Plotting Laplace Transform
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=s_real, y=L_s, mode='lines', name='Laplace Transform'))
fig2.update_layout(
    title="Laplace Transform",
    xaxis_title="Real Part of s",
    yaxis_title="Magnitude",
    height=600
)

# Save plots as HTML files and open in browser
html_file1 = 'fourier_transform_plot.html'
fig.write_html(html_file1)
webbrowser.open('file://' + os.path.realpath(html_file1))

html_file2 = 'laplace_transform_plot.html'
fig2.write_html(html_file2)
webbrowser.open('file://' + os.path.realpath(html_file2))
