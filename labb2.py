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

BG_SERIES1_START_LOAD = 10
BG_SERIES1_STOP_LOAD = 1020
BG_SERIES1_RESOLUTION = 0.5
BG_SERIES1_FILENAME = ".\\Datafiles\\background-serie1-0.5sek.lst"

BG_SERIES2_START_LOAD = 10
BG_SERIES2_STOP_LOAD = 122
BG_SERIES2_RESOLUTION = 5
BG_SERIES2_FILENAME = ".\\Datafiles\\background-serie2-5sek.lst"

BG_SERIES3_START_LOAD = 10
BG_SERIES3_STOP_LOAD = 89
BG_SERIES3_RESOLUTION = 5
BG_SERIES3_FILENAME = ".\\Datafiles\\background-serie3-5sek.lst"

AG_SERIES1_START_LOAD = 78
AG_SERIES1_STOP_LOAD = 1209
AG_SERIES1_RESOLUTION = 0.5
AG_SERIES1_FILENAME = ".\\Datafiles\\silver-serie1-0.5sek.lst"

AG_SERIES2_START_LOAD = 20
AG_SERIES2_STOP_LOAD = 172
AG_SERIES2_RESOLUTION = 5
AG_SERIES2_FILENAME = ".\\Datafiles\\silver-serie2-5sek.lst"

ShowDiagrams = False

###################################################
# Task 2: Plot background noice
###################################################
bg1 = BackgroundData(BG_SERIES1_FILENAME, BG_SERIES1_RESOLUTION, ShowDiagrams)
bg1.LoadValues(BG_SERIES1_START_LOAD, BG_SERIES1_STOP_LOAD)
bg1.MergeBuckets(AG_SERIES2_RESOLUTION/AG_SERIES1_RESOLUTION) # Merge channels with dwell time 0.5 sec to channels with dwell time 5 sec
# Figure 2
bg1.PlotWithPoisson()

bg2 = BackgroundData(BG_SERIES2_FILENAME, BG_SERIES2_RESOLUTION, ShowDiagrams)
bg2.LoadValues(BG_SERIES2_START_LOAD, BG_SERIES2_STOP_LOAD)
# Figure 3
bg2.PlotWithPoisson()

bg3 = BackgroundData(BG_SERIES3_FILENAME, BG_SERIES3_RESOLUTION, ShowDiagrams)
bg3.LoadValues(BG_SERIES3_START_LOAD, BG_SERIES3_STOP_LOAD)
# Figure 4
bg3.PlotWithPoisson()

bg4 = BackgroundData(BG_SERIES3_FILENAME, BG_SERIES3_RESOLUTION, ShowDiagrams)
bg4.LoadValues(BG_SERIES3_START_LOAD, BG_SERIES3_STOP_LOAD)
bg4.Merge(bg1)
bg4.Merge(bg2)
# Figure 5
bg4.PlotWithPoisson()


###################################################
# Task 3: Calculate background noice
###################################################

# bg4 has all measurements for background noice,
# so it can be used to calculate the average value
bg_mean = bg4.Mean() / bg4.resolution
print("Average number of background events per second= ", bg_mean)

bg1 = BackgroundData(BG_SERIES1_FILENAME, BG_SERIES1_RESOLUTION, ShowDiagrams)
bg1.LoadValues(BG_SERIES1_START_LOAD, BG_SERIES1_STOP_LOAD)
totalCount = bg1.GetTotalCount()
totalTime = bg1.GetTotalTime()
print("Background series 1: totalCount= ",totalCount, ", totalTime= ", totalTime, ", average= ", totalCount/totalTime, "uncertainty= ", np.sqrt(totalCount/totalTime))

bg2 = BackgroundData(BG_SERIES2_FILENAME, BG_SERIES2_RESOLUTION, ShowDiagrams)
bg2.LoadValues(BG_SERIES2_START_LOAD, BG_SERIES2_STOP_LOAD)
totalCount = bg2.GetTotalCount()
totalTime = bg2.GetTotalTime()
print("Background series 2: totalCount= ",totalCount, ", totalTime= ", totalTime, ", average= ", totalCount/totalTime, "uncertainty= ", np.sqrt(totalCount/totalTime))

bg3 = BackgroundData(BG_SERIES3_FILENAME, BG_SERIES3_RESOLUTION, ShowDiagrams)
bg3.LoadValues(BG_SERIES3_START_LOAD, BG_SERIES3_STOP_LOAD)
totalCount = bg3.GetTotalCount()
totalTime = bg3.GetTotalTime()
print("Background series 3: totalCount= ",totalCount, ", totalTime= ", totalTime, ", average= ", totalCount/totalTime, "uncertainty= ", np.sqrt(totalCount/totalTime))

totalCount = bg4.GetTotalCount()
totalTime = bg4.GetTotalTime()
print("Full background series: totalCount= ",totalCount, ", totalTime= ", totalTime, ", average= ", totalCount/totalTime, "uncertainty= ", np.sqrt(totalCount/totalTime))

