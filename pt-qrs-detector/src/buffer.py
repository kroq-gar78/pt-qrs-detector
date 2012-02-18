'''
Created on Jan 27, 2012
@author: Sergio
'''
from collections import deque as originaldeque
import numpy

class deque(originaldeque):
    '''
    Buffer de longitud fija. Inicialmente lleno de 0.0
    '''
    def __init__(self,length):
        '''
        Constructor
        '''
        self.len = length
        self.buffer = originaldeque(numpy.zeros(length))
        
    def append(self,elemento):
        self.buffer.append(elemento)
        return self.buffer.popleft()
    
    def pop(self,elemento=0.0):
        self.buffer.append(elemento)
        return self.buffer.popleft()
    
    def len(self):
        return self.length
    
    def purge(self):
        array = numpy.array(self.buffer)
        self.buffer = originaldeque(numpy.zeros(self.length))
        return array
    
    def get(self,position):
        array = numpy.array(self.buffer)
        return array[position]
    
    def sum(self):
        array = numpy.array(self.buffer)
        return array.sum()
    
    def getarray(self):
        array = numpy.array(self.buffer)
        return array