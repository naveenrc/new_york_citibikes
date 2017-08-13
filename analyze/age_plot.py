import os
import pandas as pd
from bokeh.models import HoverTool, Axis
import bokeh.plotting as plt
from bokeh.io import show
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.layouts import gridplot
from bokeh.palettes import Blues4


curdir = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/rides_age.csv')
# setup basic map
df = df.groupby('age').agg('sum')
table = {}
table['ages'] = ['16-26','27-39','40-60']
table['rides'] = [df.loc[16:26]['rides'].sum(),df.loc[27:39]['rides'].sum(),df.loc[40:60]['rides'].sum()]
print(table)

source1 = plt.ColumnDataSource(table)
source = plt.ColumnDataSource(df)

hover1 = HoverTool(tooltips=[
    ("Age", "@age"),
    ("Rides", "@rides{int}")
    ],
    mode='vline'
)
plot = plt.figure(
    width=1000, height=600,
    title="Rides by user age",
    tools="pan,wheel_zoom,box_zoom,reset",
    toolbar_location="above",
    active_drag='box_zoom',
    x_range=(10, 70), y_range=(-10000, 1500000)
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

columns = [
        TableColumn(field="ages", title="Age group"),
        TableColumn(field="rides", title="Number of rides"),
    ]
data_table = DataTable(source=source1, columns=columns, width=250, height=280)
layout = gridplot([[plot,data_table]])
show(layout)