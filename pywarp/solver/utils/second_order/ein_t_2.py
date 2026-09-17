def ein_t_2(
        R_munu,
        R,
        g_l
):

    E = [[None for _ in range(4)] for _ in range(4)]

    for mu in range(4):
        for nu in range(4):

            E[mu][nu] = R_munu[mu][nu] - 0.5 * g_l[mu][nu] * R

    return E
