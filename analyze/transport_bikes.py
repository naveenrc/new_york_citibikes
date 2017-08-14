import pandas as pd
import os
import time
from multiprocessing import Pool, Lock
import sys


def func(x):
    x.reset_index(inplace=True)
    # compare previous end station id to current start station id to check if both are same
    # calculate cumsum and get max value, this is the number of bikes that are transported on that day
    # subtract 1 because the first value is counted 1, which is excess
    return max((x['start_sta_id'] != x['end_sta_id'].shift()).cumsum(skipna=True))-1


def transported_bikes(file):
    curdir = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/'+file)
    df['date'] = pd.DatetimeIndex(pd.to_datetime(df['start_time'])).normalize()
    # group by date and bike id then use
    # custom aggregate function
    transported = df.groupby(['date', 'bike_id']).agg(func).unstack()
    transported = transported.sum(axis=1, skipna=True, numeric_only=True)
    transported = pd.DataFrame({'date': transported.index, 'count': transported.values})
    transported.set_index('date', inplace=True)

    with lock:
        try:
            output = pd.read_csv(os.path.join(curdir, '../data/rides') + '/transported.csv')
            output.set_index('date', inplace=True)
            output = output.append(transported)
            output.to_csv(os.path.join(curdir, '../data/rides') + '/transported.csv')
        except pd.errors.EmptyDataError:
            transported.to_csv(os.path.join(curdir, '../data/rides') + '/transported.csv')


def init_child(lock_):
    global lock
    lock = lock_


if __name__ == '__main__':
    curdir = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/cleaned_files.csv', header=None)
    files = df[0].tolist()
    f = open(os.path.join(curdir, '../data/rides') + '/transported.csv', 'w')

    t = time.time()
    lock = Lock()
    p = Pool(4, initializer=init_child, initargs=(lock,))
    # Display progress
    for i, _ in enumerate(p.imap_unordered(transported_bikes, files), 1):
        #        sys.stderr.write('\rdone {0:%}'.format(i / len(final_list[:2])))
        sys.stderr.write('\rdone {0:}'.format(i))
    p.close()
    p.join()
    print("\nCompleted in.....", time.time() - t)