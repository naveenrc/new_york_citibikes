import os
import pandas as pd
from bokeh.models import Axis,HoverTool
import bokeh.plotting as plt
from bokeh.io import show
from bokeh.layouts import gridplot
from bokeh.palettes import Blues4

def plot(df,xval,yval,title,hoverx,hovery,labelx,labely):
    source = plt.ColumnDataSource(df)

    plot = plt.figure(
        width=500, height=500,
        title=title,
        tools="pan,wheel_zoom,box_zoom,reset",
        toolbar_location="above",
        active_drag='box_zoom'
    )
    plot.xaxis.axis_label = labelx
    plot.yaxis.axis_label = labely
    hover1 = HoverTool(tooltips=[
        (hoverx, "@"+xval+"{1.11}"),
        (hovery, "@"+yval+"{int}")
    ])
    plot.add_tools(hover1)
    plot.circle(
        xval, yval,
        source=source,
        alpha=1, color=Blues4[1], size=10,
    )
    yaxis = plot.select(dict(type=Axis, layout="left"))[0]
    yaxis.formatter.use_scientific = False
    return plot


curdir = os.path.dirname(__file__)
weather = pd.read_csv(os.path.join(curdir, '../data/weather') + '/weather.csv')
weather['start_time'] = pd.to_datetime(weather['DATE'].astype(str), format='%Y%m%d')
weather.set_index('start_time',inplace=True)
weather.drop(['DATE'],axis=1,inplace=True)

df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/rides_count.csv')
df['start_time'] = pd.to_datetime(df['start_time'])
df['start_time'] = pd.DatetimeIndex(df['start_time']).normalize()
df = df.groupby('start_time').agg('sum')
df['total_distance'] = df['male_dist']+df['female_dist']+df['un_dist']
df['total_rides'] = df['male_rides']+df['female_rides']+df['un_rides']

final = df.join(weather,how='left')
final['TAVG'] = (final['TMAX']+final['TMIN'])/2
snow = final.groupby('SNOW')['total_rides'].agg('sum')
snow_df = pd.DataFrame(dict(index=snow.index,values=snow.values)).set_index('index')

rain = final.groupby('PRCP')['total_rides'].agg('sum')
rain_df = pd.DataFrame(dict(index=rain.index,values=rain.values)).set_index('index')

temp = final.groupby('TAVG')['total_rides'].agg('sum')
temp_df = pd.DataFrame(dict(index=temp.index,values=temp.values)).set_index('index')

snow_d = final.groupby('SNWD')['total_rides'].agg('sum')
snow_d_df = pd.DataFrame(dict(index=snow_d.index,values=snow_d.values)).set_index('index')


plot1 = plot(snow_df,'index','values','snow fall vs rides','snow depth:','rides:','Snow fall in inches','Number of rides')
plot2 = plot(rain_df,'index','values','rain vs rides','rain:','rides:','Rain in inches','Number of rides')
plot3 = plot(temp_df,'index','values','temperature vs rides','temperature:','rides:','Temperature','Number of rides')
plot4 = plot(snow_d_df,'index','values','snow depth vs rides','snow depth:','rides:','Snow depth in inches','Number of rides')

layout = gridplot([[plot1,plot2],[plot3,plot4]])
show(layout)
