"""Quota planner: deficit-driven cell assignment so the family's balance gates hold BY CONSTRUCTION (the gates then verify).

Every categorical axis (head, language, step bin, label, gold letter, exception-gold, YES construction, mutator class,
hard-NO, pair kind) is assigned by "largest deficit against its target share first". Counts are updated from rows that
survive Solver A (drops therefore pull the planner back toward balance). No gate bar is relaxed here.
"""
import collections
import random

from LC_COMMON import transforms as T
from LC_COMMON import irmut

from . import config as C

HEAD_BIN_SHARE = {"OUT4": {"lt10": 0.30, "mid": 0.30, "gt40": 0.40},
                  "EQV2": {"lt10": 0.45, "mid": 0.55, "gt40": 0.0},
                  "TFAIL2": {"lt10": 0.30, "mid": 0.40, "gt40": 0.30}}
UNIT_ROW_SHARE = {"single": 0.68, "invariant": 0.18, "nearmiss": 0.14}


def option_feature_rows(spec):
    """[(is_gold, [overlap, is_exception, is_int, is_text_or_list])] for an OUT4 spec: the role-independent option features
    that the K6/K7 probes can learn from. Used by the gap balancer."""
    from .out4 import overlap_flag
    out = []
    ints = [o["obs"]["ok"] if ("ok" in o["obs"] and isinstance(o["obs"]["ok"], int) and not isinstance(o["obs"]["ok"], bool)) else None
            for o in spec["options"]]
    numeric = all(v is not None for v in ints)
    order = sorted(ints) if numeric else None
    mean = sum(ints) / float(len(ints)) if numeric else None
    nearest = min(range(len(ints)), key=lambda i: abs(ints[i] - mean)) if numeric else None
    for k, o in enumerate(spec["options"]):
        ob = o["obs"]
        isexc = "exc" in ob
        isint = (not isexc) and isinstance(ob["ok"], int) and not isinstance(ob["ok"], bool)
        # numeric-position cues (build-review fix 18 Oct): shifted-gold distractors sit on both sides of the gold, so "the gold is one
        # of the two middle values / the one nearest the mean" otherwise beat chance (gold was a middle value in ~66% of numeric rows)
        mid = float(numeric and order.index(ints[k]) in (1, 2))
        top = float(numeric and ints[k] == order[-1])
        near = float(numeric and k == nearest)
        out.append((o["kind"] == "GOLD", [float(overlap_flag(ob, spec.get("shown_src", ""))), float(isexc), float(isint),
                                          float((not isexc) and not isint), mid, top, near]))
    return out


class GapBalancer:
    """Keeps mean(feature | gold option) - mean(feature | distractor option) near zero for every tracked feature, by
    refusing rows that would widen a gap beyond `tau` (matched sampling; no model is involved)."""

    def __init__(self, nfeat=4, tau=0.03, warmup=40, max_rejects=12):
        self.rejects = 0
        self.max_rejects = max_rejects
        self.overrides = 0
        self.g = [0.0] * nfeat
        self.d = [0.0] * nfeat
        self.ng = self.nd = 0
        self.tau, self.warmup = tau, warmup

    def _gaps(self, g, d, ng, nd):
        return [(g[i] / ng - d[i] / nd) if ng and nd else 0.0 for i in range(len(g))]

    def _apply(self, rows, sign=1):
        g, d, ng, nd = list(self.g), list(self.d), self.ng, self.nd
        for is_gold, f in rows:
            for i, x in enumerate(f):
                if is_gold:
                    g[i] += sign * x
                else:
                    d[i] += sign * x
            if is_gold:
                ng += sign
            else:
                nd += sign
        return g, d, ng, nd

    def ok(self, rows):
        if self.ng < self.warmup:
            return True
        before = self._gaps(self.g, self.d, self.ng, self.nd)
        after = self._gaps(*self._apply(rows, 1))
        if all(abs(a) <= self.tau or abs(a) <= abs(b) for a, b in zip(after, before)):
            self.rejects = 0
            return True
        self.rejects += 1
        if self.rejects > self.max_rejects:          # never deadlock: accept, count the override, let the gates speak
            self.rejects = 0
            self.overrides += 1
            return True
        return False

    def add(self, rows, sign=1):
        self.g, self.d, self.ng, self.nd = self._apply(rows, sign)


