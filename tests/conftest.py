import numpy as np
import pytest

from pywarp.metrics.minkowski.metric_get_minkowski import metric_get_minkowski


@pytest.fixture
def small_grid_size() -> np.ndarray:
    """A grid large enough for metric tests without making them expensive."""
    return np.array([5, 7, 7, 7])


@pytest.fixture
def unit_grid_scaling() -> np.ndarray:
    return np.ones(4)


@pytest.fixture
def small_world_centre(small_grid_size: np.ndarray) -> np.ndarray:
    return (small_grid_size + 1) / 2

@pytest.fixture
def numerical_tolerances() -> dict[str, float]:
    return {
        "atol": 1e-12,
        "rtol": 1e-10,}

@pytest.fixture
def minkowski_metric(
    small_grid_size: np.ndarray, 
    unit_grid_scaling: np.ndarray
) -> dict:
    return metric_get_minkowski(small_grid_size, unit_grid_scaling)