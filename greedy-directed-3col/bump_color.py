from graphs.digraph_with_coloring import DigraphWithColoring


def bump_color(graph: DigraphWithColoring, v):
    color = graph.get_color(v)
    graph.set_color(v, (color+1)%3)
