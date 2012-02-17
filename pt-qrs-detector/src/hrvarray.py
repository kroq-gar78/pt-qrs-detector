'''
Created on Feb 15, 2012

@author: sergio
'''

class array:
    '''
    classdocs
    '''
    def append(self,r):
        self.array.append(r)
        self.len += 1
        
    def rrav(self):
        if self.len < 8:
            count = self.len
        else:
            count = 8
        sum = 0
        for i in range(count):
            sum += self.array[self.len-i]
        
        return (float(sum)/count)
    
    def getarray(self):
        return self.array

    def __init__(self):
        '''
        Constructor
        '''
        self.len = 0
        self.array = [0]