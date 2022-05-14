from DataFile import *
from DecayData import *
from BackgroundData import *
import matplotlib.pyplot as plt
import pandas as pd
from scipy.special import factorial
from scipy.stats import poisson

# Load data for background noice

###################################################
# Task 2: Plot background noice
###################################################
#print("Loading data for background noise")
#bg1 = DataFile(".\Datafiles\background-serie1-0.5sek.lst", 0.5)
#bg1.LoadValues(10, 1020)
#bg1.MergeBuckets(10)
#bg1.PlotWithPoisson()

print("Loading data for background noise")
bg2 = BackgroundData(".\\Datafiles\\background-serie2-5sek.lst", 5)
bg2.LoadValues(10, 122)
#bg2.PlotWithPoisson("Distribution of background noice")

#print("Loading data for background noise")
#bg3 = DataFile(".\Datafiles\background-serie3-5sek.lst", 5)
#bg3.LoadValues(10, 89)
#bg3.PlotWithPoisson()

###################################################
# Task 3: Calculate background noice
###################################################


###################################################
# Task 4: Calculate decay speed for Ag
###################################################
print("Loading data for Ag decay")
ag1 = DecayData(".\\Datafiles\\silver-serie2-5sek.lst", 5)
ag1.LoadValues(20, 172)
bg_mean = bg2.Mean()
print(bg_mean)
ag1.AdjustWithFixedValue(bg_mean)

###################################################
# Task 5: Plot combined Ag decay
###################################################

ag1.ScaleByLn()
ag1.PlotWithLSF("Ag decay (both isotops)", 24, 120)
ag1.PlotWithLSF("Ag decay (both isotops)", 1, 23)

