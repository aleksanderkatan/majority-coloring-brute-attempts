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
        for neigh in nx.neighbors(graph, unsatisfied_node):
            if colored.get_color(neigh) == colored.get_color(unsatisfied_node):
                bump_color(colored, neigh)
                break
    if display:
        display_graph(graph, vertex_colors=colored.coloring)

    return 3 ** len(graph.nodes), None



