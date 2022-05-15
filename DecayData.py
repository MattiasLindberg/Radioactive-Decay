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
        self.values = temp

    def ScaleByLn(self):
        temp = []
        for val in self.values:
            temp.append(np.log(val))
        data ={ "rownr" : temp, "events" : temp }
        self.dataframe = pd.DataFrame(data)
        self.values = temp

    def PlotWithLinearFit(self, title, A, B, start, stop):
        # ax = self.dataframe.plot()

        fig = plt.figure()
        plt.plot(self.time, self.values, "b")
        plt.xlabel("Seconds")
        plt.ylabel("Events detected")
        plt.title(title)

        plt.plot(self.time[start:stop+1], A + B*np.array(self.time[start:stop+1]), "r")

        colors = {'Events Detected per 5 second interval':'blue', 'Ag decay least square fit':'red'}         
        labels = list(colors.keys())
        handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
        plt.legend(handles, labels)
        plt.show()

        
    def AdjustForDecay(self, A, B):
        temp = []
        adjustment = []

        adjustment = A + B*np.array(self.time)
        temp = self.values - adjustment
        self.values = temp
