"""Deprecated alias of :mod:`nexclamp` (renamed twice: neurosem -> neuraxis -> nexclamp).

``import neurosem.x`` returns the very same module object as ``import nexclamp.x``, so existing
scripts, the hidden agent-study checks and historical provenance references keep working.
New code imports ``nexclamp``.
"""

from __future__ import annotations

import importlib
import importlib.abc
import importlib.util
import sys
from typing import Any

_OLD, _NEW = "neurosem", "nexclamp"


class _AliasLoader(importlib.abc.Loader):
    def __init__(self, target: str) -> None:
        self.target = target
        self._spec = None

    def create_module(self, spec):  # noqa: ANN001
        module = importlib.import_module(self.target)
        self._spec = module.__spec__
        return module

    def exec_module(self, module) -> None:  # noqa: ANN001
        module.__spec__ = self._spec          # the import system overwrote it with the alias spec


class _AliasFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname: str, path=None, target=None):  # noqa: ANN001
        if not fullname.startswith(_OLD + "."):
            return None
        return importlib.util.spec_from_loader(fullname, _AliasLoader(_NEW + fullname[len(_OLD):]))


if not any(isinstance(f, _AliasFinder) for f in sys.meta_path):
    sys.meta_path.insert(0, _AliasFinder())

import nexclamp as _pkg  # noqa: E402

__path__: list[str] = []          # submodules are resolved by _AliasFinder
__version__ = getattr(_pkg, "__version__", "")


def __getattr__(name: str) -> Any:
    return getattr(_pkg, name)
