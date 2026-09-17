from unittest import case

import numpy as np

def take_finite_difference_1_2(
        A,
        k,
        delta
):

    s = A.shape
    B = np.zeros(s)

    if s(k) >= 3:
        match k
            case 0:
                B[1:-1, :, :, :] = (A[2:, :, :, :] - A[:-2, :, :, :]) / (2 * delta[k])
                B[0, :, :, :] = B[1, :, :, :]
                B[-1, :, :, :] = B[-2, :, :, :]
            case 1:
                B[:, 1:-1, :, :] = (A[:, 2:, :, :] - A[:, :-2, :, :]) / (2 * delta[k])
                B[:, 0, :, :] = B[:, 1, :, :]
                B[:, -1, :, :] = B[:, -2, :, :]
            case 2:
                B[:, :, 1:-1, :] = (A[:, :, 2:, :] - A[:, :, :-2, :]) / (2 * delta[k])
                B[:, :, 0, :] = B[:, :, 1, :]
                B[:, :, -1, :] = B[:, :, -2, :]
            case 3:
                B[:, :, :, 1:-1] = (A[:, :, :, 2:] - A[:, :, :, :-2]) / (2 * delta[k])
                B[:, :, :, 0] = B[:, :, :, 1]
                B[:, :, :, -1] = B[:, :, :, -2]

    return B