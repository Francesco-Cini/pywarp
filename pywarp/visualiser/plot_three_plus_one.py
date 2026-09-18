import numpy as np
import matplotlib.pyplot as plt
from pywarp.analyser.change_tensor_index import change_tensor_index
from pywarp.metrics.three_plus_one_decomposer import three_plus_one_decomposer
from pywarp.visualiser.plot_tensor import _slice_setup
from pywarp.visualiser.utils.plot_component import plot_component


def plot_three_plus_one(metric, sliced_planes=None, slice_locations=None, alpha=None):
    """Return (figure, 2x5 axes) for lapse, covariant shift and spatial metric."""
    metric = change_tensor_index(metric, "covariant")
    indices, coords, labels = _slice_setup(metric, sliced_planes, slice_locations)
    lapse, beta, gamma, _, _ = three_plus_one_decomposer(metric)
    components = [(r"$\alpha$ (lapse)", lapse)]
    components += [(rf"$\beta_{{{i+1}}}$", beta[i]) for i in range(3)]
    components += [(rf"$\gamma_{{{i+1}{j+1}}}$", gamma[i][j]) for i in range(3) for j in range(i,3)]
    fig, axes = plt.subplots(2,5,figsize=(16,6.5),layout="constrained")
    for ax,(title,field) in zip(axes.flat,components):
        plot_component(np.asarray(field)[indices], title, *labels,
                       alpha=1 if alpha is None else alpha, ax=ax,x=coords[0],y=coords[1])
    if all(not label.startswith("t ") for label in labels):
        for ax in axes.flat:
            ax.set_aspect("equal")
    fig.suptitle(metric.get("name", "Metric")+" - 3+1 decomposition")
    return fig, axes


def plotThreePlusOne(metric, slicedPlanes=None, sliceLocations=None, alpha=None):
    """Compatibility alias for the original MATLAB-style name."""
    return plot_three_plus_one(metric,slicedPlanes,sliceLocations,alpha)
