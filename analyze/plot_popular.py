import os
import pandas as pd
from nyctile import nyc_map
from bokeh.models import CustomJS, ColumnDataSource, Slider, HoverTool, Label
from bokeh.models.widgets import Div
from bokeh.models.glyphs import Circle, Text
from bokeh.layouts import gridplot
from bokeh.resources import CDN
from bokeh.embed import file_html


curdir = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/stationdf.csv')
df.drop(['Unnamed: 0','Unnamed: 0.1', 'Unnamed: 0.1.1'],axis=1,inplace=True)
df.set_index('station_id',inplace=True)
# print(df.head())


# setup basic map
fig = nyc_map('Popular Stations from 2013-07 to 2017-03. Hover to know bikes in/out at that station. \
Zoom in using mouse or box select tool from the toolbox on top right')

jc_x=df.loc[3269]['x']
jc_y=df.loc[3269]['y']
nyc_x=df.loc[519]['x']
nyc_y=df.loc[519]['y']
df.reset_index(inplace=True)
df['transform'] = df['transform']*300
df['fill2'] = df['fill']
source = ColumnDataSource(df)
# print(source.data)

jc = Label(text = 'Jersey', text_alpha=1,x=jc_x,y=jc_y,text_font_size='1.5em',x_offset=-50)
nyc = Label(text = 'NYC', text_alpha=1,x=nyc_x,y=nyc_y,text_font_size='1.5em')
region_glyph = Circle(x="x", y="y", fill_color="fill2", line_color="line", radius='transform', fill_alpha=0.5)
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
        var data = source.data;
        var year = year.value;
        var month = month.value;
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
        
        data['count'] = data['count'+column].slice();
        for(i=0;i<668;i++){
            data['transform'][i] = data['transform'+column][i]*300;
        }
        data.fill2 = data.fill.slice();
        
        var arr = data.count.slice();
        arr.sort(function(a, b){return b - a});
        for(var i=0;i<5;i++){
            var high = data.count.indexOf(arr[i]);
            data.fill2[high] = "yellow";
        }
        console.log(data['count']);
        console.log(data['transform']);
        source.change.emit();
    """)
year.callback = callback
month.callback = callback

p = Div(text="Click Reset in the top right tool box.<br>Please select year and month to get started.<br>Yellow circles represent top five popular stations",width=400, height=50)
layout = gridplot([[p,year, month],[fig]])

outfile=open('plot_popular.html','w')
outfile.write(file_html(layout,CDN,'Popular Stations'))
outfile.close()