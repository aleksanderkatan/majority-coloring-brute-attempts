from find_directed_3_colorings import find_directed_3_colorings
from graphs.display_graph import display_graph
from graphs.graph_iterator import random_digraphs_iterator
from graphs.digraph_with_coloring import DigraphWithColoring

# random 1000 test run finished for n in range(8, 20+1)


if __name__ == "__main__":
    for n in range(8, 20+1):
        for p in range(1, 19+1):
            prob = p/20
            for g in random_digraphs_iterator(n, prob, 10, 1000):
                solutions = find_directed_3_colorings(g, list_all_solutions=False)
                if len(solutions) == 0:
                    display_graph(g)
                colored = DigraphWithColoring(g, solutions[0])
                assert colored.is_correct_coloring()
