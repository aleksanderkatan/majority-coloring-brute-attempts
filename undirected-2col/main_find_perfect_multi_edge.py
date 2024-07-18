import networkx as nx
from all_colorings_encoder import Encoder
from graphs.graph_display import display_graph
from graphs.new_graph_iterator import graph_iterator


# def check_all_connections(g: nx.Graph):
#     interface = len(g.nodes)
#     free, chain = interface+1, interface+2
#     for interface_neighbor in g.nodes:
#         for free_neighbor in g.nodes:
#             for chain_neighbor_1 in g.nodes:
#                 for chain_neighbor_2 in g.nodes:
#                     if chain_neighbor_1 == chain_neighbor_2:
#                         continue
#                     new_g = g.copy()
#                     new_g.add_edge(interface, interface_neighbor)
#                     new_g.add_edge(free, free_neighbor)
#                     new_g.add_edge(chain, chain_neighbor_1)
#                     new_g.add_edge(chain, chain_neighbor_2)
#                     encoder = Encoder(new_g, skip_requirements=[interface, free, chain])
#                     all_solutions = encoder.solve()
#                     valid = True
#                     for solution in all_solutions:
#                         if solution[interface] != solution[free_neighbor] or solution[interface] != solution[chain_neighbor_1] or solution[interface] != solution[chain_neighbor_2]:
#                             valid = False
#                             break
#                     if valid:
#                         return interface, free, chain, new_g
#     return None

# checked up to and including 7
# def check_all_connections(g: nx.Graph):
#     e1 = len(g.nodes)
#     e2 = e1+1
#     for e1n1 in g.nodes:
#         for e1n2 in g.nodes:
#             for e2n1 in g.nodes:
#                 for e2n2 in g.nodes:
#                     if e1n1 == e1n2:
#                         continue
#                     if e2n1 == e2n2:
#                         continue
#                     new_g = g.copy()
#                     new_g.add_edge(e1, e1n1)
#                     new_g.add_edge(e1, e1n2)
#                     new_g.add_edge(e2, e2n1)
#                     new_g.add_edge(e2, e2n2)
#                     encoder = Encoder(new_g, skip_requirements=[e1, e2])
#                     all_solutions = encoder.solve()
#                     valid = True
#                     for solution in all_solutions:
#                         if solution[e1] != solution[e2n1] or solution[e1] != solution[e2n2]\
#                                 or solution[e2] != solution[e1n1] or solution[e2] != solution[e1n2]:
#                             valid = False
#                             break
#                     if valid:
#                         return (e1, e1n1, e1n2), (e2, e2n1, e2n2), new_g
#     return None


# def check_all_connections(g: nx.Graph):
#     e1 = len(g.nodes)
#     e2 = e1+1
#     for e1n in g.nodes:
#         for e2n in g.nodes:
#             new_g = g.copy()
#             new_g.add_edge(e1, e1n)
#             new_g.add_edge(e2, e2n)
#             new_g.add_edge(e1, e2)
#             encoder = Encoder(new_g, skip_requirements=[e1, e2])
#             all_solutions = encoder.solve()
#             valid = True
#             for solution in all_solutions:
#                 if solution[e1] != solution[e2n] or solution[e2] != solution[e1n]:
#                     valid = False
#                     break
#             if valid:
#                 return (e1, e1n), (e2, e2n), new_g
#     return None


def check_all_connections(g: nx.Graph):
    for u in g.nodes:
        for v in g.nodes:
            if g.has_edge(u, v):
                continue
            encoder = Encoder(g, skip_requirements=[u], precolored={u: 0, v: 0}, all_solutions=False)
            solutions = encoder.solve()
            if len(solutions) == 0:
                return u, v
    return None


if __name__ == "__main__":
    for g in graph_iterator(10):
        result = check_all_connections(g)
        if result is not None:
            print(result)
            display_graph(g)
