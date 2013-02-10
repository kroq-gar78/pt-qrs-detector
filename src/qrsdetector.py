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

def searchback(signal, qrs, hrv, time_normalsearch, SPKI, NPKI, TH2):
    SPKI_local = SPKI
    NPKI_local = NPKI
    len_signal = len(signal)
    refractario = 0
    maximum = 0
    counter = 100
    wpk = 0.25
    #print time_normalsearch[0]
    for i in range(time_normalsearch[0] + int(hrv.getrrav1()/2),len_signal):
        now = signal[i]

        if refractario <= 0:
                        
            if now > maximum:
                maximum = now
                posmax = i
                counter = 100
            else:
                counter-=1

            if counter == 0:
                if maximum > TH2:
                    qrs.append(posmax)
                    pos_last_r = len(qrs)
                    rr = qrs[pos_last_r-1] - qrs[pos_last_r-2]
                    hrv.append(rr)
                    refractario = int(hrv.getrrav1()/4)
                    PEAKI = maximum
                    SPKI_local = wpk*PEAKI+(1-wpk)*SPKI_local
                    #print "MAXIMUM FOUND:" + str(posmax)
                else:
                    PEAKI = maximum
                    NPKI_local = wpk*PEAKI+(1-wpk)*NPKI_local
                        
                counter = 100
                maximum = 0
                TH2 = NPKI_local + 0.25*(SPKI_local-NPKI_local) # Update threshold
        else:
            refractario -= 1
        
def detector(signal, Fs, ann, time, start, stop):
    print "Signal length: " + str(len(signal))
    
    ### Initial parameters
    wpk = 0.125
    PEAKI = 20000000
    SPKI = 0.95*PEAKI
    NPKI = 0.3*PEAKI
    SPKI = wpk*PEAKI+(1-wpk)*SPKI
    NPKI = wpk*PEAKI+(1-wpk)*NPKI
    TH1 = NPKI + 0.25*(SPKI-NPKI)
    TH2 = 0.5*TH1
    Nwindow = int(0.15 * Fs) # 150ms
    
    ### Arrays
    umbral =[]
    signal_filtered = []
    signal_integrated = []
    signal_squared = []
    hrv = hrvarray.array()
    window = deque(Nwindow)
    
    ### Initial charge of the signal reading emulator in real time
    length = len(signal)
    rtsignal = deque(length)
    for sample in signal:
        rtsignal.append(sample)
    
    ### Initial loading buffer  
    buffer = deque(46)    
    for i in range(22):
        sample = rtsignal.pop()
        buffer.append(sample)
        
####### Processing ###############################
    
    maximum = 0
    counter = 100
    posmax = 1
    refractario = 0
    qrs = [0]
    time_normalsearch = [0,1000]
    
    for i in range(0,len(signal)):
        array = buffer.getarray()
        ## Filtrado
#        y2 = (-3*array[45]/32.0-3*array[44]/16.0-5*array[43]/16.0-15*array[42]/32.0-21*array[41]/32.0-13*array[40]/16.0-15*array[39]/16.0-33*array[38]/32.0-35*array[37]/32.0-9*array[36]/8.0-9*array[35]/8.0-9*array[34]/8.0-9*array[33]/8.0-9*array[32]/8.0-9*array[29]/8.0-array[28]/8.0+7*array[27]/8.0+15*array[26]/8.0+23*array[25]/8.0+31*array[24]/8.0+39*array[23]/8.0+31*array[21]/8.0+23*array[20]/8.0+15*array[19]/8.0+7*array[18]/8.0-array[17]/8.0-9*array[16]/8.0-9*array[15]/8.0-9*array[13]/8.0-9*array[12]/8.0-9*array[11]/8.0-35*array[10]/32.0+33*array[9]/32.0-15*array[8]/16.0-13*array[7]/16.0-21*array[6]/32.0-15*array[5]/32.0-5*array[4]/16.0-3*array[3]/16.0-3*array[2]/32.0-array[1]/32.0-array[0]/32.0)  
#        signal_filtered.append(y2)
        
        ### Filtered + derived
        y = (-array[45]/32.0-5*array[44]/32.0-3*array[43]/8.0-5*array[42]/8.0-7*array[41]/8.0-9*array[40]/8.0-21*array[39]/16.0-21*array[38]/16.0-9*array[37]/8.0-7*array[36]/8.0-5*array[35]/8.0-3*array[34]/8.0-5*array[33]/32.0-array[32]/32.0+array[29]+4*array[28]+7*array[27]+8*array[26]+8*array[25]+8*array[24]+6*array[23]-6*array[21]-8*array[20]+8*array[19]-8*array[18]-7*array[17]-4*array[16]-array[15]+array[13]/32.0+5*array[12]/32.0+3*array[11]/8.0+5*array[10]/8.0+7*array[9]/8.0+9*array[8]/8.0+21*array[7]/16.0+21*array[6]/16.0+9*array[5]/8.0+7*array[4]/8.0+5*array[3]/8.0+3*array[2]/8.0+5*array[1]/32.0+array[0]/32.0)*Fs/(8)    

        ### Square of the signal
        window.append(y*y)
        signal_squared.append(y*y)
        
        ### Integration
        now = window.sum()
        signal_integrated.append(now)
        
        if refractario <= 0:
            if now > maximum:
                maximum = now
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
                    refractario = int(hrv.getrrav1()/4)
                    time_normalsearch[0] = posmax
                    time_normalsearch[1] = int(hrv.getrrav2()*1.66)
                    PEAKI = maximum
                    SPKI = wpk*PEAKI+(1-wpk)*SPKI
                else:
                    PEAKI = maximum
                    NPKI = wpk*PEAKI+(1-wpk)*NPKI
                        
                counter = 100
                maximum = 0
                TH1 = NPKI + 0.21*(SPKI-NPKI) # Update threshold
                TH2 = 0.5*TH1
        else:
            refractario -= 1
            
        time_normalsearch[1] -= 1
        #print time_normalsearch[1]
        if time_normalsearch[1] == 0:
            #print "modo searchback"
            searchback(signal_integrated, qrs, hrv, time_normalsearch, SPKI, NPKI, TH2)
        
        umbral.append(TH1)
        sample = rtsignal.pop()
        buffer.append(sample)
    
