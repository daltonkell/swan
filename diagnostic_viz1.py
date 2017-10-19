# -*- coding: utf-8 -*-

#==============================================================================
# Internal Visual Diagnostics 
#==============================================================================

# imports
# do I need any of these if I'm importing this to another script?
#==============================================================================
from datetime import datetime, timedelta, timezone
import json
from marshmallow import Schema, fields
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sys
import xarray as xr


ds = xr.open_dataset('/home/dalton/PythonCode/swan/swan.nc')
#ds = xr.open_dataset(sys.argv[some_number]) # when passed in and run through Bash

# get the significant wave height field (hs) as xarray.DataArray
hs = ds['hs']
print('hs variable in xarray Dataset')
print(hs)

# load in list of areas (collections of nodes)
n = [np.loadtxt("/home/dalton/swan/home/brianmckenna/DUBAI/warnings/areas/wave/area.{0:0=2d}.txt".format(i)).flatten().astype(int) for i in list(range(0, 31))]

# NOTE: for some reason, after the for-loop, the dict disappears from the variable list but can still be accessed and manipulated.

def wave_viz(xarray_data, n, make_heat=True, make_ts=True):
    """This function takes in an xarray data series along with a list of areas, yielding a data frame containing the maximum heights of each area for each 6-hr time interval.
    
    Arguments:
        xarray_data: An xarray series that contains all time intervals and significant wave heights for every simulated node.
        n: list of areas, which contain the nodes that represent each area respectively.
        make_heat: if True, generates a heatmap of the maximum wave heights for each area for each 6-hr time interval (deafult=True).
        make_ts: Makes a spaghetti plot ("time series") for area over the 17 time intervals (default=True).
    """
    
# Next we want to output a 17x30 array of max heights for each 6 hour time period (). There are 30 areas. 
  
    frame = pd.DataFrame()
    for area in list(range(0, len(n))):
        frame["{0:0=2d}".format(area)] = hs[:, n[area]].resample("6H",
             dim="time", how="max").max(axis=1).to_pandas()
    print("Areas: ", frame.columns)
#============================================================================== 
# Each entry into the DataFrame is constructed by first taking the resampled 6-hr maximum of the waves from an area (.resample(...)); this produces arrays for each 6-hr time interval in the area. Following this, the max (.max()) is called, which takes the maximum value for *each* interval, yielding 17 values in a single array. This process is looped for each area.

# The DataFrame is indexed by the time stamps!
#==============================================================================
    
    ## --- create a 30x17 heatmap of the max heights --- ##
    if make_heat==True:
        with sns.axes_style("whitegrid"):
            fig = plt.figure(figsize=(12, 8)) 
            ax1 = fig.add_subplot(1, 1, 1)
            sns.heatmap(frame.reset_index(drop=True).T, annot=True, annot_kws={"size": 7}, cmap=sns.light_palette("blue"), cbar_kws={"label": "Meters"}, vmin=0, vmax=3.0)
            # have to reset the index and transpose for heatmap to produce correctly
            ax1.set_title("Wave Maximum Significant Heights", size=14)
            ax1.set_ylabel("Area", size=10)
            ax1.set_xlabel("6-Hr Interval", size=10)
            plt.show(block=False)
            # when block=False, multiple windows of figures can pop up when called on the terminal
    else:
        pass
    
    ## --- create a time series plot of all the maximums over the intervals --- ##
    # note that we're not actually dealing with TIMES here, just 6-hr intervals. This makes it slightly easier to wrangle in matplotlib (seaborn's .tsplot() will be deprecated!)


    if make_ts==True:
        with sns.axes_style("darkgrid"):
             fig2 = plt.figure(figsize=(12, 8))
             ax2 = fig2.add_subplot(1, 1, 1)
             palette = sns.color_palette("hls", n_colors=31)
             color_num = 0
             xs = [i for i in range(0, len(frame))]
             # for-loop to deal with multiple lines?
             for area in frame.columns:
                 #31 areas
                 ys = frame[area]
                 ax2.plot(xs, ys, marker="o", markersize=5, color=palette[color_num], label="Area {}".format(area))
                 color_num += 1
             ax2.set_title("Maximum Wave Heights", fontsize=14)
             ax2.set_xlabel("6-Hr Interval", fontsize=12)
             ax2.set_ylabel("Maximum Wave Height (meters)", fontsize=12)
             plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0, fontsize=7)
             plt.show()
    else:
        pass
    
if __name__ == "__main__":
    wave_viz(hs, n)