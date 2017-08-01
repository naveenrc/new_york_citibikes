# Compute transit times from one station to other using Google Distance Matrix API
import requests
import pandas as pd
import time
from multiprocessing import Pool, Lock
import sys

#API request and write to file
def calc_transit(lat_lon):
    # parse destinations
    destinations = ''
    for i in lat_lon[1:]:
        destinations = destinations + "%s,%s|" % (i[1], i[2])
    destinations = destinations.rstrip(destinations[-1])

    params = dict(origins="%s,%s" % (lat_lon[0][1], lat_lon[0][2]),
                  destinations=destinations,
                  key='Enter your key here',
                  mode='bicycling')
    response = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json", params)
    content = response.json()
    try:
        data = content['rows'][0]['elements']
    except IndexError:
        data = []

    transits = []
    with lock:
        for idx, d in enumerate(data, 1):
            try:
                transits.append(
                    "%d,%d,%d,%d\n" % (lat_lon[0][0], lat_lon[idx][0], d['duration']['value'], d['distance']['value']))
                f = open(r'C:\Users\Naveen\Downloads\Springboard\GitHub\new_york_citibikes\data\transit.csv', 'a+')
                for transit in transits:
                    f.write(transit)
                f.close()
            except KeyError:
                pass
            except IndexError:
                pass


def init_child(lock_):
    global lock
    lock = lock_


if __name__ == '__main__':
    stations = pd.read_csv(r'C:\Users\Naveen\Downloads\Springboard\GitHub\new_york_citibikes\data\station_info.csv')
    lat_lon = [(sta_id, lat, lon) for sta_id, lat, lon in zip(stations['station_id'], stations['lat'], stations['lon'])]
    len_list = len(lat_lon)

    final_list = []
    for i in range(len_list):
        for j in range(i + 1, len_list, 24):
            temp = [0 for i in range(25)]
            temp[0] = lat_lon[i]
            temp[1:] = lat_lon[j:j + 24]
            final_list.append(temp)

    t = time.time()
    lock = Lock()
    p = Pool(4, initializer=init_child, initargs=(lock,))
    # Display progress
    for i, _ in enumerate(p.imap_unordered(calc_transit, final_list), 1):
        #        sys.stderr.write('\rdone {0:%}'.format(i / len(final_list[:2])))
        sys.stderr.write('\rdone {0:}'.format(i))
    p.close()
    p.join()
    print("\nCompleted in.....", time.time() - t)