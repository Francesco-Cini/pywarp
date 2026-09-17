from pywarp.solver.utils.second_order.ricci_t_2 import _ricci_tensor


def ricci_t_mem_2(g_u, g_l, delta):
    """WarpFactory ricciTMem2, recomputing second derivatives to save memory.

    Like the MATLAB memory variant, this expects x0 = ct spacing (length),
    unlike ricci_t_2 which accepts time spacing in seconds. To compare the
    two routines, multiply delta[0] by c() before calling this function.
    """
    return _ricci_tensor(g_u, g_l, delta, cache_second=False, time_is_seconds=False)
