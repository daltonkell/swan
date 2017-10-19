# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 09:51:44 2017

@author: dalton
"""

### Creating a High-Level Function Workflow for Schema and Viz ###

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

# importing viz script
import diagnostic_viz2

## -- Schema to Ensure Output -- ##
class LocationSchema(Schema):
    name = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()

class ForecastSchema(Schema):
    source = fields.Str()
    location = fields.Nested(LocationSchema, many=False)
    initialized = fields.DateTime()
    valid = fields.Dict()

forecast_schema = ForecastSchema()

## -- Callable Methods for returning max, min, mean values -- ##
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

# === Testing this out 10_19_17 === #
# choosing the desired statistic to compute (Max, Min, or Mean)
def choose_stat():
    choice = input("Max, Min, or Mean?")
    return choice 
    
stat_dict = {"Max": method_001, "Min": method_002, "Mean": method_003}

chosen_stat = choose_stat()

# ============================================================= #

# main xarray data array
ds = xr.open_dataset('/home/dalton/PythonCode/swan/swan.nc')

# wave height xarray slice of main array
hs = ds['hs']

# load in list of areas (collections of nodes)
n = [np.loadtxt("/home/dalton/swan/home/brianmckenna/DUBAI/warnings/areas/wave/area.{0:0=2d}.txt".format(i)).flatten().astype(int) for i in list(range(0, 31))]

# provides a list of areas (collections of nodes) to be used in run_method() 
a = list(range(0, len(n)))

# method
m = stat_dict[chosen_stat]
# if this doesn't work, go back to hardcoded
#m = method_001

# the main function which will pumps out the JSON output
def main():
    """First calls on run method, which requires three positional arguments: chosen_method, areas, and data. The chosen_method argument calls on the separately defined func, choose_method(), which prompts the caller to select the method; it returns the required method. The 'areas' argument is supplied by a, defined earlier in the script, and the 'data' argument is supplied by hs, also defined earlier in the script. run_method() can then actually run with these params, and returns a DataFrame."""
    frame = run_method(m, a, hs)
    # forecasts
    forecasts = []
    
    # for each location (station or warning area)
    #     *if warning area, we don't need coordinates*
    for l in frame.columns:
    
    # model initialization time
    # I want to grab the first time that the area begins "forecasting"--i.e. time 0 
        init = frame[l].index[0]
        
        # warning
        valid = pd.date_range(init, init+timedelta(days=4), freq="6H")
        fields = ['wave_warning']
        # was getting error "'list' object has not attribute 'Str'"
        forecast = dict(
            source = 'DMOFS',
            location = dict(
                name = "Area {}".format(l),
                latitude = None,
                longitude = None
            ),
            initialized = init,
            valid = {v.isoformat(): {n: np.asscalar(frame[l][v]) for n in fields} for v in valid}
            # returns the max wave height of the area (l) indexed for that period (v)
            # np.asscalar to decode numpy.float 
        )
        forecasts.append(forecast_schema.dump(forecast).data)
    print(type(forecasts[0]["valid"]['2000-01-05T00:00:00'
    ]["wave_warning"]))   
    print(json.dumps(forecasts, sort_keys=True, indent=4))
    print(l)
    # the indent separates the laines (at least it should)
    
# ask for visualizations

def ask_viz():
    """Asks the caller if they would like to visualize the data they have pulled, in addition to seeing just the JSON text output."""
    response = input("Visualize data [y]/n?")
    if response == "y":
        diagnostic_viz2.wave_viz()
        print("Warning print and visualization complete.")
    else:
        print("Warning print complete.")
        
if __name__ == "__main__":
    main()
    ask_viz()