"""families/T25/conftest.py: keeps the frozen Haiku-round records bound to the G0 they were written under.

haiku/redo2/build_redo2.py writes plugin.T25.G0_SHA256 into its TASKS.json (and its results), and those files (like every
file under haiku/) are inputs hashed by pools_v2/MANIFEST.json, so neither the records nor the script can be edited. G0 moved on
to v4 at pilot fix iteration 1 (G0_SPEC.md section 11), which changes no pool piece and no Haiku task. For the tests of
haiku/redo2 only, the pin is therefore read as the v3 sha the records carry (test_build_redo2.test_disk_matches_rebuild_when_written
compares a rebuild with the files on disk). Nothing else is patched, and nothing is written.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

G0_V3_SHA256 = "8de68753f87b885d02b15ec6207fa3ce9d69ea971a4126dd0868335dfe7fdf11"


@pytest.fixture(scope="module", autouse=True)
def _redo2_records_bind_g0_v3(request):
    if "haiku/redo2" not in str(request.fspath).replace("\\", "/"):
        yield
        return
    from families.T25 import plugin as P
    mp = pytest.MonkeyPatch()
    mp.setattr(P.T25, "G0_SHA256", G0_V3_SHA256)
    yield
    mp.undo()
