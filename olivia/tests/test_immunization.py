import networkx as nx
import itertools

from olivia.immunization import *
from olivia.model import OliviaNetwork
from olivia.packagemetrics import Impact

path = OliviaNetwork()
path.build_model(nx.path_graph(4, create_using=nx.DiGraph))


def test_immunization_delta():
    assert [immunization_delta(path, n) for n in itertools.combinations(path, 2)] == [(2.5, 1.5, 1.0),
                                                                                      (2.5, 1.0, 1.5),
                                                                                      (2.5, 1.5, 1.0),
                                                                                      (2.5, 1.0, 1.5),
                                                                                      (2.5, 1.0, 1.5),
                                                                                      (2.5, 1.5, 1.0)]
    assert [immunization_delta(path, n, cost_metric=Impact) for n in itertools.combinations(path, 2)] == [
        (1.5, 0.5, 1.0),
        (1.5, 0.0, 1.5),
        (1.5, 0.5, 1.0),
        (1.5, 0.0, 1.5),
        (1.5, 0.0, 1.5),
        (1.5, 0.5, 1.0)]


def test_iset_naive_ranking():
    assert [iset_naive_ranking(path, i) for i in range(1, len(path) + 1)] == [{0}, {0, 1}, {0, 1, 2}, {0, 1, 2, 3}]
    assert [iset_naive_ranking(path, i, metric=Impact) for i in range(1, len(path) + 1)] == [{0}, {0, 1}, {0, 1, 2},
                                                                                             {0, 1, 2, 3}]


def test_iset_delta_frame_reach():
    assert iset_delta_frame_reach(path) == {1, 2}


def test_iset_delta_frame_impact():
    assert iset_delta_frame_impact(path) == {1}


def test_iset_random():
    assert [iset_random(path, i, seed=1234) for i in range(len(path))] == [set(), {3}, {0, 3}, {0, 2, 3}]
    assert [iset_random(path, i, indirect=True, seed=1234) for i in range(len(path))] == [set(), {2}, {1, 2}, {0, 1, 2}]
