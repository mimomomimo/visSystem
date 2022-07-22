import pandas as pd
import networkx as nx
import numpy as np
from bokeh.models import Circle, MultiLine, ColumnDataSource
from bokeh.plotting import from_networkx


def get_graph_renderer(close_pair_data,network_data):
    graph_df = pd.read_csv(close_pair_data)
    node_color_df = pd.read_csv(network_data)
    network_data = ColumnDataSource(data=dict(index=node_color_df.values[:,1], color=node_color_df.values[:,2]))
    G = nx.from_pandas_edgelist(graph_df, 'pair1', 'pair2', edge_attr=True)
    np.random.seed(42)
    graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))
    graph_renderer.edge_renderer.glyph = MultiLine(line_color="black", line_alpha=0.8, line_width=1)

    graph_renderer.node_renderer.data_source.data['index'] = network_data.data['index']
    graph_renderer.node_renderer.data_source.data['colors'] = network_data.data['color']
    graph_renderer.node_renderer.glyph = Circle(
        size=10,
        fill_color='colors'
    )
    graph_renderer.edge_renderer.data_source.data["line_width"] = graph_df.values[:,3]
    graph_renderer.edge_renderer.glyph.line_width = {'field': 'line_width'}
    

    return graph_renderer, network_data