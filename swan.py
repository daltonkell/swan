# swan

# Objective: take a point (or group of points) and visualize the 
# wave height over the given time periods.

# imports
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

ds = xr.open_dataset('/home/dalton/PythonCode/swan/swan.nc')

# time index
t = 0

# we only care about the "hs" variable, as this represents the
# significant wave height. We also want the time variables.

ds.time[0:5] # first 4 time periods (just to look at a slice)

# can I slice out a point?

ds.hs[77]

# Ok, so it seems like the significant wave height ("hs") is 
# an array of the heights at each node at a specific point in time.
# This may actually make the plotting slightly easier, as 
# selecting a point in time is as simple as slicing the data ONCE

# i.e. ds.hs[time][node(s)]

ds.hs[78][0]

sample = ds.hs.to_dataframe()

sample.columns = sample.columns.get_level_values(0)
sample.columns = [" ".join(col).strip() for col in sample.columns.values]
