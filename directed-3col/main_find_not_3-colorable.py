from all_3colorings_encoder import Encoder
from graphs.graph_display import display_graph
from graphs.new_graph_iterator import directed_graph_iterator

# up to and including 6 vertices
def filter(g, solutions):
    for u in g.nodes:
        for v in g.nodes:
            if u == v:
                continue
            if g.has_edge(u, v) or g.has_edge(v, u):
                continue
            s = set()
            for solution in all_solutions:
                s.add((solution[u], solution[v]))
            if len(s) != 9:
                return u, v
    return None


if __name__ == "__main__":
    for g in directed_graph_iterator(8):
        encoder = Encoder(g)
        all_solutions = encoder.solve()
        # for solution in all_solutions:
        #     print(solution)
            # display_graph(g, vertex_colors=solution)

        pair = filter(g, all_solutions)
        if pair is not None:
            print(pair)
            display_graph(g)
