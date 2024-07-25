from ortools.linear_solver import pywraplp
import networkx as nx


def _sum(elements, negate=False):
    result = 0
    for elem in elements:
        result = result + ((1 - elem) if negate else elem)
    return result


def find_min_ones_coloring(graph: nx.DiGraph):
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


