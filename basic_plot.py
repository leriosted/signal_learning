import plotly.graph_objs as go
import plotly.io as pio
from PIL import Image
import io
import base64

# Load the image and convert to base64
with open("plot.png", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

# Create a plotly figure with the image embedded
fig = go.Figure()
fig.update_layout(
    images=[{
        'source': f'data:image/png;base64,{encoded_image}',
        'xref': 'paper',
        'yref': 'paper',
        'x': 0,
        'y': 1,
        'sizex': 1,
        'sizey': 1,
        'xanchor': 'left',
        'yanchor': 'top',
        'layer': 'below'
    }]
)

# Display the figure
pio.show(fig)
