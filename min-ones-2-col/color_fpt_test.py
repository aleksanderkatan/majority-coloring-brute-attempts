import networkx as nx
from graphs.graph_display import display_graph
from graphs.new_graph_iterator import directed_graph_iterator, random_digraphs_iterator
from min_ones_ILP_encoder import find_min_ones_coloring
from color_fpt import graph_with_coloring, calculate_min_ones


if __name__ == "__main__":
    # for graph in directed_graph_iterator(3, 7, verbose=True):
    for graph in random_digraphs_iterator(20, 0.2, notification_interval=1):
        coloring = find_min_ones_coloring(graph)
        if coloring is None:
            # the graph is not majority 2-colorable.
            continue

        expected_k = sum([c for _, c in coloring.items()])
        result_k = calculate_min_ones(graph)

        if expected_k != result_k:
            print(expected_k, result_k)
            display_graph(graph)
            result_k = calculate_min_ones(graph)