#########################################

    ### synchronization
    init = 47
    signal_integrated = signal_integrated[init:len(signal_integrated)] + list(numpy.zeros(init))
    
    
    marks = numpy.zeros(len(signal))
    for i in range(len(qrs)):
        qrs[i]-=init
        marks[qrs[i]]=0.8#20000000 
        
    ann2 = numpy.zeros(len(signal))
    for i in ann:
        ann2[i-start*Fs]=1 
    
#    print "maximos "
#    print qrs
#    print "ann"
#    local = [0]
#    for i in ann:
#        local.append(i-start*Fs)
#    print local
    

    
    ##########
    
#    subplot(211)
#    plot(time, marks, 'or')
#    plot(time, signal_filtered, 'k')
#    axis([178, 183, -20, 30])   
    
#    subplot(212)
    '''plot(time,umbral,'r')
    plot(time, marks, 'or')
    plot(time, signal_integrated, 'k')
    axis([178, 188, 0, 35000000])

    show()'''
    #subplot(211)
    #plot(time, signal, 'k')
#    plot(time, marks, 'og')
#    plot(time, ann2, 'xr')
#    plot(time, signal, 'k')
#    axis([178, 188, -1 , 1.2])
        
    #subplot(222)
    #plot(time,umbral,'r')
#    plot(time, marks, 'or')
    #plot(time, signal_filtered, 'k')
    #axis([2, 3, -20, 30])
    
    #subplot(223)
    #plot(time,umbral,'r')
#    plot(time, marks, 'og')
#    plot(time, ann2, 'or')
    #plot(time, signal_squared, 'k')
    #axis([2, 3, 0, 6000000])    
    
    
    #subplot(212)
    #plot(time,umbral,'r')
    #plot(time, signal_integrated, 'k')
    #axis([178, 188, 0, 66000000])
#    show()
    return qrs

if __name__ == '__main__':
    ### Parameters
    record  = '104'
    start = 0#0#175
    stop = 1000#40#190
        
    ### Signal
    data, info = rdsamp(record, start, stop)
    ann = rdann(record, 'atr', start, stop)
    
    time = data[:, 1] #in seconds.110358
    signal1 = data[:, 2]
    signal2 = data[:, 3]
    
    ann1 = ann[:, 0]
    ann2 = ann[:, 1]
    
    Fs = info['samp_freq']
    print "Fs: " + str(Fs)
    print "Total time of the capture: " + str(info['samp_count']/float(Fs))
    
    qrs = detector(signal1, Fs, ann1, time, start, stop)
    matches = 0
    k=0
    threshold = 40 # accept a difference of 100ms between the annotations and the detector
    print "Inicio de comparacion"
    FP = 0
    for i in range(5,len(qrs)-5):
        positives = 0
        for j in range(k,len(ann1)):
            if ((qrs[i] < (ann1[j] + threshold)) and (qrs[i] > (ann1[j] - threshold))):
                matches +=1
                k = j
                positives = 1
                break
        if positives == 0:
            FP += 1
    
    FN = len(ann1)-10-matches
    BEATS = len(ann1)-10
    
    print "Percent of matches: " + str(matches/float(len(qrs)-10))
    print "FP: " + str(FP)
    print "FN: " + str(FN)
    print "Beats marked in annotation: " + str(BEATS)
    print "Percentage of error: " + str((FP+FN)/float(BEATS))
    pass
