'''
Created on Feb 15, 2012

@author: sergio
'''

from buffer import deque

class array:
    '''
    classdocs
    '''
    def append(self,r):
        self.array.append(r)
        self.len += 1
        self.rrav1 = self.__avlast8__(self.array)
        
        rrlow = 0.92 * self.rrav1
        rrhigh = 1.16 * self.rrav1
        
        if (r > rrlow) and (r < rrhigh):
            self.rrnormalized.append(r)
        
        self.rrav2 = self.__avlast8__(self.rrnormalized)        
        
    def __avlast8__(self, array):
        len_array = len(array) - 1
        if len_array < 8:
            count = len_array
        else:
            count = 8
        sum = 0
        for i in range(count):
            sum += array[len_array-i]
        return (float(sum)/count)
    
    def getrrav1(self):
        return self.rrav1
    
    def getrrav2(self):
        return self.rrav2
    
    def getarray(self):
        return self.array

    def __init__(self):
        '''
        Constructor
        '''
        self.len = 0
        self.array = [0]
        self.rrav1 = 0
        self.rrnormalized = [0]
        self.rrav2 = 0