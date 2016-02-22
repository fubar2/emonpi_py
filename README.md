# emonpi_py
Python code to parse emoncms/emonhub php data files

The filesystem meta and dat files are unfortunately not the whole story because essential metadata like 
the name of the feed is stowed in mysql. 

Sigh

Whatever, this will take all the files found under /home/pi/data/phpfina, read the metadata (such
as it is) and then the data. Output is an .xls file with raw time, value, date-time columns.

