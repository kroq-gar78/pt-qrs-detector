'''
Created on Feb 15, 2012

@author: sergio
'''
from wfdbtools import rdsamp, rdann, plot_data
import numpy
from buffer import buffer as cola
from pylab import plot, show, subplot, stem

### Senal
record  = '104'
data, info = rdsamp(record, 201, 520)
ann = rdann(record, 'atr', 201, 520)

time = data[:, 1] #in seconds.
signal1 = data[:, 2]
signal2 = data[:, 3]

plot(time,signal1)
show()