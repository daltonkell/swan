# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 11:55:09 2017

@author: dalton
"""

### Plotting Polar Coordinates of Wave Direction ###

# imports 
from datetime import datetime, timedelta, timezone
import json
from marshmallow import Schema, fields
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sys
import xarray as xr

# data needed 
ds = xr.open_dataset('/home/dalton/PythonCode/swan/swan.nc')

# wave direction xarray slice of main array
wv_dir = ds['dir']

# load in list of areas (collections of nodes)
n = [np.loadtxt("/home/dalton/swan/home/brianmckenna/DUBAI/warnings/areas/wave/area.{0:0=2d}.txt".format(i)).flatten().astype(int) for i in list(range(0, 31))]

# provides a list of areas (collections of nodes) to be used in run_method() 
a = list(range(0, len(n)))

# functions to compute stats of the data 

def method_001(array):
    """A function that takes in an xarray data array and resamples it by the maximums over 6-hr time intervals.
    Arguments:
        array: an xarray data array
    """
    return array.resample("6H",
             dim="time", how="max").max(axis=1)

def method_002(array):
    """A function that takes in an xarray data array and resamples it by the minimums over 6-hr time intervals.
    Arguments:
        array: an xarray data array    
    """
    return array.resample("6H",
             dim="time", how="min").min(axis=1)
             
def method_003(array):
    """A function that takes in an xarray data array and resamples it by the means over 6-hr time intervals.
    Arguments:
        array: an xarray data array    
    """
    return array.resample("6H",
         dim="time", how="mean").mean(axis=1)
         
def method_004(array):
    """A function that takes in an xarray data array and resamples it by the means over 1-day time intervals.
    Arguments: 
        array: an xarray data array
        """
    return array.resample("1D", dim="time", how="mean").mean(axis=1)
    
# one method to run them all (or at least the one you chose)
def run_method(m, areas, data):
    """Runs the chosen method from methods 001, 002, and 003 and outputs the array to a pandas DataFrame object. Each entry into the DataFrame is constructed by first taking the resampled 6-hr maximum of the waves from an area (.resample(...)); this produces arrays for each 6-hr time interval in the area. Following this, the max (.max()) is called, which takes the maximum value for *each* interval, yielding 17 values in a single array. This process is looped for each area. The DataFrame's indices are the time stamps.
        Arguments:
            m: the method of aggregating the original array, chosen by caller. This method actually calls either method_001(), method_002(), or method_003().
            areas: list of areas in the xarray data array; each area consists of a collection of nodes. 
            data: the original xarray array to be acted on by the chosen_method.
    """
    method = m 
    frame = pd.DataFrame()
    for i in areas:
        print("Collecting data for Area {0:0=2d}...".format(i))
        _d = data[:, n[i]]
        frame["{0:0=2d}".format(i)] = method(_d).to_pandas()
    # make sure the function actually returns something, or downstream it will break!
    print("Finished collecting all areas.")
    return frame
    
data1 = run_method(method_003, a, wv_dir) # mean, 6-hr
data2 = run_method(method_004, a, wv_dir) # mean, 1-day


with sns.axes_style("white"):
    fig1 = plt.figure(figsize=(12, 8), tight_layout=True)
    palette = sns.color_palette("hls", n_colors=31) # 31 areas
    ax1 = fig1.add_subplot(1,2,1, polar=True)
    ax2 = fig1.add_subplot(1,2,2)
    color_num = 0
    for area in data2.columns:
        degrees = data1[area]
        points = np.radians(degrees) # convert to rad
        times = list(range(0, len(points))) # 5 days
        ax1.plot(points, times, linestyle="-", marker=".", c=palette[color_num], label="Area {}".format(area))
        ax1.set_theta_zero_location("N")
        sns.kdeplot(degrees, ax=ax2, legend=False)
        color_num += 1
    ax1.set_ylim(0, len(points))
    ax1.set_yticks(np.arange(0, len(points), np.round(len(points)/5)))
    # kde of degree distributions 
    ax1.set_title("Wave Direction Through Time Intervals", size=12, y=1.08)
    ax2.set_title("Distribution of Wave Directions", size=12)
    ax2.set_xlabel("Degrees")
    plt.show()




    