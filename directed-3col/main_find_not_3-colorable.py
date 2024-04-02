from all_3colorings_encoder import Encoder
from graphs.graph_display import display_graph
from graphs.new_graph_iterator import directed_graph_iterator


# up to and including 6 vertices

if __name__ == "__main__":
    for g in directed_graph_iterator(3):
        encoder = Encoder(g, list_all_solutions=False)
        all_solutions = encoder.solve()

        # if len(all_solutions) == 0:
        #     display_graph(g)
