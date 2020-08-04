import networkx as nx
import pytest

from olivia.model import OliviaNetwork
from olivia.networkmetrics import failure_vulnerability, attack_vulnerability
from olivia.packagemetrics import Impact

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


def test_failure_vulnerability():
    assert pytest.approx(failure_vulnerability(net), 37 / 6)
    assert pytest.approx(failure_vulnerability(net, normalize=True), 37 / (6 * 12))
    assert pytest.approx(failure_vulnerability(net, metric=Impact), 53 / 6)
    assert pytest.approx(failure_vulnerability(net, metric=Impact, normalize=True), 53 / (6 * 17))


def test_attack_vulnerability():
    assert attack_vulnerability(net) == 12
    assert attack_vulnerability(net, normalize=True) == 12 / 12
    assert attack_vulnerability(net, metric=Impact) == 17
    assert attack_vulnerability(net, metric=Impact, normalize=True) == 17 / 17
