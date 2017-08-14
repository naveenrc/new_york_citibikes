import pandas as pd
import os
import time
from multiprocessing import Pool, Lock
import sys
from files_df import weather


def func(x):
    x.reset_index(inplace=True)
    # compare previous end station id to current start station id to check if both are same
    # calculate cumsum and get max value, this is the number of bikes that are transported on that day
    #subtract 1 because the first value is counted 1, which is excess
    temp = []
    for idx,i in enumerate(x['start_sta_id'] != x['end_sta_id'].shift()):
        if i:
            temp.append([x.loc[idx,'start_sta_id'], x.loc[idx,'hour']])
    return temp[1:]

def listtodf(lists):
    temp = []
    for list in lists:
        for sublist in list:
            temp.append(sublist)
    df = pd.DataFrame({'station':[x[0] for x in temp],'hour':[x[1] for x in temp]})
    df.set_index('hour', inplace=True)
    return df


def groups_year():
    curdir = os.path.dirname(__file__)
    transports = pd.read_csv(os.path.join(curdir, '../data/rides') + '/transported_hour.csv')
    transports['hour'] = pd.to_datetime(transports['hour']).map(lambda t: t.strftime('%Y-%m-%d %H'))
    transports['count'] = 1
    result = transports.groupby(['station','hour']).agg('count')
    result.to_csv(os.path.join(curdir, '../data/rides') + '/transported_hour1.csv')


def data():
    curdir = os.path.dirname(__file__)
    transports = pd.read_csv(os.path.join(curdir, '../data/rides') + '/transported_hour1.csv')
    transports['date_int'] = pd.to_datetime(transports['hour']).map(lambda t: t.strftime('%m%d%H')).astype(int)
    transports['normal_date'] = pd.DatetimeIndex(pd.to_datetime(transports['hour'])).normalize()
    weather_df = weather()
    transports = transports.merge(weather_df,left_on='normal_date',right_on='start_time')
    transports.drop(['hour','start_time'],axis=1,inplace=True)
    transports.sort_values(['station','date_int'],inplace=True)
    transports.set_index('station',inplace=True)
    transports.to_csv(os.path.join(curdir, '../data/rides') + '/transported_hour_data.csv')


def transports_station(file):
    curdir = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(curdir, '../data/rides/') + file)
    df['day'] = pd.DatetimeIndex(pd.to_datetime(df['start_time'])).normalize()
    df['hour'] = pd.to_datetime(df['start_time']).map(lambda t: t.strftime('%Y-%m-%d %H'))
    result = df.groupby(['day','bike_id']).agg(func).values
    result = [x for x in result if x != []]
    result = listtodf(result)
    with lock:
        try:
            output = pd.read_csv(os.path.join(curdir, '../data/rides') + '/transported_hour.csv')
            output.set_index('hour',inplace=True)
            output = output.append(result)
            output.to_csv(os.path.join(curdir, '../data/rides') + '/transported_hour.csv')
        except pd.errors.EmptyDataError:
            result.to_csv(os.path.join(curdir, '../data/rides') + '/transported_hour.csv')


def init_child(lock_):
    global lock
    lock = lock_


if __name__ == '__main__':
    curdir = os.path.dirname(__file__)
    '''
    df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/cleaned_files.csv', header=None)
    files = df[0].tolist()
    f = open(os.path.join(curdir, '../data/rides') + '/transported_hour.csv', 'w')

    t = time.time()
    lock = Lock()
    p = Pool(4, initializer=init_child, initargs=(lock,))
    # Display progress
    for i, _ in enumerate(p.imap_unordered(transports_station, files), 1):
        #        sys.stderr.write('\rdone {0:%}'.format(i / len(final_list[:2])))
        sys.stderr.write('\rdone {0:}'.format(i))
    p.close()
    p.join()
    print("\nCompleted in.....", time.time() - t)

    groups_year()
    '''
    data()