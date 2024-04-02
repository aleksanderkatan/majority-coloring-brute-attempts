import itertools

from all_colorings_encoder import Encoder
from graph_display import display_graph
from graphs.graph_iterator import graph_iterator


def all_colorings(of_what):
    for coloring in itertools.product(*tuple([[0, 1] for _ in of_what])):
        result = {}
        for vertex, color in zip(of_what, coloring):
            result[vertex] = color
        yield result, coloring


def check_graph(g, precolored_num):
    precolored = [i for i in range(precolored_num)]
    forced_1 = precolored_num
    extra = len(g.nodes)
    g.add_edge(forced_1, extra)

    precoloring = {v: 0 for v in precolored}
    precoloring[extra] = 0
    precoloring[forced_1] = 1
    encoder = Encoder(g, precolored=precoloring, skip_requirements=precolored + [extra])
    all_solutions = encoder.solve()
    if len(all_solutions) == 0:
        return True

    return False


if __name__ == "__main__":
    VERTICES_TO_CHECK = 7
    PRECOLORED = 3

    for g in graph_iterator(VERTICES_TO_CHECK):
        if check_graph(g, PRECOLORED):
            display_graph(g, {i: str(i) for i in g.nodes}, {i: 0 for i in g.nodes})
