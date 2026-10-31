"""T65 generator: plan (300 twin pairs over 9 classes, oversampled by 15%) and group generation (pair -> two VULN rows); head rows (CWE class, G7) derived from KEPT YES
rows. No rows are written; dynamic witnesses go through ctx.executor (SimExecutor = PyEval in the dry run). The Juliet slice (L-R) is not built here."""
import hashlib

from LP_COMMON import plan as plan_mod
from LP_COMMON import sandbox_iface as S
from LP_COMMON import tokens, util, wording
from LP_COMMON.plan import Ctx as BaseCtx

from . import config as C
from . import specs as SP

TRANSFORMS = ("strip", "lower", "fmt", "box")


def form_slots():
    return dict(C.FORM_SLOTS)


INVERTED = (r"neutralis(?:e|es|ed) its", r"handled safely", r"on every path\?", r"covers the operation", r"\bsound\b", r"\bsafe(?:ly)?\b")


def pool_problems(pool):
    """Problems of a T65 wording pool ([] = usable): the shared rules plus the VULN polarity: YES = FLAWED, so no frame may ask the converse (does the function
    neutralise / handle safely / is it sound): a YES answer to such a frame means NO to the gold."""
    bad = list(wording.validate(pool, form_slots()))
    bad += wording.frame_problems(pool, "T65-Q-VULN", deny=INVERTED)
    return bad


class Ctx(BaseCtx):
    def __init__(self, seed, standin=False, pool_path=None, pool=None, executor=None, deny_check=None):
        if pool is None and pool_path is None and standin:
            pool = wording.make_test_pool(form_slots())
        super().__init__(seed, standin=standin, pool_path=pool_path, pool=pool, deny_check=deny_check)
        if self.pool is None:
            raise wording.PoolError("no wording pool")
        if executor is None and standin:
            executor = S.SimExecutor()
        if executor is None:
            raise ValueError("an executor is required (the od-sbx1 two-phase driver, or SimExecutor for tests)")
        if not standin:
            wording.require_real(self.pool)
            problems = pool_problems(self.pool)
            if problems:
                raise wording.PoolError("the T65 wording pool is not usable: " + "; ".join(problems[:4]))
            if isinstance(executor, S.SimExecutor):
                raise ValueError("SimExecutor cannot build rows (it predicts; it does not witness)")
        self.executor = executor
        self.picker = wording.Picker(self.pool, util.rng_for("T65-picker", seed))


def pair_kinds_for(cls):
    ns = ["NS-1", "NS-3"] + (["NS-2"] if cls in C.DYNAMIC else []) + (["NS-4"] if cls in ("CWEC-78", "CWEC-89") else [])
    return ns


LEVELS = ("L1", "L2", "L3", "L4")
TARGET = {"L1": 0.20, "L2": 0.30, "L3": 0.30, "L4": 0.20}
_DS_YES = {"DS-1": "high", "DS-2": "low", "DS-4": "high"}


def kind_flags(kind):
    """(yes_flags, no_flags): the mechanism flags the KIND contributes to each member (mirrors specs.ladder_flags; flow is added separately)."""
    if kind.startswith("decoy:"):
        f = _DS_YES.get(kind.split(":")[1])
        return ([f] if f else []), []
    if kind == "ns:NS-1":
        return ["high"], ["high"]
    if kind == "ns:NS-3":
        return [], ["high"]
    return [], []


def _lvl(flags):
    return plan_mod.ladder_level(sum(1 for f in flags if f == "low"), sum(1 for f in flags if f == "high"))


FLOW_OPTIONS = ((), ("strip",), ("lower",), ("fmt",), ("box",), ("strip", "lower"), ("fmt", "strip"))


def _flow_flag(tr):
    return "high" if (len(tr) >= 2 or "fmt" in tr or "box" in tr) else ("low" if tr else None)


