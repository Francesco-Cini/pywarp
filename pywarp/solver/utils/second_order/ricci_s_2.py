def ricci_s_2(
        R_munu,
        g_u
):
    R = 0

    for mu in range(4):
        for nu in range(4):

            R = R + g_u[mu][nu] * R_munu[mu][nu]

    return R
