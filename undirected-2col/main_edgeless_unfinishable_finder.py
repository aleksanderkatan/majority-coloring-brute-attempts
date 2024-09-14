from find_undirected_2_colorings import find_undirected_2_colorings
from graphs.display_graph import display_graph
from graphs.graph_iterator import graph_iterator


def check_graph(g):
    for v in g.nodes:
        for u in g.nodes:
            if v == u or g.has_edge(u, v):
                continue
            for v_color in [0, 1]:
                all_solutions = find_undirected_2_colorings(g, list_all_solutions=False,
                                                            precolored={v: v_color, u: 0},
                                                            skip_requirements={v, u}
                                                            )
            if len(all_solutions) == 0:
                return True
    return False


if __name__ == "__main__":
    for g in graph_iterator(9):
        if check_graph(g):
            display_graph(g, {i: str(i) for i in g.nodes}, {i: 0 for i in g.nodes})
