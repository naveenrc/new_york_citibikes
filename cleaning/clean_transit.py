import pandas as pd

path = r'C:\Users\Naveen\Downloads\Springboard\GitHub\new_york_citibikes\data\transit.csv'
df = pd.read_csv(path,header=None)
df.drop_duplicates(keep='first', inplace=True)
df = df.rename(columns={0:'start_sta_id', 1:'end_sta_id', 2:'duration', 3:'distance'})
df.reset_index(inplace=True)
df.drop('index',axis=1,inplace=True)
print(df.info())

write_path = r'C:\Users\Naveen\Downloads\Springboard\GitHub\new_york_citibikes\data\transit_cleaned.csv'
df.to_csv(write_path)