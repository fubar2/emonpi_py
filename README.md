# emonpi_py

Some code developed as I figured out what the emonpi is capable of
It's good kit but emoncms is php/mysql which seems like overkill

I'm groping my way to a more lightweight solution based on bokeh, probably running on a desktop 
rather than the emonpi pi although it seems to run ok there...

Probably need a blaze server or something for emonhub to stock up which the bokeh app sucks in
as a source?

Meanwhile we have

mqtt_emon: a simple mqtt listener for an arbitrary mqtt server and subscription - currently
emonhub/rx/5/values

mqtt_bokeh: as above but with an updating plot - best with chrome rather than firefox...

emondata_bokeh: reads archived data into a dynamic plot - bokeh serve --show emondata_bokeh.py
after you edit the data path

readrawemoncms: reads the php binary data into tabular suitable for emondata_bokeh

feb 26
mqtt_bokeh.py will plot from mqtt 
emondata_bokeh.py plots archived tabular data
DOES NOT work well with firefox - chromium is fine

feb 25
Bokeh is really good.
Have a bokeh power stripchart working !!
Date times on x axis need fixin but, holy sheet it works.


feb 23
Added a simple mqtt test which does the needful for collecting future data

For legacy data:

Python code to parse emoncms/emonhub v8.5 php data files

The filesystem meta and dat files are unfortunately not the whole story because essential metadata like 
the name of the feed is stowed in mysql. Can't be bothered going there.

Sigh

Whatever, this will take all the files found under /home/pi/data/phpfina, read the metadata (such
as it is) and then the data. Output is an .xls file with raw time, value, date-time columns.

enjoy.

pull requests welcomed.



