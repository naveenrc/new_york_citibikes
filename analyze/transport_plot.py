import pandas as pd
import os
from bokeh.models import HoverTool
import bokeh.plotting as plt
from bokeh.io import show
from bokeh.palettes import Blues4


curdir = os.path.dirname(__file__)
output = pd.read_csv(os.path.join(curdir, '../data/rides') + '/transported.csv')
output['date'] = pd.DatetimeIndex(output['date']).normalize()
output.set_index('date',inplace=True)
output = output.groupby('date').agg('sum')

source = plt.ColumnDataSource(output)

hover1 = HoverTool(tooltips=[
    ("Transported bikes", "@count{int}")
])
plot = plt.figure(
    width=600, height=600,
    x_axis_type="datetime",
    title="Transported bikes by date",
    tools="pan,wheel_zoom,box_zoom,reset",
    toolbar_location="above",
    active_drag='box_zoom'
)
plot.add_tools(hover1)
plot.line(
    'date', 'count',
    source=source,
    alpha=1, color=Blues4[0], line_width=2
)
plot.yaxis.axis_label = 'Number of transported bikes'
show(plot)