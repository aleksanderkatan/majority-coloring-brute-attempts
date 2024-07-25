import networkx as nx


# unoptimised implementation
class DigraphWithColoring:
    def __init__(self, graph: nx.DiGraph, coloring=None):
        self.graph = graph
        if coloring is None:
            coloring = {v: 0 for v in graph.nodes}
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

    def is_correct_coloring(self):
        for v in self.graph.nodes:
            if not self.is_satisfied(v):
                return False
        return True

    def set_color(self, v: int, c: int):
        self.coloring[v] = c
