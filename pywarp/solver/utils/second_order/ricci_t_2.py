import numpy as np

from pywarp.solver.utils.second_order.take_finite_difference_1_2 import take_finite_difference_1_2
from pywarp.solver.utils.second_order.take_finite_difference_2_2 import take_finite_difference_2_2
from pywarp.units.universal_constants import c

def ricci_t_2(
        g_u,
        g_l,
        delta
):

    s = g_l[0][0].shape

    R_munu = [[None for _ in range(4)] for _ in range(4)]

    diff_1_g_l = [[[None for _ in range(4)] for _ in range(4)] for _ in range(4)]
    diff_2_g_l = [[[[None for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]

    for i in range(4):
        for j in range(4):
            for k in range(4):
                diff_1_g_l[i][j][k] = take_finite_difference_1_2(g_l[i][j], k, delta)
                if k==1:
                    diff_1_g_l[i][j][k] = 1 / c * diff_1_g_l[i][j][k]

                    for n in range(4):
                        diff_2_g_l[i][j][k][n] = take_finite_difference_2_2(g_l[i][j], k, n, delta)

                        if (n==1 and k!=1) or (n!=1 and k==1):
                            diff_2_g_l[i][j][k][n] = 1 / c * diff_2_g_l[i][j][k][n]
                        elif n==1 and k==1:
                            diff_2_g_l[i][j][k][n] = 1 / c**2 * diff_2_g_l[i][j][k][n]

                        if k!=n:
                            diff_2_g_l[i][j][n][k] = diff_2_g_l[i][j][k][n]

    for k in range(4):
        diff_1_g_l[1][0][k] = diff_1_g_l[0][1][k]
        diff_1_g_l[2][0][k] = diff_1_g_l[0][2][k]
        diff_1_g_l[2][1][k] = diff_1_g_l[1][2][k]
        diff_1_g_l[3][0][k] = diff_1_g_l[0][3][k]
        diff_1_g_l[3][1][k] = diff_1_g_l[1][3][k]
        diff_1_g_l[3][2][k] = diff_1_g_l[2][3][k]

        for n in range(4):
            diff_2_g_l[1][0][k][n] = diff_2_g_l[0][1][k][n]
            diff_2_g_l[2][0][k][n] = diff_2_g_l[0][2][k][n]
            diff_2_g_l[2][1][k][n] = diff_2_g_l[1][2][k][n]
            diff_2_g_l[3][0][k][n] = diff_2_g_l[0][3][k][n]
            diff_2_g_l[3][1][k][n] = diff_2_g_l[1][3][k][n]
            diff_2_g_l[3][2][k][n] = diff_2_g_l[2][3][k][n]

        for i in range(4):
            for j in range(4):

                R_munu_temp = np.zeros(s)

                diff_1_g_l_jXi = [None for _ in range(4)]
                diff_1_g_l_iXj = [None for _ in range(4)]
                diff_1_g_l_ijX = [None for _ in range(4)]

                for X in range(4):
                    diff_1_g_l_jXi[X] = diff_1_g_l[j][X][i]
                    diff_1_g_l_iXj[X] = diff_1_g_l[i][X][j]
                    diff_1_g_l_ijX[X] = diff_1_g_l[i][j][X]

                for a in range(4):
                    for b in range(4):

                        g_ab = g_u[a][b]

                        R_munu_temp =

                        for r in range(4):
                            for d in range(4):
                                R_munu_temp = 
                                R_munu_temp = 

                R_munu[i][j] = R_munu_temp

    R_munu[1][0] = R_munu[0][1]
    R_munu[2][0] = R_munu[0][2]
    R_munu[2][1] = R_munu[1][2]
    R_munu[3][0] = R_munu[0][3]
    R_munu[3][1] = R_munu[1][3]
    R_munu[3][2] = R_munu[2][3]

    return R_munu