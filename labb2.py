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
print("Loading data for background noise")
bg1 = BackgroundData(".\\Datafiles\\background-serie1-0.5sek.lst", 0.5)
bg1.LoadValues(10, 1020)
bg1.MergeBuckets(10)
bg1.PlotWithPoisson()

print("Loading data for background noise")
bg2 = BackgroundData(".\\Datafiles\\background-serie2-5sek.lst", 5)
bg2.LoadValues(10, 122)
bg2.PlotWithPoisson()

print("Loading data for background noise")
bg3 = BackgroundData(".\\Datafiles\\background-serie3-5sek.lst", 5)
bg3.LoadValues(10, 89)
bg3.PlotWithPoisson()

###################################################
# Task 3: Calculate background noice
###################################################


###################################################
# Task 4: Calculate decay speed for Ag
###################################################
print("Task 4")
ag1 = DecayData(".\\Datafiles\\silver-serie2-5sek.lst", 5)
ag1.LoadValues(20, 172)

bg_mean = bg2.Mean()
print(bg_mean)
ag1.AdjustWithFixedValue(bg_mean)

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

print("A= ", A)
print("B= ", B)

ag1 = DecayData(".\\Datafiles\\silver-serie2-5sek.lst", 5)
ag1.LoadValues(20, 121)
print("values1= ", ag1.values)
ag1.AdjustWithFixedValue(bg_mean)
print("values2= ", ag1.values)
ag1.ScaleByLn()
print("values3= ", ag1.values)
ag1.AdjustForDecay(A, B)
print("values4= ", ag1.values)
A, B = AnalyserHelper.LeastSquareFit(ag1, 1, 23)
print(A,B)
# ag1.PlotWithLinearFit("Ag decay (both isotops)", A, B, 1, 23)
