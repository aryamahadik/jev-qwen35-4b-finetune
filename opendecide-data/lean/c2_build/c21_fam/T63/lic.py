"""T63 LIC head: licence-ID compatibility from the Opus-written, hashed T63-LIC-TABLE (identifiers only; no licence text), SOLVER A =
table lookup. The table is written by a SEPARATE fresh Opus 5.5 high session before any LIC row (T63-B6); until then only a FIXTURE table
(clearly flagged, refused for row builds) exists for tests.

Table file: {"table_id": "T63-LIC-TABLE", "fixture": bool, "sha256": <sha of the canonical cells>, "dep_ids": [16], "project_ids": [8],
             "use": ["LC-USE-1".."LC-USE-5"], "dist": ["LC-DIST-1".."LC-DIST-3"],
             "cells": {"dep|project|use|dist": {"label": COMPATIBLE|REVIEW|INCOMPATIBLE, "rationale": "<identifiers only>"}}}
Selection rules (T63-M4): cells drawn stratified by LABEL only (no per-licence cap), each cell used once, one-axis-flip pairs for >= 30% of rows
(>= 50% of the pairs flip on usage mode or distribution, not on a licence id), >= 40% of rows from (dependency, project) pairs whose 15
mode x distribution cells hold >= 2 labels.
"""
import collections
import itertools
import json
import math

from LP_COMMON import util

from . import config as C

DEP_IDS = ("MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "CC0-1.0", "Unlicense", "MPL-2.0", "LGPL-2.1-only", "LGPL-3.0-only",
           "GPL-2.0-only", "GPL-3.0-only", "AGPL-3.0-only", "CC-BY-4.0", "CC-BY-NC-4.0", "NOASSERTION")
PROJECT_IDS = ("MIT", "Apache-2.0", "BSD-3-Clause", "MPL-2.0", "LGPL-3.0-only", "GPL-3.0-only", "AGPL-3.0-only", "NOASSERTION")
USE_IDS = tuple(C.LIC_USE)
DIST_IDS = tuple(C.LIC_DIST)


class Reject(Exception):
    pass


def key(dep, proj, use, dist):
    return "%s|%s|%s|%s" % (dep, proj, use, dist)


class LicTable(object):
    def __init__(self, data):
        self.data = data
        self.fixture = bool(data.get("fixture", False))
        self.cells = {k: v["label"] for k, v in data["cells"].items()}
        self.dep_ids, self.project_ids = tuple(data["dep_ids"]), tuple(data["project_ids"])
        self.use, self.dist = tuple(data["use"]), tuple(data["dist"])
        self.sha = util.sha_obj({"cells": self.cells, "dep_ids": self.dep_ids, "project_ids": self.project_ids, "use": self.use, "dist": self.dist})
        if data.get("sha256") and data["sha256"] != self.sha:
            raise ValueError("licence table sha does not match its content")
        want = len(self.dep_ids) * len(self.project_ids) * len(self.use) * len(self.dist)
        if len(self.cells) != want or any(v not in C.LIC_LABELS for v in self.cells.values()):
            raise ValueError("licence table incomplete or with an unknown label")

    @classmethod
    def load(cls, path):
        with open(path, "r", encoding="utf-8") as f:
            return cls(json.load(f))

    def require_real(self):
        if self.fixture:
            raise ValueError("a FIXTURE licence table cannot be used to build rows (the Opus table is a separate session)")
        if not self.data.get("sha256"):
            raise ValueError("the licence table must DECLARE its sha256 (hashed before the first LIC row, T63-B6): an undeclared sha cannot be checked against the Opus record")
        return self

    def label(self, dep, proj, use, dist):
        return self.cells[key(dep, proj, use, dist)]

    def all_keys(self):
        return itertools.product(self.dep_ids, self.project_ids, self.use, self.dist)

    def neighbours(self, cell):
        """One-axis neighbours: (axis, neighbour cell). Axes: use, dist, dep, proj."""
        dep, proj, use, dist = cell
        out = []
        for u in self.use:
            if u != use:
                out.append(("use", (dep, proj, u, dist)))
        for d in self.dist:
            if d != dist:
                out.append(("dist", (dep, proj, use, d)))
        for x in self.dep_ids:
            if x != dep:
                out.append(("dep", (x, proj, use, dist)))
        for x in self.project_ids:
            if x != proj:
                out.append(("proj", (dep, x, use, dist)))
        return out

    def mixed_pair(self, dep, proj):
        return len({self.label(dep, proj, u, d) for u in self.use for d in self.dist}) >= 2


