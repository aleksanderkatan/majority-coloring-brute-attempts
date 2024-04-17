import networkx as nx
from colored_graph import ColoredGraph


def color_greedily(graph: nx.DiGraph):
    colored = ColoredGraph(graph)
    for step in range(3 ** len(graph.nodes)):
        unsatisfied_node = colored.find_unsatisfied()
        if unsatisfied_node is None:
            return step, colored.colors
        colored.bump_color(unsatisfied_node)

    return 3 ** len(graph.nodes), None



