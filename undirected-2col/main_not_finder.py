from all_colorings_encoder import Encoder
from graphs.display_graph import display_graph
from graphs.new_graph_iterator import graph_iterator


# sprawdzone NOT do 7 włącznie
# sprawdzone bez not do 6 włącznie


def check_graph(g):
    v = 0
    not_v = 1
    not_v_extra = len(g.nodes)
    g.add_edge(not_v, not_v_extra)

    # if g.degree(a_related) < 3:
    #     return False

    for v_color in [0, 1]:
        for not_v_extra_color in [0, 1]:
            encoder = Encoder(g,
                              precolored={v: v_color, not_v_extra: not_v_extra_color},
                              skip_requirements=[v, not_v_extra])
            all_solutions = encoder.solve()
            if len(all_solutions) == 0:
                raise RuntimeError()

            for coloring in all_solutions:
                if coloring[not_v] == v_color:
                    return False
    return True


if __name__ == "__main__":
    for g in graph_iterator(9):
        if check_graph(g):
            display_graph(g, {i: str(i) for i in g.nodes}, {i: 0 for i in g.nodes})
