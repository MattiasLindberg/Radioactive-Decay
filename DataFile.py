import numpy as np


class DataFile(object):
    def __init__(self, filename, dwelltime, showDiagrams):
        self.filename = filename
        self.file = open(self.filename, "r")
        self.dwelltime = dwelltime
        self.values = []
        self.time = []
        self.showDiagrams = showDiagrams
 
    def LoadValues(self, start, stop):
        count = 0
        for line in self.file:
            if start <= count and count <= stop:
                values = line.split()
                self.values.append(int(values[1]))
            count = count + 1
        self.time = np.arange(0, self.dwelltime * len(self.values), self.dwelltime)


    def Length(self):
        return len(self.values)

    def Mean(self):
        return np.mean(self.values)

    def StandardDeviation(self):
        return np.std(self.values)
    
    def MergeChannels(self, mergeCount):
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

        self.dwelltime = int(mergeCount * self.dwelltime)
        self.values = temp
        self.time = np.linspace(start=0, stop=self.dwelltime * len(self.values), num=len(self.values))

    def Merge(self, otherDataFile):
        for value in otherDataFile.values:
            self.values.append(value)
        self.time = np.arange(0, self.dwelltime * len(self.values), self.dwelltime)

