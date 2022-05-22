from DataFile import *
from itertools import count
import numpy as np
import matplotlib.pyplot as plt


class BackgroundData(DataFile):

    def GroupBy(self):
        t = [0, 0, 0, 0, 0, 0, 0, 0, 0 ]
        for n in self.values:
            t[n] = t[n] + 1
        return t

    def GetTotalTime(self):
        return self.resolution * len(self.time)

    def GetTotalCount(self):
        return np.sum(self.values)
    
    def PlotWithPoisson(self):
        t = self.GroupBy()
        s = [0, 1, 2, 3, 4, 5, 6, 7, 8, ]

        bucketCount = np.sum(t)

        plt.bar(s, t, color='slategray')
        mean = self.Mean()
        k = np.arange(0, 8, 0.2)
        d = np.exp(-mean)*np.power(mean, k)/factorial(k)
        d = bucketCount*d
        plt.plot(k, d, 'red')

        plt.axvline(x=mean, color='orange', ls='--', lw='4')

        plt.xlabel("Detected events in 5 second interval")
        plt.ylabel("Buckets with specific event count")
        titleText = "Distribution of background noice (N={:d})".format(bucketCount)
        plt.title(titleText)

        avgText = "Average value ({:.1f})".format(mean)
        colors = {'Buckets with event count':'slategray', 'Poisson distribution':'red', avgText :'orange'}         
        labels = list(colors.keys())
        handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
        plt.legend(handles, labels)

        plt.show()
