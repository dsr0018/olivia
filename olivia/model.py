import networkx as nx
import gzip
import pickle


class OliviaNetwork:
    """
    Model for studying the vulnerability of package dependency networks. Uses a directed acyclic graph to represent
    the fundamental structure of the network.

    Olivia stands for 'Open-source Library Indexes Vulnerability Identification and Analysis'.
    Includes tools for the analysis of package dependency networks vulnerability to failures and attacks.
    """

    def __init__(self, file=None):
        """
        Creates and initializes an OliviaNetwork object.

        Parameters
        ----------
        file: file or string
            File or file name to read an OliviaNetwork model from.
        """
        if file is None:
            self._dag = None
            self._metrics_cache = dict()  # In-model metrics cache
            self._network = None
        else:
            self.load(file)

    def load(self, file):
        """
        Loads an OliviaNetwork model from file

        Parameters
        ----------
        file: file or string
            File or file name to read an OliviaNetwork model from.
            Filenames ending in .gz or .bz2 will be uncompressed.

        Returns
        -------
        None
        """
        with gzip.GzipFile(file, 'rb') as f:
            load_dict = pickle.load(f)

        self._network = nx.from_dict_of_lists(load_dict['network'])
        self._dag = load_dict['dag']
        self._metrics_cache = load_dict['cache']

    def save(self, file):
        """
        Saves an OliviaNetwork model to file

        Parameters
        ----------
        file: file or string
            File or file name to write an OliviaNetwork model to.
            Filenames ending in .gz or .bz2 will be compressed.

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
        """ Returns the package network"""
        return self._network

    @property
    def dag(self):
        """ Returns the model's underlying DAG graph"""
        return self._dag

    def get_metric(self, func):
        if func.__name__ in self._metrics_cache:
            print(f'{func.__name__} retrieved from metrics cache')
        else:
            self._metrics_cache[func.__name__] = func(self).compute()
        return self._metrics_cache[func.__name__]

    def build_model(self, source):
        """
        Builds the model from specified source.

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
