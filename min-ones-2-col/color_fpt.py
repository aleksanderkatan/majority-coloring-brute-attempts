import networkx as nx

from graphs.digraphwithcoloring import DigraphWithColoring
from graphs.graph_display import display_graph
from itertools import chain


# the argument `original_k` is only here for debug purposes
def recursive_try_fill_min_ones(g: DigraphWithColoring, original_k: int, current_k: int):
    # print(k)
    # display_graph(g.graph, vertex_colors=g.coloring)
    if g.is_correct_coloring():
        return True
    if current_k == 0:
        return False
    if g.try_find_unsatisfied_vertex(color=1) is not None:
        return False
    for v in g.graph.nodes:
        if g.coloring[v] == 0:
            zeroes = g.same_colored_neighbors(v)
            ones = g.differently_colored_neighbors(v)
            if zeroes - current_k > ones + current_k:
                g.set_color(v, 1)
                result = recursive_try_fill_min_ones(g, original_k, current_k - 1)
                # we pass the coloring by reference, we must retain its state
                g.set_color(v, 0)
                return result
    v = g.try_find_unsatisfied_vertex(color=0)
    # vvv asserts vvv
    assert v is not None
    branches = 1 + len([u for u in g.graph.successors(v) if g.coloring[u] == 0])
    assert branches <= original_k + 2 * current_k + 1
    assert branches <= 3 * original_k + 1
    # ^^^ asserts ^^^
    for u in chain([v], g.graph.successors(v)):
        if g.coloring[u] == 0:
            g.set_color(u, 1)
            if recursive_try_fill_min_ones(g, original_k, current_k - 1):
                return True
            g.set_color(u, 0)
    return False


def calculate_min_ones(g: nx.DiGraph):
    for i in range(len(g.nodes)):
        gwc = DigraphWithColoring(g)
        if recursive_try_fill_min_ones(gwc, i, i):
            return i
    return None
