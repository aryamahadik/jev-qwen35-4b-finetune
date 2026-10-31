"""rc_repair: drop a few whole views or units so one family part passes mv_core's balance, missing-info and
artefact checks exactly (yn2b/SPEC.md 4.6 and 8.4: "45-55% yes in every stratum", |corr(gold, x)| < 0.05).

Generation balances the gold greedily, unit by unit; small strata (a joint stratum of 3-7 rows) can still end one row
off. This step removes the fewest rows that fix that: first single non-base views (JB, ladder, format, attack,
contrast, mirror rows; their relations go with them), and whole latent units only when no single view helps. It never
changes a label, never edits a row and never adds one ("nothing is padded to reach a count"). The metrics are the
exact mv_core definitions (balance_report, edge_report's missing-info share, artefact_corr), kept incrementally.
"""
from __future__ import annotations

import math
from collections import defaultdict

import mv_core as mv

DROPPABLE = ("jb", "ladder", "format", "contrast", "mirror")      # attack rows only go with their whole unit
ART_DIMS = {"yn": ("fmt", "tier", "polarity", "len_bin", "card_style"), "jb": ("fmt", "tier", "polarity", "len_bin")}


def _bal_keys(r) -> list:
    m = r["meta"]
    ks = [("joint",) + tuple(m.get(d) for d in mv.BALANCE_JOINT)]
    for d in mv.BALANCE_MARGINAL:
        ks.append((d, m.get(d)))
    tags = set((m["edge"] or "").split(","))
    if any(t.startswith("missing_info") for t in tags):
        ks.append(("missing_info",))
    return ks


class State:
    def __init__(self, rows):
        self.bal = defaultdict(lambda: [0, 0])
        self.art = {q: {"n": 0, "y": 0, "sx": 0.0, "sxx": 0.0, "sxy": 0.0, "cat": defaultdict(lambda: [0, 0])}
                    for q in ART_DIMS}
        self.plant = defaultdict(lambda: [0, 0])     # template (or "all") -> [for_gold, rows]
        self.spoof = [0, 0]
        self.spoof_fam = bool(rows) and rows[0]["key"] in mv.SPOOF_FAMILIES
        for r in rows:
            self.apply(r, +1)

    def apply(self, r, s: int):
        m = r["meta"]
        if m["view"] == "attack":
            fg = int(m["plant_dir"] == "for_gold")
            for k in ("all", m["plant_tpl"]):
                self.plant[k][0] += s * fg
                self.plant[k][1] += s
            self.spoof[0] += s * int(bool(m["plant_spoof"]))
            self.spoof[1] += s
        y = mv._yes(r)
        if y is None:
            return
        for k in _bal_keys(r):
            self.bal[k][0] += s * y
            self.bal[k][1] += s
        q = r["meta"]["qkind"]
        a = self.art[q]
        x = float(len(r["state"]))
        a["n"] += s
        a["y"] += s * y
        a["sx"] += s * x
        a["sxx"] += s * x * x
        a["sxy"] += s * x * y
        for d in ART_DIMS[q]:
            c = a["cat"][(d, str(r["meta"].get(d)))]
            c[0] += s * y
            c[1] += s
        if q == "yn":
            c = a["cat"][("card_presence", str(r["meta"]["card_style"] not in (None, "none")))]
            c[0] += s * y
            c[1] += s

    @staticmethod
    def _corr_bin(n, Y, nv, Yv) -> float:
        if n < 3 or nv in (0, n) or Y in (0, n):
            return 0.0
        cov = Yv / n - (nv / n) * (Y / n)
        return abs(cov / math.sqrt((nv / n) * (1 - nv / n) * (Y / n) * (1 - Y / n)))

    def objective(self) -> tuple:
        bad, excess = 0, 0.0
        for k, (y, n) in self.bal.items():
            if n and not mv.share_ok(y, n):
                bad += 1
                excess += abs(y - n / 2) - max(0.05 * n, 1.0)
        for k, (fg, n) in self.plant.items():
            if n and not mv.share_ok(fg, n):
                bad += 1
                excess += abs(fg - n / 2)
        if self.spoof_fam and self.spoof[1] and abs(self.spoof[0] - 0.25 * self.spoof[1]) > max(0.05 * self.spoof[1], 1):
            bad += 1
            excess += abs(self.spoof[0] - 0.25 * self.spoof[1])
        over = 0
        for q, a in self.art.items():
            n, Y = a["n"], a["y"]
            if n < 3:
                continue
            for (d, v), (yv, nv) in a["cat"].items():
                if nv <= 0:
                    continue
                c = self._corr_bin(n, Y, nv, yv)
                if d == "card_presence" and c >= 0.05:
                    over += 1
                    excess += c
                elif c >= 0.05:
                    over += 1
                    excess += c
            vx = n * a["sxx"] - a["sx"] ** 2
            vy = n * Y - Y * Y
            if vx > 0 and vy > 0:
                c = abs((n * a["sxy"] - a["sx"] * Y) / math.sqrt(vx * vy))
                if c >= 0.05:
                    over += 1
                    excess += c
        return bad + over, excess


