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


if __name__ == "__main__":
    for graph_base in directed_graph_iterator(3, 6):
        for graph in all_permutations(graph_base):
            steps, coloring = color_greedily(graph, display=False)
            if coloring is None:
                print("Returned no coloring.")
                display_graph(graph)
                color_greedily(graph, display=True)
                continue
            colored = DigraphWithColoring(graph, coloring)
            if not colored.is_correct_coloring():
                print("Returned invalid coloring.")
                display_graph(graph, vertex_colors=coloring)
                color_greedily(graph, display=True)
                continue
