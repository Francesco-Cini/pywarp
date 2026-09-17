from pywarp.solver.utils.take_finite_difference_1 import take_finite_difference_1
from pywarp.solver.utils.second_order.take_finite_difference_1_2 import take_finite_difference_1_2
from pywarp.solver.utils.get_christoffel_sym import get_christoffel_sym
from pywarp.units.universal_constants.c import c


def cov_div(g_l, g_u, vec_u, vec_d, idx_div, idx_vec, delta, stair_sel, diff_order="fourth"):
    """Covariant derivative on a Cartesian (t,x,y,z) grid in the ct basis."""
    if diff_order not in ("second", "fourth"):
        raise ValueError("diff_order must be second or fourth")
    derivative = take_finite_difference_1_2 if diff_order == "second" else take_finite_difference_1

    def partial(field, axis):
        value = derivative(field, axis, delta)
        return value / c() if axis == 0 else value

    diff = [[[partial(g_l[i][j], k) for k in range(4)] for j in range(4)] for i in range(4)]
    if stair_sel == 0:
        result = partial(vec_d[idx_vec], idx_div)
        for i in range(4):
            result = result - get_christoffel_sym(g_u, diff, i, idx_vec, idx_div) * vec_d[i]
    elif stair_sel == 1:
        result = partial(vec_u[idx_vec], idx_div)
        for i in range(4):
            result = result + get_christoffel_sym(g_u, diff, idx_vec, idx_div, i) * vec_u[i]
    else:
        raise ValueError("Invalid variance selected")
    return result
