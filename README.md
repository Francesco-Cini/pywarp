# pywarp

Python numerical tools for spacetime metrics, stress-energy tensors and
sampled energy-condition analysis, ported from WarpFactory.

## Start here

From the repository root, with Python 3.10 or newer:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[test]"
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m examples.basic.minkowski
.\.venv\Scripts\python.exe -m examples.analysis.alcubierre
```

Install `".[test,plot]"` if you also want plotting examples. On Linux/macOS,
use `.venv/bin/python` in place of `.\.venv\Scripts\python.exe`.

- [Testing and examples: a beginner's guide](docs/testing.md)
- [Runnable examples](examples/README.md)
- [Second-order source conventions](pywarp/solver/utils/second_order/README.md)

CPU checks cover both finite-difference orders and all built-in metric
families. This is not yet a MATLAB parity certification or a GPU validation.
