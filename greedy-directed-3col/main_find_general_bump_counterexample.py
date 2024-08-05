from queue import Queue

from graphs.digraph_with_coloring import DigraphWithColoring
from graphs.display_graph import display_graph
from graphs.graph_iterator import directed_graph_iterator, all_permutations
from color_greedily_bump_unsatisfied import color_greedily
# from color_greedily_but_choose_best_color import color_greedily
# from color_greedily_num_of_bichromatic_edges import color_greedily
# from color_greedily_bump_all_neighbors import color_greedily
from color_greedily_bump_one_wrong_neighbor import color_greedily
# from graphs.display_graph import display_graph
import networkx as nx


def flatten(col):
    return (col[i] for i in range(len(col)))


def is_counterexample(g):
    starting_col = {v: 0 for v in g.nodes}
    reachable = {flatten(starting_col)}
    q = Queue()
    q.put(starting_col)
    while not q.empty():
        current_col = q.get()
        if flatten(current_col) in reachable:
            continue
        reachable.add(flatten(current_col))

        colored = DigraphWithColoring(g, current_col)
        all_unsatisfied = colored.find_all_unsatisfied_vertices()
        if len(all_unsatisfied) == 0:
            return False
        for v in all_unsatisfied:
            # for c in [0, 1, 2]:
            #     cp = dict(current_col)
            #     cp[v] = c
            #     q.put(cp)
            c = (current_col[v] + 1) % 3
            cp = dict(current_col)
            cp[v] = c
            q.put(cp)
    return True


if __name__ == "__main__":
    for graph in directed_graph_iterator(7, 7):
        if is_counterexample(graph):
            display_graph(graph)