print(" ")
print("-----------------------------------------------------------------")
print(" ")

###################################################
# Task 4: Adjust decay speed for Ag
###################################################
print("Task 4")

print("AG SERIES 1")
ag108_1 = DecayData(AG_SERIES1_FILENAME, AG_SERIES1_RESOLUTION, ShowDiagrams)
ag108_1.LoadValues(AG_SERIES1_START_LOAD, AG_SERIES1_STOP_LOAD)
ag108_1.MergeBuckets(AG_SERIES2_RESOLUTION/AG_SERIES1_RESOLUTION) # Merge channels with dwell time 0.5 sec to channels with dwell time 5 sec
ag108_1.AdjustWithFixedValuePerSec(bg_mean)
ag108_1.CalculatePoissonErrors()

temp = np.array(ag108_1.values) / (AG_SERIES2_RESOLUTION/AG_SERIES1_RESOLUTION)
print("Ag count rate adjusted for background noice (events/sec): ", temp[0:4])
print("Uncertaintiy for Ag count rate adjusted for background noice (events/sec): ", np.sqrt(temp[0:4]))

print (" ")
print("AG SERIES 2")
ag108_2 = DecayData(AG_SERIES2_FILENAME, AG_SERIES2_RESOLUTION, ShowDiagrams)
ag108_2.LoadValues(AG_SERIES2_START_LOAD, AG_SERIES2_STOP_LOAD)
ag108_2.AdjustWithFixedValuePerSec(bg_mean)
ag108_2.CalculatePoissonErrors()

temp = np.array(ag108_2.values) / AG_SERIES2_RESOLUTION
print("Ag count rate adjusted for background noice (events/sec): ", temp[0:4])
print("Uncertaintiy for Ag count rate adjusted for background noice (events/sec): ", np.sqrt(temp[0:4]))

print(" ")
print("-----------------------------------------------------------------")
print(" ")

###################################################
# Task 5: Plot Ag decay and determine constants 
# for 108-Ag decay
###################################################
print("Task 5")

print("AG SERIES 1")
ag108_1.ScaleByLn()
A108_1, B108_1 = AnalyserHelper.LeastSquareFit(ag108_1, 24, 110)
lambda108_1 = -B108_1
n_108_1 = np.exp(A108_1)
print("lambda108_1= ", lambda108_1)
print("n_108_1= ", n_108_1)

# Figure 6
ag108_1.PlotWithLinearFit("Decay values and linear fit for 108-Ag (series 1)", A108_1, B108_1, 24, 110, True, True)

ag108_1.ScaleByExp()
ag108_1.CalculatePoissonErrors()
#ag108_1.PlotWithExpLinearFit("Decay values and linear fit for 108-Ag (series 1)", A108_1, B108_1, 24, 110, False, False)

ag108_values_1 = n_108_1 * np.exp(-lambda108_1*ag108_1.time)
#print("108-Ag decay values (series 1) to be corrected for in task 6: ", ag108_values_1)

print(" ")
print("AG SERIES 2")
ag108_2.ScaleByLn()
A108_2, B108_2 = AnalyserHelper.LeastSquareFit(ag108_2, 24, 110)
lambda108_2 = -B108_2
n_108_2 = np.exp(A108_2)
print("lambda108_2= ", lambda108_2)
print("n_108_2= ", n_108_2)

# Figure 6
ag108_2.PlotWithLinearFit("Decay values and linear fit for 108-Ag (series 2)", A108_2, B108_2, 24, 120, True, True)

ag108_2.ScaleByExp()
ag108_2.CalculatePoissonErrors()
#ag108_2.PlotWithExpLinearFit("Decay values and linear fit for 108-Ag (series 2)", A108_2, B108_2, 24, 120, False, False)

ag108_values_2 = n_108_2 * np.exp(-lambda108_2*ag108_2.time)
#print("108-Ag decay values (series 2) to be corrected for in task 6: ", ag108_values_2)

print(" ")
print("-----------------------------------------------------------------")
print(" ")

###################################################
# Task 6: Plot Ag decay and determine constants 
# for 110-Ag decay
###################################################
print("Task 6")

print("AG SERIES 1")

ag110_1 = DecayData(AG_SERIES1_FILENAME, AG_SERIES1_RESOLUTION, ShowDiagrams)
ag110_1.LoadValues(AG_SERIES1_START_LOAD, AG_SERIES1_STOP_LOAD)
# Merge channels with dwell time 0.5 sec to channels with dwell time 5 sec
#print(ag110_1.values)
ag110_1.MergeBuckets(AG_SERIES2_RESOLUTION/AG_SERIES1_RESOLUTION)
ag110_1.AdjustWithFixedValuePerSec(bg_mean)
ag110_1.values = ag110_1.values - ag108_values_1[0:len(ag110_1.values)]
print("110-Ag decay values to be added to table (series 1): ", ag110_1.values[0:10])
ag110_1.CalculatePoissonErrors()
ag110_1.ScaleByLn()
A110_1, B110_1 = AnalyserHelper.LeastSquareFit(ag110_1, 1, 20)
lambda_110_1 = -B110_1
n_110_1 = np.exp(A110_1)
print("lambda_110_1= ", lambda_110_1)
print("n_110_1= ", n_110_1)

