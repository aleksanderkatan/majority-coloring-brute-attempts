from find_directed_3_colorings import find_directed_3_colorings
from graphs.display_graph import display_graph
from graphs.graph_iterator import directed_graph_iterator
from graphs.digraph_with_coloring import DigraphWithColoring


if __name__ == "__main__":
    for g in directed_graph_iterator(3, 7, verbose=True):
        all_solutions = find_directed_3_colorings(g, list_all_solutions=False)
        if len(all_solutions) == 0:
            display_graph(g, vertex_colors=all_solutions[0])
        colored = DigraphWithColoring(g, all_solutions[0])
        assert colored.is_correct_coloring()
