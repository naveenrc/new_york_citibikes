import os
import pandas as pd
import time
from multiprocessing import Pool, Lock
import sys
import numpy as np


def ridesbyage(file):
    # get file
    curdir = os.path.dirname(__file__)
    df_birth = pd.read_csv(os.path.join(curdir, '../data/rides') + '/'+file)
    df_birth = df_birth[df_birth['user']=='Subscriber']
    df_birth['birth'] = pd.to_numeric(df_birth['birth'],errors='ignore').fillna(0)
    df_birth['birth'].replace('\\N',0,inplace=True)
    df_birth['birth'] = df_birth['birth'].astype(np.int64)
    df_birth = df_birth[df_birth['birth']>=1957]
    df_birth['age'] = 2017-df_birth['birth']
    rides = df_birth.groupby(['age'])['bike_id'].agg(['count']).unstack()['count']
    rides_df = pd.DataFrame({'age':rides.index,'rides':rides.values})
    rides_df.set_index('age',inplace=True)


    with lock:
        try:
            output = pd.read_csv(os.path.join(curdir, '../data/rides') + '/rides_age.csv')
            output.set_index('age',inplace=True)
            output = output.append(rides_df)
            output.to_csv(os.path.join(curdir, '../data/rides') + '/rides_age.csv')
        except pd.errors.EmptyDataError:
            rides_df.to_csv(os.path.join(curdir, '../data/rides') + '/rides_age.csv')


def init_child(lock_):
    global lock
    lock = lock_


if __name__ == '__main__':
    curdir = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/cleaned_files.csv', header=None)
    files = df[0].tolist()
    f = open(os.path.join(curdir, '../data/rides') + '/rides_age.csv','w')
    f.close()

    t = time.time()
    lock = Lock()
    p = Pool(4, initializer=init_child, initargs=(lock,))
    # Display progress
    for i, _ in enumerate(p.imap_unordered(ridesbyage, files), 1):
        #        sys.stderr.write('\rdone {0:%}'.format(i / len(final_list[:2])))
        sys.stderr.write('\rdone {0:}'.format(i))
    p.close()
    p.join()
    print("\nCompleted in.....", time.time() - t)