def _pick_deficit2(rng, counts_a, counts_b, targets):
    """Like _pick_deficit but sums the deficits seen through two count contexts (for example language and step bin)."""
    ta, tb = sum(counts_a.values()) + 1, sum(counts_b.values()) + 1
    best, bv = [], None
    for k, share in targets.items():
        d = (share * ta - counts_a.get(k, 0)) + (share * tb - counts_b.get(k, 0))
        if bv is None or d > bv + 1e-9:
            best, bv = [k], d
        elif abs(d - bv) <= 1e-9:
            best.append(k)
    return rng.choice(best)


def cell_key(head, m):
    """Feature cell used to keep the label independent of the surface features the CPU probes look at (K5, K8, K9)."""
    if head == "EQV2":
        er = m["edit_ratio"]
        eb = 0 if er < 0.70 else 1 if er < 0.85 else 2 if er < 0.95 else 3
        cl = m["changed_lines"]
        cb = 0 if cl <= 1 else 1 if cl <= 3 else 2
        ad = abs(m["ast_nodes_a"] - m["ast_nodes_b"])
        ab = 0 if ad == 0 else 1 if ad <= 3 else 2
        return (eb, cb, ab)
    if head == "TFAIL2":
        return (bool(m.get("expected_in_source")), m.get("n_assert"), m["shown_chars"] // 500)
    return None


def _pick_deficit(rng, counts, targets, allowed=None):
    """argmax of (target_count - current): ties broken randomly. targets: {key: share}; counts: Counter."""
    total = sum(counts.values()) + 1
    best, bv = [], None
    for k, share in targets.items():
        if allowed is not None and k not in allowed:
            continue
        if share <= 0:
            continue
        d = share * total - counts.get(k, 0)
        if bv is None or d > bv + 1e-9:
            best, bv = [k], d
        elif abs(d - bv) <= 1e-9:
            best.append(k)
    return rng.choice(best)


class Planner:
    def __init__(self, seed=0, ts_ok=True):
        self.rng = random.Random("T42c-planner:%s" % seed)
        self.langs = dict(C.LANG_SHARE)
        if not ts_ok:
            self.langs["javascript"] += self.langs.pop("typescript")
        self.c = collections.defaultdict(collections.Counter)      # axis -> Counter
        self.bal = collections.defaultdict(collections.Counter)    # (head, feature cell) -> label Counter
        self.gap = GapBalancer(7)                                  # OUT4 option-feature gaps (gold vs distractors)
        self.next_seed = 0
        self.fails = collections.Counter()                         # consecutive generation failures per coarse cell signature
        self.starved = collections.Counter()                       # how often a signature was written off (reported, never silent)

    # ------------------------------------------------------------------ cells
    def unit(self):
        rng, c = self.rng, self.c
        head = _pick_deficit(rng, c["head"], C.HEAD_SHARE)
        lang = _pick_deficit(rng, c["lang:" + head], self.langs)
        utype = _pick_deficit(rng, c["unit"], UNIT_ROW_SHARE)
        cell = {"head": head, "lang": lang, "unit": utype, "seed": self.next_seed}
        self.next_seed += 1
        if head == "OUT4":
            cell["exc"] = _pick_deficit(rng, c["exc:" + lang], {True: C.OUT4_EXC_SHARE + 0.02, False: 1 - C.OUT4_EXC_SHARE - 0.02})
            cell["bin"] = _pick_deficit(rng, c["bin:OUT4"], HEAD_BIN_SHARE["OUT4"])
            cell["gold_pos"] = _pick_deficit(rng, c["letter"], {k: 0.25 for k in range(4)})
            cell["custom"] = bool(cell["exc"] and rng.random() < 0.15)
        elif head == "EQV2":
            cell["bin"] = _pick_deficit(rng, c["bin:EQV2"], HEAD_BIN_SHARE["EQV2"])
            cell["label"] = _pick_deficit2(rng, c["label:EQV2:" + lang], c["labelbin:EQV2:" + cell["bin"]], {"YES": 0.5, "NO": 0.5})
            cell["seq"] = rng.random() < 0.30
            if utype == "invariant":
                cell["label"] = "YES"                   # an invariant pair is two YES rows with different rewrites
            if cell["label"] == "YES":
                cell["eq"] = _pick_deficit(rng, c["eq"], {e: 1.0 / len(T.IDS) for e in T.IDS})
            else:
                cell["op"] = _pick_deficit(rng, c["op"], {o: 1.0 / len(irmut.ALL_OPS) for o in irmut.ALL_OPS})
                cell["hard"] = _pick_deficit(rng, c["hard"], {True: 0.25, False: 0.75})
                cell["restructured"] = rng.random() < 0.60
        else:
            cell["bin"] = _pick_deficit(rng, c["bin:TFAIL2"], HEAD_BIN_SHARE["TFAIL2"])
            cell["label"] = _pick_deficit2(rng, c["label:TFAIL2:" + lang], c["labelbin:TFAIL2:" + cell["bin"]], {"FAIL": 0.5, "PASS": 0.5})
            if utype == "nearmiss":
                cell["label"] = "PASS"                  # the partner (a mutant under the same test) flips to FAIL
            cell["shape"] = _pick_deficit(rng, c["shape"], {"value": 0.25, "exception": 0.2, "multi": 0.3, "sequence": 0.25})
            cell["fail_mode"] = rng.choice(["expected", "program"])
            cell["n_assert"] = _pick_deficit(rng, c["nassert"], {1: 0.25, 2: 0.3, 3: 0.25, 4: 0.2})
        return cell

    # ------------------------------------------------------------------ liveness (build-review fix 18 Oct)
    STARVE_AFTER = 30

    @staticmethod
    def _sig(cell):
        return (cell["head"], cell["lang"], cell.get("exc"), cell.get("bin"), cell.get("label"), cell.get("hard"))

    def note_result(self, cell, ok):
        """The deficit-driven planner picks the largest deficit first, so a cell the generator can (almost) never fill is picked
        again and again and the build stalls. After STARVE_AFTER consecutive failures of one coarse signature the planner books
        one PHANTOM unit on that cell's axes (its deficit shrinks, the build moves on) and counts it in `starved`; the quota gates
        still judge the real rows, so the shortfall shows up there instead of as a hang."""
        sig = self._sig(cell)
        if ok:
            self.fails[sig] = 0
            return
        self.fails[sig] += 1
        if self.fails[sig] < self.STARVE_AFTER:
            return
        self.fails[sig] = 0
        self.starved[sig] += 1
        h, lang, c = cell["head"], cell["lang"], self.c
        if h == "OUT4":
            c["bin:OUT4"][cell["bin"]] += 1
            c["exc:" + lang][cell["exc"]] += 1
        else:
            lab = cell["label"]
            c["bin:" + h][cell["bin"]] += 1
            c["label:%s:%s" % (h, lang)][lab] += 1
            c["labelbin:%s:%s" % (h, cell["bin"])][lab] += 1
            if h == "EQV2" and lab == "NO":
                c["hard"][cell["hard"]] += 1
                c["op"][cell["op"]] += 1
            elif h == "EQV2":
                c["eq"][cell["eq"]] += 1
        c["unit"][cell["unit"]] += 1

    # ------------------------------------------------------------------ bookkeeping (in-flight specs, then corrections)
    @staticmethod
    def facts_from_spec(spec):
        m = spec["meta"]
        f = {"head": spec["head"], "lang": spec["lang"], "pair_kind": m.get("pair_kind"), "bin": spec.get("bin_ir"),
             "perm": False, "exc": bool(m.get("exc_gold")), "letter": spec.get("gold_index"),
             "label": spec.get("gold_label"), "construction": m.get("construction"), "op": m.get("mutator_op"),
             "hard": bool(m.get("hard_no")), "shape": m.get("shape"), "n_assert": m.get("n_assert"),
             "cell": cell_key(spec["head"], m) if spec["head"] in ("EQV2", "TFAIL2") else None}
        return f

    @staticmethod
    def facts_from_row(row):
        m = row["meta"]
        lab = row["label"]
        f = {"head": row["head"], "lang": row["lang"], "pair_kind": m.get("pair_kind"), "bin": m.get("trace_bin"),
             "perm": bool(m.get("perm_copy")), "exc": bool(m.get("exc_gold")),
             "letter": "ABCD".index(lab) if row["head"] == "OUT4" else None,
             "label": (lab if row["head"] == "EQV2" else ("FAIL" if lab == "YES" else "PASS") if row["head"] == "TFAIL2" else None),
             "construction": m.get("construction"), "op": m.get("mutator_op"), "hard": bool(m.get("hard_no")),
             "shape": m.get("shape"), "n_assert": m.get("n_assert"),
             "cell": cell_key(row["head"], m) if row["head"] in ("EQV2", "TFAIL2") else None}
        return f

    def bal_ok(self, spec, tol=1):
        """Reject a candidate whose label is already `tol` ahead of the other label inside its feature cell (EQV2, TFAIL2),
        or that would widen the gold-vs-distractor feature gap (OUT4)."""
        if spec["head"] == "OUT4":
            return self.gap.ok(option_feature_rows(spec))
        f = self.facts_from_spec(spec)
        if f["cell"] is None:
            return True
        cnt = self.bal[(f["head"], f["cell"])]
        other = sum(v for k, v in cnt.items() if k != f["label"])
        return cnt.get(f["label"], 0) <= other + tol

    def add(self, f, sign=1):
        c = self.c
        h, lang = f["head"], f["lang"]
        c["head"][h] += sign
        c["lang:" + h][lang] += sign
        c["unit"][f["pair_kind"] or "single"] += sign
        if f["bin"]:
            c["bin:" + h][f["bin"]] += sign
        if h == "OUT4":
            c["exc:" + lang][f["exc"]] += sign
            if not f["perm"] and f["letter"] is not None:
                c["letter"][f["letter"]] += sign
        else:
            c["label:%s:%s" % (h, lang)][f["label"]] += sign
            if f["bin"]:
                c["labelbin:%s:%s" % (h, f["bin"])][f["label"]] += sign
            if f["cell"] is not None:
                self.bal[(h, f["cell"])][f["label"]] += sign
        if h == "EQV2":
            if f["label"] == "YES" and f["construction"]:
                c["eq"][f["construction"]] += sign
            if f["label"] == "NO":
                c["op"][f["op"]] += sign
                c["hard"][f["hard"]] += sign
        if h == "TFAIL2":
            c["shape"][f["shape"]] += sign
            c["nassert"][f["n_assert"]] += sign

    def reserve(self, specs):
        for s in specs:
            self.add(self.facts_from_spec(s), +1)
            if s["head"] == "OUT4":
                self.gap.add(option_feature_rows(s), +1)

    def settle(self, specs, rows):
        """After Solver A: release specs that produced no row; correct rows whose final facts differ from the plan."""
        by_id = {r["row_id"]: r for r in rows}
        for s in specs:
            r = by_id.get(s["row_id"])
            fs = self.facts_from_spec(s)
            if r is None:
                self.add(fs, -1)
                if s["head"] == "OUT4":
                    self.gap.add(option_feature_rows(s), -1)
                continue
            fr = self.facts_from_row(r)
            if fr != fs:
                self.add(fs, -1)
                self.add(fr, +1)
