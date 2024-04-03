import networkx as nx
import matplotlib.pyplot as plt


def display_graph(graph: nx.Graph, labels: {int: str} = None, vertex_colors: dict[int, bool] = None):
    if labels is None:
        labels = {i: str(i) for i in graph.nodes}
    if vertex_colors is None:
        vertex_colors = {i: 0 for i in graph.nodes}

    pos = nx.spring_layout(graph)

    # Separate nodes into two lists based on their color
    red_nodes = [node for node, color in vertex_colors.items() if color == 0]
    blue_nodes = [node for node, color in vertex_colors.items() if color == 1]
    other_nodes = list(set(graph.nodes) - set(red_nodes) - set(blue_nodes))

    # Draw nodes with specified colors
    nx.draw_networkx_nodes(graph, pos, nodelist=red_nodes, node_color='red', node_size=500)
    nx.draw_networkx_nodes(graph, pos, nodelist=blue_nodes, node_color='lightblue', node_size=500)
    nx.draw_networkx_nodes(graph, pos, nodelist=other_nodes, node_color='lightgreen', node_size=500)

    # Draw edges
    nx.draw_networkx_edges(graph, pos)

    # Draw labels
    nx.draw_networkx_labels(graph, pos, labels=labels)

    plt.title("Graph Visualization")
    plt.show()
    for u, v in graph.edges:
        print(f"({u}, {v}), ", end="")
    print()
