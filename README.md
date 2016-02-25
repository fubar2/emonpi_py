# emonpi_py

feb 26
mqtt_bokeh.py will plot from mqtt 
emondata_bokeh.py plots archived tabular data


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



