"""Proportional PILOT sample of whole spec families (the 1,000-row pilot is the first measured look at every pre-freeze gate,
G3; the 200-row G13 pilot is drawn from it). Pure function over plan cells; it builds nothing and writes nothing.
"""
from collections import defaultdict

from .canon import stable_fraction


def pilot_cells(cells, rows_of, block_of, group_of=None, n_rows=1000, salt="pilot"):
    """Pick whole cells (spec families) so each block contributes in proportion to its rows; deterministic.
    rows_of(cell) -> int rows; block_of(cell) -> block key; group_of(cell) -> stratum within a block (optional)."""
    total = sum(rows_of(c) for c in cells)
    by_block = defaultdict(list)
    for c in cells:
        by_block[block_of(c)].append(c)
    chosen = []
    for blk, cs in sorted(by_block.items()):
        want = n_rows * sum(rows_of(c) for c in cs) / float(total)
        cs = sorted(cs, key=lambda c: stable_fraction(salt, blk, repr(group_of(c)) if group_of else "", id_of(c)))
        acc = 0
        for c in cs:
            if acc >= want:
                break
            chosen.append(c)
            acc += rows_of(c)
    return chosen


def id_of(c):
    return str(getattr(c, "idx", None) if hasattr(c, "idx") else c.extras.get("idx", id(c)))
