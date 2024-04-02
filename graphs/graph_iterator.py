import networkx as nx
import random
import itertools


def filter(g):
    if len(g.nodes) < 4 or not nx.is_connected(g):
        return False
    return True


def all_first_vertices(g):
    yield g
    for i in range(1, len(g.nodes)):
        mapping = {0: i, i: 0}
        yield nx.relabel_nodes(g, mapping)


def all_base_graphs():
    for g in nx.graph_atlas_g():
        yield g


def random_graphs():
    nodes = 12
    edges_min = 0
    edges_max = 144
    count = 0
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

        if not filter(g):
            continue
        count += 1
        if count % 100 == 0:
            print(f"Random graph {count}")
        yield g


def all_graphs(n):
    for i in range(1, n+1):
        print(f"Onto {i} vertices")
        edges = []
        for u in range(i-1):
            for v in range(u+1, i):
                edges.append((u, v))
        for num_edges in range(i-1, len(edges)+1):
            for subset in itertools.combinations(edges, num_edges):
                g = nx.Graph()
                for u, v in subset:
                    g.add_edge(u, v)
                if len(g.nodes) < i:
                    continue
                yield g


def graph_iterator(vertex_limit=3):
    print("NX graphs")
    for g in all_base_graphs():
        if not filter(g):
            continue
        for g0 in all_first_vertices(g):
            yield g0

    print(f"All graphs (up to {vertex_limit} vertices)")
    for g in all_graphs(vertex_limit):
        if not filter(g):
            continue
        yield g

    print("Random graphs")
    for g in random_graphs():
        if not filter(g):
            continue
        yield g



