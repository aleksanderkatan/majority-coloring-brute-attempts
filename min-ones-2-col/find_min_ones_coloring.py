from ortools.linear_solver import pywraplp
import networkx as nx


class NotMajority2ColorableError(Exception):
    pass


def _sum(elements, negate=False):
    result = 0
    for elem in elements:
        result = result + ((1 - elem) if negate else elem)
    return result


def find_min_ones_coloring(graph: nx.DiGraph):
    """
    Finds a Min-ones Majority 2-Coloring of the given graph that minimizes the number of color 1.

    Args:
        graph (networkx.DiGraph): The graph to color.

    Returns:
        dict[int, int]: A majority 2-coloring minimizing the number of ones.

    Raises:
        NotMajority2ColorableError: If the `graph` argument is not a majority 2-colorable graph.
    """

    solver = pywraplp.Solver.CreateSolver("SAT")
    variables = {}

    for vertex in graph.nodes:
        variables[vertex] = solver.IntVar(0, 1, str(vertex))

    for vertex in graph.nodes:
        neighbourhood = [variables[n] for n in graph.neighbors(vertex)]
        requirement = (len(neighbourhood) + 1) // 2
        constraint_if_0 = _sum(neighbourhood) >= requirement * (1 - variables[vertex])
        constraint_if_1 = _sum(neighbourhood, negate=True) >= requirement * variables[vertex]
        solver.Add(constraint_if_0)
        solver.Add(constraint_if_1)


    solver.Minimize(_sum([variables[v] for v in graph.nodes]))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {}
        for vertex in graph.nodes:
            solution[vertex] = int(variables[vertex].solution_value())
        return solution
    raise NotMajority2ColorableError


