from tkinter import TRUE
from DataFile import *
from DecayData import *
from BackgroundData import *
from AnalyserHelper import *


import matplotlib.pyplot as plt

from scipy.special import factorial
from scipy.stats import poisson


###################################################
# Constants used when loading measurements
###################################################

print("Task 1: Configure measurement files")

BG_SERIES1_START_LOAD = 10
BG_SERIES1_STOP_LOAD = 1020
BG_SERIES1_DWELLTIME = 0.5
BG_SERIES1_FILENAME = ".\\Datafiles\\background-serie1-0.5sek.lst"

BG_SERIES2_START_LOAD = 10
BG_SERIES2_STOP_LOAD = 122
BG_SERIES2_DWELLTIME = 5
BG_SERIES2_FILENAME = ".\\Datafiles\\background-serie2-5sek.lst"

BG_SERIES3_START_LOAD = 10
BG_SERIES3_STOP_LOAD = 89
BG_SERIES3_DWELLTIME = 5
BG_SERIES3_FILENAME = ".\\Datafiles\\background-serie3-5sek.lst"

AG_SERIES1_START_LOAD = 110
# AG_SERIES1_START_LOAD = 82
AG_SERIES1_STOP_LOAD = 1209
AG_SERIES1_MERGECHANNELS = True
AG_SERIES1_DWELLTIME = 0.5
AG_SERIES1_FILENAME = ".\\Datafiles\\silver-serie1-0.5sek.lst"
AG_SERIES1_AG110_START_FITTING = 0
AG_SERIES1_AG110_STOP_FITTING = 10
AG_SERIES1_AG108_START_FITTING = 20
AG_SERIES1_AG108_STOP_FITTING = 55

AG_SERIES2_START_LOAD = 20
AG_SERIES2_STOP_LOAD = 172
AG_SERIES2_MERGECHANNELS = False
AG_SERIES2_DWELLTIME = 5
AG_SERIES2_FILENAME = ".\\Datafiles\\silver-serie2-5sek.lst"
AG_SERIES2_AG110_START_FITTING = 0
AG_SERIES2_AG110_STOP_FITTING = 10
AG_SERIES2_AG108_START_FITTING = 20
AG_SERIES2_AG108_STOP_FITTING = 60

#AG_START_LOAD = AG_SERIES1_START_LOAD
#AG_STOP_LOAD = AG_SERIES1_STOP_LOAD
#AG_MERGECHANNELS = AG_SERIES1_MERGECHANNELS
#AG_DWELLTIME = AG_SERIES1_DWELLTIME
#AG_FILENAME = AG_SERIES1_FILENAME
#AG_AG108_START_FITTING = AG_SERIES1_AG108_START_FITTING
#AG_AG108_STOP_FITTING = AG_SERIES1_AG108_STOP_FITTING
#AG_AG110_START_FITTING = AG_SERIES1_AG110_START_FITTING
#AG_AG110_STOP_FITTING = AG_SERIES1_AG110_STOP_FITTING

AG_START_LOAD = AG_SERIES2_START_LOAD
AG_STOP_LOAD = AG_SERIES2_STOP_LOAD
AG_DWELLTIME = AG_SERIES2_DWELLTIME
AG_FILENAME = AG_SERIES2_FILENAME
AG_MERGECHANNELS = AG_SERIES2_MERGECHANNELS
AG_AG108_START_FITTING = AG_SERIES2_AG108_START_FITTING
AG_AG108_STOP_FITTING = AG_SERIES2_AG108_STOP_FITTING
AG_AG110_START_FITTING = AG_SERIES2_AG110_START_FITTING
AG_AG110_STOP_FITTING = AG_SERIES2_AG110_STOP_FITTING

ShowDiagrams_bg = False
ShowDiagrams_ag = True

print(" ")
print("-----------------------------------------------------------------")
print(" ")

###################################################
# Task 2: Plot background noice
###################################################
print("Task 2: Plot background noice with Poisson")

bg1 = BackgroundData(BG_SERIES1_FILENAME, BG_SERIES1_DWELLTIME, ShowDiagrams_bg)
bg1.LoadValues(BG_SERIES1_START_LOAD, BG_SERIES1_STOP_LOAD)
bg1.MergeChannels(AG_SERIES2_DWELLTIME/AG_SERIES1_DWELLTIME) # Merge channels with dwell time 0.5 sec to channels with dwell time 5 sec
# Figure 2
bg1.PlotWithPoisson()

bg2 = BackgroundData(BG_SERIES2_FILENAME, BG_SERIES2_DWELLTIME, ShowDiagrams_bg)
bg2.LoadValues(BG_SERIES2_START_LOAD, BG_SERIES2_STOP_LOAD)
# Figure 3
bg2.PlotWithPoisson()

bg3 = BackgroundData(BG_SERIES3_FILENAME, BG_SERIES3_DWELLTIME, ShowDiagrams_bg)
bg3.LoadValues(BG_SERIES3_START_LOAD, BG_SERIES3_STOP_LOAD)
# Figure 4
bg3.PlotWithPoisson()

