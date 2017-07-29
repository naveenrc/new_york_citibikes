# New York citi bike

## Requirements
+ Python 3.5+
+ Selenium
+ BeautifulSoup
+ Phanomjs http://phantomjs.org/download.html
+ <a href="https://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10/">Official Bash for Windows beta version (Optional)</a>
+ csvkit for bash

## Download Data
##### Ride data
+ https://s3.amazonaws.com/tripdata/index.html has multiple data sets from 2013 to present
+ More information about these datasets can be found <a href="https://www.citibikenyc.com/system-data">here</a>

##### Weather data
+ https://www.ncdc.noaa.gov/cdo-web/datasets/GHCND/stations/GHCND:USW00094728/detail
+ Documentation is present on the left side bar of same page

##### Google Maps Distance matrix API 
Google maps distance matrix API is used to compare transit times for rides, Google estimate vs actual.

##### Automate download, extract and delete zip files
+ To automate the download, run 'wrangling/download.py'. <br>
+ I have used selenium, BeautifulSoup, <a href="http://phantomjs.org/download.html">phantomjs</a> to download Ride data,as the web page was dynamic.

+ Run 'wrangling/extract.py' which extracts the zip files. I have written this program because some zip files are having repeated files inside them. I have used a dictionary of file names after extracting each zip file`s children and check if the child already exists before extracting other zip file. ZipFile module provides namelist() which can be used to check files inside a zip file before extracting it.<br>
+ The dictionary is saved to a json file and used while running download.py repeatedly to avoid downloading files that are already downloaded before

+ To delete the zip files and save space run 'wrangling/delete_zip.py'

## Cleaning through multiprocessing
##### Ride data
+ These are huge file over 6 GB. So multiprocessing speeds up the process
+ Run cleaning/ride_clean.py to start cleaning
+ Below is a screenshot of Task Manager while tasks are executed
![tasks](https://user-images.githubusercontent.com/30205620/28745103-fb24b912-743e-11e7-8b11-fd233a840519.PNG)

+ This took 8455 seconds which is __2 hours 20 minutes__ on __4 core intel i5, 4GB RAM__

##### Weather data
+ On bash run the following command to install csvkit
```Shell
$sudo apt install csvkit
```
+ To list the columns
```Shell
$csvcut -n filename.csv
```
+ To get stats of a column, say 4. Check for outliers
```Shell
$csvcut -c 4 filename.csv | csvstat
```
+ To extract needed columns, say 3,4,5
```Shell
$csvcut -c 3,4,5 filename.csv > output_file.csv
```
