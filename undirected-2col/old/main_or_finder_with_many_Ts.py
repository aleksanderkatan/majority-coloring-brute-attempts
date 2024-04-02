from all_colorings_encoder import Encoder
from graph_display import display_graph
from graphs.graph_iterator import graph_iterator


# sprawdzone z 2T do 7 włącznie
# sprawdzone z 3T do 7 włącznie

def check_graph_2t(g):
    a = 0
    b = 1
    true_1 = 2
    true_2 = 3
    or_node = 4
    extra = len(g.nodes)
    g.add_edge(or_node, extra)

    # none of a, b, true_1, true_2 should have edges between them
    for u in [a, b, true_1, true_2]:
        for v in [a, b, true_1, true_2]:
            if u == v:
                continue
            if g.has_edge(u, v):
                return False

    # print("a", end="")

    true_color = 1
    for a_color in [0, 1]:
        for b_color in [0, 1]:
            for extra_color in [0, 1]:
                encoder = Encoder(g,
                                  precolored={a: a_color, b: b_color, true_1: true_color, true_2: true_color, extra: extra_color},
                                  skip_requirements=[a, b, true_1, true_2, extra])
                all_solutions = encoder.solve()
                if len(all_solutions) == 0:
                    return False

                for coloring in all_solutions:
                    if coloring[or_node] != min(a_color, b_color):
                        return False
    return True


def check_graph_3t(g):
    a = 0
    b = 1
    true_1 = 2
    true_2 = 3
    true_3 = 4
    or_node = 5
    extra = len(g.nodes)
    g.add_edge(or_node, extra)

    # none of a, b, true_1, true_2, true_3 should have edges between them
    for u in [a, b, true_1, true_2, true_3]:
        for v in [a, b, true_1, true_2, true_3]:
            if u == v:
                continue
            if g.has_edge(u, v):
                return False

    true_color = 1
    for a_color in [0, 1]:
        for b_color in [0, 1]:
            for extra_color in [0, 1]:
                encoder = Encoder(g,
                                  precolored={a: a_color, b: b_color,
                                              true_1: true_color, true_2: true_color, true_3: true_color,
                                              extra: extra_color},
                                  skip_requirements=[a, b, true_1, true_2, true_3, extra])
                all_solutions = encoder.solve()
                if len(all_solutions) == 0:
                    return False

                for coloring in all_solutions:
                    if coloring[or_node] != min(a_color, b_color):
                        return False
    return True


def check_graph_2t_1f(g):
    a = 0
    b = 1
    true_1 = 2
    true_2 = 3
    false_1 = 4
    false_2 = 5
    or_node = 6
    extra = len(g.nodes)
    g.add_edge(or_node, extra)

    # none of a, b, true_1, true_2, true_3 should have edges between them
    for u in [a, b, true_1, true_2, false_1, false_2]:
        for v in [a, b, true_1, true_2, false_1, false_2]:
            if u == v:
                continue
            if g.has_edge(u, v):
                return False

    true_color = 1
    for a_color in [0, 1]:
        for b_color in [0, 1]:
            for extra_color in [0, 1]:
                encoder = Encoder(g,
                                  precolored={a: a_color, b: b_color,
                                              true_1: true_color, true_2: true_color, false_1: 1-true_color, false_2: 1-true_color,
                                              extra: extra_color},
                                  skip_requirements=[a, b, true_1, true_2, false_1, false_2, extra])
                all_solutions = encoder.solve()
                if len(all_solutions) == 0:
                    return False

                for coloring in all_solutions:
                    if coloring[or_node] != min(a_color, b_color):
                        return False
    return True


if __name__ == "__main__":
    for g in graph_iterator(8):
        if check_graph_2t_1f(g):
            display_graph(g, {i: str(i) for i in g.nodes}, {i: 0 for i in g.nodes})
