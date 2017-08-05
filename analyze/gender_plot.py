import os
import pandas as pd
from bokeh.layouts import column
import bokeh.plotting as plt
from bokeh.io import show


curdir = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/rides_count.csv')
# setup basic map
df['start_time'] = pd.to_datetime(df['start_time'])
df = df.groupby('start_time').agg('sum')
source = plt.ColumnDataSource(df)

plot = plt.figure(
    width=800, height=600,
    x_axis_type="datetime",
    title="Distances",
    tools="pan,wheel_zoom,box_zoom,reset",
    toolbar_location="above"
)
plot.legend.location = "top_left"
plot.legend.click_policy="hide"
plot.line(
    'start_time', 'male_dist',
    source=source,
    alpha=1, color='green', line_width=2,
    legend="male"
)
plot.line(
    'start_time', 'female_dist',
    source=source,
    alpha=1, color='blue', line_width=2,
    legend="female"
)
plot.line(
    'start_time', 'un_dist',
    source=source,
    alpha=0.3, color='red', line_width=2,
    legend="unknown"
)
plot1 = plt.figure(
    width=800, height=600,
    x_axis_type="datetime",
    title="Rides",
    tools="pan,wheel_zoom,box_zoom,reset",
    toolbar_location="above"
)
plot1.legend.location = "top_left"
plot1.legend.click_policy="hide"
plot1.line(
    'start_time', 'male_rides',
    source=source,
    alpha=1, color='green', line_width=2,
    legend="male"
)
plot1.line(
    'start_time', 'female_rides',
    source=source,
    alpha=1, color='blue', line_width=2,
    legend="female"
)
plot1.line(
    'start_time', 'un_rides',
    source=source,
    alpha=0.3, color='red', line_width=2,
    legend="unknown"
)

show(column(plot,plot1))