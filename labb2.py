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
print("Loading data for background noice")
bg1 = BackgroundData(".\\Datafiles\\background-serie1-0.5sek.lst", 0.5)
bg1.LoadValues(10, 1020)
bg1.MergeBuckets(10)
#bg1.PlotWithPoisson()

print("Loading data for background noice")
bg2 = BackgroundData(".\\Datafiles\\background-serie2-5sek.lst", 5)
bg2.LoadValues(10, 122)
#bg2.PlotWithPoisson()

print("Loading data for background noice")
bg3 = BackgroundData(".\\Datafiles\\background-serie3-5sek.lst", 5)
bg3.LoadValues(10, 89)
#bg3.PlotWithPoisson()

print("Loading data for background noice")
bg4 = BackgroundData(".\\Datafiles\\background-serie3-5sek.lst", 5)
bg4.LoadValues(10, 89)
print("Merge all files and plot")
bg4.Merge(bg1)
bg4.Merge(bg2)
#bg4.PlotWithPoisson()


###################################################
# Task 3: Calculate background noice
###################################################

# bg4 has all measurements for background noice,
# so it can be used to calculate the average value
bg_mean = bg3.Mean()
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
# Task 4: Calculate decay speed for Ag
###################################################
print("Task 4")
ag1 = DecayData(".\\Datafiles\\silver-serie2-5sek.lst", 5)
ag1.LoadValues(20, 172)
ag1.AdjustWithFixedValue(bg_mean)
print("Adjusted Ag decay: ", ag1.values)

###################################################
# Task 5: Plot Ag decay and determine constants 
# for 108-Ag decay
###################################################
print("Task 5")

ag1.ScaleByLn()
A, B = AnalyserHelper.LeastSquareFit(ag1, 24, 120)
#print(A,B)
# ag1.PlotWithLinearFit("Ag decay (both isotops)", A, B, 24, 120)

###################################################
# Task 6: Plot Ag decay and determine constants 
# for 110-Ag decay
###################################################
print("Task 6")

ag1 = DecayData(".\\Datafiles\\silver-serie2-5sek.lst", 5)
ag1.LoadValues(20, 141)
ag1.AdjustWithFixedValue(bg_mean)
ag1.ScaleByLn()
ag1.AdjustForDecay(A, B)
A, B = AnalyserHelper.LeastSquareFit(ag1, 1, 23)
ag1.PlotWithLinearFit("Ag decay (both isotops)", A, B, 1, 23)
