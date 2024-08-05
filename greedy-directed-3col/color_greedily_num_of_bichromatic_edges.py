import networkx as nx
from graphs.display_graph import display_graph
from graphs.digraph_with_coloring import DigraphWithColoring
from bump_color import bump_color


def color_greedily(graph: nx.DiGraph, display=False):
    colored = DigraphWithColoring(graph)
    for step in range(3 ** len(graph.nodes)):
        if display:
            display_graph(graph, vertex_colors=colored.coloring)
        if colored.is_correct_coloring():
            return step, colored.coloring
        node = None
        color = None
        for v in colored.graph.nodes:
            neighbors = set(graph.predecessors(v)) | set(graph.successors(v))
            bichromatic = len([n for n in neighbors if colored.coloring[n] != colored.coloring[v]])
            for c in [0, 1, 2]:
                if colored.coloring[v] == c:
                    continue
                new_bichromatic = len([n for n in neighbors if colored.coloring[n] != c])
                if new_bichromatic > bichromatic:
                    node = v
                    color = c
                    break
            if node is not None:
                break
        if color is not None:
            colored.set_color(node, color)
    if display:
        display_graph(graph, vertex_colors=colored.coloring)

    return 3 ** len(graph.nodes), None



