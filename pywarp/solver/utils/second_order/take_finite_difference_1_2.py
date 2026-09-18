from array_api_compat import array_namespace

def take_finite_difference_1_2(
        A,
        k,
        delta
):

    if getattr(getattr(A, "device", None), "type", None) == "privateuseone":
        from pywarp.gpu.utils.directml_derivatives import derivative
        return derivative(A, k, delta, 2)

    s = A.shape
    xp = array_namespace(A)
    B = xp.zeros_like(A, dtype=A.dtype if xp.isdtype(A.dtype, "real floating") else xp.float64)

    if s[k] >= 3:
        match k:
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