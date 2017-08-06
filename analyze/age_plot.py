import os
import pandas as pd
from bokeh.models import HoverTool, Axis
import bokeh.plotting as plt
from bokeh.io import show
from bokeh.layouts import gridplot
from bokeh.palettes import Blues4


curdir = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/rides_age.csv')
# setup basic map
df = df.groupby('age').agg('sum')
source = plt.ColumnDataSource(df)

hover1 = HoverTool(tooltips=[
    ("Age of customer", "@age"),
    ("Rides", "@rides{int}")
])
plot = plt.figure(
    width=600, height=600,
    title="Rides by user age",
    tools="pan,wheel_zoom,box_zoom,reset",
    toolbar_location="above",
    active_drag='box_zoom'
)
plot.add_tools(hover1)
plot.line(
    'age', 'rides',
    source=source,
    alpha=1, color=Blues4[0], line_width=2
)
yaxis = plot.select(dict(type=Axis, layout="left"))[0]
yaxis.formatter.use_scientific = False
plot.xaxis.axis_label = 'Age'
plot.yaxis.axis_label = 'Number of rides'
show(plot)