bg4 = BackgroundData(BG_SERIES3_FILENAME, BG_SERIES3_DWELLTIME, ShowDiagrams_bg)
bg4.LoadValues(BG_SERIES3_START_LOAD, BG_SERIES3_STOP_LOAD)
bg4.Merge(bg1)
bg4.Merge(bg2)
# Figure 5
bg4.PlotWithPoisson()

print(" ")
print("-----------------------------------------------------------------")
print(" ")

###################################################
# Task 3: Calculate background noice
###################################################
print("Task 3: Count rate for background noice")

# bg4 has all measurements for background noice,
# so it can be used to calculate the average value
bg_mean = bg4.Mean() / bg4.dwelltime
print("Average number of background events per second= ", bg_mean)

bg1 = BackgroundData(BG_SERIES1_FILENAME, BG_SERIES1_DWELLTIME, ShowDiagrams_bg)
bg1.LoadValues(BG_SERIES1_START_LOAD, BG_SERIES1_STOP_LOAD)
totalCount = bg1.GetTotalCount()
totalTime = bg1.GetTotalTime()
uncertainty_1 = np.sqrt(totalCount)/totalTime
print("Background series 1: totalCount= ",totalCount, ", totalTime= ", totalTime, ", average= ", totalCount/totalTime, "uncertainty= ", uncertainty_1)

bg2 = BackgroundData(BG_SERIES2_FILENAME, BG_SERIES2_DWELLTIME, ShowDiagrams_bg)
bg2.LoadValues(BG_SERIES2_START_LOAD, BG_SERIES2_STOP_LOAD)
totalCount = bg2.GetTotalCount()
totalTime = bg2.GetTotalTime()
uncertainty_2 = np.sqrt(totalCount)/totalTime
print("Background series 2: totalCount= ",totalCount, ", totalTime= ", totalTime, ", average= ", totalCount/totalTime, "uncertainty= ", uncertainty_2)

bg3 = BackgroundData(BG_SERIES3_FILENAME, BG_SERIES3_DWELLTIME, ShowDiagrams_bg)
bg3.LoadValues(BG_SERIES3_START_LOAD, BG_SERIES3_STOP_LOAD)
totalCount = bg3.GetTotalCount()
totalTime = bg3.GetTotalTime()
uncertainty_3 = np.sqrt(totalCount)/totalTime
print("Background series 3: totalCount= ",totalCount, ", totalTime= ", totalTime, ", average= ", totalCount/totalTime, "uncertainty= ", uncertainty_3)

totalCount = bg4.GetTotalCount()
totalTime = bg4.GetTotalTime()
uncertainty_4 = np.sqrt(totalCount)/totalTime
print("Full background series: totalCount= ",totalCount, ", totalTime= ", totalTime, ", average= ", totalCount/totalTime, "uncertainty= ", uncertainty_4)

print(" ")
print("-----------------------------------------------------------------")
print(" ")

###################################################
# Task 4: Adjust decay speed for Ag
###################################################
print("Task 4: Count rate for Ag decay")

ag108_2 = DecayData(AG_FILENAME, AG_DWELLTIME, ShowDiagrams_ag)
ag108_2.LoadValues(AG_START_LOAD, AG_STOP_LOAD)
if AG_MERGECHANNELS == True:
    ag108_2.MergeChannels(10)
ag108_2.CalculateCountRateAndErrors()
print(ag108_2.values)
ag108_2.AdjustWithFixedValuePerSec(bg_mean, uncertainty_4)
###ag108_2.CalculatePoissonErrors()
#ag108_2.Plot("xxx", False)

print("Ag count rate adjusted for background noice (events/sec): ", ag108_2.values[0:5])
print("Uncertaintiy for Ag count rate adjusted for background noice (events/sec): ", ag108_2.errors[0:5])

print(" ")
print("-----------------------------------------------------------------")
print(" ")

###################################################
# Task 5: Plot Ag decay and determine constants 
# for 108-Ag decay
###################################################
print("Task 5: Determine 108-Ag decay")

ag108_2.ScaleByLn()

A108_2, B108_2 = AnalyserHelper.LeastSquareFit(ag108_2, AG_AG108_START_FITTING, AG_AG108_STOP_FITTING)
lambda108_2 = -B108_2
n_108_2 = np.exp(A108_2)
print("lambda108_2= ", lambda108_2)
print("n_108_2= ", n_108_2)

# Figure 6
ag108_2.PlotWithLinearFit("Decay logarithmic values and linear fit for 108-Ag", A108_2, B108_2, AG_AG108_START_FITTING, AG_AG108_STOP_FITTING, True, True)

ag108_2.ScaleByExp()
ag108_2.CalculatePoissonErrors()
#ag108_2.PlotWithExpLinearFit("Decay values and linear fit for 108-Ag", A108_2, B108_2, 24, 120, False, False)

