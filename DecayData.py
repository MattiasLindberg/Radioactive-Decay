from DataFile import *
from itertools import count
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.special import factorial
from scipy.stats import poisson


class DecayData(DataFile):

    def AdjustWithFixedValue(self, fixedValue):
        temp = []
        for value in self.values:
            temp.append(value - fixedValue)
        data ={ "rownr" : temp, "events" : temp }
        self.dataframe = pd.DataFrame(data)
        self.values = temp
        print(temp)

    def ScaleByLn(self):
        temp = []
        for val in self.values:
            temp.append(np.log(val))
        data ={ "rownr" : temp, "events" : temp }
        self.dataframe = pd.DataFrame(data)
        self.values = temp

    def PlotWithLSF(self, title, start, stop):
        # ax = self.dataframe.plot()

        fig = plt.figure()
        plt.plot(self.time, self.values, "b")
        plt.xlabel("Seconds")
        plt.ylabel("Events detected")
        plt.title(title)

        A, B = self.LeastSquareFit(start, stop)
        plt.plot(self.time[start:stop+1], A + B*self.time[start:stop+1], "r")

        colors = {'Events Detected per 5 second interval':'blue', 'Ag decay least square fit':'red'}         
        labels = list(colors.keys())
        handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
        plt.legend(handles, labels)
        plt.show()

        print(self.time)
        print(self.time*self.time)
        print(sum(self.time*self.time))

    def LeastSquareFit(self, start, stop):
        x = self.time[start:stop+1]
        y = self.values[start:stop+1]
        sumX2 = np.sum(x * x)
        sumX = np.sum(x)
        sumY = np.sum(y)
        sumXY = np.sum(x*y)
        delta = (stop-start+1)*sumX2 - np.power(sumX, 2)
        A = ( (sumX2*sumY) - (sumX*sumXY) ) / delta
        B = ( ((stop-start+1)*sumXY) - (sumX*sumY) ) / delta

        return A, B

        
