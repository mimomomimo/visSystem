from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.plotting import Figure
from bokeh.models import ColumnDataSource, CustomJS, TapTool,Range1d,Button
import sys
from plot_network import plot_network
from plot_trajectory import plot_trajectory
from plot_barchart import plot_barchart


close_pair_data = "data/close_pair_data.csv"
network_data = "data/network_color_data.csv"
trajectory_data = "data/trajectory_data.csv"


def main():
    HOVER_TOOLTIPS = [
       ("ID", "@index")
    ]
    data =ColumnDataSource(data=dict(ids = []))
    network_plot, reset_button, source, data, index, network_data, colo, graph_renderer = plot_network(data)
    trajectory_plot, exec_button, change_color, frame_and_no = plot_trajectory(index, colo, data)
    barchart_plot = plot_barchart(change_color, frame_and_no)
    buttons = row(exec_button, reset_button)
    colum = column(network_plot, buttons)
    rows = row(colum, trajectory_plot)
    layout = column(rows, barchart_plot)
    curdoc().add_root(layout)



main()