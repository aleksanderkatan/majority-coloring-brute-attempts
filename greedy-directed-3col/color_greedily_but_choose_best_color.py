import networkx as nx
from graphs.display_graph import display_graph
from graphs.digraph_with_coloring import DigraphWithColoring
from bump_color import bump_color


def color_greedily(graph: nx.DiGraph, display=False):
    colored = DigraphWithColoring(graph)
    for step in range(3 ** len(graph.nodes)):
        if display:
            display_graph(graph, vertex_colors=colored.coloring)
        unsatisfied_node = colored.try_find_unsatisfied_vertex()
        if unsatisfied_node is None:
            return step, colored.coloring
        bump_color(colored, unsatisfied_node)
        c2 = colored.get_different_fraction(unsatisfied_node)
        bump_color(colored, unsatisfied_node)
        c3 = colored.get_different_fraction(unsatisfied_node)
        bump_color(colored, unsatisfied_node)
        bump_color(colored, unsatisfied_node)
        if c3 > c2:
            bump_color(colored, unsatisfied_node)
    if display:
        display_graph(graph, vertex_colors=colored.coloring)

    return 3 ** len(graph.nodes), None



