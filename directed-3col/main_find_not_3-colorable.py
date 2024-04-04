import networkx
from networkx import fast_gnp_random_graph

from all_3colorings_encoder import Encoder
from graphs.graph_display import display_graph
import time
from graphs.new_graph_iterator import directed_graph_iterator, random_digraphs_iterator


if __name__ == "__main__":
    # for i in range(3, 1000):
    #     current_min = 2 ** 1000
    #     for j in range(1, 10):
    #         for k in range(100):
    #             g = fast_gnp_random_graph(i, j/100, directed=True)
    #             largest_cc_set = max(networkx.weakly_connected_components(g), key=len)
    #             if len(largest_cc_set) < i:
    #                 continue
    #             encoder = Encoder(g, list_all_solutions=True)
    #             all_solutions = encoder.solve()
    #             current_min = min(current_min, len(all_solutions))
    #     print(f"{i} nodes: {current_min}")


    for i in range(6, 7+1):
        current_min = 2 ** 1000
        min_realize = None
        for g in directed_graph_iterator(i, i, verbose=True):
            if not networkx.is_strongly_connected(g):
                continue
            encoder = Encoder(g, list_all_solutions=True)
            all_solutions = encoder.solve()

            if current_min > len(all_solutions):
                current_min = len(all_solutions)
                min_realize = g

        print(f"{i}: {current_min}")
        # display_graph(min_realize)