ag108_values_2 = n_108_2 * np.exp(-lambda108_2*ag108_2.time)
#print("108-Ag decay values (series 2) to be corrected for in task 6: ", ag108_values_2)

print(" ")
print("-----------------------------------------------------------------")
print(" ")

###################################################
# Task 6: Plot Ag decay and determine constants 
# for 110-Ag decay
###################################################
print("Task 6: Determine 110-Ag decay")

ag110_2 = DecayData(AG_FILENAME, AG_DWELLTIME, ShowDiagrams_ag)
ag110_2.LoadValues(AG_START_LOAD, AG_STOP_LOAD)
if AG_MERGECHANNELS == True:
    ag110_2.MergeChannels(10)
ag110_2.CalculateCountRateAndErrors()
ag110_2.AdjustWithFixedValuePerSec(bg_mean, uncertainty_4)
ag110_2.values = ag110_2.values - ag108_values_2[0:len(ag110_2.values)]
print("110-Ag decay values to be added to table: ", ag110_2.values[0:10])
ag110_2.CalculatePoissonErrors()
ag110_2.ScaleByLn()
# ag110_2.AdjustForDecay(A, B)
A110_2, B110_2 = AnalyserHelper.LeastSquareFit(ag110_2, AG_AG110_START_FITTING, AG_AG110_STOP_FITTING)
lambda_110_2 = -B110_2
n_110_2 = np.exp(A110_2)
print("lambda_110_2= ", lambda_110_2)
print("n_110_2= ", n_110_2)

ag110_2.PlotWithLinearFit("Decay values and linear fit for 110-Ag", A110_2, B110_2, AG_AG110_START_FITTING, AG_AG110_STOP_FITTING, True, False)

ag110_2.ScaleByExp()
ag110_2.CalculatePoissonErrors()
ag110_2.PlotWithExpLinearFit("Decay values and liner fit for 110-Ag", A110_2, B110_2, AG_AG110_START_FITTING, AG_AG110_STOP_FITTING, False, True)


ag110_2_values = n_110_2 * np.exp(-lambda_110_2*ag108_2.time)
ag108_2.values = ag108_2.values - ag110_2_values[0:len(ag108_2.values)]
ag108_2.PlotWithExpLinearFit("Decay values and linear fit for 108-Ag", A108_2, B108_2, AG_AG110_START_FITTING, AG_AG110_STOP_FITTING, False, False)

print(" ")
print("-----------------------------------------------------------------")
print(" ")

###################################################
# Task 7: Half life
###################################################
print("Task 7: Half life")

print("Half life for 108-Ag: ", np.log(1/2)/(-lambda108_2))
print("Half life for 110-Ag: ", np.log(1/2)/(-lambda_110_2))

print(" ")
print("-----------------------------------------------------------------")
print(" ")

###################################################
# Task 8: Chi^2 test
###################################################

print("Task 8: Chi^2 test")

ag = DecayData(AG_FILENAME, AG_DWELLTIME, ShowDiagrams_ag)
ag.LoadValues(AG_START_LOAD, AG_STOP_LOAD)
if AG_MERGECHANNELS == True:
    ag.MergeChannels(10)

ag.PlotMergedDiagram(n_108_2, lambda108_2, n_110_2, lambda_110_2, bg_mean)

print(ag.values)
print(len(ag.values))
ag.CalculateChi2(n_108_2, lambda108_2, n_110_2, lambda_110_2, bg_mean, len(ag.values))


print(" ")
print("-----------------------------------------------------------------")
print(" ")

###################################################
# Interval testing
###################################################

print("Interval testing")


ag_2 = DecayData(AG_FILENAME, AG_DWELLTIME, True)
ag_2.LoadValues(AG_START_LOAD, AG_STOP_LOAD)
if AG_MERGECHANNELS == True:
    ag_2.MergeChannels(10)
#ag_2.CalculateCountRateAndErrors()
ag_2.CalculatePoissonErrors()
#ag_2.AdjustWithFixedValuePerSec(bg_mean, uncertainty_4)
ag_2.ScaleByLn()


plt.scatter(ag_2.time, ag_2.values, s=10)
plt.axvline(x=ag_2.time[AG_AG108_START_FITTING], color='red', ls='--', lw='2')
plt.axvline(x=ag_2.time[AG_AG108_STOP_FITTING], color='red', ls='--', lw='2')
plt.axvline(x=ag_2.time[AG_AG110_START_FITTING], color='green', ls='--', lw='2')
plt.axvline(x=ag_2.time[AG_AG110_STOP_FITTING], color='green', ls='--', lw='2')

plt.ylabel("Detected events per channel (log)")
plt.xlabel("Time (s)")
plt.title("Logarithmic decay with fitting intervals")

colors = {'Detected events':'blue', 'Fitting interval for 108-Ag':'red', 'Fitting interval for 110-Ag':'green' }
labels = list(colors.keys())
handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
plt.legend(handles, labels)
plt.grid(True)

plt.show()

