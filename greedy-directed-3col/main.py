from graphs.new_graph_iterator import directed_graph_iterator
from color_greedily import color_greedily
from graphs.graph_display import display_graph


if __name__ == "__main__":
    for graph in directed_graph_iterator(3, 7):
        steps, coloring = color_greedily(graph)
        # display_graph(graph, vertex_colors={i: coloring[i] for i in graph.nodes})
        if coloring is None:
            display_graph(graph)

