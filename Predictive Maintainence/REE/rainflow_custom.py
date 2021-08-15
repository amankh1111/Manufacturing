import math
import numpy as np
import pandas as pd
from collections import defaultdict



class rainflow_custom():
    def __init__(self, binsize_mean = 50, binsize_rng = 50, center_mean=0, center_rng = 0):
        self.points = []
        self.counts = defaultdict(float)
        self.binsize_mean = binsize_mean
        self.binsize_rng = binsize_rng
        self.min_mean = 0
        self.min_rng = 0
        self.max_mean = 0
        self.max_rng = 0
        self.center_mean = center_mean
        self.center_rng = center_rng
        self.nmin_mean = int(np.floor((self.min_mean - self.center_mean)/self.binsize_mean))
        self.nmin_rng = int(np.floor((self.min_rng - self.center_rng)/self.binsize_rng))

        self.nmax_mean = int(np.ceil((self.max_mean - self.center_mean)/self.binsize_mean))
        self.nmax_rng = int(np.ceil((self.max_rng - self.center_rng)/self.binsize_rng))

    def update_dict_range(self):
        self.nmin_mean = int(np.floor((self.min_mean - self.center_mean)/self.binsize_mean))
        self.nmin_rng = int(np.floor((self.min_rng - self.center_rng)/self.binsize_rng))

        self.nmax_mean = int(np.ceil((self.max_mean - self.center_mean)/self.binsize_mean))
        self.nmax_rng = int(np.ceil((self.max_rng - self.center_rng)/self.binsize_rng))

        for i in range(self.nmin_rng, self.nmax_rng+1):
            for j in range(self.nmin_mean, self.nmax_mean+1):
                self.counts.setdefault((np.round(i * self.binsize_rng+self.center_rng,2),np.round(j * self.binsize_mean+self.center_mean,2)), 0.0)

        
    def reversals(self, x_next):
        result = False 
        if len(self.points) <= 1:
            result = True
        elif self.points[-1] != x_next:
            d_last = (self.points[-1] - self.points[-2])
            d_next = x_next - self.points[-1]
            if d_last * d_next < 0:
                result = True
        return result
    
    def format_output(point1, point2, count):
        x1 = point1
        x2 = point2
        rng = abs(x1 - x2)
        mean = 0.5 * (x1 + x2)
        return [rng, mean, count, x1, x2]

    def extract_cycles(self, x_next):
        result = 0
        tmp = self.reversals(x_next)
        if len(self.points) > 0 and tmp == False:
            self.points.pop()
            self.points.append(x_next)
        else:
            self.points.append(x_next)
            while len(self.points) >= 4:
                # Form ranges X and Y from the three most recent points
                x1, x2, x3 = self.points[-4], self.points[-3], self.points[-2]
                X = abs(x3 - x2)
                Y = abs(x2 - x1)

                if X < Y:
                    # Read the next point
                    break
                elif len(self.points) == 4:
                    # Y contains the starting point
                    # Count Y as one-half cycle and discard the first point
                    result = rainflow_custom.format_output(self.points[0], self.points[1], 0.5)
                    self.count_cycles(result[0],result[1],result[2])
                    print(result)
                    self.points.pop(0)
                else:
                    # Count Y as one cycle and discard the peak and the valley of Y
                    result = rainflow_custom.format_output(self.points[-4], self.points[-3], 1.0)
                    print(result)
                    self.count_cycles(result[0],result[1],result[2])
                    last = self.points.pop()
                    second_last = self.points.pop()
                    self.points.pop()
                    self.points.pop()
                    self.points.append(second_last)
                    self.points.append(last)

                    
    def count_cycles(self,rng,mean,count):
        if rng <= self.nmin_rng*self.binsize_rng + self.center_rng:
            self.min_rng = rng
            self.update_dict_range()
        elif rng >= self.nmax_rng*self.binsize_rng + self.center_rng:
            self.max_rng = rng
            self.update_dict_range()
            
        if mean <= self.nmin_mean*self.binsize_mean + self.center_mean:
            self.min_mean = mean
            self.update_dict_range()
        elif mean >= self.nmax_mean*self.binsize_mean + self.center_mean:
            self.max_mean = mean
            self.update_dict_range()

        n_mean = np.round(np.round((mean-self.center_mean)/self.binsize_mean)* self.binsize_mean+self.center_mean,2)
        n_rng = np.round(np.round((rng-self.center_rng)/self.binsize_rng)* self.binsize_rng+self.center_rng,2)

        self.counts[(n_rng,n_mean)] += count
    
    def rainflow_count(self):
        return pd.DataFrame([(k[0],k[1],v) for k, v in self.counts.items()], columns = ["Range","Mean","Count"])
