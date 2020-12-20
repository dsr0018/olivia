import networkx as nx
import itertools
import pytest

from olivia.immunization import *
from olivia.model import OliviaNetwork
from olivia.packagemetrics import Impact

path = OliviaNetwork()
path.build_model(nx.path_graph(4, create_using=nx.DiGraph))

G = nx.DiGraph()
G.add_edges_from((['a', 'b'],
                  ['b', 'c'],
                  ['c', 'd'],
                  ['d', 'e'],
                  ['e', 'b'],
                  ['d', 'f'],
                  ['f', 'g'],
                  ['g', 'j'],
                  ['f', 'i'],
                  ['f', 'h'],
                  ['i', 'h'],
                  ['h', 'i'],
                  ['i', 'j'],
                  ['h', 'k'],
                  ['j', 'k'],
                  ['k', 'j'],
                  ['a', 'l']))

net = OliviaNetwork()
net.build_model(G)


def test_immunization_delta():
    assert [immunization_delta(path, n) for n in itertools.combinations(path, 2)] == [1.75, 2.0, 1.75, 2.0, 2.0, 1.75]
    assert [immunization_delta(path, n, cost_metric=Impact) for n in itertools.combinations(path, 2)] == [1.25, 1.5,
                                                                                                          1.25, 1.5,
                                                                                                          1.5, 1.25]
    assert [immunization_delta(path, n, algorithm='analytic') for n in itertools.combinations(path, 2)] == [1.75, 2.0,
                                                                                                            1.75, 2.0,
                                                                                                            2.0, 1.75]

    assert immunization_delta(path, {}) == 0.0
    assert immunization_delta(path, {}, algorithm='analytic') == 0.0

    with pytest.raises(ValueError):
        _ = immunization_delta(path, [1], cost_metric=Impact, algorithm='analytic')

    assert immunization_delta(net, {'b'}) == pytest.approx(2.66666666666)
    assert immunization_delta(net, {'b'}, algorithm='analytic') == pytest.approx(2.66666666666)

    assert immunization_delta(net, {'b', 'f'}) == pytest.approx(4.16666666666)
    assert immunization_delta(net, {'b', 'f'}, algorithm='analytic') == pytest.approx(4.16666666666)

    assert immunization_delta(net, {'b', 'f', 'k', 'i', 'a'}) == 5.25
    assert immunization_delta(net, {'b', 'f', 'k', 'i', 'a'}, algorithm='analytic') == 5.25


def test_iset_naive_ranking():
    assert [iset_naive_ranking(i, path.get_metric(Reach)) for i in range(1, len(path) + 1)] == [{0}, {0, 1},
                                                                                                {0, 1, 2},
                                                                                                {0, 1, 2, 3}]
    assert [iset_naive_ranking(i, path.get_metric(Impact)) for i in range(1, len(path) + 1)] == [{0}, {0, 1},
                                                                                                 {0, 1, 2},
                                                                                                 {0, 1, 2, 3}]


def test_iset_delta_frame_reach():
    assert iset_delta_set_reach(path) == {1, 2}


def test_iset_delta_frame_impact():
    assert iset_delta_set_impact(path) == {1}


def test_iset_random():
    assert [iset_random(path, i, seed=1234) for i in range(len(path))] == [set(), {3}, {0, 3}, {0, 2, 3}]
    assert [iset_random(path, i, indirect=True, seed=1234) for i in range(len(path))] == [set(), {2}, {1, 2}, {0, 1, 2}]


def test_iset_sap():
    G = nx.complete_graph(5, create_using=nx.DiGraph())
    net = OliviaNetwork()
    net.build_model(G)
    assert len(iset_sap(net)) == 0

    S = nx.cycle_graph(5, create_using=nx.DiGraph())
    net = OliviaNetwork()
    net.build_model(S)
    assert iset_sap(net) == {0, 1, 2, 3, 4}

    T = nx.disjoint_union(nx.complete_graph(5, create_using=nx.DiGraph()),
                          nx.complete_graph(5, create_using=nx.DiGraph()))
    T.add_edges_from([[0, 10], [10, 7], [10, 0], [7, 10]])
    net = OliviaNetwork()
    net.build_model(T)
    assert iset_sap(net) == {0, 7, 10}

    M = nx.disjoint_union(T, S)
    net = OliviaNetwork()
    net.build_model(M)
    assert iset_sap(net) == {0, 7, 10}
    assert iset_sap(net, clusters=net.sorted_clusters()) == {0, 7, 10, 11, 12, 13, 14, 15}
