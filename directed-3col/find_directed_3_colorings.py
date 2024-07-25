import networkx as nx
from ortools.sat.python import cp_model


class SolutionCollector(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.variables = variables
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


def _sum(elements, negate=False):
    result = 0
    for elem in elements:
        result = result + ((1 - elem) if negate else elem)
    return result


def find_directed_3_colorings(g, list_all_solutions, force_2_cols=False):
    assert nx.is_directed(g)

    model = cp_model.CpModel()
    # prepare variables

    # c[v][i] = 1 iff v is colored i
    c = {}
    for vertex in g.nodes:
        c[vertex] = {}
        c[vertex][0] = model.NewIntVar(0, 1, "")
        c[vertex][1] = model.NewIntVar(0, 1, "")
        c[vertex][2] = model.NewIntVar(0, 1, "")

        if force_2_cols:
            model.Add(c[vertex][2] == 0)

    # s[v][i] = k iff v has k i-colored out-neighbours
    s = {}
    for vertex in g.nodes:
        s[vertex] = {}
        s[vertex][0] = model.NewIntVar(0, g.out_degree(vertex), "")
        s[vertex][1] = model.NewIntVar(0, g.out_degree(vertex), "")
        s[vertex][2] = model.NewIntVar(0, g.out_degree(vertex), "")


    # generate constraints

    # vertex has exactly one color
    for vertex in g.nodes:
        model.Add(c[vertex][0] + c[vertex][1] + c[vertex][2] == 1)

    # s is calculated correctly
    for vertex in g.nodes:
        for i in range(3):
            neighbor_sum = 0
            for neighbor in g.neighbors(vertex):
                neighbor_sum = neighbor_sum + c[neighbor][i]
            model.Add(neighbor_sum == s[vertex][i])

    # at most half is of the same color
    for vertex in g.nodes:
        out_total = g.out_degree(vertex)
        out_same_color_limit = out_total//2
        for i in range(3):
            model.Add(s[vertex][i] - (1 - c[vertex][i]) * out_total <= out_same_color_limit)


    # find  solutions
    solver = cp_model.CpSolver()
    collector = SolutionCollector([(vertex, c[vertex]) for vertex in g.nodes])
    solver.parameters.enumerate_all_solutions = list_all_solutions
    _ = solver.Solve(model, collector)

    return collector.solutions
