#!/usr/bin/env python
''' Temperature probabilities.

This temperature will compute the probability of temperatures occurring within a specified range as well
as exceedance probabilities. The temperature-within-range probabilities are computed by using a multivariate
distribution. This multivariate distribution is obtained by computing mean and covariance matrices from the
daily temperature data. The probabilities are finally determined by using a Monte Carlo simulation.

Version history:
    1.0: Initial build.
    1.1: Rewrote loop structures using pandas. Now uses climate tools version 2.0.
'''

# import modules
import climate_tools_v2
import numpy as np
import scipy.stats

__author__ = "Jason W. Godwin"
__copyright__ = "Public Domain"
__credits__ = ""

__license__ = "GPL"
__version__ = "1.1"
__maintainer__ = "Jason W. Godwin"
__email__ = "jasonwgodwin@gmail.com"
__status__ = "Production"

### USER SETTINGS SECTION BEGIN ###
climo_file = "dfw.csv"          # file path of CSV file containing climate data
station = "Dallas/Fort Worth"   # station name (i.e. "Dallas/Fort Worth", "DFW", "KDFW", etc.)
skip_header = True              # Does your CSV file have a header line?
### USER SETTINGS SECTION END (DO NOT EDIT BELOW THIS LINE UNLESS YOU REALLY KNOW WHAT YOU ARE DOING!) ###

# import climate data
print "Running climate statistics (this can take a few minutes for large datasets)"
dates,calendar_dates,high_medians,high_stdevs,high_means,high_max,high_min,low_medians,low_stdevs,\
    low_means,low_max,low_min,highs,lows,all_highs,all_lows = climate_tools_v2.climateStats(climo_file)

again = True
while again:
    # ask the user for the high and low temperatures
    high = float(raw_input("High temperature (degrees Fahrenheit): "))
    low = float(raw_input("Low temperature (degrees Fahrenheit): "))
    # ask the user for a date to check
    datecheck = raw_input("Date to check (MM/DD): ")
    
    # create multivariate normal distributions for each date to determine joint probability
    highdist = scipy.stats.norm(high_means[datecheck],high_stdevs[datecheck])       # normal distribution for high temperature
    lowdist = scipy.stats.norm(low_means[datecheck],low_stdevs[datecheck])          # normal distribution for low temperature
    prob_high = 1.0 - highdist.cdf(high)                         # probability of exceeding high temperature
    prob_low = lowdist.cdf(low)                                  # probability of not exceeding low temperature

    # perturbation temperature matrix
    temp_perturbation = np.array([all_highs[datecheck]-high_means[datecheck],all_lows[datecheck]-low_means[datecheck]])

    # mean temperature matrix
    temp_mean = np.array([high_means[datecheck],low_means[datecheck]])

    # covariance matrix
    temp_covariance = np.dot(temp_perturbation,np.transpose(temp_perturbation)) / (np.shape(temp_perturbation)[1] - 1.0)

    # multivariate normal distribution
    multivariate_dist = np.random.multivariate_normal(temp_mean,temp_covariance,10000)
    diurnal_range = lambda r: r[0] < high and r[1] > low
    montecarlo = np.apply_along_axis(diurnal_range,1,multivariate_dist).sum() / 10000.0

    # print the results    
    print "Probability of exeeding %.0f F on %s: %.1f%%" % (high,datecheck,100.0*prob_high)
    print "Probability of temperature falling below %.0f F on %s: %.1f%%" % (low,datecheck,100.0*prob_low)
    print "Probability of tempertature falling within range on %s: %.1f%%" % (datecheck,100.0*montecarlo)

    # compute percentile ranks for given date
    print "\nPercentile rank of high temperature: %.1f" % scipy.stats.percentileofscore(all_highs[datecheck],high,kind="mean")
    print "Percentile rank of low temperature: %.1f\n" % scipy.stats.percentileofscore(all_lows[datecheck],low,kind="mean")

    # ask the user if they want another search
    again = raw_input("Search for another date or temperature? (Y/y or N/n)? ")
    print "\n"
    if again.lower() != "y":
        again = False
