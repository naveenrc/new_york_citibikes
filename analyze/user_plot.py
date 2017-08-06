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
print(df.head())
source = plt.ColumnDataSource(df)

hover1 = HoverTool(tooltips=[
    ("Pay per use Customer", "@Customer{int}"),
    ("Member", "@Subscriber{int}")
])
plot = plt.figure(
    width=600, height=600,
    x_axis_type="datetime",
    title="Rides by user type",
    tools="pan,wheel_zoom,box_zoom,reset",
    toolbar_location="above",
    active_drag='box_zoom'
)
plot.add_tools(hover1)
plot.line(
    'start_time', 'Customer',
    source=source,
    alpha=1, color=Blues4[0], line_width=2,
    legend="Pay per use customer"
)
plot.line(
    'start_time', 'Subscriber',
    source=source,
    alpha=0.7, color='red', line_width=2,
    legend="Member"
)
show(plot)