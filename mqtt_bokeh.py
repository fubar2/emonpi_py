"""
Simple bokeh plotter for the first column of your mqtt emonhub/rx/5/values data stream
ross feb 25

based on examples and from http://bokeh.pydata.org/en/0.11.0/docs/user_guide/server.html
Works for me using bokeh 0.11.1

run as
bokeh serve --show mqtt_bokeh.py
The --show option will cause a browser to open up a new tab automatically to the address of the running application, which in this case is:

http://localhost:5006/myapp

"""
import numpy as np

from bokeh.models import Button, NumeralTickFormatter
from bokeh.palettes import RdYlBu3
from bokeh.plotting import *
from bokeh.properties import value
import paho.mqtt.client as mqtt
import time
import datetime
import sys

OUTFNAME = 'mqtt_emon.xls'
SERVER_IP = "192.168.1.3" ### ymmv
SUBSCRIPTIONS = 'emonhub/rx/5/values'

class mq():

    # adapted from example from https://pypi.python.org/pypi/paho-mqtt
    # ross feb 23 2016  
    # test direct access to emoncms
    # will append to outfile so delete to start again

    def __init__(self,outfname,subs,server,port,timeout,looptimeout,ds):
        self.OUTFNAME = outfname
        self.subs = subs
        self.server = server
        self.port = port
        self.timeout = timeout
        self.looptimeout = looptimeout
        self.ds = ds
        outf = open(OUTFNAME,'a')
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.server, self.port, self.timeout)

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self,client, userdata, flags, rc):
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        subres = client.subscribe(self.subs)
        print("Connected with result code "+str(rc))


    # The callback for when a PUBLISH message is received from the server.
    def on_message(self,client, userdata, msg):
        t = time.time()
        tdt = datetime.datetime.fromtimestamp(t)
        powr = msg.payload.split(',')[0] # take power as first
        print >> sys.stdout,'@',t,'y=',powr
        self.ds.data['x'].append(tdt)
        self.ds.data['y'].append(powr)
        self.ds.trigger('data', self.ds.data, self.ds.data)

# prepare output to server
# output_server("test_power")
# create a plot and style its properties
p = figure(plot_width=800, plot_height=600, x_axis_type="datetime")


p.xaxis.axis_label = "Time"
p.xaxis.axis_label_text_color = "darkred"
p.axis.major_label_text_font_size=value("10pt")
p.xaxis.major_label_orientation = "vertical"

# add a text renderer to out plot (no data yet)
p.line(x=[], y=[], name="power_line",line_width="2",line_color="blue")
renderer = p.select(dict(name="power_line"))
ds = renderer[0].data_source

m = mq(outfname='mqtt_emon.xls',subs=SUBSCRIPTIONS,
           server = SERVER_IP,port=1883,timeout=60,looptimeout=1,ds=ds)

def callstop():
    m.client.loop_stop()
    sys.exit(0)

def update():
    m.client.loop(timeout=0.5)

# add a button widget and configure with the call back
button = Button(label="Stop")
button.on_click(callstop)
# put the button and plot in a layout and add to the document
curdoc().add_root(vplot(button, p))
curdoc().add_periodic_callback(update, 500) # call client.loop to update if data available
