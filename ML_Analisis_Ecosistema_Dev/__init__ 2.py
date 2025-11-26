"""Shim package to provide backwards-compatible import name

Some tests import the package as `ML_Analisis_Ecosistema_Dev` (pascal case).
The real source package lives at `src/ml_analisis_ecosistema_dev` (snake case).
This small shim makes `import ML_Analisis_Ecosistema_Dev` work by delegating to
the real package without modifying other code.
"""
import importlib
import os
import sys

# Ensure `src/` is on sys.path so the real package under `src/ml_analisis_ecosistema_dev`
# can be found when running tests from the repository root.
_root = os.path.dirname(os.path.dirname(__file__))
_src = os.path.join(_root, "src")
if _src not in sys.path:
    sys.path.insert(0, _src)

try:
    _real = importlib.import_module("ml_analisis_ecosistema_dev")
except Exception:  # pragma: no cover - import errors will surface later in tests
    # If the real package isn't importable, re-raise a clear error
    raise

# Mirror public attributes from the real package into this module's globals.
for _name, _val in _real.__dict__.items():
    if _name.startswith("__"):
        continue
    globals()[_name] = _val

# Ensure package semantics (so subpackage imports work)
__path__ = getattr(_real, "__path__", [])
