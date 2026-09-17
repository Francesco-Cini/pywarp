from datetime import datetime 

from pywarp.solver.verify_tensor import verify_tensor
from pywarp.solver.utils.strcmpi import strcmpi
from pywarp.analyser.change_tensor_index import change_tensor_index
from pywarp.gpu import (
    asarray as gpu_asarray,
    asnumpy as gpu_asnumpy
)
from pywarp.solver.utils.met_2_den import met_2_den
from pywarp.solver.utils.second_order.met_2_den_2 import met_2_den_2

def get_energy_tensor(metric, diff_order, *, gpu=None):

    if diff_order is None:
        diff_order = 'fourth'
    
    if not verify_tensor(metric, 1): 
        raise Exception("Metric is not verified. Please verify metric using verify_tensor(metric).")
    
    if not strcmpi(metric['index'], "covariant"):
        metric = change_tensor_index(metric, "covariant")
        print(f"Changed metric from %s index to %s index\n", {metric["index"]}, "covariant")
    
    if gpu is not None:
        metric_tensor_gpu = [[None for _ in range(4)] for _ in range(4)]

        for i in range(4):
            for j in range(4):
                metric_tensor_gpu[i][j] = gpu_asarray(metric['tensor'][i][j], library=gpu)

        metric_sclaing_gpu = gpu_asarray(metric['scaling'], library=gpu)
        if strcmpi(diff_order, 'fourth'):
            energy_density_gpu = met_2_den(metric_tensor_gpu, metric_sclaing_gpu)
        elif strcmpi(diff_order, 'second'):
            energy_density_gpu = met_2_den_2(metric_tensor_gpu, metric_sclaing_gpu)
        else: 
            raise Exception("Order Flag Not Specified Correctly. Options: 'fourth' or 'second'")

        energy_tensor = [[None for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                energy_tensor[i][j] = gpu_asnumpy(energy_density_gpu[i][j])

    else:

        if strcmpi(diff_order, 'fourth'):
            energy_tensor = met_2_den(metric['tensor'], metric['scaling'])

        elif strcmpi(diff_order, 'second'):
            energy_tensor = met_2_den_2(metric['tensor'], metric['scaling'])

        else:
            raise Exception("Order Flag Not Specified Correctly. Options: 'fourth' or 'second'")
        
    energy = {}
        
    energy['type'] = "Stress-Energy" 
    energy['tensor'] = energy_tensor
    energy['coords'] = metric['coords']
    energy['index'] = "contravariant"
    energy['order'] = diff_order
    energy['name'] = metric['name']
    energy['date'] = datetime.now()

    return energy 