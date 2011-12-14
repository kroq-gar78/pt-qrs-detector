#!/usr/bin/env python
from wfdbtools import rdsamp, rdann, plot_data
from pprint import pprint
import pylab
from scipy import signal
import numpy

###Senal
record  = '100'
data, info = rdsamp(record, 0, 10)
ann = rdann(record, 'atr', 0, 10)

time = data[:, 1] #in seconds.
sig1 = data[:, 2]
sig2 = data[:, 3]

ann1 = ann[:, 0]
ann2 = ann[:, 1]



######################
# FILTER
# a[0]*y[n] = b[0]*x[n] + b[1]*x[n-1] + ... + b[nb]*x[n-nb]
#                         - a[1]*y[n-1] - ... - a[na]*y[n-na]

### low-pass filter
a = [1,-2,1]
b = [1,0,0,0,0,0,-2,0,0,0,0,0,1]
y1 = signal.lfilter(b,a,sig1)


### high-pass filter
a = [1,1]
b = [-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
y2 = signal.lfilter(b,a,y1)


y2 = list(y2[20:len(y2)]) + list(signal.zeros(5)) + list(signal.zeros(15))



######################
# DERIVATE

y3 = []
for i in range(3,len(y2)-2):
    y3.append((-y2[i-2]-2*y2[i-1]+2*y2[i+1]+y2[i+2])/8.0)
y3 = [0,0,0] + y3 + [0,0]

######################
# Squaring
y4 = []
for i in y3:
    y4.append(i*i)


######################
# Moving Windows Integration
Nwindow = 34

y5 = []
for i in range(0,Nwindow):
    acum = 0
    for j in range(0,i):
        acum = acum + y4[j]
    y5.append(acum)

for i in range(Nwindow,len(y4)):
    acum = acum + y4[i]-y4[i-Nwindow]
    y5.append(acum)

y5 = list(y5/numpy.max(y5))
print type(y5)

#pylab.subplot(211)
#pylab.stem(time, sig1, 'k')
#pylab.axis([0, 0.4, -1.5, 1.5])

pylab.subplot(311)
pylab.stem(time, y2, 'k')
pylab.axis([0, 0.7, -400, 400])

pylab.subplot(312)
pylab.stem(time, y3, 'k')
pylab.axis([0, 0.7, -100, 100])

pylab.subplot(313)
pylab.stem(time, y5, 'k')
pylab.axis([0, 0.7, 0, 1])

pylab.show()

