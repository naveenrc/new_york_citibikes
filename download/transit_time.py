# Compute transit times from one station to other
import requests
import pandas as pd
from itertools import combinations

def calc_transit(lat_lon):
    params = dict(origins="%s,%s" % (lat_lon[0][1],lat_lon[0][2]),
                  destinations="%s,%s" % (lat_lon[1][1],lat_lon[1][2]),
                  key='AIzaSyAp9x8pXPPesJdq0UcfiEY-698t8ruBtj4',
                  mode='bicycling')
    response = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json",params)
    content = response.json()
    data = content['rows'][0]['elements'][0]
    distance = data['distance']['value']
    transit = data['duration']['value']
    f = open(r'C:\Users\Naveen\Downloads\Springboard\GitHub\new_york_citibikes\data\transit.csv','a+')
    f.write("%s,%s,%f,%f,%f,%f,%d,%d\n"%(lat_lon[0][0],lat_lon[1][0],lat_lon[0][1],lat_lon[0][2],lat_lon[1][1],lat_lon[1][2],distance,transit))
    f.close()

if __name__ == '__main__':
    stations = pd.read_csv(r'C:\Users\Naveen\Downloads\Springboard\GitHub\new_york_citibikes\data\station_info.csv')
    lat_lon = [(sta_id,lat, lon) for sta_id,lat,lon in zip(stations['station_id'],stations['lat'], stations['lon'])]
    combs = [comb for comb in combinations(lat_lon,2)]
    for comb in combs[0:4]:
        calc_transit(comb)