"""The pool-era builders (haiku/redo2, redo3, reads) write plugin.T06Plugin.G0_SHA256 into their manifests, and their own
sha256 is recorded in TASKS.json, so they stay byte for byte as they are. They were authored against G0 v2; G0_SHA256
itself moved to v3 (pilot fix iteration 1). The tests that rebuild them (and test_freeze_v2, which does too) run under the
authored sha; every other test sees the v3 pin."""
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from families.T06 import plugin as P  # noqa: E402

# extract_build computes its G3-H field list at import (collection), so the authored describe must already be in place then;
# the autouse fixture below sets the right one for every module that runs.
P.T06Plugin.ITEM_DESCRIBE = P.T06Plugin.ITEM_DESCRIBE_AUTHORED

REBUILDING = ("test_build_redo2.py", "test_build_redo3.py", "test_build_reads.py", "test_freeze_v2.py")


@pytest.fixture(autouse=True, scope="module")
def _authored_g0(request):
    if Path(str(request.node.fspath)).name not in REBUILDING:
        P.T06Plugin.ITEM_DESCRIBE = P.T06Plugin.ITEM_DESCRIBE_I2
        try:
            yield
        finally:
            P.T06Plugin.ITEM_DESCRIBE = P.T06Plugin.ITEM_DESCRIBE_AUTHORED
        return
    keep = P.T06Plugin.G0_SHA256, P.T06Plugin.ITEM_DESCRIBE
    P.T06Plugin.G0_SHA256 = P.T06Plugin.G0_SHA256_AUTHORED
    P.T06Plugin.ITEM_DESCRIBE = P.T06Plugin.ITEM_DESCRIBE_AUTHORED       # the pool-era G3-H task files carry this text
    try:
        yield
    finally:
        P.T06Plugin.G0_SHA256 = keep[0]
        P.T06Plugin.ITEM_DESCRIBE = P.T06Plugin.ITEM_DESCRIBE_AUTHORED
