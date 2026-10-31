"""T01 tests: the pool-era G3-H task files (haiku/extract, redo*) carry the authored topic describe, so the modules that
rebuild them see it; every other module sees the iteration-3 describe (the generator's topic has no leading "the")."""
from pathlib import Path

import pytest

from families.T01 import plugin as P

REBUILDING = ("test_build_redo2.py", "test_build_redo3.py", "test_build_reads.py", "test_freeze_v2.py", "test_haiku_author.py",
              "test_build_extract.py", "test_extract.py")

P.T01.TOPIC_DESCRIBE = P.T01.TOPIC_DESCRIBE_AUTHORED       # extract builders compute the field list at import (collection)


@pytest.fixture(autouse=True, scope="module")
def _authored_describe(request):
    name = Path(str(request.node.fspath)).name
    P.T01.TOPIC_DESCRIBE = P.T01.TOPIC_DESCRIBE_AUTHORED if name in REBUILDING else P.T01.TOPIC_DESCRIBE_I3
    try:
        yield
    finally:
        P.T01.TOPIC_DESCRIBE = P.T01.TOPIC_DESCRIBE_AUTHORED
