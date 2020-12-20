"""Olivia package metrics for network vulnerability analysis."""

import numbers

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
        Create a Reach metric object.

        Parameters
        ----------
        olivia_model: OliviaModel
            Input network.
        kwargs: **kwargs
            Parameters for ~olivia.lib.aggregators.AscendentAggregator.
            Use 'compression_threshold' and 'save_memory' to adjust computation to available RAM.

        """
        super().__init__(olivia_model.dag,
                         mapping=olivia_model.dag.graph['mapping'],
                         **kwargs)
        self._scc_sizes = np.array([len(olivia_model.dag.nodes[x]['members']) for x in olivia_model.dag])

    def _aggregation(self, n, descendants):
        return self._scc_sizes[descendants].sum() + self._scc_sizes[n]

    def compute(self):
        """
        Compute the Reach metric for each package in the network.

        Returns
        -------
            ms: A ~MetricStats object with the results of the computation.

        """
        print("Computing Reach")
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
        Create an Impact metric object.

        Parameters
        ----------
        olivia_model: OliviaModel
            Input network.
        kwargs: **kwargs
            Parameters for ~olivia.lib.aggregators.AscendentAggregator.
            Use 'compression_threshold' and 'save_memory' to adjust computation to available RAM.

        """
        super().__init__(olivia_model.dag,
                         mapping=olivia_model.dag.graph['mapping'],
                         **kwargs)
        odegree = olivia_model.dag.out_degree(weight='weight')
        intra_edges = np.array([olivia_model.dag.nodes[n]['intra_edges'] for n in olivia_model.dag])
        self._out = np.array([odegree[n] for n in olivia_model.dag]) + intra_edges

    def _aggregation(self, n, descendants):
        return self._out[descendants].sum() + self._out[n]

    def compute(self):
        """
        Compute the Impact metric for each package in the network.

        Returns
        -------
            ms: A ~MetricStats object with the results of the computation.

        """
        print("Computing Impact")
        return MetricStats(super().compute(), normalize_factor=self._out.sum())


class Surface(DescendentAggregator):
    """
    Olivia Surface Metric.

    SURFACE(n) is the number of transitive ascendants of a package 'n', i.e the number
    of packets in which a defect would potentially cause the compromise of 'n'.
    """

    def __init__(self, olivia_model, **kwargs):
        """
        Create an Impact metric object.

        Parameters
        ----------
        olivia_model: OliviaModel
            Input network.
        kwargs: **kwargs
            Parameters for ~olivia.lib.aggregators.AscendentAggregator.
            Use 'compression_threshold' and 'save_memory' to adjust computation to available RAM.

        """
        super().__init__(olivia_model.dag,
                         mapping=olivia_model.dag.graph['mapping'],
                         **kwargs)
        self._scc_sizes = np.array([len(olivia_model.dag.nodes[x]['members']) for x in olivia_model.dag])

    def _aggregation(self, n, descendants):
        return self._scc_sizes[descendants].sum() + self._scc_sizes[n]

    def compute(self):
        """
        Compute the Surface metric for each package in the network.

        Returns
        -------
            ms: A ~MetricStats object with the results of the computation.

        """
        print("Computing Surface")
        return MetricStats(super().compute(), normalize_factor=self._scc_sizes.sum())


class DependenciesCount:
    """
    Dependencies Count Metric.

    Number of direct dependencies of a package.
    """

    def __init__(self, olivia_model):
        """
        Create a DependenciesCount metric object.

        Parameters
        ----------
        olivia_model: OliviaModel
            Input network.

        """
        self.net = olivia_model

    def compute(self):
        """
        Compute the Dependencies Count metric for each package in the network.

        Returns
        -------
            ms: A ~MetricStats object with the results of the computation.

        """
        print("Computing Dependencies Count")
        return MetricStats({package: self.net.network.in_degree(package) for package in self.net.network})


class DependentsCount:
    """
    Dependents Count Metric.

    Number of direct dependents of a package.
    """

    def __init__(self, olivia_model):
        """
        Create a DependentsCount metric object.

        Parameters
        ----------
        olivia_model: OliviaModel
            Input network.

        """
        self.net = olivia_model

    def compute(self):
        """
        Compute the Dependents Count metric for each package in the network.

        Returns
        -------
            ms: A ~MetricStats object with the results of the computation.

        """
        print("Computing Dependents Count")
        return MetricStats({package: self.net.network.out_degree(package) for package in self.net.network})


