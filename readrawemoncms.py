"""
Python 2.7.3 (default, Mar 18 2014, 05:13:23) 
[GCC 4.6.3] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import numpy as N
>>> import array
>>> f = open('10.dat','rb')
>>> binv = array.array('f')
>>> binv.read(f,100)
>>> N.array(binv,N.float)
array([ 5744.,  5740.,  5731.,  5723.,  5632.,  5684.,  5646.,  5733.,
        5671.,  5631.,  5669.,  5662.,  5670.,  5673.,  5680.,  5660.,
        5669.,  5697.,  5654.,  5720.,  5633.,  5627.,  5642.,  5614.,
        5625.,  5641.,  5629.,  5663.,  5727.,  5716.,  5754.,  5721.,
        5691.,  5715.,  5725.,  5704.,  5694.,  5708.,  5688.,  5684.,
        5718.,  5702.,  5705.,  5729.,  5706.,  5740.,  5770.,  5721.,
        5790.,  5746.,  5724.,  5713.,  5723.,  5699.,  5701.,  5709.,
        5686.,  5772.,  5699.,  5685.,  5682.,  5725.,  5738.,  5731.,
        5761.,  5698.,  5711.,  5695.,  5684.,  5718.,  5700.,  5709.,
        5705.,  5716.,  5669.,  5702.,  5691.,  5695.,  5717.,  5715.,
        5734.,  5726.,  5736.,  5709.,  5712.,  5696.,  5736.,  5749.,
        5708.,  5699.,  5630.,  5699.,  5784.,  5679.,  5725.,  5691.,
        5638.,  5743.,  5682.,  5700.])

"""

# read 4 byte float data and metadata for a php emoncms data file
# ross feb 22 2016

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



  


