
"""Aggregator base classes for computing metrics on Directed Acyclic Graphs."""

from abc import abstractmethod, ABC
import numpy as np
import networkx as nx
from intbitset import intbitset

from olivia.lib.transientsequence import TransientSequence


class AscendentAggregator(ABC):

    """
    Base class for the network-wide computation of ascendent aggregation metrics.

    Ascendent aggregation metrics are values computed for each node as a function of the node and the set of its
    transitive descendants. The aggregation function must be implemented in the subclasses.

    The reversed topological order of the network is used to compute descendant sets in a relatively efficient manner,
    using a modified version of the Goralcikova-Koubek algorithm [1].

    Thus input graph must be acyclic and it is expected to be indexed by reversed topological order.

    [1] Goralčíková, Alla, and Václav Koubek. "A reduct-and-closure algorithm for graphs." International Symposium
    on Mathematical Foundations of Computer Science. Springer, Berlin, Heidelberg, 1979.

    Parameters
    ----------
    G: Networkx DiGraph
        Input acyclic graph indexed in reverse topological order.
    save_memory: bool, optional
         Set to True to free descendant sets that are no longer needed. Depending on the network
         topology this can save 10 to 50% (and possibly more in large sparse networks) RAM required by the proccess.
    compression_threshold: int
         Descendant sets with sizes larger that this value will be dynamically compressed and decompressed in
         memory. Use 0 to compress all descendant sets and np.inf for no compression. Depending on the network this
         may reduce drastically the amount of RAM needed at the expense of speed.
    mapping: dict
        If a mapping is provided, computation returns a dictionary values for each key according to value indexes.
        If not, a raw array indexed by node is returned.

    Notes
    -----
    Stores descendant sets in instances of ~olivia.lib.transientsequence.TransientSequence

    """

    def __init__(self, G, save_memory=False, compression_threshold=1000, mapping=None):
        """
        Create and inits an AscendentAggregator.
    
        Parameters
        ----------
        G: Networkx DiGraph
            Input acyclic graph indexed in reverse topological order.
        save_memory: bool, optional
             Set to True to free descendant sets that are no longer needed. Depending on the network
             topology this can save 10 to 50% (and possibly more in large sparse networks) RAM required by the proccess.
        compression_threshold: int
             Descendant sets with sizes larger that this value will be dynamically compressed and decompressed in 
             memory. Use 0 to compress all descendant sets and np.inf for no compression. Depending on the network this
             may reduce drastically the amount of RAM needed at the expense of speed.
        mapping: dict
            If a mapping is provided, computation returns a dictionary with values for each key
            according to value indexes.
            If not, a raw array indexed by node is returned.

        """
        self._G = G
        self._topological_order = range(len(G))
        self._save_memory = save_memory
        self._compression_threshold = compression_threshold
        self._descendants = None
        self._mapping = mapping
        self._dag_result = None

    def _ascendent_aggregation(self):
        """
        Compute the aggregation function over the network.

        Computes descendant sets in reversed topological order and stores the result of the aggregation
        function in _dag_result

        Returns
        -------
        None

        """
        for n in self._topological_order:
            if not n % 1000:
                print('     Processing node: '+str(n // 1000)+'K      ', end='\r', flush=True)
            tempset = intbitset()
            for m in self._G[n]:
                if m not in tempset:
                    tempset.update(self._descendants[m])
                    tempset.add(m)
            self._descendants[n] = tempset
            self._dag_result[n] = self._aggregation(n, tempset)
        print()

    @abstractmethod
    def _aggregation(self, n, descendants):
        """
        Return the value of the aggregation function.

        Parameters
        ----------
        n: int
            index of the current node
        descendants: iterable
            set of transitive descendants of n

        Returns
        -------
        value: int or object
            Value of the aggregation function for n and its descendants.

        """
        pass

    def _setup(self):
        """
        Init internal structures for computation.

        Returns
        -------
        None

        """

        def intbitset_decompressor(v):
            out = intbitset()
            intbitset.fastload(out, v)
            return out

        self._dag_result = np.zeros(len(self._G), dtype='int32')
        if self._save_memory:
            expiry = [self._G.in_degree()[n] for n in self._G]
        else:
            expiry = None
        self._descendants = TransientSequence(len(self._G),
                                              class_type=intbitset,
                                              compressor=intbitset.fastdump,
                                              decompressor=intbitset_decompressor,
                                              compression_threshold=self._compression_threshold,
                                              expiry_array=expiry)

    def compute(self):
        """
        Compute the ascendent aggregation metric defined by the aggregation function.

        Returns
        -------
        result: numpy.array or dict
            If a mapping is provided, computation returns a dictionary with values for each key
            according to value indexes.
            If not, a raw array indexed by node is returned.

        """
        self._setup()
        self._ascendent_aggregation()
        if self._mapping is None:
            return self._dag_result
        else:
            return {n: self._dag_result[self._mapping[n]] for n in self._mapping}


class DescendentAggregator(AscendentAggregator, ABC):

    """
    Abstract subclass of DescendentAggregator for inverting the computing direction.

    Aggregation process is carried in topological order over the reversed input graph.
    """

    def __init__(self, *args, **kwargs):
        """Create and init an DescendentAggregator."""
        super(DescendentAggregator, self).__init__(*args, **kwargs)
        self._topological_order = reversed(self._topological_order)

    def compute(self):
        """
        Compute the descendent aggregation metric defined by the aggregation function.

        Returns
        -------
        result: numpy.array or dict
            If a mapping is provided, computation returns a dictionary with values for each key
            according to value indexes.
            If not, a raw array indexed by node is returned.

        """
        with nx.utils.contextmanagers.reversed(self._G):
            return super(DescendentAggregator, self).compute()
