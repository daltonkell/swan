# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 12:44:15 2017

@author: dalton
"""
import sys
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

ds = xr.open_dataset('/home/dalton/PythonCode/swan/swan.nc')
#ds = xr.open_dataset(sys.argv[some_number]) # when passed in and run through Bash

# get the significant wave height field (hs) as xarray.DataArray
hs = ds['hs']
print('hs variable in xarray Dataset')
print(hs)

# load in list of areas (collections of nodes)
n = [np.loadtxt("/home/dalton/swan/home/brianmckenna/DUBAI/warnings/areas/wave/area.{0:0=2d}.txt".format(i)).flatten().astype(int) for i in list(range(0, 31))]
# The above creates a list of arrays. Each array is an area, each corresponding to the index. Each array contains the nodes that are in each respective area.
# NOTE: for some reason, after the for-loop, the dict disappears from the variable list but can still be accessed and manipulated.

def hs_ops(xarray_data, n, make_heatmap=True):
    """This function takes in an xarray data series along with a list of areas, yielding a data frame containing the maximum heights of each area for each 6-hr time interval.
    
    Arguments:
        xarray_data: An xarray series that contains all time intervals and significant wave heights for every simulated node.
        n: list of areas, which contain the nodes that represent each area respectively.
        make_heatmap: if True, generates a heatmap of the maximum wave heights for each area for each 6-hr time interval (deafult=True).
    """
    
# Next we want to output a 17x30 array of max heights for each 6 hour time period (). There are 30 areas. 
    hs_areas = {}
    for area in list(range(0, len(n))):
        hs_areas["{0:0=2d}".format(area)] = hs[:, n[area]].resample("6H",
                 dim="time", how="max").max(axis=1)
    print('Subsetted - all times, by area.')
    print("Areas: ", sorted(hs_areas.keys()))
    print("")
    
    #============================================================================== 
    #Each entry into the dictionary is constructed by first taking the resampled 6-hr maximum of the waves from an area (.resample(...)); this produces arrays for each 6-hr time interval in the area. Following this, the max (.max()) is called, which takes the maximum value for *each* interval, yielding 17 values in a single array. This process is looped for each area.
    #==============================================================================
    
    # make into pandas dataframe and transpose so the time periods are the columns
    areas_df = pd.DataFrame(hs_areas).T
    
    ## --- create a 30x17 heatmap of the max heights --- ##
    if make_heatmap==True:
        with sns.axes_style("whitegrid"):
            fig = plt.figure() 
            ax1 = fig.add_subplot(1, 1, 1)
            sns.heatmap(areas_df, annot=True, annot_kws={"size": 7}, cmap=sns.light_palette("blue"), cbar_kws={"label": "Meters"}, vmin=0, vmax=3.0)
            plt.title("Wave Maximum Significant Heights", size=14)
            plt.ylabel("Area", size=10)
            plt.xlabel("6-Hr Interval", size=10)
            plt.show()
    else:
        pass
    
if __name__ == "__main__":
    hs_ops(hs, n)