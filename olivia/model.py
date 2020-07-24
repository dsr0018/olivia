import networkx as nx


class OliviaNetwork:
    """
    Model for studying the vulnerability of package dependency networks. Uses a directed acyclic graph to represent
    the fundamental structure of the network.

    Olivia stands for 'Open-source Library Indexes Vulnerability Identification and Analysis'.
    Includes tools for the analysis of package dependency networks vulnerability to failures and attacks.
    """

    def __init__(self, file=None):
        """ Creates and initializes an OliviaNetwork object.
        Parameters
        ----------
        file: file or string
            File or file name to read an OliviaNetwork model from.
        """
        if file is None:
            self._network = None
        else:
            self.load(file)

    def load(self, file):
        """ Loads an OliviaNetwork model from file
        Parameters
        ----------
        file: file or string
            File or file name to read an OliviaNetwork model from.
            Filenames ending in .gz or .bz2 will be uncompressed.

        Returns
        -------
        None
        """
        self._network = nx.read_gpickle(file)

    def save(self, file):
        """ Saves an OliviaNetwork model to file
        Parameters
        ----------
        file: file or string
            File or file name to write an OliviaNetwork model to.
            Filenames ending in .gz or .bz2 will be compressed.

        Returns
        -------
        None
        """
        nx.write_gpickle(self._network, file)

    @property
    def network(self):
        """

        Returns
        -------
            network: The model's underlying DAG graph
        """
        return self._network

    def build_model(self, source):
        """ Builds the model from specified source.

        Parameters
        ----------
        source: File or file name or Networkx DiGraph
            Source to build the model from. Files should be in adjacency list format.
            Filenames ending in .gz or .bz2 will be uncompressed.
            If a DiGraph is provided, node and edge data will be lost, as it is not included into the model.

        Returns
        -------
        None
        """
        if isinstance(source, nx.DiGraph):
            G = source
        else:
            G = nx.read_adjlist(source, create_using=nx.DiGraph())
        print('Finding strongly connected components (SCCs)...')
        scc = nx.strongly_connected_components(G)
        print('Building condensation network...')
        GC = nx.condensation(G, list(scc))
        print('Adding structural meta-data...')

        # Model includes weighted edges to represent
        # ingoing/outgoing dependencies to/from SCC
        for e in GC.edges:
            GC.edges[e]['weight'] = 0
        for n in GC.nodes:
            GC.nodes[n]['intra_edges'] = 0

        for n in G:
            for e in G.in_edges(n):
                u, v = e
                map_u = GC.graph['mapping'][u]
                map_v = GC.graph['mapping'][v]
                if map_u == map_v:
                    # Number of edges inside SCC
                    GC.nodes[map_u]['intra_edges'] += 1
                else:
                    # Weight for edge to/from SCC
                    GC.edges[(map_u, map_v)]['weight'] += 1
        self._network = GC
        print("Done")
