#!/usr/bin/env python
''' Runs statistics on daily high/low temperatures for a single station.

This program will read in a CSV file (format: date,calendar date,high,low,precip) of daily high and low
temperatures for every day in a single station's climate history. The script will then compute various
statistics including median, standard deviation, percentile ranks, records, and means for each calendar
date (i.e. all January 1sts, 2nds, etc.). The script will generate histograms of the high/low distributions
for each date, then finally create plots showing each stat throughout the year. This script will also create
a polynomial fit of each statistic to make a smoother plot (the degree of the polynomial can be determined
by the user (see the "USER SETTINGS SECTION" below for more details).

Version history:
1.0 (2017 June 22): Initial build.
'''

# import modules
import csv
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

__author__ = "Jason W. Godwin"
__copyright__ = "Public Domain"
__credits__ = ""

__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jason W. Godwin"
__email__ = "jasonwgodwin@gmail.com"
__status__ = "Production"

### USER SETTINGS SECTION BEGIN ###
climo_file = "dfw.csv"          # file path of CSV file containing climate data
annual_file = "dfw_stats.csv"   # file path of output CSV file that will contain stats for each day
station = "Dallas/Fort Worth"   # station name (i.e. "Dallas/Fort Worth", "DFW", "KDFW", etc.)
skip_header = True              # Does your CSV file have a header line?
temp_intvl = 5                  # bin interval for histogram plots
polydegree = 5                  # degree of polynomial fit
testmode = False                # set to True or False: enabled, this will stop the script after January
lower_pct = 10                  # lower percentile to computer (whole percent: i.e. 25th Percentile is entered as "25")
upper_pct = 90                  # upper percentile (as above)
### USER SETTINGS SECTION END (DO NOT EDIT BELOW THIS LINE UNLESS YOU REALLY KNOW WHAT YOU ARE DOING!) ###

# declare a bunch of lists
dates = []
high_medians = []   # median high temperatures for each date
high_stdevs = []    # standard deviation of high temperatures
high_lowers = []    # lower percentile rank for high temperatures
high_uppers = []    # upper percentile rank for high temperatures
high_means = []     # mean high temperatures
low_medians = []    # median low temperatures
low_stdevs = []     # standard deviation of low temperatures
low_lowers = []     # lower percentile rank for low temperatures
low_uppers = []     # upper percentile rank for low temperatures
low_means = []      # mean low temperatures
high_max = []       # record maximum high temperatures
high_min = []       # record minimum high temperatures (i.e. lowest max temp for a day)
low_max = []        # record maximum low temperatures (i.e. highest min temp for a day)
low_min = []        # record minimum low temperatures
actualdate = []     # actual date of record (i.e. M/D/Y)

# loop structure for going through every valid calendar date
for month in range(1,13):
    # interupt after January if in test mode
    if month == 2 and testmode:
        break

    # get correct number of days for each month
    if month in [1,3,5,7,8,10,12]:
        days = 32
    elif month in [4,6,9,11]:
        days = 31
    elif month == 2:
        days = 30
    else:
        raise Exception("Invalid month!")

    # loop through every valid date within each month
    for day in range(1,days):
        if len(str(month)) < 2:
            month = "0" + str(month)
        if len(str(day)) < 2:
            day = "0" + str(day)

        user_date = str(month) + "/" + str(day)
        print user_date

        # variables that will be reset for each calendar date
        highs = []  # daily high temperatures
        lows = []   # daily low temperatures
        precip = [] # precipitation accumulation (unused at the moment)

        # open the CSV file
        reader = csv.reader(open(climo_file,"r"))

        # import data from the CSV file
        for row in reader:
            if skip_header:
                skip_header = False
                continue
            date = row[1]
            if date == user_date:
                actualdate.append(datetime.strptime(row[0],"%m/%d/%Y"))
                highs.append(float(row[2]))
                lows.append(float(row[3]))
                precip.append(float(row[4]))

        # compute stats
        fields = [highs,lows]
        labels = ["High","Low"]

        for i in range(len(fields)):
            # calculate stats
            median = np.median(fields[i])               # median temperature
            stdev = np.std(fields[i])                   # standard deviation of temperatures
            lower = np.percentile(fields[i],lower_pct)  # lower percentile rank for temperatures
            upper = np.percentile(fields[i],upper_pct)  # upper percentile rank for temperatures
            mean = np.mean(fields[i])                   # mean temperature
            recordmax = np.max(fields[i])               # record maximum high/low temperature
            recordmin = np.min(fields[i])               # record minimum high/low temperature

            # sort the stats into the right category
            if labels[i] == "High":
                dates.append(user_date)
                high_medians.append(median)
                high_stdevs.append(stdev)
                high_lowers.append(lower)
                high_uppers.append(upper)
                high_means.append(mean)
                high_max.append(recordmax)
                high_min.append(recordmin)
            else:
                low_medians.append(median)
                low_stdevs.append(stdev)
                low_lowers.append(lower)
                low_uppers.append(upper)
                low_means.append(mean)
                low_max.append(recordmax)
                low_min.append(recordmin)
                
            # setup the bins for the histogram
            if np.min(fields[i]) % temp_intvl != 0:
                binmin = temp_intvl * round(np.min(fields[i]) / temp_intvl) - temp_intvl
            else:
                binmin = np.min(fields[i]) + temp_intvl

            if np.max(fields[i]) % temp_intvl != 0:
                binmax = temp_intvl * round(np.max(fields[i]) / temp_intvl) + temp_intvl
            else:
                binmax = np.max(fields[i]) + temp_intvl

            bins = np.arange(binmin,binmax+1,temp_intvl)

            # plot the histogram
            plt.hist(fields[i],bins,histtype="bar",color="gray")
            plt.axvline(x=median,color="red")
            plt.title("Median: %.0f | 10th Percentile: %.0f | 90th Percentile: %.0f | Standard Deviation: %.1f" % (median,lower,upper,stdev),size="x-small")
            plt.axvline(x=upper,color="red",linestyle="--")
            plt.axvline(x=lower,color="red",linestyle="--")
            plt.yticks(np.arange(0,41,5))
            plt.xticks(np.arange(-5,115,5),rotation=90,size="x-small")
            plt.grid()
            plt.suptitle("%s Temperature Distribution for %s (period of record: %i-%i)" % (labels[i],user_date,min(actualdate).year,max(actualdate).year))
            filename = "images/" + labels[i] + user_date.replace("/","_") + ".png"
            plt.savefig(filename,bbox_inches="tight")
            plt.clf()

