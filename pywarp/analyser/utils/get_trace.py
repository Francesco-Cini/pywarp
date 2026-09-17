import numpy as np
from pywarp.solver.utils.c4_inv import c4_inv


def get_trace(tensor, metric):
    """Contract a rank-two tensor without modifying the reference metric."""
    if tensor["index"].lower().startswith("mixed"):
        return sum(tensor["tensor"][i][i] for i in range(4))
    g = metric["tensor"]
    if tensor["index"].lower() == metric["index"].lower():
        g = c4_inv(g)
    return sum(g[i][j] * tensor["tensor"][i][j] for i in range(4) for j in range(4))
