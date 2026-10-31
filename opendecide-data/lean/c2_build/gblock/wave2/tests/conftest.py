"""Wave-2 builder tests: CPU only, in memory (no test writes a file). Run from lean/:
  ../.venv/bin/python -m pytest -q c2_build/gblock/wave2/tests
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
WAVE2 = Path(__file__).resolve().parents[1]
if str(WAVE2) not in sys.path:
    sys.path.insert(0, str(WAVE2))

from builders import common as C  # noqa: E402

FILLER = ("The community group meets every week to plan small projects for the neighbourhood. Members share ideas, "
          "set simple goals and report back on what worked. New people are always welcome, and no experience is "
          "needed to take part. Most sessions end with a short walk around the area to look at progress together.")


@pytest.fixture(scope="session")
def checker():
    return C.Checker()


def fake_texts(n: int = 900) -> dict:
    """Synthetic G-block-like texts (n, spread over 4 domains) for builders that need host texts."""
    out = {}
    doms = ("recipes", "travel", "museum", "news")
    for i in range(n):
        d = doms[i % 4]
        tid = f"{d}_{i:05d}"
        out[tid] = {"text_id": tid, "domain": d, "source": f"test source {d}", "licence_url": "test licence",
                    "text": f"Item {chr(65 + i % 26)} notes.\n" + FILLER}
    return out


@pytest.fixture(scope="session")
def texts():
    return fake_texts()
