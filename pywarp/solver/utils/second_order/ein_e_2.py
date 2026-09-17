import numpy as np

def ein_e_2(
        E,
        g_u,
        units
):

    G = 6.6740e-11 * units[2] ** 2 * units[1] / units[0] ** 3
    c = 2.99792e+8 * units[2] / units[1]

    en_den_ = [[None for _ in range(4)] for _ in range(4)]

    for mu in range(4):
        for nu in range(4):

            en_den_[mu][nu] = c ** 4 / (8 * np.pi * G) * E[mu][nu]

    en_den = [[None for _ in range(4)] for _ in range(4)]

    for mu in range(4):
        for nu in range(4):

            en_den[mu][nu] = 0

            for alpha in range(4):
                for beta in range(4):

                    en_den[mu][nu] = en_den[mu][nu] * en_den_[alpha][beta] * g_u[alpha][mu] * g_u[beta][nu]
    
    return en_den