import networkx as nx
from all_colorings_encoder import Encoder
from graph_display import display_graph


def graph_iterator():
    for g in nx.graph_atlas_g():
        if len(g.nodes) < 6 or not nx.is_connected(g):
            continue
        yield g


def split_groups(groups, coloring, lower_size_limit=0):
    result = []
    for group in groups:
        group_0 = [elem for elem in group if coloring[elem] == 0]
        group_1 = [elem for elem in group if coloring[elem] == 1]
        if len(group_0) > lower_size_limit:
            result.append(group_0)
        if len(group_1) > lower_size_limit:
            result.append(group_1)
    return result


def find_equivalence_classes(n, colorings):
    groups = [[i for i in range(n)]]
    for coloring in colorings:
        groups = split_groups(groups, coloring)
    return groups


def find_leniency(g, colorings):
    result = {i: len(g.nodes) for i in g.nodes}
    for coloring in colorings:
        for v in g.nodes:
            colored_the_same = len([n for n in g.neighbors(v) if coloring[n] == coloring[v]])
            colored_differently = g.degree(v) - colored_the_same
            result[v] = min(result[v], colored_differently-colored_the_same)
    return result


def find_classes_with_leniency(g, colorings):
    classes = find_equivalence_classes(len(g.nodes), all_solutions)
    leniency = find_leniency(g, colorings)
    result = [{v: leniency[v] for v in cls} for cls in classes]
    return result


def filter_interesting_classes(clss_with_l, min_size, num_of_lenient, required_leniency):
    result = []
    for cls in clss_with_l:
        if len(cls) < min_size:
            continue
        num = 0
        for v, l in cls.items():
            if l >= required_leniency:
                num += 1
        if num >= num_of_lenient:
            result.append(cls)
    return result


def find_always_equal(g, colorings):
    groups = []
    for coloring in colorings:
        groups = split_groups(groups, coloring)
    return groups



if __name__ == "__main__":
    for g in graph_iterator():
        # 0 is the vertex that others will try to copy
        encoder = Encoder(g, skip_requirements=[0])
        all_solutions = encoder.solve()

        classes_with_leniency = find_classes_with_leniency(g, all_solutions)
        interesting = filter_interesting_classes(classes_with_leniency, 3, 2, 2)
        if len(interesting) == 0:
            continue
        print(interesting)
        for sol in all_solutions:
            display_graph(g, {i: str(i) for i in g.nodes}, sol)






