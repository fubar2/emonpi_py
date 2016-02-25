"""
Simple bokeh plotter for xls archived emonpi php data
written as tabular using readrawemoncms.py

YMMV

ross feb 25

based on examples and from http://bokeh.pydata.org/en/0.11.0/docs/user_guide/server.html
Works for me using bokeh 0.11.1

run as
bokeh serve --show mqtt_bokeh.py
The --show option will cause a browser to open up a new tab automatically to the address of the running application, which in this case is:

http://localhost:5006/myapp

"""
import numpy as np
import pandas as pd

from bokeh.models import Button, NumeralTickFormatter
from bokeh.palettes import RdYlBu3
from bokeh.plotting import *
from bokeh.core.properties import value
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.io import output_file, show, vform
import time
import datetime
import sys


OLD_DATA = "/home/rlazarus/pi/data/raw/14.xls" ## and me too.

# Filter for smoothing data originates from http://stackoverflow.com/questions/20618804/how-to-smooth-a-curve-in-the-right-way
# from https://github.com/bokeh/bokeh/blob/master/examples/app/weather/main.py
def get_dataset(src, name, distribution):
    df = src[src.airport == name].copy()
    del df['airport']
    df['date'] = pd.to_datetime(df.date)
    df['left'] = df.date - pd.DateOffset(days=0.5)
    df['right'] = df.date + pd.DateOffset(days=0.5)
    df = df.set_index(['date'])
    df.sort_index(inplace=True)
    if distribution == 'Smooth':
        window, order = 51, 3
        for key in STATISTICS:
            df[key] = savgol_filter(df[key], window, order)

    return ColumnDataSource(data=df)

'''
##https://github.com/bokeh/bokeh-demos/blob/master/stocks/custom_stocks_panel.py

source = AjaxDataSource(data_url='http://localhost:5000/data', polling_interval=1000)

# Get the data for the entire time period (so that we can use on th upper plot)
url = "http://127.0.0.1:5000/alldata"
res = requests.get(url, timeout=20)
data = res.json()
'''
# create a plot and style its properties
p = figure(plot_width=800, plot_height=600, x_axis_type="datetime")


p.xaxis.axis_label = "Time"
p.xaxis.axis_label_text_color = "darkred"
p.axis.major_label_text_font_size=value("10pt")
p.xaxis.major_label_orientation = "vertical"
p.yaxis.axis_label = "Power (KW)"
p.lod_threshold = 1000
p.lod_factor = 50


d = pd.read_csv(OLD_DATA,sep='\t',parse_dates=['traw',])

source = ColumnDataSource(d )
print 'processing % rows of old data' % len(d)
print 'd=',d[:10]
p.line(x='traw', y='kw', source=source, name="power_line", line_width="2", line_color="blue")

    
def callstop():
    sys.exit(0)

# add a button widget and configure with the call back
button = Button(label="Stop")
button.on_click(callstop)
# put the button and plot in a layout and add to the document
curdoc().add_root(vplot(button, p))


