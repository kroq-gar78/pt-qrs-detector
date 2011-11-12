#!/usr/bin/env python
from wfdbtools import rdsamp, rdann, plot_data
from pprint import pprint
import pylab

record  = '100'
data, info = rdsamp(record, 0, 10)
#print data.shape
pprint(info)
ann = rdann(record, 'atr', 0, 10)
#print(ann[:4,:])
#plot_data(data, info, ann)
#print data
time = data[:, 1] #in seconds. use data[:, 0] to use sample no.
sig1 = data[:, 2]
sig2 = data[:, 3]
#pylab.plot(time,sig2)
#pylab.show()
ann_x = ann[:, 0]
pylab.plot(ann[:, 1], data[ann, 3])
pylab.show()
