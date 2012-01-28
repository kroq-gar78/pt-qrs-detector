'''
Created on Jan 27, 2012

@author: sergio
'''
#!/usr/bin/env python
from wfdbtools import rdsamp, rdann, plot_data
from pprint import pprint
import pylab
from scipy import signal
import numpy

###Senal
record  = '104'
data, info = rdsamp(record, 301, 320)
ann = rdann(record, 'atr', 301, 320)

time = data[:, 1] #in seconds.
sig1 = data[:, 2]
sig2 = data[:, 3]

ann1 = ann[:, 0]
ann2 = ann[:, 1]

Fs = info['samp_freq']

######################
# FILTER
# a[0]*y[n] = b[0]*x[n] + b[1]*x[n-1] + ... + b[nb]*x[n-nb]
#                         - a[1]*y[n-1] - ... - a[na]*y[n-na]

### low-pass filter
a = [1,-2,1]
b = [1,0,0,0,0,0,-2,0,0,0,0,0,1]
y1 = signal.lfilter(b,a,sig1)


### high-pass filter
a = [1,-1]
b = [-1.0/32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1.0/32]
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
Nwindow = int(0.15 * Fs) # window of 150 ms

y5 = []
for i in range(0,Nwindow):
    acum = 0
    for j in range(0,i):
        acum = acum + y4[j]
    if acum < 80:
        y5.append(0)
    else:
        y5.append(acum)

for i in range(Nwindow,len(y4)):
    acum = acum + y4[i]-y4[i-Nwindow]
    if acum < 40:
        y5.append(0)
    else:
        y5.append(acum)

y6 = list(numpy.diff(y5)) + [0]

y5 = list(y5[(Nwindow/2-1):len(y5)]) + list(signal.zeros((Nwindow/2-1)))

signaly = y5
wpk = 0.125

PEAKI = 1
SPKI = 0.89
NPKI = 0.42
SPKI = wpk*PEAKI+(1-wpk)*SPKI
NPKI = wpk*PEAKI+(1-wpk)*NPKI

TH1 = NPKI + 0.25*(SPKI-NPKI)
TH2 = 0.5*TH1

i=0
maximo = 0
counter = 200
maximos_locales = []
while(i < len(signaly)):
    if signaly[i] > signaly[maximo]:
        maximo = i
        counter = 200
    else:
        counter-=1
    if counter == 0 :
        maximos_locales.append(maximo)
        counter = 200
        if (i + 300) < len(signaly):
            maximo = i+300
    i+=1

print maximos_locales


marcas = signal.zeros(len(signaly))
for i in maximos_locales:
    marcas[i]=95

pylab.subplot(211)
pylab.plot(time, y1, 'k')

pylab.subplot(212)
pylab.plot(time, marcas, 'o')
pylab.plot(time, signaly, 'k')

#pylab.subplot(411)
#pylab.plot(time, y1, 'k')
#pylab.axis([1.6, 2, -1, 1])

#pylab.subplot(412)
#pylab.subplot(411)
#pylab.plot(time, y2, 'k')
#pylab.axis([1.6, 2., -1, 1])

#pylab.subplot(413)
#pylab.subplot(312)
#pylab.plot(time, y6, 'k')
#pylab.axis([1.6, 2, 0, 1])

#pylab.subplot(414)
#pylab.subplot(313)
#pylab.plot(time, signal, 'k')
#pylab.axis([1.6, 2, 0, 0.8])

pylab.show()