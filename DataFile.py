import numpy as np


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
        self.time = np.arange(0, self.resolution * len(self.values), self.resolution)


    def Length(self):
        return len(self.values)

    def Mean(self):
        return np.mean(self.values)

    def StandardDeviation(self):
        return np.std(self.values)
    
    def MergeBuckets(self, mergeCount):
        temp = []
        i = 0
        counter = 0
        for value in self.values:
            counter = counter + value
            i = i + 1
            if i == mergeCount:
                temp.append(counter)
                i = 0
                counter = 0

        self.resolution = int(mergeCount * self.resolution)
        self.values = temp
        self.time = np.linspace(start=0, stop=self.resolution * len(self.values), num=len(self.values))

    def Merge(self, otherDataFile):
        for value in otherDataFile.values:
            self.values.append(value)
        self.time = np.arange(0, self.resolution * len(self.values), self.resolution)

