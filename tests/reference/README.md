# MATLAB reference data (future parity tests)

There are no exported MATLAB fixtures here yet. This directory does not
currently establish parity with WarpFactory.

For each future fixture, save a small `.npz` dataset plus a text description
containing the upstream commit, generator parameters, grid sizes and spacing,
units, tensor index convention, expected outputs, and export command. State
whether the boundary cells are included. Keep arrays small enough for Git.

Add a test marked `@pytest.mark.parity` that reads these fixed outputs and
compares Python results with explicit tolerances. Generate expected values
from MATLAB independently, never by calling the Python implementation under
test. Document intentional corrections to upstream rather than forcing
incorrect formulas to match.
