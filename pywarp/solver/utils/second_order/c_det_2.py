def c_det_2(
        cell_array
):

    h, w = cell_array.shape

    if h==2 and w==2:
        cell_det = cell_array[0, 0] * cell_array[1, 1] - cell_array[0, 1] * cell_array[1, 0]

    cell_det = 0

    for i in range(h):
        sub_array = cell_array
        sub_array[0, :] = []
        sub_array[:, i] = []
        sub_det = c_det_2(sub_array)
        cell_det = cell_det + ((-1) ** i) * cell_array[0, i] * sub_det
    
    return cell_det