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
        colored.bump_color(unsatisfied_node)
        c2 = colored.get_different_fraction(unsatisfied_node)
        colored.bump_color(unsatisfied_node)
        c3 = colored.get_different_fraction(unsatisfied_node)
        colored.bump_color(unsatisfied_node)
        colored.bump_color(unsatisfied_node)
        if c3 > c2:
            colored.bump_color(unsatisfied_node)
    if display:
        display_graph(graph, vertex_colors={i: colored.colors[i] for i in graph.nodes})

    return 3 ** len(graph.nodes), None



