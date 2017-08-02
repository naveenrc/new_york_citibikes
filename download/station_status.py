import requests
import pandas as pd

# This url provides info about stations
response = requests.get('https://gbfs.citibikenyc.com/gbfs/en/station_status.json')
content = response.json()
# get stations info from response
stations = content['data']['stations']
# convert it to dataframe
data = pd.DataFrame(stations)
# print(data.head())

# write to file
path = input("Enter path: ")
data.to_csv(r''+path + "\station_status.csv")
