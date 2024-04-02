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
    if len(g.nodes) < precolored_num + 1:
        return None

    precolored = [i for i in range(precolored_num)]
    related = precolored_num
    extra = len(g.nodes)
    g.add_edge(related, extra)

    relation = {}
    for precoloring, precoloring_tuple in all_colorings(precolored):
        for extra_color in [0, 1]:
            precoloring[extra] = extra_color
            encoder = Encoder(g, precolored=precoloring, skip_requirements=precolored + [extra])
            all_solutions = encoder.solve()
            if len(all_solutions) == 0:
                raise RuntimeError

            if precoloring_tuple not in relation:
                relation[precoloring_tuple] = all_solutions[0][related]
            for coloring in all_solutions:
                if coloring[related] != relation[precoloring_tuple]:
                    return None

    return relation


# checked precolored 1 up to and including 6
# checked precolored 2 up to and including 6
# checked precolored 3 up to and including 7
# checked precolored 4 up to and including 6
# checked precolored 5 up to and including 6



if __name__ == "__main__":
    VERTICES_TO_CHECK = 7
    PRECOLORED = 3

    for g in graph_iterator(VERTICES_TO_CHECK):
        possible_relation = check_graph(g, PRECOLORED)
        if possible_relation is not None:
            print(possible_relation)
            display_graph(g, {i: str(i) for i in g.nodes}, {i: 0 for i in g.nodes})
