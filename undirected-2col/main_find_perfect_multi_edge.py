import networkx as nx
from all_colorings_encoder import Encoder
from graphs.graph_display import display_graph
from graphs.new_graph_iterator import graph_iterator


def check_all_connections(g: nx.Graph):
    v = len(g.nodes)
    v_copy1, v_copy2 = v+1, v+2
    for v_n in g.nodes:
        for v_copy1_n in g.nodes:
            for v_copy2_n in g.nodes:
                if v_copy1_n == v_copy2_n:
                    continue
                new_g = g.copy()
                new_g.add_edge(v, v_n)
                new_g.add_edge(v_copy1, v_copy1_n)
                new_g.add_edge(v_copy2, v_copy2_n)
                encoder = Encoder(new_g, skip_requirements=[v, v_copy1, v_copy2])
                all_solutions = encoder.solve()
                valid = True
                for solution in all_solutions:
                    if solution[v_copy1_n] != solution[v_n] or solution[v_copy2_n] != solution[v_n]:
                        valid = False
                        break
                if valid:
                    return (v, v_n), (v_copy1, v_copy1_n), (v_copy2, v_copy2_n), new_g
    return None


if __name__ == "__main__":
    g = nx.from_edgelist([(0, 1), (1, 2), (1, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 6), (5, 6)])
    encoder = Encoder(g)
    all_solutions = encoder.solve()
    for solution in all_solutions:
        display_graph(g, vertex_colors=solution)

    # for g in graph_iterator(10):
    #     # display_graph(g)
    #     result = check_all_connections(g)
    #     if result is not None:
    #         print(result)
    #         display_graph(result[3])
