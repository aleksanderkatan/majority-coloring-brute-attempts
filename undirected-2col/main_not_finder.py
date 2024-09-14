from find_undirected_2_colorings import find_undirected_2_colorings
from graphs.display_graph import display_graph
from graphs.graph_iterator import graph_iterator


def check_graph(g):
    for v in g.nodes:
        for not_v in g.nodes:
            if v == not_v:
                continue
            not_v_extra = len(g.nodes)
            g.add_edge(not_v, not_v_extra)

            for v_color in [0, 1]:
                for not_v_extra_color in [0, 1]:
                    all_solutions = find_undirected_2_colorings(g, list_all_solutions=True,
                                                                precolored={v: v_color, not_v_extra: not_v_extra_color},
                                                                skip_requirements={v, not_v_extra}
                                                                )
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
