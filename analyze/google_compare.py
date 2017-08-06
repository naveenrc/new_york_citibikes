import os
import pandas as pd


curdir = os.path.dirname(__file__)
transit = pd.read_csv(os.path.join(curdir, '../data') + '/transit_cleaned.csv')

transit['duration'] = transit['duration']/3600
transit['distance'] = transit['distance']/1609.34
#avg google transit speed
avg_time = sum(transit['distance'])/sum(transit['duration'])
#citi bike avg. speed
time_citi = 7.456
print('Difference between google and citi bike, google exceeds by',avg_time-time_citi,'miles per hour')