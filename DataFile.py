from itertools import count
import numpy as np
import pandas as pd


class DataFile(object):
    def __init__(self, filename, resolution):
        self.filename = filename
        self.file = open(self.filename, "r")
        self.resolution = resolution
        self.values = []
        self.time = []
 
    def LoadValues(self, start, stop):
        count = 0
        for line in self.file:
            if start <= count and count <= stop:
                values = line.split()
                self.values.append(int(values[1]))
            count = count + 1
#        self.time = np.linspace(0, self.resolution * len(self.values), num=self.resolution)
        self.time = np.arange(0, self.resolution * len(self.values), self.resolution)
        #data ={ "rownr" : self.values, "events" : self.values }
        #data ={ "events" : self.values }
        #self.dataframe = pd.DataFrame(data)


    def Length(self):
        return len(self.values)

    def Mean(self):
        return np.mean(self.values)

    def StandardDeviation(self):
        return np.std(self.values)
    
