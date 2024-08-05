import networkx as nx

from find_directed_3_colorings import find_directed_3_colorings, TooManySolutionsException
from graphs.display_graph import display_graph
from graphs.graph_iterator import random_digraphs_iterator, directed_graph_iterator


if __name__ == "__main__":
    # minimum = 3 ** 7
    # for g in directed_graph_iterator(7, 7):
    #     try:
    #         all_solutions = find_directed_3_colorings(g, list_all_solutions=False)
    #         minimum = min(len(all_solutions), minimum)
    #     except TooManySolutionsException:
    #         pass
    # print(minimum)


    # for n in range(3, 20):
    #     minimum = 3 ** n
    #     for g, _ in zip(random_digraphs_iterator(n, 0.5, 1), range(10)):
    #         try:
    #             all_solutions = find_directed_3_colorings(g, list_all_solutions=True, solution_limit=minimum)
    #             minimum = min(len(all_solutions), minimum)
    #         except TooManySolutionsException:
    #             pass
    #     print(f"n={n}: {minimum}")
    #
    # for n in range(3, 20):
    #     print(f"Onto {n} vertices.")
    #     for g, _ in zip(random_digraphs_iterator(n, 0.5, 100), range(1000)):
    #         all_solutions = find_directed_3_colorings(g, list_all_solutions=False)
    #         if len(all_solutions) == 0:
    #             display_graph(g)

    for n in range(3, 20):
        minimum = 3 ** n
        min_g = None
        for g in directed_graph_iterator(n, n):
            if not nx.is_strongly_connected(g):
                continue
            try:
                all_solutions = find_directed_3_colorings(g, list_all_solutions=True, solution_limit=minimum)
                if len(all_solutions) < minimum:
                    minimum = len(all_solutions)
                    min_g = g
            except TooManySolutionsException:
                pass
        print(f"n={n}: {minimum}")
        display_graph(min_g)