# create an output CSV file for the statistics for later use
with open(annual_file,"wb") as csvfile:
    statwriter = csv.writer(csvfile,delimiter=",")
    for x in range(len(dates)):
        stuff = [dates[x],high_medians[x],high_means[x],high_stdevs[x],high_lowers[x],high_uppers[x],high_max[x],high_min[x],low_medians[x],low_means[x],low_stdevs[x],low_lowers[x],low_uppers[x],low_max[x],low_min[x]]
        statwriter.writerow(stuff)

# read in the annual stats file
reader = csv.reader(open(annual_file,"r"))

# initiate "clean" variables to be read in (same definitions as above)
dates = []
median_highs = []
mean_highs = []
stdev_highs = []
lower_highs = []
upper_highs = []
max_highs = []
min_highs = []
median_lows = []
mean_lows = []
stdev_lows = []
lower_lows = []
upper_lows = []
max_lows = []
min_lows = []

# read in the file for each data
for row in reader:
    # skip leap days since the sample size will be small
    if row[0] == "02/29":
        continue
    dates.append(row[0])
    median_highs.append(float(row[1]))
    mean_highs.append(float(row[2]))
    stdev_highs.append(float(row[3]))
    lower_highs.append(float(row[4]))
    upper_highs.append(float(row[5]))
    max_highs.append(float(row[6]))
    min_highs.append(float(row[7]))
    median_lows.append(float(row[8]))
    mean_lows.append(float(row[9]))
    stdev_lows.append(float(row[10]))
    lower_lows.append(float(row[11]))
    upper_lows.append(float(row[12]))
    max_lows.append(float(row[13]))
    min_lows.append(float(row[14]))

# plotting routine for raw, unsmoothed data
plt.clf()
# figure setup
fig = plt.figure(figsize=(16,12),dpi=80,edgecolor="k")
ax = fig.add_subplot(1,1,1)
major_ticks = np.arange(-10,121,10)
minor_ticks = np.arange(-10,121,5)
ax.set_xticks(np.arange(len(dates)))
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks,minor=True)
ax.grid(which="both")
ax.grid(which="major",alpha=1.0)
ax.grid(which="minor",alpha=0.2)
dummies = np.arange(len(dates))
# create shaded area for percentile range
ax.fill_between(dummies,lower_highs,upper_highs,facecolor="red",interpolate=True,alpha=0.2)
ax.fill_between(dummies,lower_lows,upper_lows,facecolor="blue",interpolate=True,alpha=0.2)
# plot daily data
plt.plot(dummies,median_highs,color="red",linestyle="",marker="o",label="Median High")      # daily median highs
plt.plot(dummies,median_lows,color="blue",linestyle="",marker="o",label="Median Low")       # daily median lows
plt.plot(dummies,max_highs,color="red",linestyle="-",linewidth=4.0,label="Record Highs")    # daily record highs
plt.plot(dummies,min_lows,color="blue",linestyle="-",linewidth=4.0,label="Record Lows")     # daily record lows
# plot aesthetics
plt.xticks(dummies[::30],dates[::30],rotation=90)
plt.xlim([0,364])
plt.ylim([-10,120])
plt.xlabel("Calendar Day")
plt.ylabel("Temperature (degrees Fahrenheit)")
plt.title("Temperature Climatology for Dallas/Fort Worth (period of record: %i - %i)" % (min(actualdate).year,max(actualdate).year))
plt.legend(bbox_to_anchor=(1,1),loc="upper left",ncol=1,fontsize="x-small")
# freezing and 100 F lines
plt.axhline(y=32,xmin=0,xmax=364,color="cyan")
plt.text(182,32.5,"32 F")
plt.axhline(y=100,xmin=0,xmax=364,color="magenta")
plt.text(182,100.5,"100 F")
# save the figure
plt.savefig("temperatures.png",bbox_inches="tight")
plt.clf()

