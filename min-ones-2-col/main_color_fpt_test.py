import networkx as nx
from graphs.display_graph import display_graph
from graphs.graph_iterator import directed_graph_iterator, random_digraphs_iterator
from find_min_ones_coloring import find_min_ones_coloring_cp, NotMajority2ColorableError
from color_fpt import DigraphWithColoring, calculate_min_ones_fpt


if __name__ == "__main__":
    # for graph in directed_graph_iterator(3, 7, verbose=True):
    for graph in random_digraphs_iterator(15, 0.2, notification_interval=100):
        try:
            coloring = find_min_ones_coloring_cp(graph)
        except NotMajority2ColorableError:
            # the graph is not majority 2-colorable.
            continue

        expected_k = sum([c for _, c in coloring.items()])
        result_k = calculate_min_ones_fpt(graph)

        if expected_k != result_k:
            print(expected_k, result_k)
            display_graph(graph)
            result_k = calculate_min_ones_fpt(graph)


