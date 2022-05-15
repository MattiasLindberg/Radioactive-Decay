import numpy as np

class AnalyserHelper(object):

    def LeastSquareFit(datafile, start, stop):
        x = np.array(datafile.time[start:stop+1])
        y = np.array(datafile.values[start:stop+1])
        n = np.float64(stop-start+1)
        sumX2 = np.array(np.sum(x*x))
        sumX = np.array(np.sum(x))
        sumY = np.array(np.sum(y))
        sumXY = np.array(np.sum(x*y))
        delta = np.float64((n)*np.array(sumX2) - np.power(sumX, 2))
        A = ( (sumX2*sumY) - (sumX*sumXY) ) / delta
        B = ( ((n)*sumXY) - (sumX*sumY) ) / delta

        return A, B