# plot the standard deviation throughout the year
# figure setup
fig = plt.figure(figsize=(16,12),dpi=80,edgecolor="k")
ax = fig.add_subplot(1,1,1)
major_ticks = np.arange(0,15.01,0.5)
minor_ticks = np.arange(0,15.01,0.1)
ax.set_xticks(np.arange(len(dates)))
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks,minor=True)
ax.grid(which="both")
ax.grid(which="major",alpha=1.0)
ax.grid(which="minor",alpha=0.2)
dummies = np.arange(len(dates))
# plot the daily standard deviations
plt.plot(dummies,stdev_highs,color="red",linestyle="-",linewidth=4.0,label="Highs")
plt.plot(dummies,stdev_lows,color="blue",linestyle="-",linewidth=4.0,label="Lows")
# plot aesthetics
plt.xticks(dummies[::30],dates[::30],rotation=90)
plt.xlim([0,364])
plt.ylim([0,15])
plt.xlabel("Calendar Day")
plt.ylabel("Standard Deviation (degrees Fahrenheit)")
plt.title("Daily Temperature Standard Deviation for %s (period of record: %i - %i)" % (station,min(actualdate).year,max(actualdate).year))
plt.legend(bbox_to_anchor=(1,1),loc="upper left",ncol=1,fontsize="x-small")
# save the figure
plt.savefig("stdevs.png",bbox_inches="tight")
plt.clf()

# smoothed plots
x = 0
ys = []

# get the polynomial fit for each dataset
for var in [lower_highs,upper_highs,lower_lows,upper_lows,median_highs,median_lows,max_highs,min_lows]:
    coefficients = np.polyfit(dummies,var,int(polydegree))
    polynomial = np.poly1d(coefficients)
    ys.append(polynomial(dummies))
    x += 1

plt.clf()
# figure setup
fig = plt.figure(figsize=(16,12),dpi=80,edgecolor="k")
ax = fig.add_subplot(1,1,1)
major_ticks = np.arange(-10,121,10)
minor_ticks = np.arange(-10,121,5)
ax.set_xticks(np.arange(len(dates)))
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks,minor=True)
ax.grid(which="both")
ax.grid(which="major",alpha=1.0)
ax.grid(which="minor",alpha=0.2)

# create shaded area for percentile range
ax.fill_between(dummies,ys[0],ys[1],facecolor="red",interpolate=True,alpha=0.2)
ax.fill_between(dummies,ys[2],ys[3],facecolor="blue",interpolate=True,alpha=0.2)
# plot daily data
plt.plot(dummies,ys[4],color="red",linestyle="-",linewidth=2,label="Median High")       # daily median highs
plt.plot(dummies,ys[5],color="blue",linestyle="-",linewidth=2,label="Median Low")       # daily median lows
plt.plot(dummies,ys[6],color="red",linestyle="-",linewidth=4.0,label="Record Highs")    # daily record highs
plt.plot(dummies,ys[7],color="blue",linestyle="-",linewidth=4.0,label="Record Lows")    # daily record lows
# plot aesthetics
plt.xticks(dummies[::30],dates[::30],rotation=90)
plt.xlim([0,364])
plt.ylim([-10,120])
plt.xlabel("Calendar Day")
plt.ylabel("Temperature (degrees Fahrenheit)")
plt.title("Temperature Climatology for Dallas/Fort Worth (%sth degree polynomial fit, period of record: %i - %i)" % (polydegree,min(actualdate).year,max(actualdate).year))
plt.legend(bbox_to_anchor=(1,1),loc="upper left",ncol=1,fontsize="x-small")
# freezing and 100 F lines
plt.axhline(y=32,xmin=0,xmax=364,color="cyan")
plt.text(182,32.5,"32 F")
plt.axhline(y=100,xmin=0,xmax=364,color="magenta")
plt.text(182,100.5,"100 F")
# save the figure
plt.savefig("polyfit.png",bbox_inches="tight")
plt.clf()

print("Done")
