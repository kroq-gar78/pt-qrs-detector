'''
Created on Feb 17, 2012

@author: sergio
'''
from wfdbtools import rdsamp, rdann
import numpy
from buffer import deque
from pylab import plot, show, subplot, stem, axis
import hrvarray
import time as timer

def detector(signal, Fs, ann, time, start, stop):
    print "Signal length: " + str(len(signal))
    
    ### Parametros iniciales
    wpk = 0.175
    PEAKI = 17000000
    SPKI = 0.95*PEAKI
    NPKI = 0.3*PEAKI
    SPKI = wpk*PEAKI+(1-wpk)*SPKI
    NPKI = wpk*PEAKI+(1-wpk)*NPKI
    TH1 = NPKI + 0.21*(SPKI-NPKI)
    TH2 = 0.5*TH1
    Nwindow = int(0.15 * Fs) # 150ms
    
    ### Arrays
    umbral =[]
    signal_filtered = []
    signal_integrated = []
    signal_squared = []
    hrv = hrvarray.array()
    window = deque(Nwindow)
    
    ### Carga inicial de la senal a un emulador de lectura en tiempo real
    length = len(signal)
    rtsignal = deque(length)
    for sample in signal:
        rtsignal.append(sample)
    
    ### Carga inicial del buffer  
    buffer = deque(46)    
    for i in range(23):
        sample = rtsignal.pop()
        buffer.append(sample)
        
    ### Procesamiento
    
    maximum = 0
    counter = 100
    qrs = [0]
    posmax = 1
    
    refractario = 0
    
    buffer = deque(46)
    t0 = timer.clock()
    for i in range(0,len(signal)):
        array = buffer.getarray()
        ## Filtrado
        y2 = (-3*array[45]/32.0-3*array[44]/16.0-5*array[43]/16.0-15*array[42]/32.0-21*array[41]/32.0-13*array[40]/16.0-15*array[39]/16.0-33*array[38]/32.0-35*array[37]/32.0-9*array[36]/8.0-9*array[35]/8.0-9*array[34]/8.0-9*array[33]/8.0-9*array[32]/8.0-9*array[29]/8.0-array[28]/8.0+7*array[27]/8.0+15*array[26]/8.0+23*array[25]/8.0+31*array[24]/8.0+39*array[23]/8.0+31*array[21]/8.0+23*array[20]/8.0+15*array[19]/8.0+7*array[18]/8.0-array[17]/8.0-9*array[16]/8.0-9*array[15]/8.0-9*array[13]/8.0-9*array[12]/8.0-9*array[11]/8.0-35*array[10]/32.0+33*array[9]/32.0-15*array[8]/16.0-13*array[7]/16.0-21*array[6]/32.0-15*array[5]/32.0-5*array[4]/16.0-3*array[3]/16.0-3*array[2]/32.0-array[1]/32.0-array[0]/32.0)  
        signal_filtered.append(y2)
        
        ### Filtrado + derivada
        y = (-array[45]/32.0-5*array[44]/32.0-3*array[43]/8.0-5*array[42]/8.0-7*array[41]/8.0-9*array[40]/8.0-21*array[39]/16.0-21*array[38]/16.0-9*array[37]/8.0-7*array[36]/8.0-5*array[35]/8.0-3*array[34]/8.0-5*array[33]/32.0-array[32]/32.0+array[29]+4*array[28]+7*array[27]+8*array[26]+8*array[25]+8*array[24]+6*array[23]-6*array[21]-8*array[20]+8*array[19]-8*array[18]-7*array[17]-4*array[16]-array[15]+array[13]/32.0+5*array[12]/32.0+3*array[11]/8.0+5*array[10]/8.0+7*array[9]/8.0+9*array[8]/8.0+21*array[7]/16.0+21*array[6]/16.0+9*array[5]/8.0+7*array[4]/8.0+5*array[3]/8.0+3*array[2]/8.0+5*array[1]/32.0+array[0]/32.0)*Fs/(8)    

        ### cuadrado de la senial
        window.append(y*y)
        signal_squared.append(y*y)
        
        ### Integrado
        acum = window.sum()
        signal_integrated.append(acum)
        
        if refractario == 0:
            if acum > max:
                maximum = acum
                posmax = i
                counter = 100
            else:
                counter-=1
                
            if counter == 0:
                if maximum > TH1:
                    qrs.append(posmax)
                    pos_last_r = len(qrs)
                    rr = qrs[pos_last_r-1] - qrs[pos_last_r-2]
                    hrv.append(rr)
                    refractario = int(hrv.rrav()/4)
                    PEAKI = maximum
                    SPKI = wpk*PEAKI+(1-wpk)*SPKI
                else:
                    PEAKI = maximum
                    NPKI = wpk*PEAKI+(1-wpk)*NPKI
                        
                counter = 100
                maximum = 0
                TH1 = NPKI + 0.25*(SPKI-NPKI) #Actualizo umbral
        else:
            refractario -= 1
        
        umbral.append(TH1)
        sample = rtsignal.pop()
        buffer.append(sample)
    
    t = timer.clock() - t0
    
    print "tiempo: "  + str(t)
    
    ###########    
    marcas = numpy.zeros(len(signal))
    for i in qrs:
        marcas[i]=3000000 
    
    print "maximos "
    print qrs
    print "ann"
    local = [0]
    for i in ann:
        local.append(i-start*Fs)
    print local
    
    ##########
    
    subplot(211)
    #plot(time, signal, 'k')
    plot(time, signal_filtered, 'k')
    #axis([316, stop, -2, 2])
    
    subplot(212)
    #plot(time,umbral,'r')
    #plot(time, marcas, 'o')
    plot(time, signal, 'k')
    #axis([316, stop, 0, 8000000])
    show()
    

if __name__ == '__main__':
    ### Parametros
    record  = '104'
    start = 10
    stop = 15
        
    ### Senal
    data, info = rdsamp(record, start, stop)
    ann = rdann(record, 'atr', start, stop)
    
    time = data[:, 1] #in seconds.
    signal1 = data[:, 2]
    signal2 = data[:, 3]
    
    ann1 = ann[:, 0]
    ann2 = ann[:, 1]
    
    Fs = info['samp_freq']

    
    detector(signal1, Fs, ann1, time, start, stop)
    
    pass