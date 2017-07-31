import requests
import pandas as pd

# This url provides info about stations
response = requests.get('https://gbfs.citibikenyc.com/gbfs/en/station_information.json')
content = response.json()
# get stations info from response
stations = content['data']['stations']
# convert it to dataframe
data = pd.DataFrame(stations)
data = data.drop(["capacity", "rental_methods", "short_name", "eightd_has_key_dispenser"], axis=1)
data = data.set_index('station_id')

# write to file
path = input("Enter path with forward slashes inside it:")
data.to_csv(path + "/station_info.csv")