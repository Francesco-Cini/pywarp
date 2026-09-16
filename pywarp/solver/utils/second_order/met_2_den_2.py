import numpy as np

from pywarp.solver.utils.second_order.c4_inv_2 import c4_inv_2
from pywarp.solver.utils.second_order.ricci_t_2 import ricci_t_2
from pywarp.solver.utils.second_order.ricci_s_2 import ricci_s_2
2
from pywarp.solver.utils.second_order.ein_t_2 import ein_t_2
from pywarp.solver.utils.second_order.ein_e_2 import ein_e_2

def met_2_den_2(
        metric_tensor,
        delta=None, 
        units=None,
):

    if delta is None:
        delta = np.array([1, 1, 1, 1])

    if units is None:
        units = np.array([1, 1, 1, 1])

    g_l = metric_tensor
    g_u = c4_inv_2(g_l)

    R_munu = ricci_t_2(g_u, g_l, delta)

    R = ricci_s_2(R_munu, g_u)

    E = ein_t_2(R_munu, R, g_l)

    energy_density = ein_e_2(E, g_u, units)

    return energy_density