'''
Created on Jan 27, 2012

@author: sergio
'''
from wfdbtools import rdsamp, rdann, plot_data
from pprint import pprint
import pylab
from scipy import signal
import numpy
from collections import deque

###Senal
record  = '104'
data, info = rdsamp(record, 301, 320)
ann = rdann(record, 'atr', 301, 320)

time = data[:, 1] #in seconds.
signal1 = data[:, 2]
signal2 = data[:, 3]

ann1 = ann[:, 0]
ann2 = ann[:, 1]

Fs = info['samp_freq']
#1/8T(-z^2/32-5z/32-5/8z-7/8z^2-9/8z^3-21/16z^4-21/16z^5-9/8z^6-7/8z^7-5/8z^8-3/8z^9-5/32z^10-1/32z^11+1/z^14+4/z^15+7/z^16+8/z^17+8/z^18+8/z^19+6/z^20-6/z^22-8/z^23-8/z^24-8/z^25-7/z^26-4/z^27-1/z^28+1/32z^30+5/32z^31+3/8z^32+5/8z^33+7/8z^34+9/z^35+21/16z^36+21/16z^37+9/8z^38+7/8z^39+5/8z^40+3/8z^41+5/32z^42+1/32z^43-3/8)



