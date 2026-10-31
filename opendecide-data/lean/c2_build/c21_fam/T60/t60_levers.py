"""T60 lever rows (A12 character perturbation, A10 cue wrappers, A24 held-out dev-only rows). CODE ONLY. Derived from kept clean rows by
SUBSTITUTION inside the 2,000; the clean row stays (`twin_of`); the label never changes; a text that does not survive its recorded inverse is
dropped (`xform_drop`). The perturbed / wrapped field is the TASK STATEMENT only (never numbers, ids, handles, paths, step names, fact values,
order statements). Wrappers carry no instruction about delegating, planning, keeping, dropping, remembering or summarising (T60 lint).
"""
import copy
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from LK_COMMON import klevers, kpipeline  # noqa: E402
from tool_engine import render, util  # noqa: E402

FAMILY = "T60"
PER_2000 = {"a12": {"h1": 35, "h2": 30, "h3": 35}, "a10": {"h1": 30, "h2": 20, "h3": 30}, "dev_transform": 30, "dev_wrapper": 30}
TASK_KINDS = ("h1_task", "h2_task", "h3_goal")


def _scaled(n, total):
    return int(round(n * total / 2000.0))


def _task_span(rec):
    off = 0
    for kind, text in rec["lines"]:
        if kind in TASK_KINDS:
            return off, text
        off += len(text) + 1
    return None


def _protected_spans(rec, sent):
    """Names inside the task statement (entity nouns, the reference word) are never touched: they become entity spans."""
    spans = []
    sc = rec["scene"]
    names = list(sc["ent"]["nouns"])
    for nm in names:
        for m in re.finditer(r"(?<![A-Za-z0-9_])" + re.escape(nm) + r"(?![A-Za-z0-9_])", sent):
            spans.append(dict(start=m.start(), end=m.end(), text=nm, role="entity_path_flag"))
    pat = re.compile(r"(?:%s) ([A-Za-z]{4,14})" % "|".join(re.escape(nm) for nm in names))
    for m in pat.finditer(sent):                                                       # the reference word after the entity noun
        spans.append(dict(start=m.start(1), end=m.end(1), text=m.group(1), role="entity_path_flag"))
    spans.sort(key=lambda s: s["start"])
    merged = []
    for s in spans:
        if merged and s["start"] < merged[-1]["end"]:
            continue
        merged.append(s)
    return merged


def perturbed_row(clean, transform, rng, suffix):
    loc = _task_span(clean)
    if loc is None:
        return None
    off, sent = loc
    spans = _protected_spans(clean, sent) + render.decision_spans(sent, [])
    spans.sort(key=lambda s: s["start"])
    res = klevers.perturb_text(sent, spans, transform, rng)
    if res is None or not klevers.decision_spans_survive(sent, res["text"], res["ops"], []):
        return None
    ctx = clean["rendered"]["context"]
    new_ctx = ctx[:off] + res["text"] + ctx[off + len(sent):]
    ops = [[k, i + off, o] for k, i, o in res["ops"]]
    if klevers.invert(new_ctx, [tuple(o) for o in ops]) != ctx:
        return None
    row = kpipeline.derived_perturbed_row(clean, new_ctx, dict(transform=transform, ops=ops, request_offset=off), suffix)
    row["lines"] = [(k, (res["text"] if (k in TASK_KINDS and t == sent) else t)) for k, t in clean["lines"]]
    return row


def wrapped_row(clean, family, pos, sentence, suffix):
    loc = _task_span(clean)
    if loc is None:
        return None
    off, sent = loc
    new_sent = klevers.apply_wrapper(sent, sentence, pos)
    ctx = clean["rendered"]["context"]
    new_ctx = ctx[:off] + new_sent + ctx[off + len(sent):]
    r = copy.deepcopy(clean)
    r["row_id"] = clean["row_id"] + "~" + suffix
    r["twin_of"] = clean["row_id"]
    r["lever_tag"] = "lever.a10"
    r["wrapper"] = dict(family=family, pos=pos, sentence=sentence)
    r["rendered"]["context"] = new_ctx
    r["rendered"]["text"] = new_ctx + "\n\n" + clean["rendered"]["question"] + "\n" + clean["rendered"]["options_text"]
    r["lines"] = [(k, (new_sent if (k in TASK_KINDS and t == sent) else t)) for k, t in clean["lines"]]
    r.pop("stamp", None)
    return r


