from graphs.graph_iterator import directed_graph_iterator
# from color_greedily import color_greedily
from color_greedily_but_choose_best_color import color_greedily
# from color_greedily_bump_all_neighbors import color_greedily
# from color_greedily_bump_one_wrong_neighbor import color_greedily
from graphs.display_graph import display_graph
import networkx as nx


if __name__ == "__main__":
    c4 = nx.from_edgelist([(0, 1), (1, 2), (2, 3), (3, 0)], create_using=nx.DiGraph)
    steps, coloring = color_greedily(c4, display=False)
    print(coloring)
    for graph in directed_graph_iterator(4, 4):
        steps, coloring = color_greedily(graph, display=False)
        display_graph(graph, vertex_colors={i: coloring[i] for i in graph.nodes})
        if coloring is None:
            display_graph(graph)

