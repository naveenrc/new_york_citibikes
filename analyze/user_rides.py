import os
import pandas as pd
import time
from multiprocessing import Pool, Lock
import sys

# calculate rides by user type 'Subscriber' and 'Pay per use'
def ridesbyuser(file):
    # get file
    curdir = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/'+file)

    # get start and end times of rides value counts, this is going to be popularity of stations
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['distance'] = df['trip_duration'].map(lambda x: (7.456*x)/3600 if x < 7200 else 14.9)
    df['start_time'] = pd.DatetimeIndex(df['start_time']).normalize()
    df.set_index('start_time',inplace=True)
    df1 = df.groupby(['start_time','user'])['bike_id'].agg(['count']).unstack()['count']
    df1 = df1.fillna(0)


    with lock:
        try:
            output = pd.read_csv(os.path.join(curdir, '../data/rides') + '/rides_user.csv')
            output.set_index('start_time',inplace=True)
            output = pd.concat([output,df1])
            output.to_csv(os.path.join(curdir, '../data/rides') + '/rides_user.csv')
        except pd.errors.EmptyDataError:
            df1.to_csv(os.path.join(curdir, '../data/rides') + '/rides_user.csv')


def init_child(lock_):
    global lock
    lock = lock_


if __name__ == '__main__':
    curdir = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/cleaned_files.csv', header=None)
    files = df[0].tolist()
    f = open(os.path.join(curdir, '../data/rides') + '/rides_user.csv','w')
    f.close()

    t = time.time()
    lock = Lock()
    p = Pool(4, initializer=init_child, initargs=(lock,))
    # Display progress
    for i, _ in enumerate(p.imap_unordered(ridesbyuser, files), 1):
        #        sys.stderr.write('\rdone {0:%}'.format(i / len(final_list[:2])))
        sys.stderr.write('\rdone {0:}'.format(i))
    p.close()
    p.join()
    print("\nCompleted in.....", time.time() - t)