"""T56g build orchestration (CPU / dry-run side): plan -> tasks -> row specs (hack / honest, normal / contradicting-spec,
pairs) -> Solver A -> rows (+ with-outputs and swapped-hunk copies). Natural-slice intake lives in natural.py.
Never writes rows to disk."""
import collections
import random

from LC_COMMON.plan_utils import GapBalancer, pick_deficit
from T57 import task as T57

from . import config as C
from . import hacks as HK
from . import rows as ROWS
from . import task as TK
from .base import Skip, mk_rng
from .solver_a import SolverA
from T57.base import diff_text, files_of


class Planner:
    def __init__(self, seed=0, ts_ok=True):
        self.rng = random.Random("T56g-planner:%s" % seed)
        self.langs = dict(C.LANG_SHARE)
        if not ts_ok:
            self.langs["javascript"] += self.langs.pop("typescript")
        self.c = collections.defaultdict(collections.Counter)
        self.bal = collections.defaultdict(collections.Counter)      # diff-size cell -> label counter
        self.gap = GapBalancer(6, tau=0.01, warmup=30, max_rejects=40)                # HACK-vs-honest mean gaps of the K5 / K6 length features
        self.n = 0

    @staticmethod
    def gap_rows(specs):
        out = []
        for s in specs:
            d = s["diff"]
            ch, ln = len(d), d.count("\n") + 1
            out.append((s["expect_label"] == "HACK", [min(ch, 1500) / 1500.0, min(ln, 60) / 60.0, min(s["diff_meta"]["hunks"], 4) / 4.0,
                                                     min(ch / ln, 60.0) / 60.0, 1.0 if s.get("extra_file") else 0.0, min(len(s["changed_paths"]), 4) / 4.0]))
        return out

    def seed(self):
        self.n += 1
        return self.n

    @staticmethod
    def cell(spec):
        m = spec["diff_meta"]
        return min(len(spec["diff"]) // 500, 3)

    def bal_ok(self, spec, tol=8):
        cnt = self.bal[self.cell(spec)]
        lab = spec["expect_label"]
        other = sum(v for k, v in cnt.items() if k != lab)
        return cnt.get(lab, 0) <= other * 1.3 + tol

    def add(self, spec, sign=1):
        c = self.c
        self.bal[self.cell(spec)][spec["expect_label"]] += sign
        c["tx:" + spec["expect_label"]]["tt" if spec.get("extra_file") else ("tf" if spec.get("touches") else "ff")] += sign
        c["lang"][spec["g"]["lang"]] += sign
        c["label"][spec["expect_label"]] += sign
        c["sub"][spec["subtype"]] += sign
        c["contra"][bool(spec["g"].get("contra"))] += sign
        c["card"][spec["card"]] += sign
        c["pair"][bool(spec.get("pair_id"))] += sign
        if spec.get("family"):
            c["family"][spec["family"]] += sign
            c["fam_lang:%s" % spec["g"]["lang"]][spec["family"]] += sign
        c["cm"][bool(spec.get("comment_line"))] += sign
        if spec.get("comment_line"):
            c["cmk"][spec.get("comment_kind")] += sign
        c["xt"][bool(spec.get("extra_file"))] += sign


def honest_cands(g, rng):
    cands = T57.build_candidates(g, rng)
    out = []
    for c in cands:
        v, h = TK.effect_for_ir(g, c["lo"])
        out.append((c, v, h))
    return out


def _want_extra(rng, planner, expect, already, family):
    """K6 metadata balance: the 'touches a test directory' flag and the 'adds a new test file' flag follow ONE joint target for both
    labels (a new unprotected test file always counts as touching a test directory)."""
    if family == 6:
        return False
    if already:                                     # the label never shows through 'touches tests without a new test file'
        return True
    return pick_deficit(rng, planner.c["tx:" + expect], {"tt": 0.62, "ff": 0.38}) == "tt"


def make_spec(g, subtype, family, card, rng, picker, planner, pair_id=None, target_chars=None, extra_plan=None):
    lang = g["lang"]
    pre_extra = None
    base = TK.base_tree(g)
    if subtype == "HACK":
        h = HK.build_hack(g, family, rng)
        tree, effect, info = h["tree"], h["effect"], h["info"]
        expect = "HACK"
    else:
        pool = honest_cands(g, rng)
        if subtype == "HONEST-PASSING":
            sel = [c for c, v, hh in pool if v and hh and c["cls"] == "CORRECT"]
        elif subtype == "HONEST-SPECFOLLOW":
            sel = [c for c, v, hh in pool if (not v) and hh and c["cls"] == "CORRECT"]
        else:                                                    # HONEST-NOTYET: an honest attempt whose visible tests still fail
            sel = [c for c, v, hh in pool if not v and c["cls"] != "CORRECT"]
        if not sel:
            raise Skip("no honest candidate for %s" % subtype)
        pre_extra = None                                    # decided before selection so the size match sees the extra file
        if target_chars is not None:                       # size-matched to the paired hack (K5 / K6 length cues): chars AND lines
            already0 = any(TK.is_test_path(p, lang) for cd in sel[:1] for p in cd["files"])
            want_extra = _want_extra(rng, planner, "NO-HACK", already0, family) if extra_plan is None else bool(extra_plan)
            xseed = rng.random()
            tag = "x%s" % rng.randint(0, 10 ** 6)

            def tree_for(cd):
                tr = dict(base)
                tr.update(cd["files"])
                ex = None
                if want_extra:
                    tr, ex = TK.with_extra(g, tr, random.Random(xseed), tag, 1.0)
                return tr, ex

            def size(cd):
                dt = diff_text(base, tree_for(cd)[0])[0]
                return len(dt), dt.count("\n")
            tc, tl = target_chars if isinstance(target_chars, tuple) else (target_chars, None)

            def dist(cd):
                s = size(cd)
                return abs(s[0] - tc) / max(tc, 1) + (abs(s[1] - tl) / max(tl, 1) if tl else 0.0) + rng.random() * 0.08
            sel.sort(key=dist)
            c = sel[0]
            tree, pre_extra = tree_for(c)
            pre_extra = (pre_extra, want_extra)
        else:
            c = rng.choice(sel)
            tree = dict(base)
            tree.update(c["files"])
        effect = {"visible": TK.effect_for_ir(g, c["lo"])[0], "heldout": TK.effect_for_ir(g, c["lo"])[1]}
        info = {"cand": c["kind"]}
        expect = "NO-HACK"
        family = None
    extra = None
    already = any(TK.is_test_path(p, lang) and tree.get(p) != base.get(p) for p in set(tree) | set(base))
    if subtype != "HACK" and pre_extra is not None:
        extra = pre_extra[0]
    elif family != 6:
        if (_want_extra(rng, planner, expect, already, family) if extra_plan is None else (bool(extra_plan) or already)):
            tree, extra = TK.with_extra(g, tree, rng, "x%s" % rng.randint(0, 10 ** 6), 1.0)
    comment_line = None
    ctext = ckind = None
    present = pick_deficit(rng, planner.c["cm"], {True: 0.3, False: 0.7})
    if present:
        ckind = pick_deficit(rng, planner.c["cmk"], {"fixed": 0.5, "neutral": 0.5})
        _, ctext = ROWS.comment_text(picker, ckind, g["bug_fn"])
    d, tree2, comment_line, dmeta = ROWS.diff_of(g, tree, ctext)
    changed = sorted(set(p for p in tree2 if tree2.get(p) != base.get(p)) | (set(base) - set(tree2)))
    touches = any(TK.is_test_path(p, lang) for p in changed)
    return {"g": g, "touches": touches, "row_type": "LIB-CONTRA" if g.get("contra") else "LIB-NORMAL", "subtype": subtype, "family": family,
            "card": card, "tree": tree2, "effect": effect, "expect_label": expect, "diff": d, "diff_meta": dmeta,
            "changed_paths": changed, "protected": TK.protected_paths(g, card), "comment_line": comment_line,
            "comment_kind": ckind, "pair_id": pair_id, "extra_file": extra, "info": info}


def make_spec_from_tree(g, subtype, tree, effect, card, picker, planner, rng, pair_id=None):
    """Spec from an already authored patched tree (natural slice intake)."""
    base = TK.base_tree(g)
    present = pick_deficit(rng, planner.c["cm"], {True: 0.3, False: 0.7}) if planner else False
    ctext = ckind = None
    d, tree2, comment_line, dmeta = ROWS.diff_of(g, tree, None)
    changed = sorted(set(p for p in tree2 if tree2.get(p) != base.get(p)) | (set(base) - set(tree2)))
    return {"g": g, "touches": any(TK.is_test_path(p, g["lang"]) for p in changed), "row_type": "NATURAL", "subtype": subtype, "family": None, "card": card, "tree": tree2, "effect": effect,
            "expect_label": "HACK" if subtype.endswith("HACK") else "NO-HACK", "diff": d, "diff_meta": dmeta, "changed_paths": changed,
            "protected": TK.protected_paths(g, card), "comment_line": comment_line, "comment_kind": ckind, "pair_id": pair_id,
            "extra_file": None, "info": {}}


def make_units(planner, picker, rng, skips):
    lang = pick_deficit(rng, planner.c["lang"], planner.langs)
    contra = bool(pick_deficit(rng, planner.c["contra"], {True: 0.10, False: 0.90}))
    seed = planner.seed()
    try:
        gs = TK.make_g_tasks(seed, lang, n_bugs=2, contra=contra, size=rng.choice([1, 2, 3]))
    except Skip as e:
        skips["task:" + str(e)[:40]] += 1
        return []
    specs = []
    for g in gs:
        card = pick_deficit(rng, planner.c["card"], {k: 0.5 for k in C.CARD_KINDS})
        paired = bool(pick_deficit(rng, planner.c["pair"], {True: 0.6, False: 0.4}))
        pid = "p%s" % g["uid"] if paired else None
        fams = [f for f in range(1, 9) if HK.applicable(g, f)]
        if not fams:
            skips["nofamily"] += 1
            continue
        fam = pick_deficit(rng, planner.c["family"], {f: 1.0 / 8 for f in fams})
        try:
            hk = make_spec(g, "HACK", fam, card, rng, picker, planner, pid)
        except Skip as e:
            skips["hack:" + str(e)[:40]] += 1
            continue
        if g.get("contra"):
            sub = "HONEST-SPECFOLLOW"
        else:
            sub = pick_deficit(rng, planner.c["sub"], {"HONEST-PASSING": 0.83, "HONEST-NOTYET": 0.17})
        out = [hk]
        try:
            out.append(make_spec(g, sub, None, card, rng, picker, planner, pid, target_chars=(hk["diff_meta"].get("chars_hint") or len(hk["diff"]), hk["diff"].count("\n")),
                                  extra_plan=bool(hk.get("extra_file"))))
        except Skip as e:
            skips["honest:" + str(e)[:40]] += 1
            continue                                      # a hack without its honest twin would unbalance the labels
        for s in out:
            s["pair_id"] = pid or "p%s" % g["uid"]
        ha, hb = len(out[0]["diff"]), len(out[1]["diff"])
        la, lb = out[0]["diff"].count("\n"), out[1]["diff"].count("\n")
        if not (0.82 <= hb / max(ha, 1) <= 1.22) or abs(la - lb) > max(3, 0.15 * max(la, lb)):
            skips["pair size mismatch"] += 1                  # K5 / K6: the two members of a pair stay length-matched
            continue
        if not planner.gap.ok(planner.gap_rows(out)):
            skips["pair length-gap balance"] += 1
            continue
        if not all(planner.bal_ok(s) for s in out):
            skips["balance cell full"] += 1
            continue
        planner.gap.add(planner.gap_rows(out), +1)
        for s in out:
            planner.add(s, +1)
            s["_reserved"] = True
        specs += out
    final = []
    for s in specs:
        final.append(s)
        if rng.random() < C.WITH_OUTPUTS_COPIES:
            final.append(dict(s, with_outputs=True, _reserved=False))
        if rng.random() < C.SWAPPED_HUNK_COPIES:
            sw = ROWS.swap_hunks(s["diff"])
            if sw is not None:
                final.append(dict(s, diff=sw, swapped=True, _reserved=False))
    return final


def build_rows(n_target, executor, picker, seed=0, ts_ok=True, max_units=4000, checker=None):
    planner = Planner(seed, ts_ok)
    rng = random.Random("T56g-build:%s" % seed)
    solver = SolverA(executor, picker, checker)
    rows, skips, n_id, units = [], collections.Counter(), 0, 0
    prim = lambda rs: [r for r in rs if r["meta"]["variant"] == "primary"]
    while len(prim(rows)) < n_target and units < max_units:
        units += 1
        specs = make_units(planner, picker, rng, skips)
        for s in specs:
            s["row_id"] = "T56g-%06d" % n_id
            n_id += 1
        new = solver.run(specs)
        kept = {r["row_id"] for r in new}
        for s in specs:
            if s.get("_reserved") and s["row_id"] not in kept:
                planner.add(s, -1)
                planner.gap.add(planner.gap_rows([s]), -1)
        rows += new
    return rows, solver.stats, skips
