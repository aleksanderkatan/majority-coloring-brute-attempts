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


class Encoder:
    def __init__(self, g, precolored=None, skip_requirements=None):
        if precolored is None:
            precolored = {}
        if skip_requirements is None:
            skip_requirements = []
        self.graph = g
        self.precolored = precolored
        self.skip_requirements = skip_requirements
        self.variables = {}
        self.model = cp_model.CpModel()
        for vertex in g.nodes:
            self.variables[vertex] = self.model.NewIntVar(0, 1, str(vertex))

    def solve(self):
        for vertex in self.graph.nodes:
            if vertex in self.precolored:
                self.model.Add(self.variables[vertex] == self.precolored[vertex])
                # !! changed !!
                # continue
            if vertex in self.skip_requirements:
                continue
            neighbourhood = [self.variables[n] for n in self.graph.neighbors(vertex)]
            requirement = (len(neighbourhood) + 1) // 2
            constraint_if_0 = _sum(neighbourhood) >= requirement * (1-self.variables[vertex])
            constraint_if_1 = _sum(neighbourhood, negate=True) >= requirement * self.variables[vertex]
            self.model.Add(constraint_if_0)
            self.model.Add(constraint_if_1)


        solver = cp_model.CpSolver()
        collector = SolutionCollector([var for var_name, var in self.variables.items()])
        solver.parameters.enumerate_all_solutions = True
        _ = solver.Solve(self.model, collector)

        return collector.solutions
