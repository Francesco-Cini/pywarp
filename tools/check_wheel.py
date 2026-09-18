"""Install the built wheel in an isolated environment and test outside the checkout."""
import argparse
from pathlib import Path
import subprocess
import sys
import tempfile
import venv


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist",type=Path,default=Path("dist"))
    args=parser.parse_args()
    wheels=list(args.dist.resolve().glob("warp_factory_py-*.whl"))
    if len(wheels)!=1:
        raise SystemExit("Expected exactly one wheel in the selected dist directory")
    with tempfile.TemporaryDirectory(prefix="pywarp-wheel-") as directory:
        root=Path(directory)
        venv.EnvBuilder(with_pip=True).create(root/"venv")
        python=root/"venv"/("Scripts/python.exe" if sys.platform=="win32" else "bin/python")
        subprocess.run([str(python),"-m","pip","install",str(wheels[0])+"[plot]"],check=True,cwd=root)
        script = """
import pathlib, pywarp, numpy as np
import matplotlib
matplotlib.use('Agg')
from pywarp.metrics.minkowski.metric_get_minkowski import metric_get_minkowski
from pywarp.analyser.eval_metric import eval_metric
from pywarp.visualiser import plot_tensor,plot_three_plus_one
assert 'site-packages' in str(pathlib.Path(pywarp.__file__).resolve())
metric=metric_get_minkowski([1,5,5,5])
for order in ('second','fourth'):
    result=eval_metric(metric,num_angular_vec=6,num_time_vec=2,diff_order=order)
    np.testing.assert_array_equal(result['energy_tensor']['tensor'],np.zeros((4,4,1,5,5,5)))
for plot in (plot_tensor,plot_three_plus_one):
    figure,_=plot(metric)
    figure.canvas.draw()
print('Installed wheel: both solvers, analysis and plots passed')
"""
        subprocess.run([str(python),"-I","-c",script],check=True,cwd=root)


if __name__=="__main__": main()
