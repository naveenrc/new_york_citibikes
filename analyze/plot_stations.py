import pandas as pd
import os
from bokeh.io import show
from web_mercator import to_mercator
from nyctile import nyc_map
from bokeh.models import HoverTool, ColumnDataSource, tools
from bokeh.models.glyphs import Circle, Text

def mercator_df():
# get data to plot
    dir = os.path.dirname(__file__)
    sta_info = pd.read_csv(os.path.join(dir, '../data')+'/station_info.csv')
    transit = pd.read_csv(os.path.join(dir, '../data')+'/transit_cleaned.csv')

    # convert to mercator format
    df = sta_info.loc[:,['station_id','region_id','name','lon','lat']]
    return to_mercator(df)
# function call to base map

if __name__ == '__main__':
    df = mercator_df()
    fig = nyc_map()

    # colors for Jersey city and NYC regions
    fill_color = { 70: 'blue', 71: 'firebrick'}
    line_color = { 70: 'blue', 71: 'firebrick'}
    df["fill"] = df['region_id'].map(lambda x: fill_color[x])
    df["line"] = df['region_id'].map(lambda x: line_color[x])

    source = ColumnDataSource(df)
    # circle glyph for the stations
    region_glyph = Circle(x="x", y="y", fill_color="fill", line_color="line", size=10, fill_alpha=0.5)
    region = fig.add_glyph(source, region_glyph)

    # hover tooltip to display name
    tooltips = """
    <div>
        <span style="font-size: 15px;">@name</span>&nbsp;<br>
        <span style="font-size: 15px;">station id: @station_id</span>&nbsp;
    </div>
    """
    # add hover tool to figure
    hover = HoverTool(tooltips=tooltips, renderers=[region])
    fig.add_tools(hover)
    show(fig)