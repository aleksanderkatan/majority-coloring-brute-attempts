import networkx as nx
from ortools.linear_solver import pywraplp


def _sum(elements: list[int], negate=False):
    result = 0
    for elem in elements:
        result = result + ((1 - elem) if negate else elem)
    return result


class Encoder:
    def __init__(self, g: nx.Graph, constraints: dict[int, bool], skip_requirements=None):
        if skip_requirements is None:
            skip_requirements = []
        self.graph = g
        self.constraints = constraints
        self.skip_requirements = skip_requirements
        self.variables = {}
        self.solver = pywraplp.Solver.CreateSolver("SAT")
        for vertex in g.nodes:
            self.variables[vertex] = self.solver.IntVar(0.0, 1.0, "")

    def solve(self):
        for vertex in self.graph.nodes:
            if vertex in self.skip_requirements:
                continue
            neighbourhood = [self.variables[n] for n in self.graph.neighbors(vertex)]
            requirement = (len(neighbourhood) + 1) // 2
            constraint_if_0 = _sum(neighbourhood) >= requirement * (1-self.variables[vertex])
            constraint_if_1 = _sum(neighbourhood, negate=True) >= requirement * self.variables[vertex]
            self.solver.Add(constraint_if_0)
            self.solver.Add(constraint_if_1)
        for vertex, value in self.constraints.items():
            v = self.variables[vertex]
            if value:
                self.solver.Add(v >= 1)
            else:
                self.solver.Add(v <= 0)


        self.solver.Minimize(1)
        status = self.solver.Solve()
        if status == pywraplp.Solver.OPTIMAL:
            result = {}
            for vertex in self.graph.nodes:
                result[vertex] = self.variables[vertex].solution_value()
            return result
        else:
            return None
