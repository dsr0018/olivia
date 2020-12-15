
"""Olivia network vulnerability metrics."""

from olivia.packagemetrics import Reach


def failure_vulnerability(olivia_model, metric=Reach, normalize=False):
    """
    Compute network vulnerability to failure metric.

    Vulnerability to failure is the mean of some cost metric for the packages in the network, measuring
    the expected cost caused by the failure of an uniformly chosen random package.
    For example, it corresponds to the expected number of packages (using the Reach metric)
    or dependencies (using the Impact metric) potentially compromised by the introduction of a defect into a random
    package.

    If normalized, the result is given in terms of proportion to the total network cost (i.e. number of packages or
    dependencies for the Reach/Impact metrics)

    Parameters
    ----------
    olivia_model: OliviaNetwork
        Input network.
    metric: Cost metric, optional
        Usually Reach or Impact, but a custom metric class may be provided, assuming it implements
        a compute() method that returns a MetricStats() object.
    normalize: bool, optional
        Normalize the output value.

    Returns
    -------
    vulnerability: float
        Vulnerability to failure value.

    """
    ms = olivia_model.get_metric(metric)
    if normalize:
        return ms.values.mean() / ms.normalize_factor
    else:
        return ms.values.mean()


def attack_vulnerability(olivia_model, metric=Reach, normalize=False):
    """
    Compute network vulnerability to attack metric.

    Vulnerability to attack is the maximum of some cost metric for the packages in the network, measuring
    the potential cost caused by a directed attack to the network.
    For example, it corresponds to the maximum number of packages (using the Reach metric)
    or dependencies (using the Impact metric) potentially compromised by the introduction of a defect into a package
    selected by a possible attacker.

    If normalized, the result is given in terms of proportion to the total network cost (i.e. number of packages or
    dependencies for the Reach/Impact metrics).

    Parameters
    ----------
    olivia_model: OliviaNetwork
        Input network.
    metric: Cost metric, optional
        Usually Reach or Impact, but a custom metric class may be provided, assuming it implements
        a compute() method that returns a MetricStats() object.
    normalize: bool, optional
        Normalize the output value.

    Returns
    -------
    vulnerability: float
        Vulnerability to attack value.

    """
    ms = olivia_model.get_metric(metric)
    if normalize:
        return ms.top()[0][1] / ms.normalize_factor
    else:
        return ms.top()[0][1]
