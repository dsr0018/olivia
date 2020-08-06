
"""
Olivia coupling functions.

Coupling characterizes the local structure of the transitive dependency relation between packages.
"""

import networkx as nx


def coupling_interface(olivia_model, n, m):
    """
    Compute the coupling interface of one package over another.

    The coupling interface of a network package n over another package  m is the set of direct dependencies of m
    potentially compromised by a defect in n.

    Parameters
    ----------
    olivia_model: OliviaNetwork
        Input network.
    n: package
        Source package.
    m: package
        Target package.

    Returns
    -------
    coup: set
        Coupling interface of n over m.

    Notes
    -----
    For computing the coupling interface of all transitive dependencies over a package use ~coupling_profile() instead
    as it is much faster.

    """
    return set(olivia_model.network.predecessors(m)) & (nx.descendants(olivia_model.network, n) | {n})


def transitive_coupling(olivia_model, n, m):
    """
    Compute the transitive coupling of one package over another.

    The transitive coupling is the size of the transitive interface of n over m.

    Parameters
    ----------
    olivia_model: OliviaNetwork
        Input network.
    n: package
        Source package.
    m: package
        Target package.

    Returns
    -------
    tcoup: int
        Transitive coupling of n over m.

    """
    return len(coupling_interface(olivia_model, n, m))


def coupling_profile(olivia_model, m):
    """
    Compute the coupling profile of a package.

    The coupling profile is the set of all the coupling interfaces of transitive dependencies of m over m.

    Parameters
    ----------
    olivia_model: OliviaNetwork
        Input network.
    m: package
        Target package.

    Returns
    -------
    profile: dict
        Dictionary with transitive dependencies of m as keys and their transitive interface over n as values.

    """
    # Surface (transitive predecessors) of each direct dependency of m
    surface = {p: nx.ancestors(olivia_model.network, p) | {p} for p in olivia_model.network.predecessors(m)}
    # For each ancestor check if it is in the surface of each direct dependency of m
    # and add it to the coupling interface.
    return {a: {p for p in olivia_model.network.predecessors(m) if a in surface[p]}
            for a in nx.ancestors(olivia_model.network, m)}
