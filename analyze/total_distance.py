import os
import pandas as pd
from bokeh.models import HoverTool,Axis
import bokeh.plotting as plt
from bokeh.io import show
from bokeh.palettes import Blues4
from bokeh.models.widgets import Div
from bokeh.layouts import column


curdir = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/rides_count.csv')
df['start_time'] = pd.to_datetime(df['start_time'])
df['start_time'] = pd.DatetimeIndex(df['start_time']).normalize()
df['estimated_distance'] = df['un_dist']+df['male_dist']+df['female_dist']
df = df.groupby('start_time').agg('sum')

source = plt.ColumnDataSource(df)

hover1 = HoverTool(tooltips=[
    ("distance", "@estimated_distance{int}"),
    ("date","@start_time{%F}")
    ],
    formatters={
        'start_time'      : 'datetime', # use 'datetime' formatter for 'start_time' field
    },
    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='vline'
)
plot = plt.figure(
    width=1000, height=570,
    x_axis_type="datetime",
    title="Estimated total distance travelled",
    tools="pan,wheel_zoom,box_zoom,reset",
    toolbar_location="above",
    active_drag='box_zoom',
    y_axis_type="log"
)
plot.add_tools(hover1)
plot.line(
    'start_time', 'estimated_distance',
    source=source,
    alpha=1, color=Blues4[0], line_width=2
)
plot.yaxis.axis_label = 'Distance Travelled'
plot.xaxis.axis_label = 'Date'

total_distance = sum(df['estimated_distance'])
earth = 24901
trips = total_distance/earth
moon = 238900
moon_trips = total_distance/moon

p = Div(text="Estimated total distance travelled by riders is <i><b>"+str(total_distance) + "</b> miles </i><br>"+
             "Which is <i><b>" + str(trips) + "</b> trips</i> around earth, whose circumference is<i> <b>" + str(earth)+"</b> miles</i><br>"+
             "Interestingly <i><b>" + str(moon_trips/2) + "</b> trips</i> to moon, distance to it is<i> <b>" + str(moon) + "</b> miles</i>",
width=1000, height=100)

layout = column(p,plot)
show(layout)