import networkx as nx
from graphs.graph_display import display_graph
from itertools import chain


# unoptimised implementation
class graph_with_coloring:
    def __init__(self, graph: nx.DiGraph, coloring=None):
        self.graph = graph
        if coloring is None:
            coloring = {v:0 for v in graph.nodes}
        self.coloring = coloring

    def differently_colored_neighbors(self, v):
        result = 0
        for n in self.graph.successors(v):
            if self.coloring[n] != self.coloring[v]:
                result += 1
        return result

    def same_colored_neighbors(self, v):
        return self.graph.out_degree(v) - self.differently_colored_neighbors(v)

    def is_satisfied(self, v):
        return 2 * self.differently_colored_neighbors(v) >= self.graph.out_degree(v)

    def try_find_unsatisfied_vertex(self, color):
        for v in self.graph.nodes:
            if self.coloring[v] == color:
                if not self.is_satisfied(v):
                    return v
        return None

    def has_unsatisfied_one(self):
        for v in self.graph.nodes:
            if self.coloring[v] == 1:
                if not self.is_satisfied(v):
                    return True
        return False

    def find_forced_one(self, k):
        for v in self.graph.nodes:
            if self.coloring[v] == 0:
                zeroes = self.same_colored_neighbors(v)
                ones = self.differently_colored_neighbors(v)
                if zeroes - k > ones + k:
                    return v
        return None

    def is_correct_coloring(self):
        for v in self.graph.nodes:
            if not self.is_satisfied(v):
                return False
        return True

    def set_color(self, v: int, c: int):
        self.coloring[v] = c


def recursive_try_fill_min_ones(g: graph_with_coloring, k: int, kp: int):
    # print(k)
    # display_graph(g.graph, vertex_colors=g.coloring)
    if g.is_correct_coloring():
        return True
    if kp == 0:
        return False
    if g.try_find_unsatisfied_vertex(color=1) is not None:
        return False
    n = g.find_forced_one(kp)
    if n is not None:
        g.set_color(n, 1)
        result = recursive_try_fill_min_ones(g, k, kp - 1)
        g.set_color(n, 0)
        return result
    v = g.try_find_unsatisfied_vertex(color=0)
    # vvv asserts vvv
    assert v is not None
    branches = 1 + len([u for u in g.graph.successors(v) if g.coloring[u] == 0])
    assert branches <= k + 2*kp + 1
    assert branches <= 3*k + 1
    # ^^^ asserts ^^^
    for u in chain([v], g.graph.successors(v)):
        if g.coloring[u] == 0:
            g.set_color(u, 1)
            if recursive_try_fill_min_ones(g, k, kp - 1):
                return True
            g.set_color(u, 0)
    return False



def calculate_min_ones(g: nx.DiGraph):
    for i in range(len(g.nodes)):
        gwc = graph_with_coloring(g)
        if recursive_try_fill_min_ones(gwc, i, i):
            return i
    return None



