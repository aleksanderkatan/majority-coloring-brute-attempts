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


class Encoder:
    def __init__(self, g, precolored=None, skip_requirements=None, required_leniency=None, force_2_cols=False):
        assert nx.is_directed(g)

        # if precolored is None:
        #     precolored = {}
        # if skip_requirements is None:
        #     skip_requirements = []
        # if required_leniency is None:
        #     required_leniency = {}
        self.graph = g
        # self.precolored = precolored
        # self.skip_requirements = skip_requirements
        # self.required_leniency = required_leniency
        self.variables = {}
        self.edges = {}
        self.model = cp_model.CpModel()
        self.force_2_cols = force_2_cols

    def solve(self):
        # prepare variables

        # c[v][i] = 1 iff v is colored i
        c = {}
        for vertex in self.graph.nodes:
            c[vertex] = {}
            c[vertex][0] = self.model.NewIntVar(0, 1, "")
            c[vertex][1] = self.model.NewIntVar(0, 1, "")
            c[vertex][2] = self.model.NewIntVar(0, 1, "")

            if self.force_2_cols:
                self.model.Add(c[vertex][2] == 0)

        # s[v][i] = k iff v has k i-colored out-neighbours
        s = {}
        for vertex in self.graph.nodes:
            s[vertex] = {}
            s[vertex][0] = self.model.NewIntVar(0, self.graph.out_degree(vertex), "")
            s[vertex][1] = self.model.NewIntVar(0, self.graph.out_degree(vertex), "")
            s[vertex][2] = self.model.NewIntVar(0, self.graph.out_degree(vertex), "")


        # generate constraints

        # vertex has exactly one color
        for vertex in self.graph.nodes:
            self.model.Add(c[vertex][0] + c[vertex][1] + c[vertex][2] == 1)

        # s is calculated correctly
        for vertex in self.graph.nodes:
            for i in range(3):
                neighbor_sum = 0
                for neighbor in self.graph.neighbors(vertex):
                    neighbor_sum = neighbor_sum + c[neighbor][i]
                self.model.Add(neighbor_sum == s[vertex][i])

        # # at most half is of the same color
        for vertex in self.graph.nodes:
            out_total = self.graph.out_degree(vertex)
            out_same_color_limit = out_total//2
            for i in range(3):
                self.model.Add(s[vertex][i] - (1 - c[vertex][i]) * out_total <= out_same_color_limit)

        # break symmetry, at least a little bit
        # self.model.Add(c[0][0] == 1)


        # find all solutions
        solver = cp_model.CpSolver()
        collector = SolutionCollector([(vertex, c[vertex]) for vertex in self.graph.nodes])
        solver.parameters.enumerate_all_solutions = True
        _ = solver.Solve(self.model, collector)

        return collector.solutions