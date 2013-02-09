'''
Created on Jan 27, 2012

@author: sergio
'''
from wfdbtools import rdsamp, rdann
import numpy
from buffer import buffer as cola
from pylab import plot, show, subplot, stem, axis
import hrvarray
import time as timer

### Senal
record  = '104'
start = 210
stop = 320
data, info = rdsamp(record, start, stop)
ann = rdann(record, 'atr', start, stop)

time = data[:, 1] #in seconds.
signal1 = data[:, 2]
signal2 = data[:, 3]

ann1 = ann[:, 0]
ann2 = ann[:, 1]

Fs = info['samp_freq']
### Parametros
 
Nwindow = int(0.15 * Fs) # 150ms

###

print "longitud de la senal: " + str(len(signal1))

wpk = 0.175

PEAKI = 17000000
SPKI = 0.95*PEAKI
NPKI = 0.3*PEAKI
SPKI = wpk*PEAKI+(1-wpk)*SPKI
NPKI = wpk*PEAKI+(1-wpk)*NPKI

TH1 = NPKI + 0.21*(SPKI-NPKI)
TH2 = 0.5*TH1


umbral =[]
wintegrate = list(numpy.zeros(0))
output = list(numpy.zeros(0))
output2 = list(numpy.zeros(0))
hrv = hrvarray.array()

### Carga inicial de la senal a un emulador de lectura en tiempo real
length = len(signal1)
signal = cola(length)
for sample in signal1:
    signal.append(sample)

### Carga inicial del buffer  
buffer = cola(46)    
for i in range(46):
    sample = signal.pop()
    buffer.append(sample)
    
### Procesamiento

output = []
window = cola(Nwindow)

i=0

BASE = 0

maximo = BASE
counter = 100
maximos_locales1 = [0]
posmax = 1

refractario = 0


t0 = timer.clock()
for i in range(0,len(signal1)):
    ### Filtrado + derivada
    array = buffer.getarray()
#   y = (-buffer.get(45)/32.0-5*buffer.get(44)/32.0-3*buffer.get(43)/8.0-5*buffer.get(42)/8.0-7*buffer.get(41)/8.0-9*buffer.get(40)/8.0-21*buffer.get(39)/16.0-21*buffer.get(38)/16.0-9*buffer.get(37)/8.0-7*buffer.get(36)/8.0-5*buffer.get(35)/8.0-3*buffer.get(34)/8.0-5*buffer.get(33)/32.0-buffer.get(32)/32.0+buffer.get(29)+4*buffer.get(28)+7*buffer.get(27)+8*buffer.get(26)+8*buffer.get(25)+8*buffer.get(24)+6*buffer.get(23)-6*buffer.get(21)-8*buffer.get(20)+8*buffer.get(19)-8*buffer.get(18)-7*buffer.get(17)-4*buffer.get(16)-buffer.get(15)+buffer.get(13)/32.0+5*buffer.get(12)/32.0+3*buffer.get(11)/8.0+5*buffer.get(10)/8.0+7*buffer.get(9)/8.0+9*buffer.get(8)/8.0+21*buffer.get(7)/16.0+21*buffer.get(6)/16.0+9*buffer.get(5)/8.0+7*buffer.get(4)/8.0+5*buffer.get(3)/8.0+3*buffer.get(2)/8.0+5*buffer.get(1)/32.0+buffer.get(0)/32.0)*Fs/(8)
    y = (-array[45]/32.0-5*array[44]/32.0-3*array[43]/8.0-5*array[42]/8.0-7*array[41]/8.0-9*array[40]/8.0-21*array[39]/16.0-21*array[38]/16.0-9*array[37]/8.0-7*array[36]/8.0-5*array[35]/8.0-3*array[34]/8.0-5*array[33]/32.0-array[32]/32.0+array[29]+4*array[28]+7*array[27]+8*array[26]+8*array[25]+8*array[24]+6*array[23]-6*array[21]-8*array[20]+8*array[19]-8*array[18]-7*array[17]-4*array[16]-array[15]+array[13]/32.0+5*array[12]/32.0+3*array[11]/8.0+5*array[10]/8.0+7*array[9]/8.0+9*array[8]/8.0+21*array[7]/16.0+21*array[6]/16.0+9*array[5]/8.0+7*array[4]/8.0+5*array[3]/8.0+3*array[2]/8.0+5*array[1]/32.0+array[0]/32.0)*Fs/(8)    
    y2 = (-3*array[45]/32.0-3*array[44]/16.0-5*array[43]/16.0-15*array[42]/32.0-21*array[41]/32.0-13*array[40]/16.0-15*array[39]/16.0-33*array[38]/32.0-35*array[37]/32.0-9*array[36]/8.0-9*array[35]/8.0-9*array[34]/8.0-9*array[33]/8.0-9*array[32]/8.0-9*array[29]/8.0-array[28]/8.0+7*array[27]/8.0+15*array[26]/8.0+23*array[25]/8.0+31*array[24]/8.0+39*array[23]/8.0+31*array[21]/8.0+23*array[20]/8.0+15*array[19]/8.0+7*array[18]/8.0-array[17]/8.0-9*array[16]/8.0-9*array[15]/8.0-9*array[13]/8.0-9*array[12]/8.0-9*array[11]/8.0-35*array[10]/32.0+33*array[9]/32.0-15*array[8]/16.0-13*array[7]/16.0-21*array[6]/32.0-15*array[5]/32.0-5*array[4]/16.0-3*array[3]/16.0-3*array[2]/32.0-array[1]/32.0-array[0]/32.0)  

    ### cuadrado de la senial
    window.append(y*y)
    
    wintegrate.append(y*y)
    
    ### Integrado
    acum = window.sum()
    
    output.append(acum)
    output2.append(y2)
    
    if refractario == 0:
        if acum > maximo:
            maximo = acum
            posmax = i
            counter = 100
        else:
            counter-=1
            
        if counter == 0:
            if maximo > TH1:
                maximos_locales1.append(posmax)
                pos_last_r = len(maximos_locales1)
                rr = maximos_locales1[pos_last_r-1] - maximos_locales1[pos_last_r-2]
                hrv.append(rr)
                refractario = int(hrv.rrav()/4)
                PEAKI = maximo
                SPKI = wpk*PEAKI+(1-wpk)*SPKI
            else:
                PEAKI = maximo
                NPKI = wpk*PEAKI+(1-wpk)*NPKI
                    
            counter = 100
            maximo = BASE
            TH1 = NPKI + 0.25*(SPKI-NPKI) #Actualizo umbral
    else:
        refractario -= 1
    
    umbral.append(TH1)
    
    sample = signal.pop()
    buffer.append(sample)

t = timer.clock() - t0

print "tiempo: "  + str(t)

output = output
print len(umbral)
print "output " + str(len(output))
###########

marcas = numpy.zeros(len(signal1))
for i in maximos_locales1:
    marcas[i]=3000000 

print "maximos "
print maximos_locales1
print "ann"
local = [0]
for i in ann1:
    local.append(i-start*Fs)
print local

##########

subplot(211)
#plot(time, signal1, 'k')
plot(time, output2, 'k')
#axis([316, stop, -2, 2])

subplot(212)
#plot(time,umbral,'r')
#plot(time, marcas, 'o')
plot(time, signal1, 'k')
#axis([316, stop, 0, 8000000])
show()