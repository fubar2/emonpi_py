"""
from http://bokeh.pydata.org/en/0.11.0/docs/user_guide/server.html

Notice that we have not specified an output or connection method anywhere in this code. It is a simple script that creates and updates objects. The flexibility of the bokeh command line tool means that we can defer output options until the end. We could, e.g., run bokeh json myapp.py to get a JSON serialized version of the the application. But in this case, we would like to run the app on a Bokeh server, so we execute:

bokeh serve --show myapp.py
The --show option will cause a browser to open up a new tab automatically to the address of the running application, which in this case is:

http://localhost:5006/myapp

"""
import numpy as np

from bokeh.models import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc, vplot

# create a plot and style its properties
p = figure(x_range=(0, 100), y_range=(0, 100), toolbar_location=None)
p.border_fill_color = 'black'
p.background_fill_color = 'black'
p.outline_line_color = None
p.grid.grid_line_color = None

# add a text renderer to out plot (no data yet)
r = p.text(x=[], y=[], text=[], text_color=[], text_font_size="20pt",
           text_baseline="middle", text_align="center")

i = 0

ds = r.data_source

# create a callback that will add a number in a random location
def callback():
    global i
    ds.data['x'].append(np.random.random()*70 + 15)
    ds.data['y'].append(np.random.random()*70 + 15)
    ds.data['text_color'].append(RdYlBu3[i%3])
    ds.data['text'].append(str(i))
    ds.trigger('data', ds.data, ds.data)
    i = i + 1

# add a button widget and configure with the call back
button = Button(label="Press Me")
button.on_click(callback)

# put the button and plot in a layout and add to the document
curdoc().add_root(vplot(button, p))

