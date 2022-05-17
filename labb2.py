from DataFile import *
from DecayData import *
from BackgroundData import *
from AnalyserHelper import *

import matplotlib.pyplot as plt
import pandas as pd
from scipy.special import factorial
from scipy.stats import poisson

# Load data for background noice

###################################################
# Task 2: Plot background noice
###################################################
bg1 = BackgroundData(".\\Datafiles\\background-serie1-0.5sek.lst", 0.5)
bg1.LoadValues(10, 1020)
bg1.MergeBuckets(10)
#bg1.PlotWithPoisson()

bg2 = BackgroundData(".\\Datafiles\\background-serie2-5sek.lst", 5)
bg2.LoadValues(10, 122)
#bg2.PlotWithPoisson()

bg3 = BackgroundData(".\\Datafiles\\background-serie3-5sek.lst", 5)
bg3.LoadValues(10, 89)
#bg3.PlotWithPoisson()

bg4 = BackgroundData(".\\Datafiles\\background-serie3-5sek.lst", 5)
bg4.LoadValues(10, 89)
bg4.Merge(bg1)
bg4.Merge(bg2)
#bg4.PlotWithPoisson()


###################################################
# Task 3: Calculate background noice
###################################################

# bg4 has all measurements for background noice,
# so it can be used to calculate the average value
bg_mean = bg4.Mean() / bg4.resolution
print("Average number of background events per 5 second period= ", bg_mean)

bg1 = BackgroundData(".\\Datafiles\\background-serie1-0.5sek.lst", 0.5)
bg1.LoadValues(10, 1020)
totalCount = bg1.GetTotalCount()
totalTime = bg1.GetTotalTime()
print("Background series 1: totalCount= ",totalCount, ", totalTime= ", totalTime, ", average= ", totalCount/totalTime)

bg2 = BackgroundData(".\\Datafiles\\background-serie2-5sek.lst", 5)
bg2.LoadValues(10, 122)
totalCount = bg2.GetTotalCount()
totalTime = bg2.GetTotalTime()
print("Background series 2: totalCount= ",totalCount, ", totalTime= ", totalTime, ", average= ", totalCount/totalTime)

bg3 = BackgroundData(".\\Datafiles\\background-serie3-5sek.lst", 5)
bg3.LoadValues(10, 89)
totalCount = bg3.GetTotalCount()
totalTime = bg3.GetTotalTime()
print("Background series 3: totalCount= ",totalCount, ", totalTime= ", totalTime, ", average= ", totalCount/totalTime)

totalCount = bg4.GetTotalCount()
totalTime = bg4.GetTotalTime()
print("Full background series: totalCount= ",totalCount, ", totalTime= ", totalTime, ", average= ", totalCount/totalTime)

###################################################
# Task 4: Adjust decay speed for Ag
###################################################
print("Task 4")
ag108 = DecayData(".\\Datafiles\\silver-serie2-5sek.lst", 5)
ag108.LoadValues(20, 172)
ag108.AdjustWithFixedValuePerSec(bg_mean)
ag108.CalculatePoissonErrors()

print("Ag decay adjusted for background noice, to be used in task 6: ", ag108.values)

###################################################
# Task 5: Plot Ag decay and determine constants 
# for 108-Ag decay
###################################################
print("Task 5")

ag108.ScaleByLn()
A, B = AnalyserHelper.LeastSquareFit(ag108, 24, 120)
lambda_108 = -B
n_108 = np.exp(A)
#print(n_1, lambda_1)
ag108.PlotWithLinearFit("Decay values and linear fit for 108-Ag", A, B, 24, 120)

ag108.ScaleByExp()
ag108.CalculatePoissonErrors()
ag108.PlotWithExpLinearFit("Decay values and linear fit for 108-Ag", A, B, 24, 120)

ag108_values = n_108 * np.exp(-lambda_108*ag108.time)
print("108-Ag decay values to be corrected for in task 6: ", ag108_values)

###################################################
# Task 6: Plot Ag decay and determine constants 
# for 110-Ag decay
###################################################
print("Task 6")

ag110 = DecayData(".\\Datafiles\\silver-serie2-5sek.lst", 5)
ag110.LoadValues(20, 141)
ag110.AdjustWithFixedValuePerSec(bg_mean)
ag110.values = ag110.values - ag108_values[0:len(ag110.values)]
print("110-Ag decay values to be added to table: ", ag110.values)
ag110.CalculatePoissonErrors()
ag110.ScaleByLn()
# ag110.AdjustForDecay(A, B)
A, B = AnalyserHelper.LeastSquareFit(ag110, 1, 23)
lambda_110 = -B
n_110 = np.exp(A)

ag110.PlotWithLinearFit("Decay values and linear fit for 110-Ag", A, B, 1, 23)

ag110.ScaleByExp()
ag110.CalculatePoissonErrors()
ag110.PlotWithExpLinearFit("Decay values and liner fit for 110-Ag", A, B, 1, 23)

###################################################
# Task 6: Results
###################################################
ag = DecayData(".\\Datafiles\\silver-serie2-5sek.lst", 5)
ag.LoadValues(20, 141)
ag.AdjustWithFixedValuePerSec(bg_mean)

linearvalues = n_108 * np.exp(-lambda_108*ag.time)
plt.plot(ag.time, linearvalues, "r")

linearvalues = n_110 * np.exp(-lambda_110*ag.time)
plt.plot(ag.time, linearvalues, "g")

plt.plot(ag.time, ag.values, "b")
plt.xlabel("Seconds")
plt.ylabel("Events detected")
plt.title("Ag decay values with fitted lines for 108-Ag and 110-Ag decay")

# plt.plot(self.time[start:stop+1], linearvalues, "r")

colors = {'Events Detected per 5 second interval':'blue', 'Ag-108 decay least square fit':'red', 'Ag-110 decay least square fit':'green' }         
labels = list(colors.keys())
handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
plt.legend(handles, labels)
plt.grid(True)
plt.show()
