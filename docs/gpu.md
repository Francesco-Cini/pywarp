# GPU support and validation

The public `gpu` argument accelerates **curvature calculation**. Final SI
scaling/index contraction and analysis (frames, energy conditions and scalars)
run on CPU float64. Outputs are NumPy arrays. GPU calculations are opt-in;
the default remains CPU. There is no silent fallback when a requested device
backend is unavailable.

| Backend | Precision | Validation status |
| --- | --- | --- |
| NumPy | float64 | CPU analytic, integration and MATLAB reference checks |
| torch-directml | float32 curvature, float64 host energy conversion | Tested on Radeon RX 580, Windows, Python 3.12, torch 2.4.1, torch-directml 0.2.5.dev240914 |
| CuPy | float64 | Shared hardware tests provided; not executed locally because no NVIDIA GPU is present |

DirectML float64 reciprocal failed on this device, and strided slice writes
produced wrong derivatives without raising errors. The DirectML stencil path
now permutes each working axis into contiguous storage and builds boundaries
with concatenation. All four first-derivative axes and all 16 second-derivative
axis combinations are checked against NumPy for both orders. SI energy
prefactors exceed float32 range, so that conversion is deliberately done on
the host. CPU postprocessing does not restore precision lost in float32
curvature; use CPU/CUDA float64 for precision-sensitive investigations.

## Install and run hardware tests

DirectML currently needs an older supported Python; the tested environment
uses Python 3.12. Use a separate environment from Python 3.14:

```powershell
py -3.12 -m venv .venv-directml
.\.venv-directml\Scripts\python.exe -m pip install -e ".[test,directml]"
.\.venv-directml\Scripts\python.exe -m pytest tests/gpu --gpu-backend=torch-directml -q
.\.venv-directml\Scripts\python.exe -m benchmarks.backend_comparison --backend torch-directml
```

For an NVIDIA machine with a compatible CUDA 12 driver:

```powershell
python -m pip install -e ".[test,cuda]"
python -m pytest tests/gpu --gpu-backend=cupy -q
python -m benchmarks.backend_comparison --backend cupy
```

Without `--gpu-backend`, hardware tests explicitly skip. If you select a
backend that cannot initialize, tests fail rather than skip. Hosted CPU CI
excludes the hardware marker; it does not certify CUDA or DirectML.

Full GPU tests compare both solver orders on static and time-dependent
Alcubierre metrics and all analysis outputs. DirectML uses a scale-aware
2e-5 tolerance; CuPy uses 1e-10. Near-zero components use a tolerance scaled
to the largest reference component. These are selected regression cases,
not universal error bounds for arbitrary grids or near-singular metrics.

## Performance

`directml-results.json` records the machine, backend, grid, repeats, median
CPU/device elapsed times and maximum normalized error. Timings include data
transfers and float64 host conversion; the benchmark gathers outputs before
stopping the timer. GPU initialization occurs before measurements. The small
5x5x5 spatial grid is slower on this DirectML device than CPU because this
implementation dispatches many small tensor operations. No speedup is claimed.
Larger grids must be measured separately, with numerical accuracy checked too.
The report does not measure native GPU memory usage.
