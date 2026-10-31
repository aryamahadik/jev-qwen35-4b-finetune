"""Adapter for zed_orch/g6_null_max.py: T32's run_pilot_i2.main needs a `run` subcommand."""
import importlib.util
from pathlib import Path

_p = Path(__file__).resolve().parents[1] / "run_pilot_i2.py"
_spec = importlib.util.spec_from_file_location("t32_run_pilot_i2", _p)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)


def main(argv=None):
    return _mod.main(["run"] + list(argv or []))