def fixture_table(seed="fixture"):
    """TEST-ONLY synthetic table with a deterministic mixture of labels (NOT licence knowledge)."""
    rng = util.rng_for("T63-lic-fixture", seed)
    cells = {}
    for dep, proj, use, dist in itertools.product(DEP_IDS, PROJECT_IDS, USE_IDS, DIST_IDS):
        x = rng.random()
        cells[key(dep, proj, use, dist)] = {"label": C.LIC_LABELS[0] if x < 0.4 else (C.LIC_LABELS[1] if x < 0.7 else C.LIC_LABELS[2]),
                                            "rationale": "fixture"}
    data = {"table_id": "T63-LIC-TABLE", "fixture": True, "dep_ids": list(DEP_IDS), "project_ids": list(PROJECT_IDS), "use": list(USE_IDS),
            "dist": list(DIST_IDS), "cells": cells}
    return LicTable(data)


def gold_label(spec, table):
    """SOLVER A: lookup of the four axes in the hashed table."""
    return table.label(spec["dep"], spec["project"], spec["use"], spec["dist"])


def m_cell_flag(table, cell):
    """M-CELL: high = a one-axis neighbour carries another label; low = only a two-axis neighbour does; None = far from any boundary."""
    lab = table.label(*cell)
    if any(table.label(*nb) != lab for _ax, nb in table.neighbours(cell)):
        return "high"
    for _ax, nb in table.neighbours(cell):
        if any(table.label(*nb2) != lab for _ax2, nb2 in table.neighbours(nb)):
            return "low"
    return None


class CellPicker(object):
    """Draws unused cells by label (and by pair constraints). Deterministic given the rng; `used` is the 'each cell once' ledger."""

    def __init__(self, table, rng):
        self.table, self.rng, self.used = table, rng, set()
        self._by_label = {lab: [] for lab in C.LIC_LABELS}
        for cell in table.all_keys():
            self._by_label[table.label(*cell)].append(cell)
        for lab in self._by_label:
            self._by_label[lab].sort()
            self.rng.shuffle(self._by_label[lab])
        self._ptr = {lab: 0 for lab in C.LIC_LABELS}
        self._flags, self._mixed = {}, {}                          # per-cell caches (the real table has 1,920 cells; an M-CELL scan is a nested neighbour walk)
        self.rows = {}                                             # row_id -> (group_id, cell, round): the rows built on a used cell (Opus ruling Q5: release a dropped row's cell)

    def register(self, row_id, group_id, cell, rnd=0):
        self.rows[row_id] = (group_id, cell, rnd)

    def release(self, cells):
        """Hand cells back (a builder error after the draw). Only cells that no registered row sits on."""
        held = {c for _g, c, _r in self.rows.values()}
        for c in cells:
            if c not in held:
                self.used.discard(c)

    def release_unkept(self, kept_row_ids, before_round):
        """Opus ruling Q5: a cell is 'used' by a row that enters the pool. Give back the cell of every row of an EARLIER refill round (round < `before_round`) that is not in
        `kept_row_ids` (answer-check drop, G13 hit, group retirement), so the one-use rule still holds and a refill can draw it again. Rows of the current round are pending
        (not stamped yet) and are never released. -> number of cells released."""
        gone = [rid for rid, (_g, _c, rnd) in self.rows.items() if rnd < before_round and rid not in kept_row_ids]
        for rid in gone:
            self.used.discard(self.rows.pop(rid)[1])
        return len(gone)

    def flag(self, cell):
        if cell not in self._flags:
            self._flags[cell] = m_cell_flag(self.table, cell)
        return self._flags[cell]

    def mixed(self, cell):
        key = (cell[0], cell[1])
        if key not in self._mixed:
            self._mixed[key] = self.table.mixed_pair(*key)
        return self._mixed[key]

    def single(self, label, want_mixed=None, flag="any"):
        """An unused cell of `label`; `flag` (None / 'low' / 'high') filters on M-CELL, 'any' does not."""
        lst = self._by_label[label]
        for _ in range(len(lst)):
            i = self._ptr[label] % len(lst)
            self._ptr[label] += 1
            cell = lst[i]
            if cell in self.used:
                continue
            if want_mixed is not None and self.mixed(cell) != want_mixed:
                continue
            if flag != "any" and self.flag(cell) != flag:
                continue
            self.used.add(cell)
            return cell
        raise Reject("no unused %s cell" % label)

    def pair(self, axis_kind):
        """Two unused cells differing in one axis with different labels. axis_kind: 'mode' (use / dist) or 'id' (dep / proj)."""
        axes = ("use", "dist") if axis_kind == "mode" else ("dep", "proj")
        order = list(C.LIC_LABELS)
        self.rng.shuffle(order)
        for lab in order:
            lst = self._by_label[lab]
            for _ in range(min(len(lst), 400)):
                cell = lst[self._ptr[lab] % len(lst)]
                self._ptr[lab] += 1
                if cell in self.used:
                    continue
                nbs = [nb for ax, nb in self.table.neighbours(cell) if ax in axes and nb not in self.used and self.table.label(*nb) != lab]
                if nbs:
                    other = self.rng.choice(sorted(nbs))
                    self.used.update((cell, other))
                    return cell, other
        raise Reject("no pair")


