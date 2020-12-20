import networkx as nx
import numpy as np

from olivia.model import OliviaNetwork
from olivia.packagemetrics import Reach, Surface, Impact, MetricStats, DependenciesCount, DependentsCount

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


def test_reach():
    m = Reach(net).compute()
    assert m.results_dict == {'a': 12,
                              'b': 10,
                              'c': 10,
                              'd': 10,
                              'e': 10,
                              'f': 6,
                              'g': 3,
                              'h': 4,
                              'i': 4,
                              'j': 2,
                              'k': 2,
                              'l': 1}, 'Result does not match'


def test_surface():
    m = Surface(net).compute()
    assert m.results_dict == {'a': 1,
                              'b': 5,
                              'c': 5,
                              'd': 5,
                              'e': 5,
                              'f': 6,
                              'g': 7,
                              'h': 8,
                              'i': 8,
                              'j': 11,
                              'k': 11,
                              'l': 2}, 'Result does not match'


def test_impact():
    m = Impact(net).compute()
    assert m.results_dict == {'a': 17,
                              'b': 15,
                              'c': 15,
                              'd': 15,
                              'e': 15,
                              'f': 10,
                              'g': 3,
                              'h': 6,
                              'i': 6,
                              'j': 2,
                              'k': 2,
                              'l': 0}, 'Result does not match'


def test_dependenciescount():
    m = DependenciesCount(net).compute()
    assert m.results_dict == {'a': 0,
                              'b': 2,
                              'c': 1,
                              'd': 1,
                              'e': 1,
                              'f': 1,
                              'g': 1,
                              'j': 3,
                              'i': 2,
                              'h': 2,
                              'k': 2,
                              'l': 1}, 'Result does not match'


def test_dependentscount():
    m = DependentsCount(net).compute()
    assert m.results_dict == {'a': 2,
                              'b': 1,
                              'c': 1,
                              'd': 2,
                              'e': 1,
                              'f': 3,
                              'g': 1,
                              'j': 1,
                              'i': 2,
                              'h': 2,
                              'k': 1,
                              'l': 0}, 'Result does not match'


def test_metric_stats():
    ms = MetricStats({'a': 2, 'b': 4, 'c': 6}, normalize_factor=2)

    assert ms.top() == [('c', 6)]
    assert ms.top(2) == [('c', 6), ('b', 4)]
    assert ms.top(2, subset={'a', 'b'}) == [('b', 4), ('a', 2)]
    assert ms.bottom() == [('a', 2)]
    assert ms.bottom(2) == [('b', 4), ('a', 2)]
    assert ms.bottom(2, subset={'a', 'c'}) == [('a', 2), ('c', 6)]
    ms.normalize()
    assert np.array_equal(ms.values, np.array([1, 2, 3]))
    ms.normalize()
    assert np.array_equal(ms.values, np.array([1, 2, 3]))

def test_metric_ops():
    ms1 = MetricStats({'a': 2, 'b': 4, 'c': 6})
    ms2 = MetricStats({'a': 1, 'b': 2, 'c': 3})

    assert (ms1 * 2 - ms2 - 1).results_dict == {'a': 2, 'b': 5, 'c': 8}
    assert (ms1 ** 2 / ms2).results_dict == {'a': 4, 'b': 8, 'c': 12}
    assert ((ms1 + ms2) ** 2).results_dict == {'a': 9, 'b': 36, 'c': 81}
    assert (ms1 ** ms2 + 1).results_dict == {'a': 3, 'b': 17, 'c': 217}
    assert (ms2 / 2).results_dict == {'a': 0.5, 'b': 1, 'c': 1.5}
