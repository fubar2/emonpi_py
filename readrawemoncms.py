"""
read 4 byte float data and metadata for a php emoncms 8.5 data file
ross feb 22 2016

What a pity the metadata is so incomplete - the id is simply the feed id whose corresponding
name is in mysql. 

Fugly conversion from binary

"""


import os
import numpy as N
import array
import time
import logging


FROM_DIR = '/home/pi/data/phpfina/'
LOG_ON = True

class emoncmsdat():

	def __init__(self,prefix='10'):
           self.prefix = prefix
	   fd = '%s.dat' % self.prefix
	   fm = '%s.meta' % self.prefix
           ffm = open(fm,'rb')
           m = array.array('L')
           m.read(ffm,4)
           metId,metNpoints,metInterval,metStarted = N.array(m,N.uint32)
           lognote = 'file %s: id=%d, npoints=%d, interval=%d, started=%s' % (fm,metId,metNpoints,metInterval,time.ctime(metStarted))
           if LOG_ON:
              logging.info(lognote)
           tstart = time.ctime(int(metStarted))
           ffd = open(fd,'rb').read()
           d = array.array('f')
           d.fromstring(ffd)
	   self.data = []
           for i,kw in enumerate(d):
               t = metStarted + metInterval*i
               if (kw != kw): # tests for NaN
                 kw = 0
               thistime = time.ctime(t)
               v = '%d\t%6.1f\t%s' % (t,kw,thistime)
               self.data.append(v)
           dN = len(ffd)/4
           lognote = '# Read #%d, from %s, id = %s, interval = %d start time = %s' % (dN,fd,metId,metInterval,tstart)
           logging.info(lognote)

logging.basicConfig(filename='readrawemoncms.log',level=logging.DEBUG,\
  format='%(asctime)s:%(levelname)s:%(message)s', filemode='w')
flist = os.listdir(FROM_DIR)
prefs = [x.split('.')[0] for x in flist if ((x.split('.')[1] == 'dat') & ('%s.meta' % x.split('.')[0] in flist))]
dats = []
lognote = 'readrawemoncms found %s feeds in %s' % (','.join(prefs),FROM_DIR)
logging.info(lognote)
for prefix in prefs:
    e = emoncmsdat(os.path.join(FROM_DIR,prefix))
    outf = open('%s.xls' % prefix,'w')
    outf.write('traw\tkw\ttime\tsource\n')
    outf.write('\n'.join(e.data))
    outf.write('\n')
    outf.close()
    dats.append(e.data)
    # whatever else you need to do...


  


