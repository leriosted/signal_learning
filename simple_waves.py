'''
Simple Wave Generation and Plotting
12 Jan 25
T Lerios

To practice making simple waves and plotting them before moving on to testing different types of filters.

'''
import numpy as np
import plotly.graph_objs as go 
from plotly.subplots import make_subplots
from scipy.signal import butter, lfilter, freqz 
from plotly.offline import plot 

# Creating a time vector and setting parameters for the signal
duration = 6 # Duration in seconds
sampling_rate = 1000 # Samples per second
t = np.linspace(0,duration,int(sampling_rate+duration))

# Generate some waves
freqs = [3, 6, 12]
waves = [np.sin(2*np.pi*f*t) for f in freqs]

# Create the subplot structure
fig = make_subplots(rows=4, cols=1, subplot_titles=[
    "Signal 1",
    "Signal 2",
    "Signal 3",
    "All Signals",
],
vertical_spacing=0.05)

# Plot the waves
for i, wave in enumerate(waves):
    fig.add_trace(go.Scatter(x=t, y=wave, mode='lines', name=f'{freqs[i]}Hz (Clean)'),
    row=i + 1, col=1)

for i, wave in enumerate(waves):
    fig.add_trace(go.Scatter(x=t, y=wave, mode='lines', name=f'{freqs[i]}Hz (Clean)'),
    row=4, col=1)

plot(fig)