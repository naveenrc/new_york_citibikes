## Instructions
#### Requirements
+ Python 3.5+
+ Selenium
+ BeautifulSoup
+ Phanomjs http://phantomjs.org/download.html
+ <a href="https://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10/">Official Bash for Windows beta version (Optional)</a>
+ csvkit for bash

### Download Data
>Ride data: https://s3.amazonaws.com/tripdata/index.html has multiple data sets from 2013 to present<br>
>More information about these datasets can be found <a href="https://www.citibikenyc.com/system-data">here</a>

>To automate the download, run 'wrangling/download.py'. <br>
>I have used selenium, BeautifulSoup, <a href="http://phantomjs.org/download.html">phantomjs</a> to download Ride data, as it was a dynamic web page.

>Followed by 'wrangling/extract.py' which extracts the zip files. I have written this program because some zip files are having repeated files inside them. I have used a dictionary of file names after extracting each zip file`s children and check if the child already exists before extracting other zip file. ZipFile module provides namelist() which can be used to check files inside a zip file before extracting it.<br>
>The dictionary is saved to a json file and used while running download.py repeatedly to avoid downloading files that are already downloaded before

>To delete the zip files and save space run 'wrangling/delete_zip.py'

>Weather data: https://www.ncdc.noaa.gov/cdo-web/datasets/GHCND/stations/GHCND:USW00094728/detail

>Google maps distance matrix API is used to compare transit times for rides, Google estimate vs actual.
