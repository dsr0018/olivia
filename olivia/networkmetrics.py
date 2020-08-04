from olivia.packagemetrics import Reach

import numpy as np


def failure_vulnerability(olivia_model, metric=Reach, normalize=False):
    ms = olivia_model.get_metric(metric)
    if normalize:
        return ms.values.mean() / ms.normalize_factor
    else:
        return ms.values.mean()


def attack_vulnerability(olivia_model, metric=Reach, normalize=False):
    ms = olivia_model.get_metric(metric)
    if normalize:
        return ms.top()[0][1] / ms.normalize_factor
    else:
        return ms.top()[0][1]
