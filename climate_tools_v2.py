#!/usr/bin/env python
''' Library containing climate tools.

This file contains various functions for working with climate data. More will be added in the future.

Disclaimer:
This code was developed by an employee of the Department of Commerce/National Oceanic Atmospheric Administration/
National Weather Service, and is free to use within the public domain, but this code is only provided for unofficial
and educational purposes only. Anything derived from this code shall in no way be considered official or sanctioned
by any agency of the United States Government.

Version history:
1.0 (2017 June 22): Initial build.
2.0 (2017 June 25): Re-written to use the pandas library. Added computeStats function.
'''

# import modules
import numpy as np
import pandas

__author__ = "Jason W. Godwin"
__copyright__ = "Public Domain"
__credits__ = ""

__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jason W. Godwin"
__email__ = "jasonwgodwin@gmail.com"
__status__ = "Production"

# function for returning calendar day statistics
def climateStats(stats_file):
    # open the CSV file
    df = pandas.read_csv(stats_file)

    # get the column values
    dates = df['Date']
    calendar_dates = df['Calendar date']
    highs = df['High']
    lows = df['Low']
    precip = df['Precipitation']

    # get all unique dates
    unique_dates = calendar_dates.unique()

    # compute the stats for each date
    all_highs = {}
    all_lows = {}
    high_medians = {}
    high_stdevs = {}
    high_means = {}
    high_max = {}
    high_min = {}
    low_medians = {}
    low_stdevs = {}
    low_means = {}
    low_max = {}
    low_min = {}
    for key in unique_dates:
        # get indicies matching date
        indices = calendar_dates[calendar_dates[:]==key].index.tolist()
        all_highs[key] = highs[indices]
        all_lows[key] = lows[indices]
        high_medians[key],high_stdevs[key],high_means[key],high_max[key],high_min[key] = computeStats(highs[indices])
        low_medians[key],low_stdevs[key],low_means[key],low_max[key],low_min[key] = computeStats(lows[indices])

    return dates,calendar_dates,high_medians,high_stdevs,high_means,high_max,high_min,low_medians,\
        low_stdevs,low_means,low_max,low_min,highs,lows,all_highs,all_lows

# compute various statistics for a dataset
def computeStats(dataset):
    return np.median(dataset),np.std(dataset),np.mean(dataset),np.max(dataset),np.min(dataset)
