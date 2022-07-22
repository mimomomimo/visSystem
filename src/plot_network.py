
from bokeh.models import CustomJS, TapTool,Range1d,Button
from bokeh.plotting import Figure
from bokeh.layouts import column
import sys
sys.path.append('../')
from module import get_graph_renderer

close_pair_data_name = "data/close_pair_data.csv"
network_data_name = "data/network_color_data.csv"


def plot_network(data):
    data.data['ids'] = []

    HOVER_TOOLTIPS = [
       ("ID", "@index")
    ]
    graph_renderer,network_data = get_graph_renderer(close_pair_data_name, network_data_name)
    index = graph_renderer.node_renderer.data_source.data['index'] 
    colo = graph_renderer.node_renderer.data_source.data['colors']
    new_plot = Figure(tooltips = HOVER_TOOLTIPS,
              tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
              plot_width=530, plot_height=530,
            x_range=Range1d(-1.1,1.1), y_range=Range1d(-1.1,1.1), title="Proximity networks")
    new_plot.xgrid.visible = False
    new_plot.ygrid.visible = False
    new_plot.xaxis.visible = False
    new_plot.yaxis.visible = False
    new_plot.toolbar.logo = None
    new_plot.renderers.append(graph_renderer)
    source = graph_renderer.node_renderer.data_source

    new_plot.add_tools(TapTool(callback=CustomJS(args=dict(source=source, data = data, index = index, network_data=network_data), code="""
        source.change.emit();
        const num = source.selected.indices;
        const dt = source.data;
        const color = dt['colors']
        console.log(source.selected.indices); 
        if (color[num] == "gray") {
         color[num] = network_data.data['color'][network_data.data['index'].indexOf(parseInt(dt['index'][num], 10))];
            data.data['ids'].splice(data.data['ids'].indexOf(dt['index'][num]), 1);
        } else {
            color[num] = "gray";
            data.data['ids'].push(dt['index'][num]);
        }
        console.log(data.data['ids'])
        source.change.emit();
        data.change.emit();
    """)))


    button = Button(label="RESET", button_type="success",  width=250, height=50)
    button.js_on_click(CustomJS(args=dict(index = index, data = data, source=source, colo = colo), code="""
    for (let i = 0; i < data.data['ids'].length; i++) {
       source.data['colors'][source.data['index'].indexOf(parseInt(data.data['ids'][i], 10))] = colo[index.indexOf(parseInt(data.data['ids'][i], 10))] 
    }
    data.data['ids'] = [];
    source.change.emit();
    data.change.emit();
    data.change.emit(); """))
    
    return new_plot, button, source, data, index, network_data, colo, graph_renderer