ag110_1.PlotWithLinearFit("Decay values and linear fit for 110-Ag (series 1)", A110_1, B110_1, 1, 23, True, True)

ag110_1.ScaleByExp()
ag110_1.CalculatePoissonErrors()
ag110_1.PlotWithExpLinearFit("Decay values and liner fit for 110-Ag (series 1)", A110_1, B110_1, 1, 23, False, False)


ag110_1_values = n_110_1 * np.exp(-lambda_110_1*ag108_1.time)
ag108_1.values = ag108_1.values - ag110_1_values[0:len(ag108_1.values)]

ag108_1.PlotWithExpLinearFit("Decay values and linear fit for 108-Ag (series 1)", A108_1, B108_1, 24, 120, False, False)


print (" ")
print("AG SERIES 2")
ag110_2 = DecayData(AG_SERIES2_FILENAME, AG_SERIES2_RESOLUTION, ShowDiagrams)
ag110_2.LoadValues(20, 141)
ag110_2.AdjustWithFixedValuePerSec(bg_mean)
ag110_2.values = ag110_2.values - ag108_values_2[0:len(ag110_2.values)]
print("110-Ag decay values to be added to table (series 2): ", ag110_2.values[0:10])
ag110_2.CalculatePoissonErrors()
ag110_2.ScaleByLn()
# ag110_2.AdjustForDecay(A, B)
A110_2, B110_2 = AnalyserHelper.LeastSquareFit(ag110_2, 1, 23)
lambda_110_2 = -B110_2
n_110_2 = np.exp(A110_2)
print("lambda_110_2= ", lambda_110_2)
print("n_110_2= ", n_110_2)

ag110_2.PlotWithLinearFit("Decay values and linear fit for 110-Ag (series 2)", A110_2, B110_2, 1, 23, True, False)

ag110_2.ScaleByExp()
ag110_2.CalculatePoissonErrors()
ag110_2.PlotWithExpLinearFit("Decay values and liner fit for 110-Ag (series 2)", A110_2, B110_2, 1, 23, False, True)


ag110_2_values = n_110_2 * np.exp(-lambda_110_2*ag108_2.time)
ag108_2.values = ag108_2.values - ag110_2_values[0:len(ag108_2.values)]
ag108_2.PlotWithExpLinearFit("Decay values and linear fit for 108-Ag (series 2)", A108_2, B108_2, 24, 120, False, False)

print(" ")
print("-----------------------------------------------------------------")
print(" ")

###################################################
# Task 7: Half life
###################################################
print("Task 7: Half life")

print("Half life for 108-Ag (series 1): ", np.log(1/2)/(-lambda108_1))
print("Half life for 110-Ag (series 1): ", np.log(1/2)/(-lambda_110_1))
print(" ")
print("Half life for 108-Ag (series 2): ", np.log(1/2)/(-lambda108_2))
print("Half life for 110-Ag (series 2): ", np.log(1/2)/(-lambda_110_2))

print(" ")
print("-----------------------------------------------------------------")
print(" ")

###################################################
# Task 8: Chi^2 test
###################################################


print("AG SERIES 1: Chi^2 test")
ag = DecayData(AG_SERIES1_FILENAME, AG_SERIES1_RESOLUTION, ShowDiagrams)
ag.LoadValues(AG_SERIES1_START_LOAD, AG_SERIES1_STOP_LOAD)
# Merge channels with dwell time 0.5 sec to channels with dwell time 5 sec
ag.MergeBuckets(AG_SERIES2_RESOLUTION/AG_SERIES1_RESOLUTION)

# we should include bg values in this plot...
#ag.AdjustWithFixedValuePerSec(bg_mean)

ag.PlotMergedDiagram(n_108_1, lambda108_1, n_110_1, lambda_110_1, bg_mean)
ag.CalculateChi2(n_108_1, lambda108_1, n_110_1, lambda_110_1, bg_mean)


print(" ")
print("AG SERIES 2: Chi^2 test")
ag = DecayData(AG_SERIES2_FILENAME, AG_SERIES2_RESOLUTION, ShowDiagrams)
ag.LoadValues(AG_SERIES2_START_LOAD, AG_SERIES2_STOP_LOAD)

# we should include bg values in this plot...
#ag.AdjustWithFixedValuePerSec(bg_mean)

ag.PlotMergedDiagram(n_108_2, lambda108_2, n_110_2, lambda_110_2, bg_mean)
ag.CalculateChi2(n_108_2, lambda108_2, n_110_2, lambda_110_2, bg_mean)
