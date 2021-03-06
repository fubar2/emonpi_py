# example from https://pypi.python.org/pypi/paho-mqtt
# ross feb 23 2016
# test direct access to emoncms
# will append to outfile so delete to start again

import paho.mqtt.client as mqtt
import time

OUTFNAME = 'mqtt_emon.xls'
PI_IP = "192.168.1.4" # YMMV
SUBS = "emonhub/rx/5/values"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    subs = client.subscribe(SUBS)
    print 'Subscription returned:', str(subs)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    print msg.payload
    spay = msg.payload.replace(',','\t')
    s = '%f\t%s' % (time.time(),spay)
    outf.write(s)
    outf.write('\n')
    outf.flush()
    
outf = open(OUTFNAME,'a')
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(PI_IP, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
