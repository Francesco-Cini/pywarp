import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize


def plot_component(array, title_text, x_label_text, y_label_text, alpha=1.0,
                   *, ax=None, x=None, y=None):
    """Plot a 2D component as a signed heatmap; return (figure, axes). No show()."""
    values = np.asarray(array)
    if values.ndim != 2 or not np.isfinite(values).all():
        raise ValueError("Component must be a finite 2D array")
    if not 0 <= alpha <= 1:
        raise ValueError("alpha must be between zero and one")
    if ax is None:
        _, ax = plt.subplots(layout="constrained")
    x = np.arange(1, values.shape[0]+1) if x is None else np.asarray(x)
    y = np.arange(1, values.shape[1]+1) if y is None else np.asarray(y)
    limit = float(np.max(np.abs(values))) or 1.0
    mesh = ax.pcolormesh(x, y, values.T, shading="nearest", cmap="RdBu_r",
                        norm=Normalize(-limit, limit), alpha=alpha, rasterized=True)
    ax.set(title=title_text, xlabel=x_label_text, ylabel=y_label_text)
    ax.figure.colorbar(mesh, ax=ax, shrink=0.8, pad=0.02)
    return ax.figure, ax
