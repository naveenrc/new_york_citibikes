import os
import pandas as pd
import time
from multiprocessing import Pool, Lock
import sys

# calculate rides by gender
def ridesbygender(file):
    # get file
    curdir = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/'+file)

    df['start_time'] = pd.to_datetime(df['start_time'])
    df['distance'] = df['trip_duration'].map(lambda x: (7.456*x)/3600 if x < 7200 else 14.9)
    df['start_time'] = pd.DatetimeIndex(df['start_time']).normalize()
    df.set_index('start_time',inplace=True)
    df1 = df.groupby(['start_time','gender'])['distance'].agg(['count','sum']).unstack()
    # number of rides by gender 0:unknown, 1:male, 2:female
    df2 = df1['count'].rename(columns={0:'un_rides',1:'male_rides',2:'female_rides'}).fillna(0)
    # distance travelled by gender
    df2 = df2.join(df1['sum'].rename(columns={0:'un_dist',1:'male_dist',2:'female_dist'}))
    df2['duration'] = df.groupby(['start_time'])['trip_duration'].agg(['sum']).unstack()['sum']

    # store result to a file protected by lock
    with lock:
        try:
            output = pd.read_csv(os.path.join(curdir, '../data/rides') + '/rides_count.csv')
            output.set_index('start_time',inplace=True)
            start_index = df2.index.values[0]
            end_index = df2.index.values[-1]
            if start_index in output.index.values:
                output.loc[start_index:end_index, :] = output.loc[start_index:end_index,:].combine(df2,func=lambda a, b: a + b,fill_value=0)
            else:
                output = pd.concat([output,df2])
            output.to_csv(os.path.join(curdir, '../data/rides') + '/rides_count.csv')
        except pd.errors.EmptyDataError:
            df2.to_csv(os.path.join(curdir, '../data/rides') + '/rides_count.csv')

def init_child(lock_):
    global lock
    lock = lock_


if __name__ == '__main__':
    curdir = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/cleaned_files.csv', header=None)
    files = df[0].tolist()
    f = open(os.path.join(curdir, '../data/rides') + '/rides_count.csv','w')
    f.close()

    t = time.time()
    lock = Lock()
    p = Pool(4, initializer=init_child, initargs=(lock,))
    # Display progress
    for i, _ in enumerate(p.imap_unordered(ridesbygender, files), 1):
        #        sys.stderr.write('\rdone {0:%}'.format(i / len(final_list[:2])))
        sys.stderr.write('\rdone {0:}'.format(i))
    p.close()
    p.join()
    print("\nCompleted in.....", time.time() - t)