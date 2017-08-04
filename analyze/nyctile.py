import pandas as pd
import os
from bokeh.io import show
from bokeh.plotting import figure
from bokeh.tile_providers import WMTSTileSource
from web_mercator import to_mercator

# create a base map of nyc to use it later
def nyc_map():
    dir = os.path.dirname(__file__)
    sta_info = pd.read_csv(os.path.join(dir, '../data') + '/station_info.csv')
    # latitudes and longitudes for the range of map
    min_lat = sta_info['lat'].min()
    max_lat = sta_info['lat'].max()
    min_lon = sta_info['lon'].min()
    max_lon = sta_info['lon'].max()
    nyc = pd.DataFrame(dict(name = ["NYC1", "NYC2"], lon=[min_lon, max_lon], lat=[min_lat, max_lat]))
    # convert the ranges to web mercator format
    nyc_range = to_mercator(nyc)
    NYC = x_range, y_range = ((nyc_range.loc[0,'x'], nyc_range.loc[1,'x']), (nyc_range.loc[0,'y'], nyc_range.loc[1,'y']))
    fig = figure(tools='pan, wheel_zoom, box_zoom, tap, reset, save', x_range=x_range, y_range=y_range, width=1000, height=650,
                 title='Citi bikes', toolbar_location="right")
    fig.axis.visible = False
    url = 'http://a.basemaps.cartocdn.com/light_all/{Z}/{X}/{Y}.png'
    attribution = "Naveen Ch"
    fig.add_tile(WMTSTileSource(url=url, attribution=attribution))
    return fig

if __name__ == '__main__':
    base = nyc_map()
    show(base)