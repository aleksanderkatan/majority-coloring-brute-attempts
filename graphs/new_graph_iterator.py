import networkx as nx
import itertools


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
        with open(f"../graphs/{i}.txt", mode="r") as f:
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


def directed_graph_iterator(n):
    for g in graph_iterator(n):
        for orientation in itertools.product([0, 1], repeat=len(g.edges)):
            directed = nx.DiGraph()
            for (u, v), o in zip(g.edges, orientation):
                if o:
                    directed.add_edge(u, v)
                else:
                    directed.add_edge(v, u)
            yield directed
