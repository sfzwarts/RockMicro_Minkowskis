# Contributing

Thank you for helping extend RockMicro Minkowskis.

## Development setup

```bash
bash setup.sh
source .venv/bin/activate
pytest
ruff check src tests examples tools
```

Use Python 3.12, keep generated files in `outputs/`, and add tests for behavior changes.
The full OpenMC/Gmsh research stack is available through `environment.yml`.

## Data contributions

Before adding a dataset entry:

1. follow the conventions in `Data/README.md`;
2. record the random seed and all geometry, resolution, and orientation parameters;
3. keep particle coordinates grouped in packing-fraction ZIP archives;
4. do not commit unpacked or intermediate solver output; and
5. document any new table columns or normalization choices.

Large dataset releases should be archived on Zenodo and linked from the repository rather
than added to Git history without discussion.

## Pull requests

Keep changes focused and describe how you validated them. Do not reformat or regenerate
the published data as part of an unrelated code change. By contributing, you agree that
your work may be distributed under this repository's CC BY 4.0 license.
