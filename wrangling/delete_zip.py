# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 19:59:38 2017

@author: Naveen
"""
import json
import os

file_path = 'C:/Users/Naveen/Downloads/Springboard/GitHub/new_york_citibikes/data/rides/file_names.json'
f = open(file_path, 'r')
file_names = json.load(f)
f.close()

path='C:/Users/Naveen/Downloads/Springboard/GitHub/new_york_citibikes/data/rides/'
for name,value in file_names.items():
    if name.endswith(".zip"):
        os.remove(path+name)