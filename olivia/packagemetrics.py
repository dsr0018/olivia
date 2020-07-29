from olivia.lib.aggregators import AscendentAggregator, DescendentAggregator
import numpy as np


class Reach(AscendentAggregator):
    """
    Olivia Reach Metric.

    REACH(n) is the number of transitive descendants for a package 'n', i.e. the number of
    potentially affected packages by a defect in 'n'.
    """

    def __init__(self, olivia_model, **kwargs):
        """
        Creates a Reach metric object

        Parameters
        ----------
        olivia_model: OliviaModel
            Input network.
        kwargs: **kwargs
            Parameters for ~olivia.lib.aggregators.AscendentAggregator.
            Use 'compression_threshold' and 'save_memory' to adjust computation to available RAM.
        """
        super().__init__(olivia_model.network,
                         mapping=olivia_model.network.graph['mapping'],
                         **kwargs)
        self._scc_sizes = np.array([len(olivia_model.network.nodes[x]['members']) for x in olivia_model.network])

    def _aggregation(self, n, descendants):
        return self._scc_sizes[descendants].sum() + self._scc_sizes[n]

    def compute(self):
        """ Computes the Reach metric for each package in the network.

        Returns
        -------
            ms: A ~MetricStats object with the results of the computation.
        """
        return MetricStats(super().compute(), normalize_factor=self._scc_sizes.sum())


class Impact(AscendentAggregator):
    """
    Olivia Impact Metric.

    IMPACT(n) is the number of dependencies induced by a package 'n', or the size of the edge set
    of the subgraph induced by transitive descendants of n. It is the amount of dependencies that would be potentially
    compromised in the network by a defect in 'n'.
    """
    def __init__(self, olivia_model, **kwargs):
        """
        Creates an Impact metric object

        Parameters
        ----------
        olivia_model: OliviaModel
            Input network.
        kwargs: **kwargs
            Parameters for ~olivia.lib.aggregators.AscendentAggregator.
            Use 'compression_threshold' and 'save_memory' to adjust computation to available RAM.
        """
        super().__init__(olivia_model.network,
                         mapping=olivia_model.network.graph['mapping'],
                         **kwargs)
        odegree = olivia_model.network.out_degree(weight='weight')
        intra_edges = np.array([olivia_model.network.nodes[n]['intra_edges'] for n in olivia_model.network])
        self._out = np.array([odegree[n] for n in olivia_model.network]) + intra_edges

    def _aggregation(self, n, descendants):
        return self._out[descendants].sum() + self._out[n]

    def compute(self):
        """
        Computes the Impact metric for each package in the network.

        Returns
        -------
            ms: A ~MetricStats object with the results of the computation.
        """
        return MetricStats(super().compute(), normalize_factor=self._out.sum())


class Surface(DescendentAggregator):
    """
    Olivia Surface Metric.

    SURFACE(n) is the number of transitive ascendants of a package 'n', i.e the number
    or the number of packets in which a defect would potentially cause the compromise of 'n'.
    """
    def __init__(self, olivia_model, **kwargs):
        """
        Creates an Impact metric object

        Parameters
        ----------
        olivia_model: OliviaModel
            Input network.
        kwargs: **kwargs
            Parameters for ~olivia.lib.aggregators.AscendentAggregator.
            Use 'compression_threshold' and 'save_memory' to adjust computation to available RAM.
        """
        super().__init__(olivia_model.network,
                         mapping=olivia_model.network.graph['mapping'],
                         **kwargs)
        self._scc_sizes = np.array([len(olivia_model.network.nodes[x]['members']) for x in olivia_model.network])

    def _aggregation(self, n, descendants):
        return self._scc_sizes[descendants].sum() + self._scc_sizes[n]

    def compute(self):
        """ Computes the Surface metric for each package in the network.

        Returns
        -------
            ms: A ~MetricStats object with the results of the computation.
        """
        return MetricStats(super().compute(), normalize_factor=self._scc_sizes.sum())


class MetricStats:
    """
    A helper class to store and manipulate Olivia metrics.
    """
    def __init__(self, results_dict, normalize_factor=1):
        """
        Creates and initializes a MetricStats object

        Parameters
        ----------
        results_dict: dict
            {node:value} dict with metric values.
        normalize_factor: float
            Factor to perform normalization
        """
        self._results = results_dict
        self._normalize_factor = normalize_factor
        self._normalized = False
        self._build_index()

    def __getitem__(self, index):
        """
        Metric value for package 'index'

        Parameters
        ----------
        index: identifier
            Identifier of package.

        Returns
        -------
        value: int
            Metric value for package 'index'
        """
        return self._results[index]

    def _build_index(self):
        self._values = np.array([self.results_dict[k] for k in self.results_dict])
        self._keys = np.array([k for k in self.results_dict.keys()])
        sorted_indexes = np.flip(np.argsort(self._values))
        self._sorted_keys = self._keys[sorted_indexes]

    def top(self, n=1):
        """
        Returns the top 'n' elements according to its metric value

        Parameters
        ----------
        n: int
            number of top packages to retrieve.

        Returns
        -------
        result: list of duples
            List of top n (package, metric value) tuples
        """
        return [(k, self._results[k]) for k in self._sorted_keys[:n]]

    def bottom(self, n=1):
        """
        Returns the bottom 'n' elements according to its metric value

        Parameters
        ----------
        n: int
            number of bottom packages to retrieve.

        Returns
        -------
        result: list of duples
            List of bottom n (package, metric value) tuples
        """
        return [(k, self._results[k]) for k in self._sorted_keys[-n:]]

    @property
    def values(self):
        return self._values

    @property
    def keys(self):
        return self._keys

    @property
    def results_dict(self):
        return self._results

    @property
    def normalize_factor(self):
        return self._normalize_factor

    def normalize(self):
        if self._normalized:
            return
        for k in self._results:
            self._results[k] = self._results[k] / self._normalize_factor
        self._build_index()
