import pandas
import datetime
import numpy as np

# import data
headers = ['date','high','low','precip']
dtypes = {'date':'str','high':'float','low':'float','precip':'str'}
df = pandas.read_csv("dfw_new.csv",header=None,names=headers,dtype=dtypes)

# convert date string formats
dates = df['date']
new_dates = [datetime.datetime.strptime(x,'%m%d%Y') for x in dates]
final_dates = [datetime.datetime.strftime(y,'%m/%d/%Y') for y in new_dates]

# remove leading zeros from month
for i in range(len(final_dates)):
    if final_dates[i][0] == '0':
        final_dates[i] = final_dates[i][1:]

# create final dataframe
final_df = pandas.DataFrame({'dates':final_dates,'highs':df['high'],'lows':df['low'],'precip':df['precip']})

# output dataframe to csv
final_df.to_csv('dfw_final.csv',columns=['dates','highs','lows','precip'],index=False)
