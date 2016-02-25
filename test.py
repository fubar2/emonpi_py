
from __future__ import print_function

from numpy import pi, arange, sin
import numpy as np
import time
from bokeh.plotting import *
from bokeh.util.browser import view
from bokeh.io import show
from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.models.glyphs import Circle
from bokeh.models import (
    Plot, DataRange1d, DatetimeAxis,
    ColumnDataSource, PanTool, WheelZoomTool
)
from bokeh.resources import INLINE

x = arange(-2 * pi, 2 * pi, 0.1)
y = sin(x)

# Create an array of times, starting at the current time, and extending
# for len(x) number of hours.
# times = np.arange(len(x)) * 3600000 + time.time()
times = np.arange(len(x)) * 3600 + time.time()

source = ColumnDataSource(
    data=dict(x=x, y=y, times=times)
)

xdr = DataRange1d()
ydr = DataRange1d()
print ('xdr=',xdr,'ydr=',ydr)
p = figure(title="test", toolbar_location="above")
p.grid.grid_line_color = "navy"
p.background_fill_color = "#eeeeee"
p.scatter(x, y, size=15,
              line_color="navy", fill_color="orange", alpha=0.5)

#circle = Circle(x="times", y="y", fill_color="red", size=5, line_color="black")
#p.add_glyph(source, circle)

p.add_layout(DatetimeAxis(), 'below')
p.add_layout(DatetimeAxis(), 'left')

p.add_tools(PanTool(), WheelZoomTool())

show(p)
