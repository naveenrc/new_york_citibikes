import os
import pandas as pd
from bokeh.models import HoverTool
import bokeh.plotting as plt
from bokeh.io import show
from bokeh.palettes import Blues4


curdir = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/rides_user.csv')
# setup basic map
df['start_time'] = pd.to_datetime(df['start_time'])
df = df.groupby('start_time').agg('sum')

source = plt.ColumnDataSource(df)

plot = plt.figure(
    width=1000, height=570,
    x_axis_type="datetime",
    title="Rides by user type",
    tools="pan,wheel_zoom,box_zoom,reset",
    toolbar_location="above",
    active_drag='box_zoom',
    y_axis_type="log"
)
plot.yaxis.axis_label = 'Number of rides'
plot.xaxis.axis_label = 'Date'
plot.legend.location = "bottom_right"
customer = plot.line(
    'start_time', 'Customer',
    source=source,
    alpha=1, color=Blues4[0], line_width=2,
    legend="Pay per use customer"
)
member = plot.line(
    'start_time', 'Subscriber',
    source=source,
    alpha=0.7, color='red', line_width=2,
    legend="Member"
)
hover1 = HoverTool(tooltips=[
    ("Pay per use Customer", "@Customer{int}"),
    ("Member", "@Subscriber{int}"),
    ("date","@start_time{%F}")
    ],
    formatters={
        'start_time'      : 'datetime', # use 'datetime' formatter for 'start_time' field
    },
    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='vline',
    renderers=[customer]
)
plot.add_tools(hover1)
show(plot)