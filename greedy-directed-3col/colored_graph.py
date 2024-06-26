import networkx as nx


class ColoredGraph:
    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
        self.colors = [0 for _ in graph.nodes]
        self.neighbor_nums = [[graph.out_degree(n), 0, 0] for n in graph.nodes]

    def bump_color(self, node: int):
        prev_color = self.colors[node]
        next_color = (prev_color + 1) % 3
        self.colors[node] = next_color

        for in_neighbor in self.graph.predecessors(node):
            self.neighbor_nums[in_neighbor][prev_color] -= 1
            self.neighbor_nums[in_neighbor][next_color] += 1

    def get_different_fraction(self, node: int):
        if self.graph.out_degree(node) == 0:
            return 1.0
        node_color = self.colors[node]
        colored_same = self.neighbor_nums[node][node_color]
        colored_differently = self.graph.out_degree(node) - colored_same
        return colored_differently / (colored_differently + colored_same)

    def find_unsatisfied(self):
        for node in self.graph.nodes:
            if self.get_different_fraction(node) < 0.5:
                return node
        return None
