import networkx
from networkx import fast_gnp_random_graph

from all_3colorings_encoder import Encoder
from graphs.graph_display import display_graph
import time
from graphs.new_graph_iterator import directed_graph_iterator, random_digraphs_iterator


if __name__ == "__main__":
    for i in range(6, 7+1):
        known = {}
        for g in directed_graph_iterator(i, i, verbose=True):
            if not networkx.is_strongly_connected(g):
                continue
            encoder = Encoder(g, list_all_solutions=True)
            all_solutions = encoder.solve()
            degrees = tuple([g.in_degree(v) for v in g.nodes]) + tuple(g.out_degree(v) for v in g.nodes)
            if degrees not in known:
                known[degrees] = (len(all_solutions), g)
            if known[degrees][0] != len(all_solutions):
                print(degrees)
                display_graph(known[degrees][1])
                display_graph(g)