def pick_transforms(kind, cls, counts, rng):
    """Greedy: the flow option that brings the running level counts closest to the 20/30/30/20 target."""
    if cls in C.STATIC:
        return []
    yf, nf = kind_flags(kind)
    best, bs = None, None
    opts = list(FLOW_OPTIONS)
    rng.shuffle(opts)
    tot = sum(counts.values()) + 2
    for tr in opts:
        fl = _flow_flag(tr)
        lv = [_lvl(yf + [fl]), _lvl(nf + [fl])]
        c2 = dict(counts)
        for l in lv:
            c2[l] += 1
        score = sum((c2[l] / tot - TARGET[l]) ** 2 for l in LEVELS)
        if bs is None or score < bs - 1e-12:
            best, bs = tr, score
    for l in (_lvl(yf + [_flow_flag(best)]), _lvl(nf + [_flow_flag(best)])):
        counts[l] += 1
    return list(best)


def build_plan(total=C.GENERATED_ROWS, seed=0, oversample=True):
    scale = total / float(C.GENERATED_ROWS) * (plan_mod.OVERSAMPLE if oversample else 1.0)
    rng = util.rng_for("T65-plan", seed)
    groups, k = [], 0
    lvl_counts = {l: 0 for l in LEVELS}
    for cls, n0 in C.CLASS_PAIRS.items():
        n = max(1, int(round(n0 * scale)))
        n_plain, n_decoy = int(round(0.18 * n)), int(round(0.42 * n))
        n_ns = n - n_plain - n_decoy
        kinds = ["plain"] * n_plain + ["decoy:DS-%d" % (1 + i % 6) for i in range(n_decoy)]
        nsk = pair_kinds_for(cls)
        ns_list = ["ns:NS-3"] * max(1, int(round(0.25 * n_ns))) if n_ns else []
        rest = n_ns - len(ns_list)
        others = [x for x in nsk if x != "NS-3"]
        ns_list += ["ns:" + others[i % len(others)] for i in range(rest)]
        kinds += ns_list[:n_ns]
        rng.shuffle(kinds)
        for kind in kinds:
            k += 1
            tr = pick_transforms(kind, cls, lvl_counts, rng)
            groups.append({"gid": "T65-%s-%04d" % (cls[5:], k), "seed": "%s-%d" % (cls[5:], k), "size": 2, "head": "VULN",
                           "cell": {"cls": cls, "pair_kind": kind, "transforms": tr, "noise": rng.random() < 0.3}})
    rng.shuffle(groups)
    return groups


def split_of(gid):
    return "dev" if int(hashlib.sha256(("T65-split|" + gid.split("~r")[0]).encode()).hexdigest(), 16) % 10 == 0 else "train"


def names_of(spec):
    cls = spec["cls"]
    return {"policy": list(C.POLICY["VULN"]), "tool": [], "language": ["python"], "runner": list(C.RUNNERS_DYNAMIC) if cls in C.DYNAMIC else [],
            "carrier": ["FUNC_CONTEXT", "OPTIONS", "QUESTION_FORM", "SRC_FILE"]}


def context_of(spec):
    ctx_line = ("The parameter `%s` is read from the query string of the request." % spec["spec"]["names"]["param"]) if spec["cls"] in C.DYNAMIC else \
        "The function is called by the service for each request it handles."
    return "\n\n".join([C.DEFS["VULN"], ctx_line, "Function (%s.py):\n%s" % (spec["stem"], spec["source_text"].rstrip("\n"))])


