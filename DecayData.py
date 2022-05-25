from DataFile import *
from itertools import count
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

class DecayData(DataFile):
    def CalculateCountRateAndErrors(self):
        # New time scale should be moved back half the dwell time
        newtime = self.time - self.dwelltime/2

        countrate = []
        for value in self.values:
            countrate.append(value / self.dwelltime)
        self.values = countrate

        self.errors = np.sqrt(self.values) / self.dwelltime

    def AdjustWithFixedValuePerSec(self, fixedValue, uncertainty):
        temp = []
        adjustment = fixedValue * self.dwelltime
        for value in self.values:
            temp.append(value - adjustment)

        temperrors = []
        for errorvalue in self.errors:
            temperrors.append(np.sqrt(errorvalue*errorvalue + uncertainty*uncertainty))

        self.values = temp
        self.errors = temperrors

    def CalculatePoissonErrors(self):
        temp = []
        uncertainty = np.sqrt(np.abs(self.values)) / self.dwelltime
        #print("u= ", uncertainty)
        #for val in self.values:
        #    temp.append(uncertainty)
        self.errors= uncertainty

    def ScaleByLn(self):
        self.errors = np.log(np.sqrt(np.abs(self.values)) / self.dwelltime)

        self.values = np.log(np.abs(self.values))
        #self.errors = np.sqrt(np.abs(self.values))

    def ScaleByExp(self):
        temp = []
        for val in self.values:
            temp.append(np.exp(val))
        self.values = temp

    def Plot(self, title, logornot):
        if self.showDiagrams == False: 
            return

        plt.plot(self.time, self.values, "b")
        plt.title(title)
        if logornot == True:
            plt.ylabel("Events detected ( log(n) )")
        else:
            plt.ylabel("Events detected")

        plt.grid(True)
        plt.show()

    def PlotWithLinearFit(self, title, A, B, start, stop, showerrorsbars, logornot):
        if self.showDiagrams == False: 
            return

        plt.scatter(self.time[start:stop], self.values[start:stop], s=10)
        plt.title(title)
        plt.xlabel("Seconds")
        if logornot == True:
            plt.ylabel("Events detected ( log(n) )")
        else:
            plt.ylabel("Events detected")

        print("errors 5= ", self.errors)

        if showerrorsbars == True:
            plt.errorbar(self.time[start:stop], self.values[start:stop], yerr=self.errors[start:stop], linestyle='None', capsize=4)

        plt.plot(self.time[start:stop], A + B*np.array(self.time[start:stop]), "r")
        # plt.plot(self.time, A + B*np.array(self.time), "r")

        colors = {'Events Detected per 5 second interval':'blue', 'Ag decay least square fit':'red'}         
        labels = list(colors.keys())
        handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
        plt.legend(handles, labels)
        plt.grid(True)
        plt.show()

    def PlotWithExpLinearFit(self, title, A, B, start, stop, showerrorsbars, logornot):
        if self.showDiagrams == False: 
            return

        lambda_1 = -B
        n_1 = np.exp(A)
        print("lambda in plot=", lambda_1)
        print("n in plot=", n_1)
        linearvalues = n_1 * np.exp(-lambda_1*self.time)

        #print("lambda= ", lambda_1)
        #print("n_1= ", n_1)
        #print("linearvalues= ", linearvalues)

        plt.scatter(self.time, self.values, s=10)
        plt.title(title)
        plt.xlabel("Seconds")
        if logornot == True:
            plt.ylabel("Events detected ( log(n) )")
        else:
            plt.ylabel("Events detected")

        if showerrorsbars == True:
            plt.errorbar(self.time, self.values, yerr=self.errors)

        # plt.plot(self.time[start:stop], linearvalues, "r")
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

    def PlotMergedDiagram(self, n_108, lambda108, n_110, lambda_110, bg_mean):
        if self.showDiagrams == False: 
            return

        linearvalues_108 = self.dwelltime * n_108 * np.exp(-lambda108*self.time)
        plt.plot(self.time, linearvalues_108, "r")

        linearvalues_110 = self.dwelltime * n_110 * np.exp(-lambda_110*self.time)
        plt.plot(self.time, linearvalues_110, "g")

        linearvalues = self.dwelltime * bg_mean + linearvalues_108 + linearvalues_110
        plt.plot(self.time, linearvalues, "m")

        plt.axhline(y=bg_mean*self.dwelltime, color='orange', ls='--', lw='1')

        plt.scatter(self.time, self.values, s=10)
        plt.xlabel("Seconds")
        plt.ylabel("Events detected")
        plt.title("Ag decay values with fitted lines for 108-Ag and 110-Ag decay")

        colors = {'Events Detected per 5 second interval':'blue', 'Ag-108 decay least square fit':'red', 'Ag-110 decay least square fit':'green', 'Ag-108 and Ag-110 decays combined':'m' }
        labels = list(colors.keys())
        handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
        plt.legend(handles, labels)
        plt.grid(True)
        plt.show()

    def CalculateChi2(self, n_108, lambda108, n_110, lambda_110, bg_mean, endposition):
        linearvalues = self.dwelltime * bg_mean + (n_110 * np.exp(-lambda_110*self.time)) + (n_108 * np.exp(-lambda108*self.time))
        linearvalues = linearvalues * self.dwelltime

        chi2 = 0
        variance = 5
        for index in range(0, endposition):
            # When calculating chi2 we should be using count rate per second.
            # The values we have are count rate per 5 seconds so we divide by the resolution of the
            measurement_persecond =  self.values[index]/self.dwelltime
            model_persecond = linearvalues[index]/self.dwelltime
            diff = np.abs(measurement_persecond - model_persecond)
            diff = (diff * diff) / np.sqrt(model_persecond)
            #print("index= ", index, ", diff= ", diff, ", measurement_persec= ", measurement_persecond, ", model_persec= ", model_persecond, ", measured value=", self.values[index])
            chi2 = chi2 + diff

        ndof = endposition - 4
        p = 1 - stats.chi2.cdf(chi2, ndof)

        chi2tilde = chi2 / ndof

        print("chi2= ", chi2)
        print("ndof= ", ndof)
        print("p= ", p)
        print("chi2tilde= ", chi2tilde)
        

