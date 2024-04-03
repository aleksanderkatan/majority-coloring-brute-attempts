from all_3colorings_encoder import Encoder
from graphs.graph_display import display_graph
import time
from graphs.new_graph_iterator import directed_graph_iterator, random_digraphs_iterator


def filter(g, solutions):
    for u in g.nodes:
        for v in g.nodes:
            if u == v:
                continue
            fine = False
            for solution in solutions:
                if solution[u] != solution[v]:
                    fine = True
                    break
            if not fine:
                return u, v
    return None



if __name__ == "__main__":
    start_time = time.time()
    for g in directed_graph_iterator(3, 6):
    # for g in random_digraphs_iterator(10, notification_interval=100):
        encoder = Encoder(g, list_all_solutions=True)
        all_solutions = encoder.solve()

        pair = filter(g, all_solutions)
        if pair is not None:
            print(pair)
            display_graph(g)
        # encoder = Encoder(g, list_all_solutions=False, workers=1)
        # all_solutions = encoder.solve()
        #
        # if len(all_solutions) == 0:
        #     display_graph(g)
    print(f"--- {(time.time() - start_time)} seconds ---")
