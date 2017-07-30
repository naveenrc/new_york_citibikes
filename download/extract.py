# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 19:16:28 2017

@author: Naveen
"""

import os
import json
import zipfile

file_names = {}
file_path = 'C:/Users/Naveen/Downloads/Springboard/GitHub/new_york_citibikes/data/rides/extracted.json'
try:
    f = open(file_path, 'r')
    file_names = json.load(f)
    # if the file is empty the ValueError will be thrown
except ValueError:
    file_names = {}
except FileNotFoundError:#create file if not present
    f = open(file_path, 'w')
    f.close()
    f = open(file_path, 'r')
    file_names = json.load(f)
f.close()

#Below code is needed to avoid duplicate extractions
path = r'C:/Users/Naveen/Downloads/Springboard/GitHub/new_york_citibikes/data/rides/'
for path, subdirs, files in os.walk(path):#check for sub-directories, files
    for filename in files: #iterate through filenames 
        if filename.endswith('.zip'):#check for zip files
            temp = zipfile.ZipFile(path+filename,'r') #read zip file as aipfile object
            childs = temp.namelist() #retrive children names of zip file
            for child in childs:
                if child not in file_names:
                    print("Extracting.."+child) #Extract child
                    temp.extract(child,path=path)
                    file_names[child] = 1
            temp.close()

print("Done")
with open(file_path, 'w') as f:
    json.dump(file_names, f)
    f.close()