"""Tiny dry run: 20 IN-MEMORY T51 examples for unit tests (never written to disk): 4 matrix rows (one per label/lane
combination), 2 trajectory pairs (4), 1 consent quad (4), 2 compaction pairs (4) = 16 + 4 more matrix rows = 20."""
from .blocks import build_cell, plan


def select_dry_cells(cells=None):
    cells = cells if cells is not None else plan()

    def first(pred, k=1):
        return [c for c in cells if pred(c)][:k]

    sel = []
    sel += first(lambda c: c.kind == "matrix" and c.extras["variant"] == "V1" and c.extras["R"] == "contained")
    sel += first(lambda c: c.kind == "matrix" and c.extras["variant"] == "V2" and c.extras["R"] == "contained")
    sel += first(lambda c: c.kind == "matrix" and c.extras["variant"] == "V2" and c.extras["R"] == "shared")
    sel += first(lambda c: c.kind == "matrix" and c.extras["variant"] == "V4")
    sel += first(lambda c: c.kind == "matrix" and c.extras["variant"] == "V5")
    sel += first(lambda c: c.kind == "matrix" and c.extras["variant"] == "V6" and c.extras["S"] == "S3")
    sel += first(lambda c: c.kind == "matrix" and c.extras["variant"] == "V3")
    sel += first(lambda c: c.kind == "traj" and c.extras["edit"] == "partial")
    sel += first(lambda c: c.kind == "traj" and c.extras["edit"] == "revoked_boundary" and c.extras["lane"] == "shared")
    sel += first(lambda c: c.kind == "consent")
    sel += first(lambda c: c.kind == "compaction" and c.extras["compliant"])
    sel += first(lambda c: c.kind == "compaction" and not c.extras["compliant"])
    return sel


def build_dry():
    drops, specs = [], []
    for c in select_dry_cells():
        specs += build_cell(c, drops)
    return specs, drops
