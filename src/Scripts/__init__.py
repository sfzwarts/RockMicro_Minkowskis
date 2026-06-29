"""Compatibility layer for releases that exposed a capitalized ``Scripts`` package.

New code should import the explicit modules from :mod:`rockmicro` instead.
"""

from importlib import import_module

__all__ = ["handling_moose", "meshing", "microstructures", "moose", "postprocessing"]


def __getattr__(name: str):
    if name not in __all__:
        raise AttributeError(name)
    module_name = "moose" if name == "handling_moose" else name
    module = import_module(f"rockmicro.{module_name}")
    globals()[name] = module
    return module
