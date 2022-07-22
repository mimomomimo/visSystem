
import pandas as pd
from bokeh.models import Range1d,ColumnDataSource, CustomJS, Button
from bokeh.plotting import Figure

def plot_barchart(change_color,frame_and_no):

    hover_info = [
        ("time", "@frame"),
        ("number", "@no")
    ]
    pl = Figure(width=1100, height=100,toolbar_location=None, tooltips = hover_info, tools="pan, wheel_zoom, reset")
    fff = frame_and_no[:,1]
    nnn = frame_and_no[:,2]
    ccc = frame_and_no[:,3]

    ninzu = ColumnDataSource(data=dict(frame = fff, no = nnn, color=ccc))
    pl.vbar(x='frame', top='no', line_color='color', fill_color='color', source=ninzu)
    pl.vbar(x='frame', top='no', line_color='color', fill_color='color', source=change_color)

    return pl
