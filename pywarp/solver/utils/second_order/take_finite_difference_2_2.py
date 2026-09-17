from array_api_compat import array_namespace

def take_finite_difference_2_2(
        A,
        k_1,
        k_2,
        delta
):

    s = A.shape
    xp = array_namespace(A)
    B = xp.zeros_like(A, dtype=xp.float64)

    if s[k_1] >= 3 and s[k_2] >= 3:
        if k_1 == k_2:
            match k_1:
                case 0:
                    B[1:-1, :, :, :] = (A[2:, :, :, :] - 2 * A[1:-1, :, :, :] + A[:-2, :, :, :]) / (delta[k_1] ** 2)
                    B[0, :, :, :] = B[1, :, :, :]
                    B[-1, :, :, :] = B[-2, :, :, :]
                case 1:
                    B[:, 1:-1, :, :] = (A[:, 2:, :, :] - 2 * A[:, 1:-1, :, :] + A[:, :-2, :, :]) / (delta[k_1] ** 2)
                    B[:, 0, :, :] = B[:, 1, :, :]
                    B[:, -1, :, :] = B[:, -2, :, :]
                case 2:
                    B[:, :, 1:-1, :] = (A[:, :, 2:, :] - 2 * A[:, :, 1:-1, :] + A[:, :, :-2, :]) / (delta[k_1] ** 2)
                    B[:, :, 0, :] = B[:, :, 1, :]
                    B[:, :, -1, :] = B[:, :, -2, :]
                case 3:
                    B[:, :, :, 1:-1] = (A[:, :, :, 2:] - 2 * A[:, :, :, 1:-1] + A[:, :, :, :-2]) / (delta[k_1] ** 2)
                    B[:, :, :, 0] = B[:, :, :, 1]
                    B[:, :, :, -1] = B[:, :, :, -2]
        else:
            k_L = max(k_1, k_2)
            k_S = min(k_1, k_2)

            x1 = slice(2, s[k_S])
            x0 = slice(1, s[k_S] - 1)
            x_1 = slice(0, s[k_S] - 2)

            y1 = slice(2, s[k_L])
            y0 = slice(1, s[k_L] - 1)
            y_1 = slice(0, s[k_L] - 2)

            match k_S:
                case 0:
                    match k_L:
                        case 1:
                            B[x0, y0, :, :] = (
                                A[x_1, y_1, :, :] - A[x_1, y1, :, :]
                                - A[x1, y_1, :, :] + A[x1, y1, :, :]
                            ) / (4 * delta[k_L] * delta[k_S])
                        case 2:
                            B[x0, :, y0, :] = (
                                A[x_1, :, y_1, :] - A[x_1, :, y1, :]
                                - A[x1, :, y_1, :] + A[x1, :, y1, :]
                            ) / (4 * delta[k_L] * delta[k_S])
                        case 3:
                            B[x0, :, :, y0] = (
                                A[x_1, :, :, y_1] - A[x_1, :, :, y1]
                                - A[x1, :, :, y_1] + A[x1, :, :, y1]
                            ) / (4 * delta[k_L] * delta[k_S])
                case 1:
                    match k_L:
                        case 2:
                            B[:, x0, y0, :] = (
                                A[:, x_1, y_1, :] - A[:, x_1, y1, :]
                                - A[:, x1, y_1, :] + A[:, x1, y1, :]
                            ) / (4 * delta[k_L] * delta[k_S])
                        case 3:
                            B[:, x0, :, y0] = (
                                A[:, x_1, :, y_1] - A[:, x_1, :, y1]
                                - A[:, x1, :, y_1] + A[:, x1, :, y1]
                            ) / (4 * delta[k_L] * delta[k_S])
                case 2:
                    match k_L:
                        case 3:
                            B[:, :, x0, y0] = (
                                A[:, :, x_1, y_1] - A[:, :, x_1, y1]
                                - A[:, :, x1, y_1] + A[:, :, x1, y1]
                            ) / (4 * delta[k_L] * delta[k_S])

    return B
