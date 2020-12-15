
"""Graph utils and algorithms."""

from contextlib import contextmanager
from networkx.utils.contextmanagers import reversed
import networkx as nx
import random


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
        g.add_nodes_from(n)
        g.add_edges_from(in_rem)
        g.add_edges_from(out_rem)


def is_sap(scc, n):
    """
    Determine if a node is a strong articulation point (cut vertex) of a given strongly connected graph.

    A strong articulation point is a node whose removal would create additional strongly connected components
    in a strongly connected graph.

    Parameters
    ----------
    scc: Networkx DiGraph.
        Input strongly connected graph.
    n: node
        Node pertaining to the graph.

    Returns
    -------
    is_sap: bool
        True if n is a strong cut vertex (articulation point) of the graph and False otherwise.

    """
    scc2 = scc.copy()
    scc2.remove_node(n)
    if len(list(nx.strongly_connected_components(scc2))) > 1:
        return True
    else:
        return False


def strong_articulation_points(scc):
    """
    Compute the set of strong articulation points (cut vertexes) of a given strongly connected graph.

    A strong articulation point is a node whose removal would create additional strongly connected components
    in a strongly connected graph.

    Implements the algorithm based in flow network dominators published in [1]

    [1] Firmani, Donatella, et al. "Strong articulation points and strong bridges in large scale graphs."
    Algorithmica 74.3 (2016): 1123-1147.

    Parameters
    ----------
    scc: NetworkX DiGraph.
        Input strongly connected graph.

    Returns
    -------
    sap: set
        Set of the strong articulation points of the graph.

    """
    sap = set()
    start = random.choice(list(scc.nodes))
    idom = nx.immediate_dominators(scc, start)
    with reversed(scc):
        idom_r = nx.immediate_dominators(scc, start)
    sap.update(idom.values())
    sap.update(idom_r.values())
    if not is_sap(scc, start):
        sap.remove(start)
    return sap

