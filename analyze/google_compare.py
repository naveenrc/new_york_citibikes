import os
import pandas as pd


curdir = os.path.dirname(__file__)
transit = pd.read_csv(os.path.join(curdir, '../data') + '/transit_cleaned.csv')

transit['duration'] = transit['duration']/3600
transit['distance'] = transit['distance']/1609.34

avg_time = sum(transit['distance'])/sum(transit['duration'])
time_citi = 7.456
print(avg_time-time_citi)