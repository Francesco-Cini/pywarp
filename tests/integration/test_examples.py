"""Ensure the public teaching examples stay executable as the API evolves."""
import subprocess
import sys
from pathlib import Path
import pytest

pytestmark=pytest.mark.integration


@pytest.mark.parametrize("module",[
    "examples.basic.minkowski", "examples.basic.custom_metric",
    "examples.analysis.alcubierre", "examples.analysis.compare_orders",
])
def test_example_runs(module):
    result=subprocess.run([sys.executable,"-m",module],cwd=Path(__file__).resolve().parents[2],
                          capture_output=True,text=True,timeout=30)
    assert result.returncode==0,result.stderr
    assert result.stdout.strip()
