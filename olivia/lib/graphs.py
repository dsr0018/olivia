
"""Graph utils and algorithms."""

from contextlib import contextmanager


@contextmanager
def removed(g, n):
    """
    Temporarily removes nodes in-place from a directed graph.

    Parameters
    ----------
    g: DiGraph
        Input networkx graph.
    n: container
        Container of nodes to be immunized

    Returns
    -------
    None

    """
    in_rem = list(g.in_edges(n))  # list conversion forces copy
    out_rem = list(g.out_edges(n))
    g.remove_nodes_from(n)
    try:
        yield
    finally:
        g.add_edges_from(in_rem)
        g.add_edges_from(out_rem)
