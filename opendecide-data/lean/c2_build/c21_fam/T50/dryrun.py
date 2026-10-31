"""Tiny dry run: builds 20 IN-MEMORY examples for unit tests. Never writes rows to disk (the caller owns any temp dir).

The 20 cells are picked from the frozen plan so every block, a card-swap pair, a view twin, a quad, an opaque and a
write-then-run construct appear. Nothing is saved; nothing here is training data.
"""
from .blocks import plan
from .generator import DropLedger, build_cell, spec_rows

# block -> how many of the 20 examples
DRY_SPLIT = {"A": 3, "B": 2, "C": 3, "D": 4, "E": 2, "F": 1, "G": 5}


def select_dry_cells(cells=None, n=20):
    cells = cells if cells is not None else plan()
    picked = []
    per = dict(DRY_SPLIT)
    for blk, k in per.items():
        pool = [c for c in cells if c.block == blk]
        if blk == "G":                       # one cell of each block-G pair / quad type
            sel = [next(c for c in pool if c.extras["g"] == g) for g in ("g1f", "g1m", "g2f", "g3q", "g4p")]
        elif blk == "C":                     # one mandatory quad and two regular cells
            sel = [c for c in pool if c.tag == "quad4"][:1] + [c for c in pool if c.tag != "quad4"][:2]
        elif blk == "A":                     # one swap cell, one twin, one plain
            sw = [c for c in pool if c.tag == "swap"][:1]
            tw = [c for c in pool if c.extras.get("twin") and c.tag not in ("swap", "alias", "quad4")][:1]
            rest = [c for c in pool if c.tag not in ("swap", "alias", "quad4", "late") and not c.extras.get("twin")]
            sel = sw + tw + rest[:: max(1, len(rest) // max(1, k - 2))][: k - 2]
        elif blk == "D":                     # opaque, wtr allow, wtr block (and wtr modified when there is room)
            op = [c for c in pool if c.tag == "opaque"][:1]
            wa = [c for c in pool if c.intent.startswith("wtr.") and c.label == "ALLOW"][:1]
            wb = [c for c in pool if c.intent.startswith("wtr.") and c.label == "BLOCK"][:1]
            wm = [c for c in pool if c.tag == "modified"][:1]
            sel = op + wa + wb + wm
        elif blk == "E":
            sq = [c for c in pool if c.tag == "soft_quad"]
            hq = [c for c in pool if c.tag == "hard_quad"]
            sel = [sq[len(sq) // 2], hq[0]]
        else:
            sel = pool[:: max(1, len(pool) // k)][:k]
        picked += sel[:k]
    return picked[:n]


def build_dry(n=20):
    """-> (specs, ledger, cells). Specs live in memory only."""
    ledger = DropLedger()
    cells = select_dry_cells(n=n)
    specs = []
    for c in cells:
        specs += build_cell(c, ledger)
    return specs, ledger, cells
