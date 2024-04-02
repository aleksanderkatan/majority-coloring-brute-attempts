from all_colorings_encoder import Encoder
from graph_display import display_graph
from graphs.graph_iterator import graph_iterator

# sprawdzone do 7 włącznie


def check_graph(g):
    A = 0
    B = 1
    TRUE = 2
    OR = 3
    EXTRA = len(g.nodes)
    g.add_edge(OR, EXTRA)

    TRUE_color = 1
    for A_color in [0, 1]:
        for B_color in [0, 1]:
            for EXTRA_color in [0, 1]:
                encoder = Encoder(g, precolored={A: A_color, B: B_color, TRUE: TRUE_color, EXTRA: EXTRA_color})
                all_solutions = encoder.solve()
                if len(all_solutions) == 0:
                    return False

                for coloring in all_solutions:
                    if coloring[OR] != min(A_color, B_color):
                        return False
    return True


if __name__ == "__main__":
    for g in graph_iterator(8):
        if check_graph(g):
            display_graph(g, {i: str(i) for i in g.nodes}, {i: 0 for i in g.nodes})
