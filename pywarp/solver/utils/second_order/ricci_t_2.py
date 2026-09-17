from array_api_compat import array_namespace

from pywarp.solver.utils.second_order.take_finite_difference_1_2 import take_finite_difference_1_2
from pywarp.solver.utils.second_order.take_finite_difference_2_2 import take_finite_difference_2_2
from pywarp.units.universal_constants.c import c


def ricci_t_2(g_u, g_l, delta):
    """WarpFactory ricciT2: symmetric metric on a (t, x, y, z) grid.

    Time spacing is in seconds; time derivatives are converted to ct.
    Cache first and second derivatives as in the original MATLAB routine.
    """
    return _ricci_tensor(g_u, g_l, delta, cache_second=True, time_is_seconds=True)


def _ricci_tensor(g_u, g_l, delta, *, cache_second, time_is_seconds):
    xp = array_namespace(g_l[0][0])
    R_munu = [[None for _ in range(4)] for _ in range(4)]
    diff_1_g_l = [[[None for _ in range(4)] for _ in range(4)] for _ in range(4)]
    diff_2_g_l = {}

    def second(i, j, k, n):
        # Symmetric metric and commuting mixed partial derivatives.
        i, j = min(i, j), max(i, j)
        k, n = min(k, n), max(k, n)
        key = (i, j, k, n)
        if cache_second and key in diff_2_g_l:
            return diff_2_g_l[key]
        value = take_finite_difference_2_2(g_l[i][j], k, n, delta)
        if time_is_seconds:
            value = value / c() ** (int(k == 0) + int(n == 0))
        if cache_second:
            diff_2_g_l[key] = value
        return value

    for i in range(4):
        for j in range(i, 4):
            for k in range(4):
                value = take_finite_difference_1_2(g_l[i][j], k, delta)
                if time_is_seconds and k == 0:
                    value = value / c()
                diff_1_g_l[i][j][k] = value
                diff_1_g_l[j][i][k] = value
                if cache_second:
                    for n in range(k, 4):
                        second(i, j, k, n)

    for i in range(4):
        for j in range(i, 4):
            R_munu_temp = xp.zeros_like(g_l[0][0], dtype=xp.float64)
            diff_1_g_l_jXi = [diff_1_g_l[j][r][i] for r in range(4)]
            diff_1_g_l_iXj = [diff_1_g_l[i][r][j] for r in range(4)]
            diff_1_g_l_ijX = [diff_1_g_l[j][i][r] for r in range(4)]

            for a in range(4):
                for b in range(4):
                    g_ab = g_u[a][b]
                    # First term: second derivatives of the metric.
                    R_munu_temp = R_munu_temp - 0.5 * (
                        second(i, j, a, b) + second(a, b, i, j)
                        - second(i, b, j, a) - second(j, b, i, a)
                    ) * g_ab

                    for r in range(4):
                        for d in range(4):
                            # Second and third terms, directly from ricciT2.m.
                            R_munu_temp = R_munu_temp + 0.5 * (
                                0.5 * diff_1_g_l[a][r][i] * diff_1_g_l[b][d][j]
                                + diff_1_g_l[i][r][a] * diff_1_g_l[j][d][b]
                                - diff_1_g_l[i][r][a] * diff_1_g_l[j][b][d]
                            ) * g_ab * g_u[r][d]
                            R_munu_temp = R_munu_temp - 0.25 * (
                                diff_1_g_l_jXi[r] + diff_1_g_l_iXj[r] - diff_1_g_l_ijX[r]
                            ) * (
                                2 * diff_1_g_l[b][d][a] - diff_1_g_l[a][b][d]
                            ) * g_ab * g_u[r][d]

            R_munu[i][j] = R_munu_temp
            R_munu[j][i] = R_munu_temp

    return R_munu
