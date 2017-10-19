#!/usr/bin/env python                                                                                                                                                           
# -*- coding: utf-8 -*-

import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

ds = xr.open_dataset('/home/dalton/PythonCode/swan/swan.nc')
#print('Full xarray Dataset')
#print(ds)
#print('')

# get the significant wave height field (hs) as xarray.DataArray
hs = ds['hs']
print('hs variable in xarray Dataset')
print(hs)

# Here we want to output a 17x30 array of max heights for each 6 hour time period (there are 97 "hours", and 97/6 ~= 17). There are 30 areas. 


n = [np.loadtxt("/home/dalton/swan/home/brianmckenna/DUBAI/warnings/areas/wave/area.{0:0=2d}.txt".format(i)).flatten().astype(int) for i in list(range(0, 31))]
# creates a list of arrays. Each array is an area, each corresponding to the index. Each array contains the nodes that are in each respective area.
# subsetting each area, through the entire time period
# NOTE: for some reason, after the for-loop, the dict disappears from the variable list but can still be accessed and manipulated.

#==============================================================================
# def func_name(xarray_data, n, make_heatmap=True):
#     """This function takes in an xarray data series along with a list of areas, yielding a data frame containing the maximum heights of each area for each 6-hr time interval.
#     
#     Arguments:
#         xarray_data: An xarray series that contains all time intervals and significant wave heights for every simulated node.
#         n: list of areas, which contain the nodes that represent each area respectively.
#         make_heatmap: if True, generates a heatmap of the maximum wave heights for each area for each 6-hr time interval.
#     """
#==============================================================================
    
hs_areas = {}
for area in list(range(0, len(n))):
    hs_areas["{0:0=2d}".format(area)] = hs[:, n[area]].resample("6H",
             dim="time", how="max").max(axis=1)
print('Subsetted - all times, by area.')
print(hs_areas.keys())
print("")

#============================================================================== 
#Each entry into the dictionary is constructed by first taking the resampled 6-hr maximum of the waves from an area (.resample(...)); this produces arrays for each 6-hr time interval in the area. Following this, the max (.max()) is called, which takes the maximum value for *each* interval, yielding 17 values in a single array. This process is looped for each area.
#==============================================================================

# make into pandas df
areas_df = pd.DataFrame(hs_areas)
# transpose so the time periods are the columns
areas_dfT = pd.DataFrame(hs_areas).T

## --- create a 30x17 heatmap of the max heights --- ##
#if make_heatmap==True:
with sns.axes_style("whitegrid"):
    fig = plt.figure() 
    ax1 = fig.add_subplot(1, 1, 1)
    sns.heatmap(areas_dfT, annot=True, annot_kws={"size": 7}, cmap=sns.light_palette("blue"), cbar_kws={"label": "Meters"}, vmin=0, vmax=3.0)
    plt.title("Wave Maximum Significant Heights", size=14)
    plt.ylabel("Area", size=10)
    plt.xlabel("6-Hr Interval", size=10)
    plt.show()
#else:
#    pass


#test spaghetti plot
fig.clear()
with sns.axes_style("darkgrid"):
#==============================================================================
#     fig2 = plt.figure()
#     ax2 = fig2.add_subplot(2, 1, 1)
#     #palette = sns.color_palette("hls", n_colors=30)
#==============================================================================
    #color_num = 0
    xs = areas_df.index
#==============================================================================
#     # for-loop to deal with multiple lines?
#     for area in list(range(0, len(areas_df.columns))):
#         ys = areas_df["{0:0=2d}".format(area)]
#         ax2.plot(y=ys, x=xs, marker="o", markersize=8) #color=palette[color_num]
#         color_num += 1
#==============================================================================
    plt.plot([0.01, 0.02], [0.01, 0.02])    
    plt.title("Time Series of Areas")
    plt.xlabel("6-Hr Interval")
    plt.ylabel("Maximum Wave Height")
    plt.show()
             #plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0, fontsize=8, label="Areas")
#==============================================================================
#     print(hs_25)
#     print("")
#     print(hs_25.max(axis=1))
#==============================================================================

#==============================================================================
# # resample the data by 6 hour maximum
# hs_25max = hs_25.resample('6H', dim='time', how='max')
# print('6H max value of the subset')
# print(hs_25max)
# print('')
# 
# # similar to Pandas, let's use axis 1 (the 25 different points) and get the max among them at each 6H interval
# 
# # max heights for the first 6 hr interval 
# with sns.axes_style("darkgrid"):
#     sns.tsplot(hs_25max[0])
#     plt.suptitle("HS Max Across Nodes 100-125")
#     plt.title("First 6hr Interval")
#     #plt.show()
# 
# # Let's make hs_25 into a pandas dataframe
# hs_25_df = hs_25.to_dataframe()
# hs_25_df.reset_index(inplace=True)
# hs_25_df.head()
# 
# # Ok, so let's look at one node through time--say node 0
# 
# hs_25_df[hs_25_df["node"]==0].head()
# with sns.axes_style("dark"):
#     heights = hs_25_df[hs_25_df["node"]==0]["hs"]
#     intervals = hs_25_df[hs_25_df["node"]==0]["time"]
#     plt.plot(intervals, heights)
#     plt.title("Node 0 Heights")
#     plt.xlabel("Time")
#     plt.ylabel("Wave Height (m)")
#     
# # can we look at them all?    
# with sns.axes_style("dark"):
#     fig, axes = plt.subplots(ncols=1, nrows=1)    
#     #heights = hs_25_df["hs"]
#     #intervals = hs_25_df["time"]
#     sns.tsplot(data=hs_25_df, time="time", value="hs", condition="node", unit="node")
#     plt.title("Nodes 100-125", size=12)
#     plt.xlabel("Time")
#     plt.ylabel("Wave Height (em)")
#     plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, fontsize=8)
# 
# # get a distribution of all the heights of one node (say, node 0)
# with sns.axes_style("darkgrid"):
#     sns.distplot(hs_25_df[hs_25_df["node"]==0]["hs"], bins=50, kde=True)
#     plt.title("Node 0 Height Distribution")
#     plt.xlabel("Height (m)")
#==============================================================================

# now get a distribution of the node MAX heights. This will involve some wrangling with xarray
# so the hs_25.max(axis=1) returns an array of 97 max heights. That is, the max height of all the nodes for each time period. However, what it *doesn't* tell us is *which* node the max is coming from. Is there a way to do that?

    