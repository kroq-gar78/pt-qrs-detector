'''
Created on Jan 27, 2012

@author: sergio
'''
from wfdbtools import rdsamp, rdann, plot_data
import numpy
from buffer import buffer as cola
from pylab import plot, show, subplot, stem, axis
import hrvarray

### Senal
record  = '104'
data, info = rdsamp(record, 100, 225)
ann = rdann(record, 'atr', 100, 225)

time = data[:, 1] #in seconds.
signal1 = data[:, 2]
signal2 = data[:, 3]

ann1 = ann[:, 0]
ann2 = ann[:, 1]

Fs = info['samp_freq']
### Parametros
 
Nwindow = int(0.15 * Fs) # 150ms

###

print len(signal1)

#1/8T(-z^2/32-5z/32-5/8z-7/8z^2-9/8z^3-21/16z^4-21/16z^5-9/8z^6-7/8z^7-5/8z^8-3/8z^9-5/32z^10-1/32z^11+1/z^14+4/z^15+7/z^16+8/z^17+8/z^18+8/z^19+6/z^20-6/z^22-8/z^23-8/z^24-8/z^25-7/z^26-4/z^27-1/z^28+1/32z^30+5/32z^31+3/8z^32+5/8z^33+7/8z^34+9/z^35+21/16z^36+21/16z^37+9/8z^38+7/8z^39+5/8z^40+3/8z^41+5/32z^42+1/32z^43-3/8)


wpk = 0.125

PEAKI = 17000000
SPKI = 0.95*PEAKI
NPKI = 0.7*PEAKI
SPKI = wpk*PEAKI+(1-wpk)*SPKI
NPKI = wpk*PEAKI+(1-wpk)*NPKI

TH1 = NPKI + 0.25*(SPKI-NPKI)
TH2 = 0.5*TH1


umbral =[]

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
    
    umbral.append(TH1)
umbral.pop()
umbral.pop()
### Procesamiento

output = []
window = cola(Nwindow)

i=0

BASE = 0

maximo = BASE
counter = 100
maximos_locales1 = []
posmax = 1
hrv = hrvarray.array()
refractario = 0

for i in range(len(signal1+2)-44):
    ### Filtrado + derivada
    array = buffer.getarray()
#   y = (-buffer.get(45)/32.0-5*buffer.get(44)/32.0-3*buffer.get(43)/8.0-5*buffer.get(42)/8.0-7*buffer.get(41)/8.0-9*buffer.get(40)/8.0-21*buffer.get(39)/16.0-21*buffer.get(38)/16.0-9*buffer.get(37)/8.0-7*buffer.get(36)/8.0-5*buffer.get(35)/8.0-3*buffer.get(34)/8.0-5*buffer.get(33)/32.0-buffer.get(32)/32.0+buffer.get(29)+4*buffer.get(28)+7*buffer.get(27)+8*buffer.get(26)+8*buffer.get(25)+8*buffer.get(24)+6*buffer.get(23)-6*buffer.get(21)-8*buffer.get(20)+8*buffer.get(19)-8*buffer.get(18)-7*buffer.get(17)-4*buffer.get(16)-buffer.get(15)+buffer.get(13)/32.0+5*buffer.get(12)/32.0+3*buffer.get(11)/8.0+5*buffer.get(10)/8.0+7*buffer.get(9)/8.0+9*buffer.get(8)/8.0+21*buffer.get(7)/16.0+21*buffer.get(6)/16.0+9*buffer.get(5)/8.0+7*buffer.get(4)/8.0+5*buffer.get(3)/8.0+3*buffer.get(2)/8.0+5*buffer.get(1)/32.0+buffer.get(0)/32.0)*Fs/(8)
    y = (-array[45]/32.0-5*array[44]/32.0-3*array[43]/8.0-5*array[42]/8.0-7*array[41]/8.0-9*array[40]/8.0-21*array[39]/16.0-21*array[38]/16.0-9*array[37]/8.0-7*array[36]/8.0-5*array[35]/8.0-3*array[34]/8.0-5*array[33]/32.0-array[32]/32.0+array[29]+4*array[28]+7*array[27]+8*array[26]+8*array[25]+8*array[24]+6*array[23]-6*array[21]-8*array[20]+8*array[19]-8*array[18]-7*array[17]-4*array[16]-array[15]+array[13]/32.0+5*array[12]/32.0+3*array[11]/8.0+5*array[10]/8.0+7*array[9]/8.0+9*array[8]/8.0+21*array[7]/16.0+21*array[6]/16.0+9*array[5]/8.0+7*array[4]/8.0+5*array[3]/8.0+3*array[2]/8.0+5*array[1]/32.0+array[0]/32.0)*Fs/(8)    

    ### cuadrado de la senial
    window.append(y*y)
    
    ### Integrado
    acum = window.sum()
    
    output.append(acum)
    
    if acum > maximo:
        maximo = acum
        posmax = i + 18
        counter = 100
    else:
        counter-=1
        
    if counter == 0:
        if maximo > TH1:
            maximos_locales1.append(posmax)
            hrv.append(posmax)
            refractario = int(hrv.rrav()/4)
            PEAKI = maximo
            SPKI = wpk*PEAKI+(1-wpk)*SPKI
        else:
            PEAKI = maximo
            NPKI = wpk*PEAKI+(1-wpk)*NPKI
                
        counter = 100
        maximo = BASE
        TH1 = NPKI + 0.25*(SPKI-NPKI) #Actualizo umbral
    
    umbral.append(TH1)
    
    sample = signal.pop()
    buffer.append(sample)

output = list(numpy.zeros(44)) + output

#print hrv.getarray()

###########
y5 = output

y6 = list(numpy.diff(y5)) + [0]

y5 = list(y5[(Nwindow/2-1):len(y5)]) + list(numpy.zeros((Nwindow/2-1)))

signaly = y5

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

#print maximos_locales
print "maximos locales "
print maximos_locales1

marcas = numpy.zeros(len(signaly))
for i in maximos_locales1:
    marcas[i]=30000000

##########

subplot(211)
plot(time, signal1, 'k')
axis([100, 225, -2, 2])

subplot(212)
plot(time,umbral,'r')
plot(time, marcas, 'o')
plot(time, signaly, 'k')
axis([100, 225, 0, 80000000])
show()