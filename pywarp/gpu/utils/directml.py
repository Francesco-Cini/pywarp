"""DirectML uses float32: some required float64 operators are unsupported."""
def asarray(value):
    import torch 
    import torch_directml

    return torch.as_tensor(
        value,
        dtype=torch.float32,
        device=torch_directml.device(),
    )

def asnumpy(value):
    return value.detach().cpu().numpy()
