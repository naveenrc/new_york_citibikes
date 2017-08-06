import pandas as pd
import os
import numpy as np


def func(x):
    x.reset_index(inplace=True)
    return max((x['start_sta_id'] != x['end_sta_id'].shift()).cumsum(skipna=True))-1

def transported_bikes(file):
    curdir = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/'+file)
    df['transported'] = 0
    transported = df.groupby('bike_id').agg(func)['transported']
    print(sum(transported.values))

if __name__ == '__main__':
    curdir = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/cleaned_files.csv', header=None)
    files = df[0].tolist()
    transported_bikes(files[63])