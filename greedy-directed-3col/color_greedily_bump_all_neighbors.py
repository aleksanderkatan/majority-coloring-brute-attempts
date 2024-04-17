import networkx as nx
from colored_graph import ColoredGraph
from graphs.graph_display import display_graph


def color_greedily(graph: nx.DiGraph, display=False):
    colored = ColoredGraph(graph)
    for step in range(3 ** len(graph.nodes)):
        if display:
            display_graph(graph, vertex_colors={i: colored.colors[i] for i in graph.nodes})
        unsatisfied_node = colored.find_unsatisfied()
        if unsatisfied_node is None:
            return step, colored.colors
        for neigh in nx.neighbors(graph, unsatisfied_node):
            colored.bump_color(neigh)
    if display:
        display_graph(graph, vertex_colors={i: colored.colors[i] for i in graph.nodes})

    return 3 ** len(graph.nodes), None



