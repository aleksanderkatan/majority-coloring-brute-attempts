import networkx as nx
from ortools.sat.python import cp_model


class SolutionCollector(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.variables = variables
        self.solutions = []

    def on_solution_callback(self):
        result = {}
        for var in self.variables:
            result[int(str(var))] = self.Value(var)
        self.solutions.append(result)


def _sum(elements, negate=False):
    result = 0
    for elem in elements:
        result = result + ((1 - elem) if negate else elem)
    return result


def find_undirected_2_colorings(graph, list_all_solutions, precolored=None, skip_requirements=None):
    """
    Finds and lists all majority 2-colorings of the given undirected graph,
    while respecting given constraints.

    Args:
        graph (networkx.Graph): The graph to color.
        list_all_solutions (bool): A flag that when set to true limits the result to at most one coloring.
        precolored (dict[int, int]): A dictionary of pairs (vertex, color), the result colorings are limited only to ones matching those pairs.
        skip_requirements (set[int]): A set of vertices that are omitted from the cardinality constraints, in other words the set of lenient vertices.

    Returns:
        list[dict[int, int]]: A list of all majority 2-colorings satisfying the constraints given in arguments.

    Notes:
        The function assumes that the input graph is an undirected graph.
    """

    assert not nx.is_directed(graph)
    if precolored is None:
        precolored = {}
    if skip_requirements is None:
        skip_requirements = []
    variables = {}
    model = cp_model.CpModel()
    for vertex in graph.nodes:
        variables[vertex] = model.NewIntVar(0, 1, str(vertex))

    for vertex in graph.nodes:
        if vertex in precolored:
            model.Add(variables[vertex] == precolored[vertex])
        if vertex in skip_requirements:
            continue
        neighbourhood = [variables[n] for n in graph.neighbors(vertex)]
        requirement = (len(neighbourhood) + 1) // 2
        constraint_if_0 = _sum(neighbourhood) >= requirement * (1 - variables[vertex])
        constraint_if_1 = _sum(neighbourhood, negate=True) >= requirement * variables[vertex]
        model.Add(constraint_if_0)
        model.Add(constraint_if_1)

    solver = cp_model.CpSolver()
    collector = SolutionCollector([var for var_name, var in variables.items()])
    solver.parameters.enumerate_all_solutions = list_all_solutions
    _ = solver.Solve(model, collector)

    return collector.solutions
