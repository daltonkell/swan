# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 11:36:36 2017

@author: dalton
"""

from datetime import datetime, timedelta, timezone
import json
from marshmallow import Schema, fields
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sys
import xarray as xr

# importing diagnostic_viz.py file 
import diagnostic_viz

ds = xr.open_dataset('/home/dalton/PythonCode/swan/swan.nc')
#ds = xr.open_dataset(sys.argv[some_number]) # when passed in and run through Bash

# get the significant wave height field (hs) as xarray.DataArray
hs = ds['hs']
print('hs variable in xarray Dataset')
print(hs)

# load in list of areas (collections of nodes)
n = [np.loadtxt("/home/dalton/swan/home/brianmckenna/DUBAI/warnings/areas/wave/area.{0:0=2d}.txt".format(i)).flatten().astype(int) for i in list(range(0, 31))]
# The above creates a list of arrays. Each array is an area, each corresponding to the index. Each array contains the nodes that are in each respective area.


def method_001(da):
    return da.resample("6H",
             dim="time", how="max").max(axis=1)

def method_002(da):
    return da.resample("6H",
             dim="time", how="mean").mean(axis=1)
             
def run(method, areas, data):
    frame = pd.DataFrame()
    for area in areas:
#==============================================================================
#         frame["{0:0=2d}".format(area)] = data[:, n[area]].resample("6H",
#                  dim="time", how="max").max(axis=1).to_pandas()
#==============================================================================
        frame["{0:0=2d}".format(area)] = hs[:, n[area]].resample("6H",
                  dim="time", how="max").max(axis=1).to_pandas()

a = list(range(0, len(n)))
m = method_001

run(m, a, hs)

#============================================================================== 
# Each entry into the DataFrame is constructed by first taking the resampled 6-hr maximum of the waves from an area (.resample(...)); this produces arrays for each 6-hr time interval in the area. Following this, the max (.max()) is called, which takes the maximum value for *each* interval, yielding 17 values in a single array. This process is looped for each area.

# The DataFrame is indexed by the time stamps!
#==============================================================================

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

def main():

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
    # the indent separates the laines (at least it should)

# ask for visualizations

def ask_viz():
    response = input("Visualize data [y]/n?")
    if response == "y":#main()
        diagnostic_viz.wave_viz(hs, n)
        print("Warning print complete.")
    else:
        print("Warning print complete.")
        

if __name__ == '__main__':
     main()
     ask_viz()