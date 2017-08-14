import os
import pandas as pd


def weather():
    curdir = os.path.dirname(__file__)
    weather_df = pd.read_csv(os.path.join(curdir, '../data/weather') + '/weather.csv')
    weather_df['start_time'] = pd.to_datetime(weather_df['DATE'].astype(str), format='%Y%m%d')
    weather_df.set_index('start_time', inplace=True)
    weather_df.drop(['DATE'], axis=1, inplace=True)
    weather_df['TAVG'] = (weather_df['TMAX'] + weather_df['TMIN']) / 2
    weather_df.drop(['TMAX', 'TMIN', 'WT14', 'WT04', 'WT16'], axis=1, inplace=True)
    weather_df.reset_index(inplace=True)
    return weather_df


def station():
    curdir = os.path.dirname(__file__)
    station_df = pd.read_csv(os.path.join(curdir, '../data/') + 'station_info.csv')
    return station_df

if __name__ == '__main__':
    print(weather().head())
    print(station().head())