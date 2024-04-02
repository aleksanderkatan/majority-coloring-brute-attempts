from all_colorings_encoder import Encoder
from graph_display import display_graph
from graphs.graph_iterator import graph_iterator


def find_correlations(g, colorings):
    same = set(g.nodes)
    different = set(g.nodes)
    for coloring in colorings:
        same_colored = {v for v in g.nodes if coloring[v] == coloring[0]}
        differently_colored = {v for v in g.nodes if coloring[v] != coloring[0]}
        same = same - differently_colored
        different = different - same_colored
    return same, different


def find_leniency(g, colorings):
    result = {i: len(g.nodes) for i in g.nodes}
    for coloring in colorings:
        for v in g.nodes:
            colored_the_same = len([n for n in g.neighbors(v) if coloring[n] == coloring[v]])
            colored_differently = g.degree(v) - colored_the_same
            result[v] = min(result[v], colored_differently-colored_the_same)
    return result


if __name__ == "__main__":
    for g in graph_iterator(6):
        # 0 is the vertex that others will try to copy
        encoder = Encoder(g, skip_requirements=[0])
        all_solutions = encoder.solve()

        always_equal, always_different = find_correlations(g, all_solutions)
        leniency = find_leniency(g, all_solutions)

        # display_graph(g, {i: str(i) for i in g.nodes}, all_solutions[0])

        for v in g.nodes:
            if leniency[v] > 1:
                print(always_equal, always_different)
                print(leniency)
                for sol in all_solutions:
                    display_graph(g, {i: str(i) for i in g.nodes}, sol)
                break






