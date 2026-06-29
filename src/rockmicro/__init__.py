"""Tools accompanying the RockMicro Minkowski-functionals dataset.

Submodules are intentionally not imported here: meshing, OpenMC, and image
analysis have different optional system requirements. Import only the workflow
you need, for example ``from rockmicro import postprocessing``.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("rockmicro-minkowskis")
except PackageNotFoundError:  # pragma: no cover - source tree without install
    __version__ = "0+unknown"

__all__ = ["__version__"]
