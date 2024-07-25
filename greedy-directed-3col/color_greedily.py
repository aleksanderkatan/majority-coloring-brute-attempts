import networkx as nx
from graphs.digraph_with_coloring import DigraphWithColoring
from bump_color import bump_color


def color_greedily(graph: nx.DiGraph, display=None):
    colored = DigraphWithColoring(graph)
    for step in range(3 ** len(graph.nodes)):
        unsatisfied_node = colored.try_find_unsatisfied_vertex()
        if unsatisfied_node is None:
            return step, colored.coloring
        bump_color(colored, unsatisfied_node)

    return 3 ** len(graph.nodes), None



