"""Shared fixtures for the c2_kit tests. CPU only, in memory: no test writes a file (A37 f: no C2 data before A38).

Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/c2_kit/tests
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit.reference import r00, r00_fixtures  # noqa: E402


@pytest.fixture(scope="session")
def ctx():
    return r00_fixtures.ctx()


@pytest.fixture(scope="session")
def plugin(ctx):
    return r00.R00(lexicon=ctx.lexicon)
