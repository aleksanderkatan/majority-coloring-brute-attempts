from graphs.graph_iterator import directed_graph_iterator
# from color_greedily import color_greedily
from color_greedily_but_choose_best_color import color_greedily
# from color_greedily_bump_all_neighbors import color_greedily
# from color_greedily_bump_one_wrong_neighbor import color_greedily
from graphs.display_graph import display_graph
import networkx as nx


if __name__ == "__main__":
    for graph in directed_graph_iterator(3, 6):
        steps, coloring = color_greedily(graph, display=True)
        if coloring is None:
            display_graph(graph)

