import networkx as nx
from all_colorings_encoder import Encoder
import itertools
import random
from graph_display import display_graph


def graph_iterator():
    # for g in nx.graph_atlas_g():
    #     if len(g.nodes) < 3 or not nx.is_connected(g):
    #         continue
    #     for a, b, c in itertools.combinations(g.nodes, 3):
    #         yield a, b, c, g
    nodes = 10
    edges_min = 10
    edges_max = 100
    while True:
        g = nx.Graph()
        g.add_nodes_from(range(nodes))
        for _ in range(random.randint(edges_min, edges_max)):
            u = random.randint(0, nodes - 1)
            v = random.randint(0, nodes - 1)
            if u == v:
                continue
            if g.has_edge(u, v):
                continue
            g.add_edge(u, v)

        if len(g.nodes) < 3 or not nx.is_connected(g):
            continue
        for a, b, c in itertools.combinations(g.nodes, 3):
            yield a, b, c, g

        for a, b, c in itertools.combinations(g.nodes, 3):
            yield a, b, c, g


def iterate_construction(a, b, c, g):
    ug = nx.disjoint_union(g, g)
    a, b, c, d, e, f = a, b, c, a + len(g.nodes), b + len(g.nodes), c + len(g.nodes)
    # print(ug.nodes, a, b, c, d, e, f)

    cg = nx.contracted_nodes(ug, b, d)
    a, bd, c, e, f = a, b, c, e, f
    # print(cg.nodes, a, bd, c, e, f)

    rg = nx.convert_node_labels_to_integers(cg)
    a, bd, c, e, f = a, bd, c, e-1, f-1
    # print(rg.nodes, a, bd, c, e, f)

    return a, bd, c, e, f, rg



if __name__ == "__main__":
    for A, B, C, g in graph_iterator():
        valid = True

        encoder = Encoder(g)
        all_solutions = encoder.solve()
        for solution in all_solutions:
            valid = valid and solution[A] == solution[B]
            valid = valid and solution[A] == solution[C]

        if valid:
            print("triple")
            # display_graph(g, {A: "A", B: "B", C: "C"}, all_solutions[0])
            A1, BD, C1, E1, F1, g1 = iterate_construction(A, B, C, g)
            # display_graph(g1, {A1: "A", BD: "BD", C1: "C", E1: "E", F1: "F"}, {i: 1 for i in g1.nodes})

            encoder1 = Encoder(g1)
            all_solutions1 = encoder1.solve()
            for solution in all_solutions1:
                valid = valid and solution[A1] == solution[BD]
                valid = valid and solution[A1] == solution[C1]
                valid = valid and solution[A1] == solution[E1]
                valid = valid and solution[A1] == solution[F1]

            if valid:
                display_graph(g, {A: "A", B: "B", C: "C"}, all_solutions[0])
                display_graph(g1, {A1: "A", BD: "BD", C1: "C", E1: "E", F1: "F"}, all_solutions1[0])





