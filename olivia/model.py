"""
Olivia Model for studying the vulnerability of package dependency networks.

Olivia stands for 'Open-source Library Indexes Vulnerability Identification and Analysis'.
Includes tools for the analysis of package dependency networks vulnerability to failures and attacks.
"""

import networkx as nx
import gzip
import pickle
import numpy as np

from olivia.coupling import coupling_interface, coupling_profile


class PackageInfoView:
    """
    Helper class for retrieving individual package information and metrics.

    For network-wide analysis use suitable classes and methods from ~networkmetrics, ~packagemetrics or ~coupling
    instead, as individual computation can be orders of magnitude slower.
    """

    def __init__(self, network, name):
        """Create and initialize a PackageInfoView object."""
        self._model = network
        self._name = name

    def transitive_dependencies(self):
        """Return a set containing the transitive dependencies of the package."""
        return nx.ancestors(self._model.network, self._name)

    def transitive_dependants(self):
        """Return a set containing the transitive dependants of the package."""
        return nx.descendants(self._model.network, self._name)

    def direct_dependencies(self):
        """Return a set containing the direct dependencies of the package."""
        return set(self._model.network.predecessors(self._name))

    def direct_dependants(self):
        """Return a set containing the direct dependants of the package."""
        return set(self._model.network.successors(self._name))

    def scc(self):
        """
        Return the strongly connected component(SCC) of the package.

        The SCC of a package is the set of packages in the network that are strongly connected to it in
        the underlying graph -that is to say each of the packages in the scc are transitively dependant on
        each other.-
        """
        dag_id = self._model.dag.graph['mapping'][self._name]
        return self._model.dag.nodes[dag_id]['members']

    def reach(self):
        """Return the value of the Olivia reach metric for the package."""
        return len(nx.descendants(self._model.network, self._name)) + 1

    def surface(self):
        """Return the value of the Olivia surface metric for the package."""
        return len(nx.ancestors(self._model.network, self._name)) + 1

    def impact(self):
        """Return the value of the Olivia impact metric for the package."""
        out_degrees = self._model.network.subgraph({self._name} |
                                                   nx.descendants(self._model.network, self._name)).out_degree()
        return np.array([n[1] for n in out_degrees]).sum()

    def coupling_interface_to(self, n):
        """Return the coupling interface for this package over n."""
        return coupling_interface(self._model, self._name, n)

    def coupling_interface_from(self, n):
        """Return the coupling interface for n over this package."""
        return coupling_interface(self._model, n, self._name)

    def coupling_profile(self):
        """Return the coupling profile for this package."""
        return coupling_profile(self._model, self._name)


class OliviaNetwork:
    """
    Model for studying the vulnerability of package dependency networks.

    Uses a directed acyclic graph to represent the fundamental structure of the network. Also acts as a gateway for
    querying cached metric values for the packages in the network.
    """

    def __init__(self, file=None):
        """
        Create and initializes an OliviaNetwork object.

        Parameters
        ----------
        file: file or string
            File or file name to read an OliviaNetwork model from.

        """
        if file is None:
            self._dag = {}
            self._metrics_cache = dict()  # In-model metrics cache
            self._network = {}
        else:
            self.load(file)

    def load(self, file):
        """
        Load an OliviaNetwork model from file.

        Parameters
        ----------
        file: file or string
            File or file name to read an OliviaNetwork model from.

        Returns
        -------
        None

        """
        with gzip.GzipFile(file, 'rb') as f:
            load_dict = pickle.load(f)

        self._network = nx.from_dict_of_lists(load_dict['network'], create_using=nx.DiGraph())
        self._dag = load_dict['dag']
        self._metrics_cache = load_dict['cache']

    def save(self, file):
        """
        Save an OliviaNetwork model to file.

        Parameters
        ----------
        file: file or string
            File or file name to write an OliviaNetwork model to.

        Returns
        -------
        None

        """
        save_dict = {'network': nx.to_dict_of_lists(self._network),
                     'dag': self._dag,
                     'cache': self._metrics_cache}

        with gzip.GzipFile(file, 'wb') as f:
            pickle.dump(save_dict, f, protocol=pickle.HIGHEST_PROTOCOL)

    @property
    def network(self):
        """Return the package network."""
        return self._network

    @property
    def dag(self):
        """Return the model's underlying DAG graph."""
        return self._dag

    def get_metric(self, metric_class, **kwargs):
        """
        Compute or get form the internal cache metric values for the packages in the network.

        If metric values are not available, the are computed instantiating metric_class and calling compute(),and
        are subsequently stored for future use.

        Parameters
        ----------
        metric_class: class
            Class implementing compute()
        kwargs: keyword args
            Arguments for the metric class constructor.

        Returns
        -------
        ms: object
            An object containing the computed metric values. For Olivia metrics this is always a MetricStats instance.

        """
        if metric_class.__name__ in self._metrics_cache:
            print(f'{metric_class.__name__} retrieved from metrics cache')
        else:
            self._metrics_cache[metric_class.__name__] = metric_class(self, **kwargs).compute()
        return self._metrics_cache[metric_class.__name__]

    def sccs(self):
        """
        Return a generator of strongly connected components (SCCs) present in the network.

        SCCs are sets of packages in which all the packages are transitively
        dependent on each other, so SCCs of more than one package imply the existence of cycles in the network.
        This method generates the partition into strongly connected components of the directed graph
        underlying the package network.
        """
        for p in self.dag:
            yield self.dag.nodes[p]['members']

    def sorted_clusters(self):
        """Return a list of clusters in reverse size order."""
        return sorted(self.sccs(), key=lambda x: len(x), reverse=True)

    def __getitem__(self, package):
        """Return a ~DegreeInfoView of the package."""
        return PackageInfoView(self, package)

    def __len__(self):
        """Return the number of packages in the network."""
        return len(self.network)

    def __iter__(self):
        """Return an iterator over the packages in the network."""
        return iter(self.network)

    def build_model(self, source):
        """
        Build the model from specified source.

        Parameters
        ----------
        source: File or file name or Networkx DiGraph
            Source to build the model from. Files should be in adjacency list format.
            Filenames ending in .gz or .bz2 will be uncompressed.

        Returns
        -------
        None

        """
        if isinstance(source, nx.DiGraph):
            self._network = source
        else:
            print("Reading dependencies file...")
            self._network = nx.read_adjlist(source, create_using=nx.DiGraph())
        print("Building Olivia Model")
        print('     Finding strongly connected components (SCCs)...')
        scc = nx.strongly_connected_components(self._network)
        print('     Building condensation network...')
        GC = nx.condensation(self._network, list(scc))
        print('     Adding structural meta-data...')

        # Model includes weighted edges to represent
        # ingoing/outgoing dependencies to/from SCC
        for e in GC.edges:
            GC.edges[e]['weight'] = 0
        for n in GC.nodes:
            GC.nodes[n]['intra_edges'] = 0

        for n in self._network:
            for e in self._network.in_edges(n):
                u, v = e
                map_u = GC.graph['mapping'][u]
                map_v = GC.graph['mapping'][v]
                if map_u == map_v:
                    # Number of edges inside SCC
                    GC.nodes[map_u]['intra_edges'] += 1
                else:
                    # Weight for edge to/from SCC
                    GC.edges[(map_u, map_v)]['weight'] += 1
        self._dag = GC
        print("     Done")
