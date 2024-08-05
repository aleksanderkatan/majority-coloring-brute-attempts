import itertools

import networkx as nx

from networkx import fast_gnp_random_graph

amounts = {
    2: 1,
    3: 2,
    4: 6,
    5: 21,
    6: 112,
    7: 853,
    8: 11117,
    9: 261080,
    10: 11716571,
}

directed_oriented_amounts = {
    2: 2,
    3: 7,
    4: 42,
    5: 582,
    6: 21480,
    7: 2142288,
}

directed_amounts = {
    1: 1,
    2: 3,
    3: 16,
    4: 218,
    5: 9608,
    6: 1540944,
}


def next_int(file):
    word = ''
    while True:
        char = file.read(1)
        if char.isalnum():
            word += char
        elif char == '':
            return None
        else:
            if word:
                return int(word)


def graph_iterator(n):
    for i in range(2, n+1):
        print(f"Onto {i} vertices.")
        with open(f"../graphs/graph_files/{i}.txt", mode="r") as f:
            count = 0

            while True:
                eof_test = next_int(f)
                if eof_test is None:
                    break

                n, m = eof_test, next_int(f)
                g = nx.Graph()
                g.add_nodes_from(range(n))

                for _ in range(m):
                    u, v = next_int(f), next_int(f)
                    g.add_edge(u, v)
                yield g

                count += 1
                if count*100//amounts[i] > (count-1)*100//amounts[i]:
                    print(f"{count*100//amounts[i]}% done.")


def directed_graph_iterator(_from, to, verbose=True, oriented=True):
    path = "orient" if oriented else "dig"
    amounts = directed_oriented_amounts if oriented else directed_amounts

    for i in range(_from, to + 1):
        print(f"Onto {i} vertices.")
        with open(f"../graphs/graph_files/{path}{i}.txt", mode="r") as f:
            count = 0

            while True:
                eof_test = next_int(f)
                if eof_test is None:
                    break

                n, m = eof_test, next_int(f)
                g = nx.DiGraph()
                g.add_nodes_from(range(n))

                for _ in range(m):
                    u, v = next_int(f), next_int(f)
                    g.add_edge(u, v)
                yield g

                count += 1
                if verbose and count * 100 // amounts[i] > (count - 1) * 100 // amounts[i]:
                    print(f"{count * 100 // amounts[i]}% done.")


def random_digraphs_iterator(nodes, edge_probability=0.5, notification_interval=None):
    count = 0
    while True:
        count += 1
        if notification_interval is not None and count % notification_interval == 0:
            print(f"Random graph {count}")
        yield fast_gnp_random_graph(nodes, edge_probability, seed=42+count, directed=True)


def all_permutations(graph: nx.Graph):
    for perm in itertools.permutations(graph.nodes):
        if graph.is_directed():
            new_graph = nx.DiGraph()
        else:
            new_graph = nx.Graph()
        for u, v in graph.edges:
            new_graph.add_edge(perm[u], perm[v])
        yield new_graph
