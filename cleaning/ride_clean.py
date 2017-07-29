# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 10:46:26 2017

@author: Naveen
"""
from __future__ import division
import pandas as pds
import numpy as npy
import chardet

import json
from multiprocessing import Pool
import time

import sys

def clean(file):
    path = 'C:/Users/Naveen/Downloads/Springboard/GitHub/new_york_citibikes/data/rides/'
    ftype = chardet.detect(open(path+file,'rb').read())['encoding'] #detect file encoding type
    data = pds.read_csv(path+file,encoding = ftype)
    
    temp = data.copy(deep=True)
    
    #Replace old column names with new names
    old_names = temp.columns
    new_names = ['trip_duration','start_time','stop_time','start_sta_id',\
                 'start_sta_name','start_sta_lat','start_sta_lon',\
                 'end_sta_id','end_sta_name','end_sta_lat','end_sta_lon',\
                 'bike_id','user','birth','gender']
    col_rename_dict = {i:j for i,j in zip(old_names,new_names)}
    temp.rename(columns=col_rename_dict,inplace=True)
    
    #Convert time stamps to datetime
    temp.start_time = pds.to_datetime(temp.start_time,errors='ignore')
    temp.stop_time = pds.to_datetime(temp.stop_time,errors='ignore')
    #Station id missing fields are filled with 0
    temp.start_sta_id = temp.start_sta_id.fillna(0)
    #Station name missing fields are filled with ''
    temp.start_sta_name = temp.start_sta_name.fillna('')
    #These are the most critical
    #Check to see if coordinates fall in the list, which are NYC latitudes and longitudes
    temp = temp[temp.start_sta_lat.apply(lambda x: npy.floor(x) in [39,40,41])]
    temp = temp[temp.start_sta_lon.apply(lambda x: npy.ceil(x) in [-72,-73,-74,-75])]
    
    temp.end_sta_id = temp.end_sta_id.fillna(0)
    temp.end_sta_name = temp.end_sta_name.fillna('')
    temp = temp[temp.end_sta_lat.apply(lambda x: npy.floor(x) in [39,40,41])]
    temp = temp[temp.end_sta_lon.apply(lambda x: npy.ceil(x) in [-72,-73,-74,-75])]
    
    temp.bike_id.fillna('0')
    temp.user = temp.user.fillna(method='bfill')
    #Missing birth fields with 0
    temp.birth = temp.birth.fillna(0)
    temp.gender = temp.gender.fillna(method='ffill')
    temp.dropna(axis=0)
    
    #Write output to a file
    file_name = str(file).split('.')[0]
    temp.to_csv(path+file_name+'_cleaned.csv',encoding=ftype,header=True,index=False)
    


if __name__ == '__main__':
    
    f = open('C:/Users/Naveen/Downloads/Springboard/GitHub/new_york_citibikes/data/rides/extracted.json','r')
    file_names = json.load(f)
    f.close()
    names = list(file_names.keys())
    
    #Multiprocessing
    t = time.time()
    p = Pool()
    #Display progress
    for i, _ in enumerate(p.imap_unordered(clean, names), 1):
        sys.stderr.write('\rdone {0:%}'.format(i/len(names)))
    p.close()
    p.join()
    print("Completed in.....", time.time()-t)