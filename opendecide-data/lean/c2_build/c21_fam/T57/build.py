"""T57 build orchestration (CPU / dry-run side): plan units -> tasks -> row specs -> Solver A -> rows (+ copies).

Units: an 'A' unit is one base module with up to 3 injected bugs and yields VERDICT / BEST4 / LOCALISE rows (reuse limits: <= 4
rows per module per head, <= 8 per module overall). A 'T' unit is a TESTSEL-only module (Opus C1). Copies: rename twins
(10% of rows), with-outputs variants (+25%), option-order copies (+20% for option heads), reason head rows (<= 25% of the
INCORRECT specs, outside the family size). This module never writes rows to disk.
"""
import collections
import copy
import random

from LC_COMMON import ir as I
from LC_COMMON import transforms as T
from LC_COMMON.plan_utils import GapBalancer, pick_deficit, pick_deficit2

from . import config as C
from . import heads as H
from . import rows as ROWS
from . import task as TK
from .base import Skip, mk_rng
from .solver_a import SolverA


class Planner:
    def __init__(self, seed=0, ts_ok=True):
        self.rng = random.Random("T57-planner:%s" % seed)
        self.langs = dict(C.LANG_SHARE)
        if not ts_ok:
            self.langs["javascript"] += self.langs.pop("typescript")
        self.c = collections.defaultdict(collections.Counter)
        self.bal = collections.defaultdict(collections.Counter)      # VERDICT style cell -> label counter
        self.gap = GapBalancer(10, tau=0.15, warmup=30, max_rejects=6)                          # BEST4 gold-vs-distractor style gaps
        self.rmem = collections.defaultdict(list)
        self.vmem = {"CORRECT": [], "INCORRECT": []}
        self.rgap = {r: GapBalancer(9, tau=0.12, warmup=30, max_rejects=12) for r in C.REASON_MIX}   # K7: reason vs the other reasons (INCORRECT rows)
        self.vgap = GapBalancer(9, tau=0.10, warmup=30, max_rejects=12)   # VERDICT correct-vs-incorrect style gaps
        self.lgap = GapBalancer(3, tau=0.08)                         # LOCALISE gold-vs-distractor option-flag gaps
        self.n = 0

    @staticmethod
    def v_cell(spec):
        c = spec["cands"][0]
        return (min(c["changed"], 5) // 2, min(c["hunks"], 2), min(c["n_files"], 2))

    @staticmethod
    def b_rows(spec):
        """BEST4 option style vectors in units of (about) one standard deviation (gold = the correct option)."""
        out = []
        meds = ROWS.medoid_feature(spec["cands"])
        for k, c in enumerate(spec["cands"]):
            s = ROWS.style_feats(c)
            out.append((k == spec["gold_index"], [min(s["chars"], 900) / 150.0, min(s["lines"], 40) / 3.5, min(s["added"], 14) / 1.5,
                                                  min(s["removed"], 14) / 1.0, min(s["hunks"], 4) / 0.5, min(s["files"], 3) / 0.5,
                                                  min(s["n_idents"], 40) / 6.0, min(s["mean_ident_len"], 12) / 2.0, float(bool(c.get("comment"))) / 0.45,
                                                  meds[k] / 0.115]))
        return out

    @staticmethod
    def l_rows(spec):
        return [(k == spec["gold_index"], [float(spec["opt_flags"][n]["traversed"]), float(spec["opt_flags"][n]["same_file"]),
                                           min(len(n), 24) / 24.0]) for k, n in enumerate(spec["options"])]

    def bal_ok(self, spec, tol=8):
        if spec["head"] == "LOCALISE":
            return self.lgap.ok(self.l_rows(spec))
        if spec["head"] == "VERDICT":
            cnt = self.bal[self.v_cell(spec)]
            lab = spec["label_exp"]
            other = sum(v for k, v in cnt.items() if k != lab)
            return cnt.get(lab, 0) <= other * 1.3 + tol
        if spec["head"] == "BEST4":
            return self.gap.ok(self.b_rows(spec))
        return True

    def unit_ok(self, unit):
        """VERDICT rows are judged on the whole unit by the mean-gap balancer over the shown patch's style vector (a near-miss pair is
        one CORRECT plus one INCORRECT row, so it cannot widen a gap by itself); the other heads keep their per-spec gap checks."""
        vr = [r for s in unit if s["head"] == "VERDICT" for r in self.v_rows(s)]
        if vr and not self.vgap.ok(vr):
            return False
        for r in self.rgap:
            rr = self.r_rows(unit, r)
            if rr and not self.rgap[r].ok(rr):
                return False
        return all(self.bal_ok(s) for s in unit if s["head"] != "VERDICT")

    @staticmethod
    def v_rows(spec):
        """Style vector in units of (about) one standard deviation, so the balancer's tau is a fraction of a standard deviation."""
        c = spec["cands"][0]
        s = ROWS.style_feats(c)
        return [(spec["label_exp"] == "CORRECT",
                 [min(s["chars"], 900) / 150.0, min(s["lines"], 40) / 3.5, min(s["added"], 14) / 1.5, min(s["removed"], 14) / 1.0,
                  min(s["hunks"], 4) / 0.5, min(s["n_idents"], 40) / 6.0, min(s["mean_ident_len"], 12) / 2.0, min(s["digits"], 20) / 2.5,
                  float(bool(c.get("comment"))) / 0.45])]

    def r_rows(self, specs, reason):
        out = []
        for s in specs:
            if s["head"] == "VERDICT" and s["label_exp"] == "INCORRECT":
                out += [(s["reason_exp"] == reason, f) for _, f in self.v_rows(s)]
        return out

    def rscore(self, specs):
        tot = 0.0
        for r, g in self.rgap.items():
            rr = self.r_rows(specs, r)
            if rr:
                tot += sum(abs(x) for x in g._gaps(*g._apply(rr, 1)))
        return tot

    def bscore(self, spec):
        rows = self.b_rows(spec)
        return sum(abs(x) for x in self.gap._gaps(*self.gap._apply(rows, 1)))

    def vscore(self, specs):
        """Sum of the absolute CORRECT-vs-INCORRECT style gaps (std units) the specs would leave behind (lower is better)."""
        rows = [r for s in specs for r in self.v_rows(s)]
        return sum(abs(x) for x in self.vgap._gaps(*self.vgap._apply(rows, 1)))

    def ref_vec(self, label, rng):
        """Style vector of a random already-planned VERDICT row of the OTHER label (None while the memory is small)."""
        mem = self.vmem["INCORRECT" if label == "CORRECT" else "CORRECT"]
        return rng.choice(mem) if len(mem) >= 12 else None

    def ref_reason(self, reason, rng):
        """Style vector of an already-planned INCORRECT row of a DIFFERENT reason (K7: the reason must not show in the style)."""
        mem = [v for k, m in self.rmem.items() if k != reason for v in m]
        return rng.choice(mem) if len(mem) >= 12 else None

    def lang(self):
        return pick_deficit(self.rng, self.c["lang"], self.langs)

    def unit_kind(self):
        frac = {h: self.c["head"][h] / float(C.HEAD_ROWS[h]) for h in C.HEADS}
        if frac["TESTSEL"] + 0.02 < min(frac["VERDICT"], frac["BEST4"]):
            return "T"
        if frac["LOCALISE"] + 0.02 < max(frac["VERDICT"], frac["BEST4"]):
            return "L"
        return "A"

    def seed(self):
        self.n += 1
        return self.n

    def add_spec(self, spec, sign=1):
        c = self.c
        h = spec["head"]
        if h == "VERDICT":
            self.bal[self.v_cell(spec)][spec["label_exp"]] += sign
            self.vgap.add(self.v_rows(spec), sign)
            for r in self.rgap:
                self.rgap[r].add(self.r_rows([spec], r), sign)
            vec = H._vec(spec["cands"][0])
            mem = self.vmem[spec["label_exp"]]
            rm = self.rmem[spec["reason_exp"]] if spec["reason_exp"] else None
            if sign > 0:
                mem.append(vec)
                del mem[:-300]
                if rm is not None:
                    rm.append(vec)
                    del rm[:-200]
            else:
                if vec in mem:
                    mem.remove(vec)
                if rm is not None and vec in rm:
                    rm.remove(vec)
        if h == "BEST4":
            self.gap.add(self.b_rows(spec), sign)
        if h == "LOCALISE":
            self.lgap.add(self.l_rows(spec), sign)
        c["head"][h] += sign
        c["lang"][spec["task"]["lang"]] += sign
        c["lang:" + h][spec["task"]["lang"]] += sign
        if h == "VERDICT":
            c["label"][spec["label_exp"]] += sign
            if spec["reason_exp"]:
                c["reason"][spec["reason_exp"]] += sign
        else:
            c["letter:" + h][spec["gold_index"]] += sign
        if h == "BEST4":
            c["altfix"][bool(spec.get("altfix"))] += sign
        c["pair"][spec.get("pair_kind") or "single"] += sign
        for cd in spec["cands"]:
            grp = "CORRECT" if cd["cls"] == "CORRECT" else "INCORRECT"
            c["cm:%s:%s" % (h, grp)][bool(cd.get("comment"))] += sign
            if cd.get("comment"):
                c["cmk:%s:%s" % (h, grp)][cd.get("comment_kind")] += sign
        if spec.get("twin_of"):
            c["twin"][True] += sign


def decorate(spec, planner, rng, picker):
    """Comments on the shown patches: presence ~30% in BOTH classes (deficit-balanced), kind fixed/neutral independent of the
    class, so a comment tells nothing; INCORRECT patches that carry a 'fixed' claim are the decoys (~15% of INCORRECT)."""
    task = spec["task"]
    new = []
    for cd in spec["cands"]:
        grp = "CORRECT" if cd["cls"] == "CORRECT" else "INCORRECT"
        present = pick_deficit(rng, planner.c["cm:%s:%s" % (spec["head"], grp)], {True: C.COMMENT_RATE, False: 1 - C.COMMENT_RATE})
        if present:
            kind = pick_deficit(rng, planner.c["cmk:%s:%s" % (spec["head"], grp)], {"fixed": 0.5, "neutral": 0.5})
            wid, text = ROWS.comment_text(picker, kind, task["bug_fn"])
            cd = ROWS.with_comment(task, cd, text, task["lang"])
            cd["comment_kind"] = kind
            cd["comment_wording"] = wid
            cd["decoy"] = kind == "fixed" and grp == "INCORRECT"
        new.append(cd)
    spec["cands"] = new
    return spec


def twin_of_spec(spec, rng):
    """Rename twin: locals of the bug function renamed (EQ-YES-1) in the buggy module and in every shown patch; same gold."""
    task = spec["task"]
    ids, lang = task["ids"], task["lang"]
    fn = task["bug_fn"]
    nb = T.apply(task["buggy"], fn, "EQ-YES-1", rng, ids, "twin")
    if nb is None:
        return None
    try:
        b_lo = TK.lower(nb, lang, ids)
    except Skip:
        return None
    t2 = dict(task)
    t2.update({"uid": task["uid"] + ".tw", "buggy": nb, "buggy_lo": b_lo, "cands": None, "_tf": task.get("_tf")})
    cands = []
    for cd in spec["cands"]:
        nbase = T.apply(cd["base"], fn, "EQ-YES-1", rng, ids, "twin") or cd["base"]
        c2 = TK._cand(t2, cd["kind"], nbase, rng, cd.get("info"))
        if c2 is None:
            return None
        c2["cls"] = cd["cls"]
        cands.append(c2)
    new = dict(spec)
    new.update({"task": t2, "cands": cands, "twin_of": task["uid"], "pair_id": None, "pair_kind": None})
    return new


def verdict_plan(planner, rng, room_left):
    """(unit type, label) for the next VERDICT unit. The CORRECT / INCORRECT balance is controlled here because pairs add
    labels two at a time (an altfix pair is two CORRECT rows, a near-miss pair one of each)."""
    diff = planner.c["label"]["CORRECT"] - planner.c["label"]["INCORRECT"]
    if diff > 3:
        return "single", "INCORRECT"
    if diff < -3:
        return ("altfix", None) if (room_left >= 2 and rng.random() < 0.4) else ("single", "CORRECT")
    u = pick_deficit(rng, planner.c["pair"], {"single": 0.33, "nearmiss": 0.45, "altfix": 0.22})
    if u == "altfix" and room_left < 2:
        u = "single"
    if u == "nearmiss" and room_left < 2:
        u = "single"
    if u == "single":
        return "single", pick_deficit(rng, planner.c["label"], {"CORRECT": 0.5, "INCORRECT": 0.5})
    return u, None


def derive_rows_a(tasks, planner, rng, picker, caps):
    """Row specs from the tasks of one 'A' / 'L' unit, following the deficits and the per-module reuse caps. Returns a list of
    UNITS (a unit = [spec] or a pair [spec, spec]); decoration and balancing happen per unit afterwards."""
    units = []
    used = collections.Counter()

    def room(head):
        return used[head] < C.REUSE_PER_MODULE_PER_HEAD and sum(used.values()) < C.REUSE_PER_MODULE

    for task in tasks:
        cands = TK.build_candidates(task, rng)
        if not [c for c in cands if c["cls"] == "CORRECT"]:
            continue
        if not task["multi"] and room("LOCALISE") and caps.get("LOCALISE", 1) > 0:
            try:
                gp = pick_deficit(rng, planner.c["letter:LOCALISE"], {k: 0.25 for k in range(4)})
                units.append([H.localise_spec(task, rng, gp)])
                used["LOCALISE"] += 1
            except Skip:
                pass
        if room("BEST4") and caps.get("BEST4", 1) > 0:
            try:
                gp = pick_deficit(rng, planner.c["letter:BEST4"], {k: 0.25 for k in range(4)})
                alt = pick_deficit(rng, planner.c["altfix"], {True: 0.35, False: 0.65})
                tries = []
                for _ in range(14):                        # matched sampling at the source: keep the variant that leaves the gaps smallest
                    try:
                        tries.append(H.best4_spec(task, rng, gp, alt))
                    except Skip:
                        break
                if not tries:
                    raise Skip("no BEST4 variant")
                units.append([min(tries, key=lambda sp: planner.bscore(sp) + rng.random() * 0.03)])
                used["BEST4"] += 1
            except Skip:
                pass
        n_v = 0
        while room("VERDICT") and caps.get("VERDICT", 1) > 0 and n_v < 3:
            n_v += 1
            utype, label = verdict_plan(planner, rng, C.REUSE_PER_MODULE_PER_HEAD - used["VERDICT"])
            try:
                if utype == "nearmiss":
                    reason = pick_deficit(rng, planner.c["reason"], C.REASON_MIX)
                    bads = [c for c in H.incorrect_cands(task) if c["kind"] == "CAND-NEARMISS" and c["cls"] == reason]
                    goods = [c for c in H.correct_cands(task) if c["kind"] in ("CAND-INVERSE", "CAND-ALTFIX")]
                    if not bads or not goods:
                        raise Skip("no near-miss pair for the cell")
                    combos = [(b, g) for b in bads for g in goods]
                    rng.shuffle(combos)
                    # matched sampling at the source: of up to 12 (near-miss, correct) combinations of this module, the one that
                    # leaves the running CORRECT-vs-INCORRECT style gap smallest
                    b, g = min(combos[:12], key=lambda bg: planner.vscore([H.verdict_spec_of(task, bg[1]), H.verdict_spec_of(task, bg[0])]) + planner.rscore([H.verdict_spec_of(task, bg[0])]) + rng.random() * 0.04)
                    inv, bad = H.verdict_spec_of(task, g), H.verdict_spec_of(task, b)
                    pid = "p%s.%d" % (task["uid"], n_v)
                    for s in (inv, bad):
                        s.update({"pair_id": pid, "pair_kind": "nearmiss"})
                    units.append([inv, bad])
                    used["VERDICT"] += 2
                elif utype == "altfix":
                    a = H.verdict_spec(task, rng, "CORRECT", kinds=("CAND-INVERSE",))
                    b = H.verdict_spec(task, rng, "CORRECT", kinds=("CAND-ALTFIX",))
                    pid = "p%s.%d" % (task["uid"], n_v)
                    for s in (a, b):
                        s.update({"pair_id": pid, "pair_kind": "altfix"})
                    units.append([a, b])
                    used["VERDICT"] += 2
                else:
                    reason = pick_deficit(rng, planner.c["reason"], C.REASON_MIX) if label == "INCORRECT" else None
                    pool = [c for c in (H.correct_cands(task) if label == "CORRECT" else H.incorrect_cands(task))
                            if (reason is None or c["cls"] == reason)]
                    if not pool:
                        raise Skip("no candidate for the VERDICT cell")
                    rng.shuffle(pool)
                    c = min(pool[:10], key=lambda cd: planner.vscore([H.verdict_spec_of(task, cd)]) + planner.rscore([H.verdict_spec_of(task, cd)]) + rng.random() * 0.04)
                    units.append([H.verdict_spec_of(task, c)])
                    used["VERDICT"] += 1
            except Skip:
                continue
    return units


def derive_rows_t(tasks, planner, rng, picker):
    units = []
    for task in tasks[:C.REUSE_PER_MODULE_PER_HEAD]:
        TK.build_candidates(task, rng)
        try:
            gp = pick_deficit(rng, planner.c["letter:TESTSEL"], {k: 0.25 for k in range(4)})
            units.append([H.testsel_spec(task, rng, gp)])
        except Skip:
            continue
    return units


def make_units(planner, picker, rng, skips):
    kind = planner.unit_kind()
    lang = planner.lang()
    seed = planner.seed()
    try:
        if kind == "T":
            tasks = TK.make_tasks(seed, lang, "T", multi=False, n_bugs=4)
            units = derive_rows_t(tasks, planner, rng, picker)
        elif kind == "L":
            tasks = TK.make_tasks(seed, lang, "L", multi=False, need_functions=4, n_bugs=4, distinct_fns=True,
                                  module_kw={"n_pure": 4, "force_wrapper": True, "wrapper_depth": 2, "n_files": 1, "want_state": False}, prefer_trace=True)
            units = derive_rows_a(tasks, planner, rng, picker, {"LOCALISE": 1, "BEST4": 1, "VERDICT": 1})
        else:
            multi = rng.random() < 0.25
            tasks = TK.make_tasks(seed, lang, "A", multi=multi, need_functions=1, n_bugs=3)
            units = derive_rows_a(tasks, planner, rng, picker, {"VERDICT": 1, "BEST4": 1, "LOCALISE": 0})
    except Skip as e:
        skips["unit:" + str(e)[:40]] += 1
        return []
    out = []
    for unit in units:
        for s in unit:
            decorate(s, planner, rng, picker)
        if not planner.unit_ok(unit):
            skips["balance cell full"] += 1
            continue
        for s in unit:
            planner.add_spec(s, +1)
            s["_reserved"] = True
        for s in unit:
            out.append(s)
            if (s["head"] in ("VERDICT", "LOCALISE")) and rng.random() < C.RENAME_TWIN_SHARE:
                tw = twin_of_spec(s, rng)
                if tw is not None:
                    out.append(tw)
            if s["head"] in ("VERDICT", "BEST4", "LOCALISE") and rng.random() < C.WITH_OUTPUTS_COPIES:
                cp = dict(s)
                cp["with_outputs"] = True
                cp["_reserved"] = False
                out.append(cp)
    return out


def permuted_row(row, rng, new_id, picker):
    """Order-invariance copy of an option row: same content, a random NON-IDENTITY permutation of the options."""
    head = row["head"]
    n = 4
    for _ in range(100):
        perm = list(range(n))
        rng.shuffle(perm)
        if perm != list(range(n)):
            break
    new = copy.deepcopy(row)
    new["row_id"] = new_id
    gi = row["meta"]["gold_index"]
    new_gi = perm.index(gi)
    new["meta"].update({"perm_copy": True, "perm_of": row["row_id"], "perm": perm, "gold_index": new_gi})
    new["label"] = ROWS.LETTERS[new_gi]
    car = new["carriers"]
    if head == "BEST4":
        old = car["PATCH_DIFF"]
        car["PATCH_DIFF"] = [{"option": ROWS.LETTERS[i], "diff": old[perm[i]]["diff"]} for i in range(4)]
        new["meta"]["cands"] = [row["meta"]["cands"][perm[i]] for i in range(4)]
        txt_old = "\n\n".join("Patch %s:\n%s" % (ROWS.LETTERS[i], old[i]["diff"]) for i in range(4))
        txt_new = "\n\n".join("Patch %s:\n%s" % (ROWS.LETTERS[i], car["PATCH_DIFF"][i]["diff"]) for i in range(4))
        new["prompt_text"] = row["prompt_text"].replace(txt_old, txt_new)
    else:
        opts_old = car["OPTIONS"]
        body = [o.split(". ", 1)[1] if head == "LOCALISE" else o.split(".\n", 1)[1] for o in opts_old]
        sep = ". " if head == "LOCALISE" else ".\n"
        car["OPTIONS"] = ["%s%s%s" % (ROWS.LETTERS[i], sep, body[perm[i]]) for i in range(4)]
        new["meta"]["options"] = [row["meta"]["options"][perm[i]] for i in range(4)]
        new["prompt_text"] = row["prompt_text"].replace("\n".join(opts_old), "\n".join(car["OPTIONS"]))
    wid, question = picker.render(row["question_form"], **row["meta"]["slots"])
    new["prompt_text"] = new["prompt_text"].replace(row["carriers"]["QUESTION_FORM"]["text"], question)
    car["QUESTION_FORM"] = {"form": row["question_form"], "wording_id": wid, "text": question}
    new["wording_id"] = wid
    new["meta"]["wording_id"] = wid
    return new


def reason_rows(rows, rng, picker, n_start):
    """Head rows for the reason head (G7): same rendered context, a separate question form with lettered options; at most
    25% of the INCORRECT VERDICT rows; gold from the same execution class; outside the family size."""
    out = []
    cands = [r for r in rows if r["head"] == "VERDICT" and r["label"] == "INCORRECT" and r["meta"]["variant"] == "primary"]
    rng.shuffle(cands)
    for r in cands[:int(0.25 * len(cands))]:
        reason = r["manifest"]["reason"]
        order = list(ROWS.REASON_OPTIONS)
        rng.shuffle(order)
        new = copy.deepcopy(r)
        new["row_id"] = "T57-REASON-%06d" % (n_start + len(out))
        new["head"] = "REASON"
        wid, question = picker.render("T57-Q-VERDICT-REASON", ask=ROWS.DEFAULT_ASK["REASON"], lang=r["meta"]["slots"]["lang"])
        opts = ["%s. %s" % (ROWS.LETTERS[i], n) for i, n in enumerate(order)]
        new["carriers"]["QUESTION_FORM"] = {"form": "T57-Q-VERDICT-REASON", "wording_id": wid, "text": question}
        new["carriers"]["OPTIONS"] = opts
        new["prompt_text"] = r["prompt_text"].replace(r["carriers"]["QUESTION_FORM"]["text"], "\n".join(opts) + "\n\n" + question)
        new["label"] = ROWS.LETTERS[order.index(reason)]
        new["question_form"] = "T57-Q-VERDICT-REASON"
        new["wording_id"] = wid
        new["meta"].update({"reason_head": True, "wording_id": wid, "form": "T57-Q-VERDICT-REASON", "reason_options": order,
                            "reason_gold": order.index(reason), "head": "REASON"})
        new["names"] = ROWS.row_names("REASON", r["lang"], set(new["carriers"]) - {"QUESTION_FORM"})
        out.append(new)
    return out


def build_rows(n_target, executor, picker, seed=0, ts_ok=True, max_units=2000, with_copies=True, checker=None):
    planner = Planner(seed, ts_ok)
    rng = random.Random("T57-build:%s" % seed)
    solver = SolverA(executor, picker, checker)
    rows, skips = [], collections.Counter()
    n_id, units = 0, 0
    while sum(1 for r in rows if r["meta"]["variant"] == "primary" and not r["meta"].get("twin_of")) < n_target and units < max_units:
        units += 1
        specs = make_units(planner, picker, rng, skips)
        if not specs:
            continue
        for s in specs:
            s["row_id"] = "T57-%s-%06d" % (s["head"], n_id)
            n_id += 1
        new = solver.run(specs)
        kept = {r["row_id"] for r in new}
        for s in specs:
            if s.get("_reserved") and s["row_id"] not in kept:
                planner.add_spec(s, -1)
        rows += new
    out = list(rows)
    n_before_copies = len(out)
    if with_copies:
        o = [r for r in rows if r["head"] in ("BEST4", "TESTSEL", "LOCALISE") and r["meta"]["variant"] == "primary" and not r["meta"].get("twin_of")]
        rng.shuffle(o)
        for r in o[:int(round(C.ORDER_COPIES * len(o)))]:
            out.append(permuted_row(r, rng, "T57-%s-%06d" % (r["head"], n_id), picker))
            n_id += 1
        out += reason_rows(rows, rng, picker, n_id)
    if checker is not None:                                    # order-invariance and reason-head rows are rows too: checked and stamped when made
        out = out[:n_before_copies] + checker.filter(out[n_before_copies:])
    return out, solver.stats, skips
