from all_colorings_encoder import Encoder
from graph_display import display_graph
from graphs.graph_iterator import graph_iterator


# sprawdzone NOT do 7 włącznie
# sprawdzone bez not do 6 włącznie
# z 2T do 7 włącznie

def check_graph(g):
    a = 0
    a_related = 1
    true_1 = 2
    true_2 = 3
    extra = len(g.nodes)
    g.add_edge(a_related, extra)

    # if g.degree(a_related) < 3:
    #     return False
    for u in [a, true_1, true_2]:
        for v in [a, true_1, true_2]:
            if u == v:
                continue

            if g.has_edge(u, v):
                return False


    always_same = True
    always_different = True
    true_color = 1
    for a_color in [0, 1]:
        for extra_color in [0, 1]:
            encoder = Encoder(g,
                              precolored={a: a_color, extra: extra_color, true_1: true_color, true_2: true_color},
                              skip_requirements=[a, extra, true_1, true_2])
            all_solutions = encoder.solve()
            if len(all_solutions) == 0:
                raise RuntimeError()

            for coloring in all_solutions:
                if coloring[a_related] == a_color:
                    always_different = False
                else:
                    always_same = False
                if not always_different and not always_same:
                    return False
    return True


if __name__ == "__main__":
    for g in graph_iterator(8):
        if check_graph(g):
            display_graph(g, {i: str(i) for i in g.nodes}, {i: 0 for i in g.nodes})
