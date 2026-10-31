"""Word 10-gram hashing shared by the golden_train near-duplicate filter (public-1 fix, review item 3) and the QC
checks. Words: NFKC, lower case, split on every non [0-9a-z] run (the review's tokenisation). A 10-gram's hash is a
polynomial over the words' xxh64 hashes (mod 2^64), so whole-file indexes stay numpy arrays (no text is stored).
"""
from __future__ import annotations

import re
import unicodedata

import numpy as np
import xxhash

N = 10
_NA = re.compile(r"[^0-9a-z]+")
_M = np.uint64(0x9E3779B97F4A7C15)
_POW = [np.uint64(1)]
for _ in range(N - 1):
    _POW.append(np.uint64((int(_POW[-1]) * int(_M)) & 0xFFFFFFFFFFFFFFFF))
_POW = _POW[::-1]  # weight of word j in a window is M^(N-1-j)


def words(s: str) -> list[str]:
    return _NA.sub(" ", unicodedata.normalize("NFKC", s or "").lower()).split()


def gram_hashes(text: str) -> np.ndarray:
    """Distinct 10-gram hashes of one text (empty array if it has fewer than 10 words)."""
    ws = words(text)
    if len(ws) < N:
        return np.zeros(0, dtype=np.uint64)
    w = np.fromiter((xxhash.xxh64_intdigest(x.encode()) for x in ws), dtype=np.uint64, count=len(ws))
    L = len(ws) - N + 1
    h = np.zeros(L, dtype=np.uint64)
    with np.errstate(over="ignore"):
        for j in range(N):
            h += w[j:j + L] * _POW[j]
    return np.unique(h)


class GramIndex:
    """Sorted unique 10-gram hashes of C1 golden_train (tmp/golden_g10.npy, built by build_golden_grams.py)."""

    def __init__(self, path):
        self.a = np.load(path, mmap_mode=None)

    def coverage(self, text: str) -> float:
        g = gram_hashes(text)
        if g.size == 0:
            return 0.0
        i = np.searchsorted(self.a, g)
        i[i >= self.a.size] = self.a.size - 1
        return float((self.a[i] == g).sum()) / g.size