def _pick(rows, head, n, rng):
    cand = [r for r in rows if r["hd"] == head and r.get("lever_tag", "lever.none") == "lever.none" and r["split"] == "train"]
    cand.sort(key=lambda r: r["row_id"])
    rng.shuffle(cand)
    return cand[:n]


def make_extra_rows(ctx, kept, a10=False, wrapper_pool=None, include_dev=True):
    total = len(kept)
    rng = util.rng_for(ctx.seed, "levers")
    out = []
    pool_rows = [r for r in kept if r.get("lever_tag", "lever.none") == "lever.none"]
    k = 0
    drops = 0
    for head, n in PER_2000["a12"].items():
        for r in _pick(pool_rows, head, _scaled(n, total), rng):
            row = perturbed_row(r, klevers.TRAINED[k % len(klevers.TRAINED)], util.rng_for(ctx.seed, "a12", r["row_id"]), "a12")
            k += 1
            if row is None:
                drops += 1
                continue
            out.append(row)
    ctx.xform_drop = getattr(ctx, "xform_drop", 0) + drops
    pool = wrapper_pool or klevers.seed_pool_clean(FAMILY)
    if a10:
        for head, n in PER_2000["a10"].items():
            for i, r in enumerate(_pick(pool_rows, head, _scaled(n, total), rng)):
                fam = klevers.WRAPPERS_TRAINED[i % 3]
                sent = pool[fam][i % len(pool[fam])]
                if klevers.lint_wrapper(sent, FAMILY):
                    continue
                row = wrapped_row(r, fam, klevers.WRAP_POS[i % 2], sent, "a10")
                if row:
                    out.append(row)
    if include_dev:
        # skeptic fix: held-out dev rows come from rows of the DEV split only (see T59/t59_levers.py)
        devs = sorted([r for r in pool_rows if r["split"] == "dev"], key=lambda r: r["row_id"])
        rng.shuffle(devs)
        j = 0
        want_t = _scaled(PER_2000["dev_transform"], total)
        for r in devs:
            if j >= want_t:
                break
            tr = klevers.HELD_OUT[j % 3]
            row = perturbed_row(r, tr, util.rng_for(ctx.seed, "dev", r["row_id"]), "dev")
            if row is None:
                continue
            row.update(split="dev", group_id=r["group_id"] + "~dev", scenario_id=r.get("scenario_id", r["group_id"]) + "~dev", heldout_family=tr,
                       dev_only="split.dev_only")
            out.append(row)
            j += 1
        if a10:
            for i, r in enumerate(devs[::-1][:_scaled(PER_2000["dev_wrapper"], total)]):
                fam = klevers.WRAPPERS_HELD_OUT[i % 2]
                sent = pool[fam][i % len(pool[fam])]
                if klevers.lint_wrapper(sent, FAMILY):                    # the lint binds the held-out wrapper families too
                    continue
                row = wrapped_row(r, fam, klevers.WRAP_POS[i % 2], sent, "dev")
                if row:
                    row.update(split="dev", group_id=r["group_id"] + "~dev", scenario_id=r.get("scenario_id", r["group_id"]) + "~dev", heldout_family=fam,
                               dev_only="split.dev_only")
                    out.append(row)
    return out


def check_lever_row(h):
    why = []
    a = h.get("a12")
    if a:
        back = klevers.invert(h["rendered"]["context"], [tuple(o) for o in a["ops"]])
        if "​" in back or any(ord(c) > 127 for c in back):
            why.append("xform_inverse")
        allowed = klevers.allowed_nonascii([a["transform"]])        # skeptic fix: the perturbed text holds the characters of ITS transform only
        if any(ord(c) > 127 and c not in allowed for c in h["rendered"]["text"]):
            why.append("non_ascii_off_transform")
        if h.get("heldout_family") is None and a["transform"] in klevers.HELD_OUT:
            why.append("heldout_transform_in_train")
        if h.get("heldout_family") is not None and a["transform"] not in klevers.HELD_OUT:
            why.append("trained_transform_in_dev")
    w = h.get("wrapper")
    if w and h.get("heldout_family") is None and w["family"] in klevers.WRAPPERS_HELD_OUT:
        why.append("heldout_wrapper_in_train")
    if w and (not w.get("sentence") or klevers.lint_wrapper(w["sentence"], FAMILY)):
        why.append("wrapper_lint")
    if h.get("heldout_family") is not None and h.get("split") != "dev":
        why.append("heldout_not_dev_split")
    return why
