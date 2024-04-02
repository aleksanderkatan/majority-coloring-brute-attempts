from all_colorings_encoder import Encoder
from graphs.graph_display import display_graph
from graphs.new_graph_iterator import graph_iterator


def check_graph(g, a):
    always_same = {i for i in g.nodes if i != a}
    always_different = {i for i in g.nodes if i != a and not g.has_edge(i, a)}

    encoder = Encoder(g, skip_requirements=[a])
    all_solutions = encoder.solve()
    if len(all_solutions) == 0:
        raise RuntimeError()

    for coloring in all_solutions:
        same = {v for v in g.nodes if v != a and coloring[v] == coloring[a]}
        different = {v for v in g.nodes if v != a and coloring[v] != coloring[a]}

        always_same = always_same - different
        always_different = always_different - same

        if len(always_same) == 0 and len(always_different) == 0:
            return False

    print(a, always_same, always_different)
    return True


def check_graph(g, a):
    encoder = Encoder(g)
    all_solutions = encoder.solve()
    if len(all_solutions) == 0:
        raise RuntimeError()

    for coloring in all_solutions:
        same = {v for v in g.nodes if v != a and coloring[v] == coloring[a]}
        different = {v for v in g.nodes if v != a and coloring[v] != coloring[a]}

        always_same = always_same - different
        always_different = always_different - same

        if len(always_same) == 0 and len(always_different) == 0:
            return False

    print(a, always_same, always_different)
    return True



# sprawdzone do 9 włącznie


if __name__ == "__main__":
    for g in graph_iterator(10):
        # display_graph(g)
        for a in g.nodes:
            if check_graph(g, a):
                encoder = Encoder(g, skip_requirements=[a])
                all_solutions = encoder.solve()
                for solution in all_solutions:
                    display_graph(g, {i: str(i) for i in g.nodes}, solution)
