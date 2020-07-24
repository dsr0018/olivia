from olivia.model import OliviaNetwork
import networkx as nx


def aux_get_intraedges(net):
    return [net.network.nodes[n]['intra_edges'] for n in net.network]


def aux_get_weights(net):
    return [net.network.edges[e]['weight'] for e in net.network.edges]


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


def test_simple_network():
    net = OliviaNetwork()
    net.build_model(nx.path_graph(4, create_using=nx.DiGraph))
    assert set(net.network.edges) == {(1, 0), (2, 1), (3, 2)}, 'Edge set does not match'
    assert net.network.graph['mapping'] == {3: 0, 2: 1, 1: 2, 0: 3}, 'Wrong mapping'
    assert aux_get_weights(net) == [1, 1, 1], 'Non unitary weights'
    assert aux_get_intraedges(net) == [0, 0, 0, 0], 'Non null intra-edge counts'


def test_scc_network():
    assert set(net.network.edges) == {(1, 0),
                                      (2, 0),
                                      (3, 1),
                                      (3, 2),
                                      (4, 3),
                                      (6, 4),
                                      (6, 5)}, 'Edge set does not match'
    assert net.network.graph['mapping'] == {'k': 0,
                                            'j': 0,
                                            'g': 1,
                                            'h': 2,
                                            'i': 2,
                                            'f': 3,
                                            'e': 4,
                                            'c': 4,
                                            'b': 4,
                                            'd': 4,
                                            'l': 5,
                                            'a': 6}, 'Wrong mapping'
    assert aux_get_weights(net) == [1, 2, 1, 2, 1, 1, 1], 'Weights do not match'
    assert aux_get_intraedges(net) == [2, 0, 2, 0, 4, 0, 0], 'Intra-edge counts do  not match'


def test_io():
    net.save('test.bz2')
    net2 = OliviaNetwork('test.bz2')
    assert net.network.edges == net2.network.edges, 'Edge set does not match'
    assert net.network.graph['mapping'] == net2.network.graph['mapping'], 'Wrong mapping'
    assert aux_get_weights(net) == aux_get_weights(net2), 'Weights do not match'
    assert aux_get_intraedges(net) == aux_get_intraedges(net2), 'Intra-edge counts do  not match'