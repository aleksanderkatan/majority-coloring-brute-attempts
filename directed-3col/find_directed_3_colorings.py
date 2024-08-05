import networkx as nx
from ortools.sat.python import cp_model


class TooManySolutionsException(Exception):
    pass


class SolutionCollector(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables, solution_limit=None):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.variables = variables
        self.solution_limit = solution_limit
        self.solutions = []

    def on_solution_callback(self):
        result = {}
        for vertex, variables in self.variables:
            if self.Value(variables[0]) == 1:
                result[vertex] = 0
            elif self.Value(variables[1]) == 1:
                result[vertex] = 1
            else:
                result[vertex] = 2
        self.solutions.append(result)
        if self.solution_limit is not None and len(self.solutions) > self.solution_limit:
            raise TooManySolutionsException()


def _sum(elements, negate=False):
    result = 0
    for elem in elements:
        result = result + ((1 - elem) if negate else elem)
    return result


def find_directed_3_colorings(graph, list_all_solutions, force_2_cols=False, solution_limit=None):
    """
    Finds and lists all majority 3-colorings of the given directed graph.

    Args:
        graph (networkx.Graph): The graph to color.
        list_all_solutions (bool): A flag that when set to true limits the result to at most one coloring.
        force_2_cols (bool): A flag that when set to true limits the result colorings to only use 2 colors.
        solution_limit (int): An upper limit for the number of solutions returned.

    Returns:
        list[dict[int, int]]: A list of all majority 3-colorings of the graph `graph`.

    Notes:
        The function assumes that the input graph is a directed graph.
    """

    assert nx.is_directed(graph)

    model = cp_model.CpModel()
    # prepare variables

    # c[v][i] = 1 iff v is colored i
    c = {}
    for vertex in graph.nodes:
        c[vertex] = {}
        c[vertex][0] = model.NewIntVar(0, 1, "")
        c[vertex][1] = model.NewIntVar(0, 1, "")
        c[vertex][2] = model.NewIntVar(0, 1, "")

        if force_2_cols:
            model.Add(c[vertex][2] == 0)

    # s[v][i] = k iff v has k i-colored out-neighbours
    s = {}
    for vertex in graph.nodes:
        s[vertex] = {}
        s[vertex][0] = model.NewIntVar(0, graph.out_degree(vertex), "")
        s[vertex][1] = model.NewIntVar(0, graph.out_degree(vertex), "")
        s[vertex][2] = model.NewIntVar(0, graph.out_degree(vertex), "")


    # generate constraints

    # vertex has exactly one color
    for vertex in graph.nodes:
        model.Add(c[vertex][0] + c[vertex][1] + c[vertex][2] == 1)

    # s is calculated correctly
    for vertex in graph.nodes:
        for i in range(3):
            neighbor_sum = 0
            for neighbor in graph.neighbors(vertex):
                neighbor_sum = neighbor_sum + c[neighbor][i]
            model.Add(neighbor_sum == s[vertex][i])

    # at most half is of the same color
    for vertex in graph.nodes:
        out_total = graph.out_degree(vertex)
        out_same_color_limit = out_total//2
        for i in range(3):
            model.Add(s[vertex][i] - (1 - c[vertex][i]) * out_total <= out_same_color_limit)


    # find  solutions
    solver = cp_model.CpSolver()
    collector = SolutionCollector([(vertex, c[vertex]) for vertex in graph.nodes], solution_limit=solution_limit)
    solver.parameters.enumerate_all_solutions = list_all_solutions
    _ = solver.Solve(model, collector)

    return collector.solutions
