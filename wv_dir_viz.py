### Plotting Polar Coordinates of Wave Direction ###

# imports
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import wv_json

def wv_dir_viz():
    """Operates in conjuntion with the wv_json.py script. After importing that script, it calls on the run_method() function to return a pandas DataFrame. From there, it will generate polar coordinate plot of mean  wave direction over time, as well as a distribution of the wave directions.
    Arguments:
      """
    frame = wv_json.run_method(wv_json.method_004, wv_json.a, wv_json.dirs)
    print("Areas: ", frame.columns)

    with sns.axes_style("white"):
        fig1 = plt.figure(figsize=(12, 8), tight_layout=True)
        palette = sns.color_palette("hls", n_colors=31) # 31 areas
        ax1 = fig1.add_subplot(1, 2, 1, polar=True)
        ax2 = fig1.add_subplot(1, 2, 2)
        color_num = 0
        for area in frame.columns:
            degrees = frame[area]
            points = np.radians(degrees)  # convert to rad
            times = list(range(0, len(points)))  # 5 days
            ax1.plot(points, times, linestyle="-", marker=".", c=palette[color_num], label="Area {}".format(area))
            ax1.set_theta_zero_location("N")
            # kde of degree distributions
            sns.kdeplot(degrees, ax=ax2, legend=False)
            color_num += 1
    ax1.set_ylim(0, len(points))
    ax1.set_yticks(np.arange(0, len(points), np.round(len(points)/5)))
    ax1.set_title("Wave Direction Through Time Intervals", size=12, y=1.08)
    ax2.set_title("Distribution of Wave Directions", size=12)
    ax2.set_xlabel("Degrees")
    plt.savefig("wv_directions.png")

if __name__ == "__main__":
    wv_dir_viz()


    
