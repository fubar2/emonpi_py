"""
read 4 byte float data and metadata for a php emoncms 8.5 data file
ross feb 22 2016

What a pity the metadata is so incomplete - the id is simply the feed id whose corresponding
name is in mysql. 

Fugly.

"""


import os
import numpy as N
import array
import datetime
import time

fromdir = '/home/pi/data/phpfina/'

class emoncmsdat():

	def __init__(self,prefix='10'):
           self.prefix = prefix
	   fd = '%s.dat' % self.prefix
	   fm = '%s.meta' % self.prefix
           ffm = open(fm,'rb')
           m = array.array('L')
           m.read(ffm,4)
           metId,metNpoints,metInterval,metStarted = N.array(m,N.uint32)
           print 'file %s: id=%d, npoints=%d, interval=%d, started=%s' % (fm,metId,metNpoints,metInterval,time.ctime(metStarted))
           tstart = time.ctime(int(metStarted))
           ffd = open(fd,'rb').read()
           dN = len(ffd)/4
           d = array.array('f')
           d.fromstring(ffd)
	   self.data = []
           for i,kw in enumerate(d):
               t = metStarted + metInterval*i
               if (kw != kw): # tests for NaN
                 kw = 0
               v = '%d\t%6.1f\t%s' % (t,kw,time.ctime(t))
               self.data.append(v)
           print '# Read %d values from %s, id=%s, at interval %d starting %s' % (dN,fd,metId,metInterval,tstart)

flist = os.listdir(fromdir)
prefs = [x.split('.')[0] for x in flist if ((x.split('.')[1] == 'dat') & ('%s.meta' % x.split('.')[0] in flist))]
dats = []
for prefix in prefs:
    e = emoncmsdat(os.path.join(fromdir,prefix))
    outf = open('%s.xls' % prefix,'w')
    outf.write('traw\tkw\ttime\n')
    outf.write('\n'.join(e.data))
    outf.write('\n')
    outf.close()
    dats.append(e.data)
    # whatever else you need to do...


  


