from array_api_compat import array_namespace

def take_finite_difference_1(A, k, delta, phi_phi_flag=0):

    if getattr(getattr(A, "device", None), "type", None) == "privateuseone":
        from pywarp.gpu.utils.directml_derivatives import derivative
        return derivative(A, k, delta, 4)

    s = A.shape
    xp = array_namespace(A)
    B = xp.zeros_like(A, dtype=A.dtype if xp.isdtype(A.dtype, "real floating") else xp.float64)

    if s[k] >= 5:
        match k:
            case 0:
                B[2:-2, :, :, :] = (-(A[4:, :, :, :]-A[:-4, :, :, :]) + 8 * (A[3:-1, :, :, :] - A[1:-3, :, :, :])) / (12 * delta[k])
                B[0, :, :, :] = B[2, :, :, :]
                B[1, :, :, :] = B[2, :, :, :]
                B[-2, :, :, :] = B[-3, :, :, :]
                B[-1, :, :, :] = B[-3, :, :, :]
            case 1:
                B[:, 2:-2, :, :] = (-(A[:, 4:, :, :]-A[:, :-4, :, :]) + 8 * (A[:, 3:-1, :, :] - A[:, 1:-3, :, :])) / (12 * delta[k])
                B[:, 0, :, :] = B[:, 2, :, :]
                B[:, 1, :, :] = B[:, 2, :, :]
                B[:, -2, :, :] = B[:, -3, :, :]
                B[:, -1, :, :] = B[:, -3, :, :]
            case 2:
                B[:, :, 2:-2, :] = (-(A[:, :, 4:, :]-A[:, :, :-4, :]) + 8 * (A[:, :, 3:-1, :] - A[:, :, 1:-3, :])) / (12 * delta[k])
                if phi_phi_flag:
                    B[:, :, 0, :] = 2 * 4
                    B[:, :, 1, :] = 2 * 3
                    B[:, :, -2, :] = 2 * (s[2] - 5 - 1)
                    B[:, :, -1, :] = 2 * (s[2] - 5)
                else:
                    B[:, :, -2, :] = B[:, :, -3, :]
                    B[:, :, -1, :] = B[:, :, -3, :]
                    B[:, :, 0, :] = B[:, :, 2, :]
                    B[:, :, 1, :] = B[:, :, 2, :]
            case 3:
                B[:, :, :, 2:-2] = (-(A[:, :, :, 4:]-A[:, :, :, :-4]) + 8 * (A[:, :, :, 3:-1] - A[:, :, :, 1:-3])) / (12 * delta[k])
                B[:, :, :, 0] = B[:, :, :, 2]
                B[:, :, :, 1] = B[:, :, :, 2]
                B[:, :, :, -2] = B[:, :, :, -3]
                B[:, :, :, -1] = B[:, :, :, -3]

    return B
