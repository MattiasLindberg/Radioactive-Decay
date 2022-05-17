from DataFile import *
from itertools import count
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.special import factorial
from scipy.stats import poisson


class DecayData(DataFile):

    def AdjustWithFixedValuePerSec(self, fixedValue):
        temp = []
        adjustment = fixedValue * self.resolution
        for value in self.values:
            temp.append(value - adjustment)
        self.values = temp

    def CalculatePoissonErrors(self):
        #temp = []
        #for val in self.values:
        #    temp.append(np.sqrt(val))
        #self.errors= temp
        self.errors = np.sqrt(np.abs(self.values))

    def ScaleByLn(self):
        #temp = []
        #for val in self.values:
        #    logval = np.log(val)
        #    temp.append(logval)
        #self.values = temp
        self.values = np.log(np.abs(self.values))

        #temperrors = []
        #for val in self.errors:
        #    temperrors.append(np.log(val))
        #self.errors = temperrors
        self.errors = np.sqrt(np.abs(self.values))

    def ScaleByExp(self):
        temp = []
        for val in self.values:
            temp.append(np.exp(val))
        self.values = temp

    def PlotWithLinearFit(self, title, A, B, start, stop):
        plt.plot(self.time, self.values, "b")
        plt.xlabel("Seconds")
        plt.ylabel("Events detected")
        plt.title(title)

        plt.errorbar(self.time, self.values, yerr=self.errors)

        plt.plot(self.time[start:stop+1], A + B*np.array(self.time[start:stop+1]), "r")
        # plt.plot(self.time, A + B*np.array(self.time), "r")

        colors = {'Events Detected per 5 second interval':'blue', 'Ag decay least square fit':'red'}         
        labels = list(colors.keys())
        handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
        plt.legend(handles, labels)
        plt.grid(True)
        plt.show()

    def PlotWithExpLinearFit(self, title, A, B, start, stop):
        lambda_1 = -B
        n_1 = np.exp(A)
        # linearvalues = n_1 * np.exp(-lambda_1*self.time[start:stop+1])
        linearvalues = n_1 * np.exp(-lambda_1*self.time)

        #print("lambda= ", lambda_1)
        #print("n_1= ", n_1)
        #print("linearvalues= ", linearvalues)

        fig = plt.figure()
        plt.plot(self.time, self.values, "b")
        plt.xlabel("Seconds")
        plt.ylabel("Events detected")
        plt.title(title)

        plt.errorbar(self.time, self.values, yerr=self.errors)

        # plt.plot(self.time[start:stop+1], linearvalues, "r")
        plt.plot(self.time, linearvalues, "r")

        colors = {'Events Detected per 5 second interval':'blue', 'Ag decay least square fit':'red'}         
        labels = list(colors.keys())
        handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
        plt.legend(handles, labels)
        plt.grid(True)
        plt.show()

        
    def AdjustForDecay(self, A, B):
        temp = []
        adjustment = []

        adjustment = A + B*np.array(self.time)
        temp = self.values - adjustment
        self.values = temp
