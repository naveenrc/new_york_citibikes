import os
import pandas as pd
from bokeh.models import HoverTool, Circle
import bokeh.plotting as plt
from bokeh.io import show
from bokeh.layouts import gridplot
from bokeh.palettes import Blues4


curdir = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/rides_count.csv')
# setup basic map
df['start_time'] = pd.to_datetime(df['start_time'])
df = df.groupby('start_time').agg('sum')
df['total_distance'] = df['male_dist']+df['female_dist']+df['un_dist']
df['total_rides'] = df['male_rides']+df['female_rides']+df['un_rides']
df['duration'] = df['duration']/3600
source = plt.ColumnDataSource(df)


plot = plt.figure(
    width=500, height=500,
    x_axis_type="datetime",
    title="Distances",
    tools="pan,wheel_zoom,box_zoom,reset",
    toolbar_location="above",
    active_drag='box_zoom',
    y_axis_type="log"
)
male=plot.line(
    'start_time', 'male_dist',
    source=source,
    alpha=1, color=Blues4[0], line_width=2,
    legend="male"
)
plot.line(
    'start_time', 'female_dist',
    source=source,
    alpha=1, color='red', line_width=2,
    legend="female"
)
plot.line(
    'start_time', 'un_dist',
    source=source,
    alpha=0.3, color='orange', line_width=2,
    legend="unknown"
)
plot.legend.location = "bottom_left"
plot.yaxis.axis_label = 'Distances'
plot.xaxis.axis_label = 'Date'
hover1 = HoverTool(tooltips=[
    ("male distance", "@male_dist{int}"),
    ("female distance", "@female_dist{int}"),
    ("unknown distance", "@un_dist{int}"),
    ("Total Distance", "@total_distance{int} in miles"),
    ("date","@start_time{%F}"),
    ],
    formatters={
        'start_time'      : 'datetime', # use 'datetime' formatter for 'start_time' field
    },
    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='vline',
    renderers=[male]
)
plot.add_tools(hover1)


plot1 = plt.figure(
    width=500, height=500,
    x_axis_type="datetime",
    title="Rides",
    tools="pan,wheel_zoom,box_zoom,reset",
    toolbar_location="above",
    x_range=plot.x_range,
    active_drag='box_zoom',
    y_axis_type="log",
)
male = plot1.line(
    'start_time', 'male_rides',
    source=source,
    alpha=1, color=Blues4[0], line_width=2,
    #legend="male"
)
plot1.line(
    'start_time', 'female_rides',
    source=source,
    alpha=1, color='red', line_width=2,
    #legend="female"
)
plot1.line(
    'start_time', 'un_rides',
    source=source,
    alpha=0.3, color='orange', line_width=2,
    #legend="unknown"
)
hover1 = HoverTool(tooltips=[
    ("male rides", "@male_rides{int}"),
    ("female rides", "@female_rides{int}"),
    ("unknown rides", "@un_rides{int}"),
    ("Total rides", "@total_rides{int}"),
    ("date","@start_time{%F}")
    ],
    formatters={
        'start_time'      : 'datetime', # use 'datetime' formatter for 'start_time' field
    },
    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='vline',
    renderers=[male]
)
plot1.yaxis.axis_label = 'Number of rides'
plot1.xaxis.axis_label = 'Date'
plot1.add_tools(hover1)
grid = gridplot([[plot1, plot]])
show(grid)