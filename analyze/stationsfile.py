import pandas as pd
import os
from plot_stations import mercator_df


curdir = os.path.dirname(__file__)
# get station info dataframe with 668 stations(id, lat, lon, name)
stationdf = mercator_df()
stationdf.to_csv(os.path.join(curdir, '../data/rides') + '/stationdf.csv')
print('Done')