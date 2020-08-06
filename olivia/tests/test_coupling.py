import networkx as nx

from olivia.coupling import coupling_interface, transitive_coupling, coupling_profile
from olivia.model import OliviaNetwork

H = nx.DiGraph()
H.add_edges_from([(0, 1),
                  (1, 2),
                  (1, 3),
                  (1, 4),
                  (1, 5),
                  (4, 6),
                  (5, 6),
                  (1, 6)
                  ])
net = OliviaNetwork()
net.build_model(H)


def test_coupling_interface():
    assert coupling_interface(net, 0, 6) == {1, 4, 5}
    assert coupling_interface(net, 1, 6) == {1, 4, 5}
    assert len(coupling_interface(net, 2, 6)) == 0
    assert len(coupling_interface(net, 3, 6)) == 0
    assert coupling_interface(net, 4, 6) == {4}


def test_transitive_coupling():
    assert transitive_coupling(net, 0, 6) == 3
    assert transitive_coupling(net, 1, 6) == 3
    assert transitive_coupling(net, 2, 6) == 0
    assert len(coupling_interface(net, 3, 6)) == 0
    assert transitive_coupling(net, 4, 6) == 1


def test_coupling_profile():
    assert coupling_profile(net, 6) == {0: {1, 4, 5}, 1: {1, 4, 5}, 4: {4}, 5: {5}}
    assert coupling_profile(net, 3) == {0: {1}, 1: {1}}
    assert coupling_profile(net, 4) == {0: {1}, 1: {1}}
    assert coupling_profile(net, 5) == {0: {1}, 1: {1}}
    assert len(coupling_profile(net, 0)) == 0
