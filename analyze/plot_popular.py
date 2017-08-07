import os
import pandas as pd
from nyctile import nyc_map
from bokeh.io import show
from bokeh.layouts import column
from bokeh.models import CustomJS, ColumnDataSource, Slider, HoverTool, Label
from bokeh.models.glyphs import Circle, Text


curdir = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/stationdf.csv')
# setup basic map
fig = nyc_map('Popular Stations from 2013-07 to 2017-03. Hover to know bikes in/out at that station. \
Zoom in using mouse or box select tool from the toolbox on right')
jc_x=df[df['station_id']==3269]['x'].values[0]
jc_y=df[df['station_id']==3269]['y'].values[0]
nyc_x=df[df['station_id']==519]['x'].values[0]
nyc_y=df[df['station_id']==519]['y'].values[0]
source = ColumnDataSource(df)
jc = Label(text = 'Jersey', text_alpha=1,x=jc_x,y=jc_y,text_font_size='1.5em',x_offset=-50)
nyc = Label(text = 'NYC', text_alpha=1,x=nyc_x,y=nyc_y,text_font_size='1.5em')
region_glyph = Circle(x="x", y="y", fill_color="fill", line_color="line", size='transform', fill_alpha=0.5)
region = fig.add_glyph(source, region_glyph)
fig.add_layout(jc)
fig.add_layout(nyc)
# hover tooltip to display name
tooltips = """
        <div>
            <span style="font-size: 15px;">@name</span><br>
            <span style="font-size: 15px;">Bicycles in/out:@count</span><br>
        </div>
        <div>
            <span style="font-size: 15px;">station id: @station_id</span><br>
            <span style="font-size: 15px;">lat:@lat,lon:@lon</span>
        </div>
        """
# add hover tool to figure
hover = HoverTool(tooltips=tooltips, renderers=[region])
fig.add_tools(hover)

year = Slider(start=2013, end=2017, value=2017, step=1, title="year")
month = Slider(start=1, end=12, step=1, title='month')
callback = CustomJS(args=dict(source=source, year=year, month=month), code="""
        var data = source.get('data');
        var year = year.get('value');
        var month = month.get('value');
        if(year==2013 && month<7){
            year.value=2013;
            month.value=8;
            alert("Select month more than 6");
        }
        if(year==2017 && month>3){
            year.value=2017;
            month.value=2;
            alert("Select month less than 4");
        }
        var column = year*100+month;
        for(i=0;i<668;i++){
            data.count[i]=data['count'+column][i];
            data.transform[i]=data['transform'+column][i]+3;
        }
        source.trigger('change');
    """)
year.callback = callback
month.callback = callback
layout = column(year, month, fig)
show(layout)