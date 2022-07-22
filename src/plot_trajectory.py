import pandas as pd
from bokeh.models import Range1d,ColumnDataSource, CustomJS, Button
from bokeh.plotting import Figure
trajectory_data_name = "data/trajectory_data.csv"
frame_and_no_data_name = "data/frame_and_no_data.csv"

def plot_trajectory(index, colo, data):
    trajectory = pd.read_csv(trajectory_data_name)
    print(trajectory.values)
    id =trajectory.values[:,1]
    time =trajectory.values[:,2]
    x = trajectory.values[:,3]
    y = trajectory.values[:,4]


    trajectory_source = ColumnDataSource(data=dict(x = x, y = y, h_id = id, time = time))
    trace = ColumnDataSource(data=dict(x = [], y = [],time=[], h_id = [],color=[]))


    frame_and_no = pd.read_csv(frame_and_no_data_name)
    frame_and_no = frame_and_no.values
    fff = frame_and_no[:,1]
    nnn = frame_and_no[:,2]

    HOVER_TOOLTIPS2 = [
       ("x", "@x"),
     ("y", "@y"),
    ("frame", "@time"),
    ("ID", "@h_id")]


    plot = Figure(tooltips = HOVER_TOOLTIPS2,width=530, height=630,  x_range=Range1d(0,14), y_range=Range1d(0,18.9))
    plot.circle('x', 'y',color= 'color',source=trace, line_width=3, line_alpha=0.6)
    plot.xaxis.ticker = [0, 2.5, 5, 7.5,  10, 12.5]
    plot.yaxis.ticker = [0, 2.5, 5, 7.5,  10, 12.5, 15, 17.5]
    plot.toolbar.logo = None

    change_color = ColumnDataSource(data=dict(no = [], frame = [], color=[]))


    print(index)
    callback2 = CustomJS(args=dict(fff=fff, nnn=nnn, change_color = change_color, trajectory_source = trajectory_source, trace = trace, index = index, colo = colo, data=data), code="""
    trace.data['x'] = [];
    trace.data['y'] = [];
    trace.data['time'] = [];
    trace.data['h_id'] = [];
    trace.data['color'] = [];
    for (let i = 0; i < trajectory_source.data['x'].length; i++) {
        console.log(data.data['ids']);
        if (data.data['ids'].includes(trajectory_source.data['h_id'][i])) {
            trace.data['x'].push(trajectory_source.data['x'][i]);
            trace.data['y'].push(trajectory_source.data['y'][i]);
            trace.data['time'].push(trajectory_source.data['time'][i]);
            trace.data['h_id'].push(trajectory_source.data['h_id'][i]);
        }
    }  
    const mn = Math.min(...trace.data['time']);
    const mx = Math.max(...trace.data['time']);
    const tt = (mx - mn) / 10
    
    change_color.data['color'] = [];
    change_color.data['frame'] = [];
    change_color.data['no'] = [];
    var start_val = mn - (mn%10);
    var nn = fff.indexOf(start_val);
    while (fff[nn] <= mx) {
        console.log(fff[nn]);
        change_color.data['color'].push("gray");
        change_color.data['frame'].push(fff[nn]);
        change_color.data['no'].push(nnn[nn]);
        nn++;
    }
    for (let i = 0; i < trace.data['x'].length; i++) {
        if (trace.data['time'][i] <= (mn + tt)) {
            trace.data['color'].push("#003366");
        } 
        else if (trace.data['time'][i] <= (mn + (tt*2))) {
            trace.data['color'].push("#003399");
        }
        else if (trace.data['time'][i] <= (mn + (tt*3))) {
            trace.data['color'].push("#3333CC");
        }
        else if (trace.data['time'][i] <= (mn + (tt*4))) {
            trace.data['color'].push("#6633CC");
        }
        else if (trace.data['time'][i] <= (mn + (tt*5))) {
            trace.data['color'].push("#9933CC");
        }
        else if (trace.data['time'][i] <= (mn + (tt*6))) {
            trace.data['color'].push("#CC33CC");
        }
        else if (trace.data['time'][i] <= (mn + (tt*7))) {
            trace.data['color'].push("#FF33CC");
        }
        else if (trace.data['time'][i] <= (mn + (tt*8))) {
            trace.data['color'].push("#FF6699");
        }
        else if (trace.data['time'][i] <= (mn + (tt*9))) {
            trace.data['color'].push("#FF6600");
        }
        else {
            trace.data['color'].push("#FF9900");
        }
    }  
    change_color.change.emit();
    trace.change.emit();
    """)

    button = Button(label="EXECUTE", button_type="success",  width=250, height=50)
    button.js_on_click(callback2)

    return plot, button, change_color, frame_and_no