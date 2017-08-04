import os
import pandas as pd
from nyctile import nyc_map
from plot_stations import mercator_df
from bokeh.io import show
from bokeh.layouts import column
from bokeh.models import CustomJS, ColumnDataSource, Slider, HoverTool
from bokeh.models.glyphs import Circle, Text


def popular_stations(file):
    curdir = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/'+file)
    fig = nyc_map()
    stationdf = mercator_df()
    starts = df['start_sta_id'].value_counts()
    ends = df['end_sta_id'].value_counts()
    starts_df = pd.DataFrame({'station_id':starts.index, 'count1':starts.values})
    ends_df = pd.DataFrame({'station_id': ends.index, 'count2': ends.values})
    count = stationdf.set_index('station_id').join(starts_df.set_index('station_id'))
    count = count.fillna(0)
    count = count.join(ends_df.set_index('station_id'))
    count = count.fillna(0)
    year = pd.to_datetime(df.loc[0,'start_time']).year
    count['year'] = year
    count['count'+str(year)] = count['count1'] + count['count2']
    count.drop(['count1', 'count2'], axis=1, inplace=True)
    # colors for Jersey city and NYC regions
    fill_color = {70: 'blue', 71: 'firebrick'}
    line_color = {70: 'blue', 71: 'firebrick'}
    count["fill"] = count['region_id'].map(lambda x: fill_color[x])
    count["line"] = count['region_id'].map(lambda x: line_color[x])
    count['transform'+str(year)] = count['count'+str(year)]/100+3
    count['count']=0
    count['transform']=count['transform'+str(year)]
    count['count2016'] = 0
    count['transform2016'] = 3
    source = ColumnDataSource(count)
    region_glyph = Circle(x="x", y="y", fill_color="fill", line_color="line", size='transform', fill_alpha=0.5)
    region = fig.add_glyph(source, region_glyph)

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
    callback = CustomJS(args=dict(source=source), code="""
        var data = source.get('data');
        var f = cb_obj.get('value');
        console.log(data.count);
        for(i=0;i<668;i++){
            data.count[i]=data['count'+f][i];
            data.transform[i]=data['transform'+f][i];
        }
        console.log(data.count);
        source.trigger('change');
    """)

    slider = Slider(start=2013, end=2017, value=2017, step=1, title="year", callback=callback)
    layout = column(slider, fig)
    show(layout)


if __name__ == '__main__':
    curdir = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(curdir, '../data/rides') + '/cleaned_files.csv', header=None)
    files = df[0].tolist()

    popular_stations(files[63])