from pywarp.solver.utils.c4_inv import c4_inv


def get_inner_product(vec_a, vec_b, metric):
    """Contract vectors in either index convention without changing inputs."""
    if vec_a["index"].lower() != vec_b["index"].lower():
        return sum(vec_a["field"][i] * vec_b["field"][i] for i in range(4))
    g = metric["tensor"]
    if vec_a["index"].lower() == metric["index"].lower():
        g = c4_inv(g)
    return sum(vec_a["field"][i] * vec_b["field"][j] * g[i][j]
               for i in range(4) for j in range(4))