class MetricStats:
    """A helper class to store and manipulate Olivia metrics."""

    def __init__(self, results_dict, normalize_factor=1):
        """
        Create and initializes a MetricStats object.

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
        Metric value for package 'index'.

        Parameters
        ----------
        index: identifier
            Identifier of package.

        Returns
        -------
        value: int
            Metric value for package 'index'.

        """
        return self._results[index]

    def _build_index(self):
        self._values = np.array([self.results_dict[k] for k in self.results_dict], dtype=np.float64)
        self._keys = np.array([k for k in self.results_dict.keys()])
        sorted_indexes = np.flip(np.argsort(self._values))
        self._sorted_keys = self._keys[sorted_indexes]

    def top(self, n=1, subset=None):
        """
        Return the top 'n' elements according to its metric value.

        Parameters
        ----------
        n: int
            number of top packages to retrieve.
        subset: container of nodes
            subset of packages to limit the ranking to

        Returns
        -------
        result: list of duples
            List of top n (package, metric value) tuples.

        """
        if subset:
            result = []
            for k in self._sorted_keys:
                if k in subset:
                    result.append((k, self._results[k]))
                if len(result) == n:
                    break
            return result
        else:
            return [(k, self._results[k]) for k in self._sorted_keys[:n]]

    def bottom(self, n=1, subset=None):
        """
        Return the bottom 'n' elements according to its metric value.

        Parameters
        ----------
        n: int
            number of bottom packages to retrieve.
        subset: container of nodes
            subset of packages to limit the ranking to

        Returns
        -------
        result: list of duples
            List of bottom n (package, metric value) tuples.

        """
        if subset:
            result = []
            for k in reversed(self._sorted_keys):
                if k in subset:
                    result.append((k, self._results[k]))
                if len(result) == n:
                    break
            return result
        else:
            return [(k, self._results[k]) for k in self._sorted_keys[-n:]]


    @property
    def values(self):
        """Return array with metric values."""
        return self._values

    @property
    def keys(self):
        """Return package names."""
        return self._keys

    @property
    def results_dict(self):
        """Return metric values in a package:value dictionary."""
        return self._results

    @property
    def normalize_factor(self):
        """Return factor used for performing metric normalization."""
        return self._normalize_factor

    def normalize(self):
        """Perform metric normalization."""
        if self._normalized or self._normalize_factor == 1:
            return
        for k in self._results:
            self._results[k] = self._results[k] / self._normalize_factor
        self._normalized = True
        self._build_index()

    def __add__(self, other):
        """Add metric values element-wise or to a numeric constant."""
        if isinstance(other, numbers.Number):
            return MetricStats({e: self[e] + other for e in self.keys})
        else:
            return MetricStats({e: self[e] + other[e] for e in self.keys})

    def __sub__(self, other):
        """Subtract metric values element-wise or a numeric constant."""
        if isinstance(other, numbers.Number):
            return MetricStats({e: self[e] - other for e in self.keys})
        else:
            return MetricStats({e: self[e] - other[e] for e in self.keys})

    def __mul__(self, other):
        """Multiply metric values element-wise or to a numeric constant."""
        if isinstance(other, numbers.Number):
            return MetricStats({e: self[e] * other for e in self.keys})
        else:
            return MetricStats({e: np.multiply(self[e], other[e], dtype=np.int64) for e in self.keys})

    def __truediv__(self, other):
        """Divide metric values element-wise or with a numeric constant."""
        if isinstance(other, numbers.Number):
            return MetricStats({e: np.true_divide(self[e], other, dtype=np.float64) for e in self.keys})
        else:
            return MetricStats({e: np.true_divide(self[e], other[e], dtype=np.float64) for e in self.keys})

    def __pow__(self, other):
        """Power metric values element-wise  or to a numeric constant."""
        if isinstance(other, numbers.Number):
            return MetricStats({e: self[e] ** other for e in self.keys})
        else:
            return MetricStats({e: self[e] ** other[e] for e in self.keys})
