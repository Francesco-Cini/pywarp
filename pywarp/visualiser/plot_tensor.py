import numpy as np
import matplotlib.pyplot as plt
from pywarp.solver.verify_tensor import verify_tensor
from pywarp.visualiser.utils.get_slice_data import get_slice_data
from pywarp.visualiser.utils.plot_component import plot_component


def _slice_setup(tensor, sliced_planes, slice_locations):
    if tensor.get("coords", "").lower() != "cartesian":
        raise ValueError("Only Cartesian coordinates are supported")
    planes = (1, 4) if sliced_planes is None else sliced_planes
    indices = get_slice_data(planes, slice_locations, tensor)
    axes = [i for i,index in enumerate(indices) if isinstance(index,slice)]
    shape = np.shape(tensor["tensor"][0][0])
    spacing = tensor.get("scaling")
    centre = tensor.get("params", {}).get("world_centre", np.zeros(4))
    coords, labels = [], []
    for axis in axes:
        label = ("t","x","y","z")[axis]
        if spacing is None:
            coords.append(np.arange(1,shape[axis]+1))
            labels.append(f"{label} (grid index)")
        else:
            coords.append((np.arange(shape[axis])+1)*spacing[axis]-centre[axis])
            labels.append(f"{label} ({'s' if axis == 0 else 'm'})")
    return indices, coords, labels


def _component_title(symbol, index, i, j):
    if index == "covariant": return rf"${symbol}_{{{i}{j}}}$"
    if index == "contravariant": return rf"${symbol}^{{{i}{j}}}$"
    if index == "mixedupdown": return rf"${symbol}^{{{i}}}_{{{j}}}$"
    return rf"${symbol}_{{{i}}}^{{{j}}}$"


def plot_tensor(tensor, alpha=None, sliced_planes=None, slice_locations=None):
    """Return (figure, 4x4 axes) for all components. Axes and slice cells are one-based.

    Default slice fixes time and z at their middle cells. Call plt.show() or
    figure.savefig(...) yourself. Coordinates use SI grid scaling if available.
    """
    if not verify_tensor(tensor, 1):
        raise ValueError("Invalid tensor")
    indices, coords, labels = _slice_setup(tensor, sliced_planes, slice_locations)
    fig, axes = plt.subplots(4,4,figsize=(13,11),layout="constrained")
    symbol = "g" if tensor["type"].lower() == "metric" else "T"
    for i in range(4):
        for j in range(4):
            plot_component(np.asarray(tensor["tensor"][i][j])[indices],
                           _component_title(symbol,tensor["index"].lower(),i,j),
                           *labels, alpha=1 if alpha is None else alpha,
                           ax=axes[i,j], x=coords[0], y=coords[1])
    if all(not label.startswith("t ") for label in labels):
        for ax in axes.flat:
            ax.set_aspect("equal")
    fig.suptitle(tensor.get("name", "Tensor"))
    return fig, axes
