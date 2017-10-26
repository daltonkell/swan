# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 11:08:31 2017

@author: dalton
"""
# imports
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

# import script that's calling this script
import wv_json

def wv_viz(make_heat=True, make_ts=True):
    """This function operates in conjuntion with the schema_high_level_func.py script. After importing that script, it calls on the run_method() function to return a pandas DataFrame. From there, it will generate a heatplot and a time series spahgetti plot.
    Arguments:
        make_heat: if True, generates a heatmap of the maximum wave heights for each area for each 6-hr time interval (deafult=True).
        make_ts: Makes a spaghetti plot ("time series") for area over the 17 time intervals (default=True).
    """
    
# Next we want to output a 17x30 array of max heights for each 6 hour time period (). There are 30 areas. 
  
    frame = wv_json.run_method(wv_json.m, wv_json.a, wv_json.hs)
    print("Areas: ", frame.columns)
    
    ## --- create a 30x17 heatmap of the max heights --- ##
    if make_heat==True:
        with sns.axes_style("whitegrid"):
            fig = plt.figure(figsize=(12, 8)) 
            ax1 = fig.add_subplot(1, 1, 1)
            sns.heatmap(frame.reset_index(drop=True).T, annot=True, annot_kws={"size": 7}, cmap=sns.light_palette("blue"), cbar_kws={"label": "Meters"}, vmin=0, vmax=3.0)
            # have to reset the index and transpose for heatmap to produce correctly
            ax1.set_title("{} Significant Wave Heights".format(wv_json.chosen_stat), size=14)
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
            # for-loop to deal with multiple lines
            for area in frame.columns:
                #31 areas
                ys = frame[area]
                ax2.plot(xs, ys, marker="o", markersize=5, color=palette[color_num], label="Area {}".format(area))
                color_num += 1
            ax2.set_title("{} Wave Heights".format(wv_json.chosen_stat), fontsize=14)
            ax2.set_xlabel("6-Hr Interval", fontsize=12)
            ax2.set_ylabel("Maximum Wave Height (meters)", fontsize=12)
            plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0, fontsize=7)
            plt.show()
    else:
        pass


if __name__ == "__main__":
    wv_viz()