def repair(rows: list[dict], rels: list[dict], max_iter: int = 600, protect=()) -> tuple[list, list, dict]:
    """Greedy: while the part fails, apply the removal (one view, else one unit) that lowers (failures, excess) the
    most. Returns (rows, rels, log). protect: latent ids never dropped as whole units."""
    rows = list(rows)
    by_lat = defaultdict(list)
    for r in rows:
        by_lat[r["meta"]["latent_id"]].append(r)
    st = State(rows)
    alive = {r["rid"] for r in rows}
    log = {"dropped_rows": 0, "dropped_units": 0, "start": st.objective(), "steps": []}
    jb = [r for r in rows if r["meta"]["qkind"] == "jb"]
    if 0 < len(jb) < 120:
        # a small JB set cannot reach |corr| < 0.05 with an odd split in any format: drop the surplus JB rows of
        # each format (the ones whose tier / length bin are most over-represented on their side)
        by_fmt = defaultdict(list)
        for r in jb:
            by_fmt[(r["meta"]["fmt"], r["meta"]["tier"], r["meta"]["len_bin"])].append(r)
        for f, rs in sorted(by_fmt.items()):
            ys = [r for r in rs if mv._yes(r)]
            ns = [r for r in rs if not mv._yes(r)]
            surplus = ys if len(ys) > len(ns) else ns
            k = abs(len(ys) - len(ns))
            for r in sorted(surplus, key=lambda r: (r["meta"]["tier"], r["meta"]["len_bin"], r["rid"]))[:k]:
                st.apply(r, -1)
                alive.discard(r["rid"])
                log["dropped_rows"] += 1
                log["steps"].append(("row", [r["rid"]]))
    for _ in range(max_iter):
        obj = st.objective()
        if obj[0] == 0:
            break
        # rows that sit in a failing balance stratum or a failing artefact category, on the surplus side
        bad_keys = {k: (y, n) for k, (y, n) in st.bal.items() if n and not mv.share_ok(y, n)}
        cands = []
        for r in rows:
            if r["rid"] not in alive:
                continue
            y = mv._yes(r)
            if y is None:
                continue
            hit = False
            for k in _bal_keys(r):
                if k in bad_keys:
                    yy, nn = bad_keys[k]
                    if (yy > nn / 2) == bool(y):
                        hit = True
                        break
            if not hit:
                q = r["meta"]["qkind"]
                a = st.art[q]
                if a["n"] >= 3:
                    for d in ART_DIMS[q]:
                        yv, nv = a["cat"][(d, str(r["meta"].get(d)))]
                        c = State._corr_bin(a["n"], a["y"], nv, yv)
                        if c >= 0.05 and ((yv / max(1, nv)) > (a["y"] / a["n"])) == bool(y):
                            hit = True
                            break
                    if not hit and q == "jb":
                        hit = True       # JB sets are small: any JB row may fix a length or category correlation
            if hit:
                cands.append(r)
        best = None
        seen_units = set()
        pair_acts = []
        jb_alive = [r for r in rows if r["rid"] in alive and r["meta"]["qkind"] == "jb"]
        if 0 < len(jb_alive) < 120:
            cells = defaultdict(lambda: ([], []))
            for r in jb_alive:
                cells[(r["meta"]["fmt"], r["meta"]["tier"], r["meta"]["len_bin"])][0 if mv._yes(r) else 1].append(r)
            for ys, ns in cells.values():
                if ys and ns:
                    ys = sorted(ys, key=lambda r: len(r["state"]))
                    ns = sorted(ns, key=lambda r: len(r["state"]))
                    pair_acts += [[ys[-1], ns[0]], [ys[0], ns[-1]]]
        for group in pair_acts:
            for x in group:
                st.apply(x, -1)
            o = st.objective()
            for x in group:
                st.apply(x, +1)
            if o[0] < obj[0] or (o[0] == obj[0] and o[1] < obj[1] - 1e-9):
                score = (o[0], o[1] + 0.3)
                if best is None or score < best[0]:
                    best = (score, "row", group)
        for r in cands:
            lid = r["meta"]["latent_id"]
            if r["meta"]["view"] in DROPPABLE:
                acts = [("row", [r])]
            else:
                acts = []
            if lid not in seen_units and lid not in protect:
                seen_units.add(lid)
                acts.append(("unit", [x for x in by_lat[lid] if x["rid"] in alive]))
            for kind, group in acts:
                for x in group:
                    st.apply(x, -1)
                o = st.objective()
                for x in group:
                    st.apply(x, +1)
                pen = (0, 0.15 * len(group) + (0.5 if kind == "unit" else 0.0))
                score = (o[0], o[1] + pen[1])
                if o[0] < obj[0] or (o[0] == obj[0] and o[1] < obj[1] - 1e-9):
                    if best is None or score < best[0]:
                        best = (score, kind, group)
        if best is None:
            break
        _, kind, group = best
        for x in group:
            st.apply(x, -1)
            alive.discard(x["rid"])
        log["dropped_rows" if kind == "row" else "dropped_units"] += 1
        log["steps"].append((kind, [x["rid"] for x in group]))
    rows = [r for r in rows if r["rid"] in alive]
    rels = [x for x in rels if x["a"] in alive and x["b"] in alive]
    log["end"] = st.objective()
    log["rows_dropped_total"] = sum(len(s[1]) for s in log["steps"])
    return rows, rels, log
