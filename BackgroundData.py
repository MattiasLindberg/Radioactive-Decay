from DataFile import *
from itertools import count
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.special import factorial
from scipy.stats import poisson


class BackgroundData(DataFile):

    def MergeBuckets(self, mergeCount):
        temp = []
        i = 0
        counter = 0
        for index, row in self.dataframe.iterrows():
            counter = counter + row['events']
            i = i + 1
            if i == 10:
                temp.append(counter)
                i = 0
                counter = 0
        #data ={ "rownr" : temp, "events" : temp }
        #self.dataframe = pd.DataFrame(data)
        self.values = temp
        self.time = np.linspace(0, self.resolution * len(self.values). self.resolution)

    def GroupBy(self):
        temp = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
        for n in self.values:
            temp[n] = temp[n] + 1
        return temp


    
    def PlotWithPoisson(self, title):
        groupDict = self.GroupBy()
        #agg_df = self.dataframe.groupby('events').agg(['count'])
        #print(agg_df)

        fig = plt.figure()
        ax = fig.add_axes([1,1,1,1])
        ax.bar(groupDict.keys, groupDict.values)
        plt.xlabel("Events per 5 seconds")
        plt.ylabel("Buckets with specific event count")
        plt.title(title)

        mean = self.Mean()
        print("Mean= ", mean)
        k = np.arange(0, 10, 0.2)
        d = np.exp(-mean)*np.power(mean, k)/factorial(k)
        d = 100*d
        plt.plot(k, d, 'r')
        ax.autoscale()

        colors = {'Instance with event count':'blue', 'Poisson distribution':'red'}         
        labels = list(colors.keys())
        handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
        plt.legend(handles, labels)
        plt.show()
