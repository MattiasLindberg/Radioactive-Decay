import numpy as np
from scipy.optimize import leastsq
from numpy.polynomial import polynomial as P

class AnalyserHelper(object):

    def LeastSquareFit(datafile, start, stop):
        x = np.array(datafile.time[start:stop+1])
        y = np.array(datafile.values[start:stop+1])
        N = np.float64(stop-start+1)

        sumX2 = np.array(np.sum(x*x))
        sumX = np.array(np.sum(x))
        sumY = np.array(np.sum(y))
        sumXY = np.array(np.sum(x*y))

        delta = np.float64(N * np.array(sumX2) - np.power(sumX, 2))

        A = ( (sumX2*sumY) - (sumX*sumXY) ) / delta
        B = ( (N*sumXY) - (sumX*sumY) ) / delta

        sumofdifferencesquared = 0
        for index in range(0, len(x)):
          temp = np.power(y[index] - A - B*x[index], 2)
          #print("temp= ", temp)
          sumofdifferencesquared = sumofdifferencesquared  + temp

        #print("sumofdifferencesquared= ", sumofdifferencesquared)
        #print("N= ", N)

        sigma_y = np.sqrt(sumofdifferencesquared/(N-2))
        sigma_A = sigma_y * np.sqrt(sumX2/delta)
        sigma_B = sigma_y * np.sqrt(N/delta)

        #print("sigma_y= ", sigma_y)
        #print("sigma_A= ", sigma_A)
        #print("sigma_B= ", sigma_B)

        return A, B, sigma_y, sigma_A, sigma_B