def build_record(ctx, g, spec, member, head="VULN"):
    form = C.QUESTION_FORM[head]
    rng = ctx.rng("t65rec", g["gid"], member, head)
    wid, question = ctx.picker.render(form, fn=spec["fn"])
    labels = ["YES", "NO"] if head == "VULN" else None
    gold = spec["label"]
    order = util.place_gold(labels, gold, rng.randrange(2), rng)
    options = [{"letter": util.LETTERS[i], "label": lab, "text": lab} for i, lab in enumerate(order)]
    options_text = "\n".join("%s) %s" % (o["letter"], o["text"]) for o in options)
    context = context_of(spec)
    text = "\n\n".join([context, question, options_text])
    level = SP.level_of(spec["mech"])
    return {"row_id": "%s-%s" % (g["gid"], "ab"[member]), "family": C.FAMILY, "head": "VULN", "sub_block": spec["cls"], "group_id": g["gid"], "gold": gold, "label": gold,
            "gold_letter": next(o["letter"] for o in options if o["label"] == gold), "options": options, "question_form": form, "slots": {"fn": spec["fn"]},
            "rendered": {"context": context, "question": question, "options_text": options_text, "text": text}, "names": names_of(spec), "spec": spec,
            "witness_inputs": {"head": "VULN", "lang": "python", "class_group": "dynamic" if spec["cls"] in C.DYNAMIC else "static"},
            "meta": {"template_id": "t65.%s.v1" % ("dyn" if spec["cls"] in C.DYNAMIC else "static"), "wording_id": wid, "construction_id": "%s:%s" % (spec["cls"], spec["pair_kind"]),
                     "ladder": level, "tokens": tokens.count(text), "split": split_of(g["gid"]), "pair_id": g["gid"], "twin_of": "%s-%s" % (g["gid"], "ab"[1 - member]),
                     "reuse_group": g["gid"].split("~r")[0], "mech": spec["mech"], "sub_block": spec["cls"], "lang": "python", "member": spec["member"],
                     "pair_kind": spec["pair_kind"], "edit_lines": spec["edit_lines"]},
            "manifest": {"gold_method": "static_taint", "solver_a_version": "t65.solver_a.v1", "pins": ("image:%s" % spec["witness"].get("image")) if spec["witness"] else "n/a:static_pattern_engine", "witness": spec["witness"]}}


def generate_group(ctx, g):
    last = None
    for t in range(8):
        try:
            specs = SP.make_pair_specs(ctx, dict(g, seed="%s#t%d" % (g["seed"], t)), g["cell"])
            break
        except SP.Reject as e:
            last = e
    else:
        raise last
    return [build_record(ctx, g, s, i) for i, s in enumerate(specs)]


# ---- CWE head rows (G7): <= 25% of the YES specs, <= 75 rows, outside the 600 ----------------------------------------------------------------
def _pick(gid):
    return int(hashlib.sha256(("T65-head|" + gid).encode()).hexdigest(), 16) % 1000 < 250


def extra_rows(ctx, kept):
    out = []
    for r in kept:
        if r.get("head_row") or r["gold"] != "YES" or not _pick(r["group_id"]):
            continue
        if len(out) >= C.HEAD_ROWS_MAX:
            break
        out.append(_cwe_row(ctx, r))
    return out


def _cwe_row(ctx, parent):
    spec = parent["spec"]
    cls = spec["cls"]
    rng = ctx.rng("t65cwe", parent["row_id"])
    wid, question = ctx.picker.render(C.QUESTION_FORM["CWE"], fn=spec["fn"])
    words = [C.CLASS_WORDS[cls]] + [C.CLASS_WORDS[c] for c in C.NEAREST[cls]]
    gold = C.CLASS_WORDS[cls]
    order = util.place_gold(words, gold, rng.randrange(4), rng)
    options = [{"letter": util.LETTERS[i], "label": w, "text": w} for i, w in enumerate(order)]
    options_text = "\n".join("%s) %s" % (o["letter"], o["text"]) for o in options)
    context = "\n\n".join([C.DEFS["CWE"], "Function (%s.py):\n%s" % (spec["stem"], spec["source_text"].rstrip("\n"))])
    text = "\n\n".join([context, question, options_text])
    names = dict(parent["names"], policy=list(C.POLICY["CWE"]))
    return {"row_id": parent["row_id"] + "-c", "family": C.FAMILY, "head": "CWE", "sub_block": cls, "group_id": parent["group_id"], "gold": gold, "label": gold,
            "gold_letter": next(o["letter"] for o in options if o["label"] == gold), "options": options, "question_form": C.QUESTION_FORM["CWE"], "slots": {"fn": spec["fn"]},
            "rendered": {"context": context, "question": question, "options_text": options_text, "text": text}, "names": names, "spec": spec, "head_row": True,
            "witness_inputs": {"head": "CWE", "lang": "python"},
            "meta": dict(parent["meta"], wording_id=wid, head="CWE", tokens=tokens.count(text), pair_id=None, twin_of=None, head_of=parent["row_id"], construction_id=cls + ":CWE"),
            "manifest": dict(parent["manifest"], head_of=parent["row_id"])}


def check_cwe_row(rec):
    why = []
    if rec["gold"] not in [o["label"] for o in rec["options"]] or len({o["label"] for o in rec["options"]}) != 4:
        why.append("options")
    return why
