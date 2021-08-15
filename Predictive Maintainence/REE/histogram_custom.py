import math
import numpy as np
import pandas as pd
from collections import defaultdict



class histogram_custom():
    def __init__(self, binsize_x = 50, binsize_y = 50, center_x=0, center_y = 0):
        self.points = []
        self.counts = defaultdict(float)
        self.binsize_x = binsize_x
        self.binsize_y = binsize_y
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0
        self.center_x = center_x
        self.center_y = center_y
        self.nmin_x = int(np.floor((self.min_x - self.center_x)/self.binsize_x))
        self.nmin_y = int(np.floor((self.min_y - self.center_y)/self.binsize_y))

        self.nmax_x = int(np.ceil((self.max_x - self.center_x)/self.binsize_x))
        self.nmax_y = int(np.ceil((self.max_y - self.center_y)/self.binsize_y))

    def update_dict_range(self):
        self.nmin_x = int(np.floor((self.min_x - self.center_x)/self.binsize_x))
        self.nmin_y = int(np.floor((self.min_y - self.center_y)/self.binsize_y))

        self.nmax_x = int(np.ceil((self.max_x - self.center_x)/self.binsize_x))
        self.nmax_y = int(np.ceil((self.max_y - self.center_y)/self.binsize_y))

        for i in range(self.nmin_y, self.nmax_y+1):
            for j in range(self.nmin_x, self.nmax_x+1):
                self.counts.setdefault((np.round(i * self.binsize_y+self.center_y,2),np.round(j * self.binsize_x+self.center_x,2)), 0.0)

                                
    def count_cycles(self,y,x,count):
        if y <= self.nmin_y*self.binsize_y + self.center_y:
            self.min_y = y
            self.update_dict_range()
        elif y >= self.nmax_y*self.binsize_y + self.center_y:
            self.max_y = y
            self.update_dict_range()
            
        if x <= self.nmin_x*self.binsize_x + self.center_x:
            self.min_x = x
            self.update_dict_range()
        elif x >= self.nmax_x*self.binsize_x + self.center_x:
            self.max_x = x
            self.update_dict_range()

        n_x = np.round(np.round((x-self.center_x)/self.binsize_x)* self.binsize_x+self.center_x,2)
        n_y = np.round(np.round((y-self.center_y)/self.binsize_y)* self.binsize_y+self.center_y,2)

        self.counts[(n_y,n_x)] += count
    
    def df_count(self):
        return pd.DataFrame([(k[0],k[1],v) for k, v in self.counts.items()], columns = ["y","x","Count"])
