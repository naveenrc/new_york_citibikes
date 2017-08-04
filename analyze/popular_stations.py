import os
import pandas as pd
from nyctile import nyc_map
from plot_stations import mercator_df
from bokeh.io import show
from bokeh.layouts import column
from bokeh.models import CustomJS, ColumnDataSource, Slider, HoverTool
from bokeh.models.glyphs import Circle, Text
import time
from multiprocessing import Pool, Lock
import sys


def popular_stations(file):
    # get file
    curdir = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/'+file)

    # get start and end times of rides value counts, this is going to be popularity of stations
    df['start_time'] = pd.to_datetime(df['start_time'])
    date = 100 * df.loc[0, 'start_time'].year + df.loc[0, 'start_time'].month
    starts = df['start_sta_id'].value_counts()
    ends = df['end_sta_id'].value_counts()
    # Convert these Serires objects to dataframes
    starts_df = pd.DataFrame({'station_id':starts.index, 'count1':starts.values})
    ends_df = pd.DataFrame({'station_id': ends.index, 'count2': ends.values})

    with lock:
        # join start time and end time value counts on station id to station info df, new dataframe is count
        stationdf = pd.read_csv(os.path.join(curdir, '../data/rides') + '/stationdf.csv')
        count = stationdf.set_index('station_id').join(starts_df.set_index('station_id'))
        count = count.fillna(0)
        count = count.join(ends_df.set_index('station_id'))
        count = count.fillna(0)

        if 'count'+str(date) in count.columns:
            count['count' + str(date)] = count['count'+str(date)] + count['count1'] + count['count2']
            count.drop(['count1', 'count2'], axis=1, inplace=True)
        else:
            count['count'+str(date)] = count['count1'] + count['count2']
            count.drop(['count1', 'count2'], axis=1, inplace=True)

        # colors for Jersey city and NYC regions
        fill_color = {70: 'blue', 71: 'firebrick'}
        line_color = {70: 'blue', 71: 'firebrick'}
        count["fill"] = count['region_id'].map(lambda x: fill_color[x])
        count["line"] = count['region_id'].map(lambda x: line_color[x])
        count['transform'+str(date)] = count['count'+str(date)]/1000+3
        count['count']=count['count'+str(date)]
        count['transform']=count['transform'+str(date)]
        count.to_csv(os.path.join(curdir, '../data/rides') + '/stationdf.csv')


def init_child(lock_):
    global lock
    lock = lock_


if __name__ == '__main__':
    curdir = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/cleaned_files.csv', header=None)
    files = df[0].tolist()

    t = time.time()
    lock = Lock()
    p = Pool(4, initializer=init_child, initargs=(lock,))
    # Display progress
    for i, _ in enumerate(p.imap_unordered(popular_stations, files), 1):
        #        sys.stderr.write('\rdone {0:%}'.format(i / len(final_list[:2])))
        sys.stderr.write('\rdone {0:}'.format(i))
    p.close()
    p.join()
    print("\nCompleted in.....", time.time() - t)