# ---- the downstream cut: drawn rows -> kept quota ------------------------------------------------------------------------------------
def _cut_key(seed, row_id):
    return util.sha256_text("T63-lic-cut|%s|%s" % (seed, row_id))


def cut_to_quota(rows, seed, quota=None, min_pair_rows=None):
    """Opus ruling Q5: cut the LIC rows that survived the drops (at most 44 / 44 / 40 cells were drawn) to the kept quota (38 / 38 / 34 of 110).
    Rule (nothing else is looked at): a label over its quota loses rows; SINGLES go first (a row with no partner in the batch counts as a single, an orphan too), in the
    order of sha256(seed | row_id); only when no single of an over-quota label is left, pair members go (their partner then counts as a single). A label under its quota
    loses nothing. No model score, no row text, no spec field, no label other than the quota decides: the only inputs are row_id, gold, pair_id and the seed.
    -> (kept_rows in input order, report). `report["pair_ok"]` is False when fewer than `min_pair_rows` (33 of 110: 30%) rows remain in complete pairs."""
    rows = list(rows)
    quota = dict(quota or C.LIC_ROWS)
    if min_pair_rows is None:
        min_pair_rows = int(math.ceil(C.LIC_PAIR_MIN * sum(quota.values()) - 1e-9))
    alive = {r["row_id"]: r for r in rows}
    cnt = collections.Counter(r["gold"] for r in rows)
    excess = {lab: max(0, cnt.get(lab, 0) - quota.get(lab, 0)) for lab in C.LIC_LABELS}
    pid_of = {r["row_id"]: r["meta"].get("pair_id") for r in rows}

    def paired(rid):
        pid = pid_of[rid]
        return bool(pid) and sum(1 for o in alive if pid_of[o] == pid) == 2

    dropped = []
    while any(excess.values()):
        over = {lab for lab, e in excess.items() if e > 0}
        cands = [rid for rid, r in alive.items() if r["gold"] in over and not paired(rid)] or [rid for rid, r in alive.items() if r["gold"] in over]
        victim = min(cands, key=lambda rid: _cut_key(seed, rid))
        excess[alive.pop(victim)["gold"]] -= 1
        dropped.append(victim)
    kept = [r for r in rows if r["row_id"] in alive]
    pair_rows = sum(1 for rid in alive if paired(rid))
    return kept, {"before": dict(cnt), "kept": dict(collections.Counter(r["gold"] for r in kept)), "dropped": dropped, "pair_rows": pair_rows,
                  "min_pair_rows": min_pair_rows, "pair_ok": pair_rows >= min_pair_rows}
