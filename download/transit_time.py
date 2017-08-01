# Compute transit times from one station to other
import requests
import pandas as pd
from itertools import combinations

def calc_transit(lat_lon):
    #parse destinations
    destinations = ''
    for i in lat_lon[1:]:
        destinations = destinations + "%s,%s|" % (i[1], i[2])
    destinations = destinations.rstrip(destinations[-1])

    params = dict(origins="%s,%s" % (lat_lon[0][1],lat_lon[0][2]),
                  destinations=destinations,
                  key='AIzaSyAp9x8pXPPesJdq0UcfiEY-698t8ruBtj4',
                  mode='bicycling')
    response = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json",params)
    content = response.json()
    data = content['rows'][0]['elements']
    transits = []
    for idx, d in enumerate(data,1):
        transits.append("%d,%d,%d,%d\n"%(lat_lon[0][0],lat_lon[idx][0],d['duration']['value'],d['distance']['value']))


    f = open(r'C:\Users\Naveen\Downloads\Springboard\GitHub\new_york_citibikes\data\transit.csv','w')
    for transit in transits:
        f.write(transit)
    f.close()

if __name__ == '__main__':
    stations = pd.read_csv(r'C:\Users\Naveen\Downloads\Springboard\GitHub\new_york_citibikes\data\station_info.csv')
    lat_lon = [(sta_id,lat, lon) for sta_id,lat,lon in zip(stations['station_id'],stations['lat'], stations['lon'])]
    len_list = len(lat_lon)

    final_list = []
    for i in range(len_list):
        for j in range(i+1, len_list,24):
            temp = [0 for i in range(25)]
            temp[0] = lat_lon[i]
            temp[1:25] = lat_lon[j:j+24]
            final_list.append(temp)

    calc_transit(final_list[0])