"""T59 lever rows (A12 character perturbation, A10 cue wrappers, A24 held-out dev-only rows). CODE ONLY.

All lever rows are DERIVED from kept clean rows (by SUBSTITUTION inside the 2,000: the main plan is sized total - n_levers): the clean row
stays in the family (`twin_of`), the label never changes, and a row whose decision spans do not survive the recorded inverse is DROPPED
(`xform_drop`). The pipeline checks and stamps every derived row exactly like a generated one (check-at-creation).
Wrapper pools: the seeds in LK_COMMON.klevers extended by the Haiku writers (>= 20 per family); the literal ban is applied by the
stamp service, writers never see it.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from LK_COMMON import klevers, kpipeline  # noqa: E402
from tool_engine import render, util  # noqa: E402
import t59_render as R  # noqa: E402

FAMILY = "T59"
PER_2000 = {"a12": {"A": 90, "B": 30, "D": 30}, "a10": {"A": 60, "B": 20, "C": 20}, "dev_transform": 40, "dev_wrapper": 40}


def _scaled(n, total):
    return int(round(n * total / 2000.0))


def _request_span(rec):
    """(offset, sentence) of the request user line inside rendered.context, or None."""
    off = 0
    for kind, text in rec["lines"]:
        if kind == "user_req":
            pre = "User: "
            return off + len(pre), text[len(pre):]
        off += len(text) + 1
    return None


def _pick(rows, block, n, rng):
    cand = [r for r in rows if r["block"] == block and r.get("lever_tag", "lever.none") == "lever.none" and r["split"] == "train"]
    cand.sort(key=lambda r: r["row_id"])
    rng.shuffle(cand)
    return cand[:n]


def perturbed_row(clean, transform, rng, suffix):
    """-> row or None (xform_drop)."""
    loc = _request_span(clean)
    if loc is None:
        return None
    off, sent = loc
    auth = R.authority_values(clean["scene"])
    spans = render.decision_spans(sent, auth)
    res = klevers.perturb_text(sent, spans, transform, rng)
    if res is None or not klevers.decision_spans_survive(sent, res["text"], res["ops"], auth):
        return None
    ctx = clean["rendered"]["context"]
    new_ctx = ctx[:off] + res["text"] + ctx[off + len(sent):]
    ops = [[k, i + off, o] for k, i, o in res["ops"]]
    a12 = dict(transform=transform, ops=ops, request_offset=off)
    row = kpipeline.derived_perturbed_row(clean, new_ctx, a12, suffix)
    if klevers.invert(new_ctx, [tuple(o) for o in ops]) != ctx:
        return None
    row["lines"] = [(k, (t if k != "user_req" else "User: " + res["text"])) for k, t in clean["lines"]]
    return row


def wrapped_row(clean, family, pos, sentence, suffix):
    loc = _request_span(clean)
    if loc is None:
        return None
    off, sent = loc
    new_sent = klevers.apply_wrapper(sent, sentence, pos)
    ctx = clean["rendered"]["context"]
    new_ctx = ctx[:off] + new_sent + ctx[off + len(sent):]
    import copy
    r = copy.deepcopy(clean)
    r["row_id"] = clean["row_id"] + "~" + suffix
    r["twin_of"] = clean["row_id"]
    r["lever_tag"] = "lever.a10"
    r["wrapper"] = dict(family=family, pos=pos, sentence=sentence)
    r["rendered"]["context"] = new_ctx
    r["rendered"]["text"] = new_ctx + "\n\n" + clean["rendered"]["question"] + "\n" + clean["rendered"]["options_text"]
    r["lines"] = [(k, (t if k != "user_req" else "User: " + new_sent)) for k, t in clean["lines"]]
    r.pop("stamp", None)
    return r


def make_extra_rows(ctx, kept, a10=False, wrapper_pool=None, include_dev=True):
    """-> list of derived rows. `kept` = the stamped clean rows (the dev-only rows are drawn from rows of the dev split's complement:
    they are NEW renderings tagged split.dev_only / heldout_family; the mix guard refuses them)."""
    total = len(kept)
    rng = util.rng_for(ctx.seed, "levers")
    out = []
    n_drop = 0
    clean_pool = [r for r in kept if r.get("lever_tag", "lever.none") == "lever.none"]
    trained = klevers.TRAINED
    k = 0
    for block, n in PER_2000["a12"].items():
        want = _scaled(n, total)
        for r in _pick(clean_pool, block, want, rng):
            tr = trained[k % len(trained)]
            k += 1
            row = perturbed_row(r, tr, util.rng_for(ctx.seed, "a12", r["row_id"]), "a12")
            if row is None:
                n_drop += 1
                continue
            out.append(row)
    ctx.xform_drop = getattr(ctx, "xform_drop", 0) + n_drop
    if a10:
        pool = wrapper_pool or klevers.seed_pool_clean(FAMILY)
        for block, n in PER_2000["a10"].items():
            want = _scaled(n, total)
            for i, r in enumerate(_pick(clean_pool, block, want, rng)):
                fam = klevers.WRAPPERS_TRAINED[i % 3]
                sent = pool[fam][i % len(pool[fam])]
                if klevers.lint_wrapper(sent, FAMILY):
                    continue
                row = wrapped_row(r, fam, klevers.WRAP_POS[i % 2], sent, "a10")
                if row:
                    out.append(row)
    if include_dev:
        held = klevers.HELD_OUT
        # skeptic fix: the held-out dev rows are derived from rows of the DEV split only. Derived from a train-split row they would be a
        # held-out transform of a scenario the model trains on (clean and trained-transform twins), which contaminates the P6 comparison.
        devs = [r for r in clean_pool if r["block"] in ("A", "B", "D") and r["split"] == "dev"]
        devs.sort(key=lambda r: r["row_id"])
        rng.shuffle(devs)
        want_t = _scaled(PER_2000["dev_transform"], total)
        j = 0
        for r in devs:
            if j >= want_t:
                break
            tr = held[j % len(held)]
            row = perturbed_row(r, tr, util.rng_for(ctx.seed, "dev", r["row_id"]), "dev")
            if row is None:
                continue
            row["split"] = "dev"
            row["group_id"] = r["group_id"] + "~dev"
            row["heldout_family"] = tr
            row["lever_tag"] = "lever.a12"
            row["dev_only"] = "split.dev_only"
            out.append(row)
            j += 1
        if a10:
            pool = wrapper_pool or klevers.seed_pool_clean(FAMILY)
            want_w = _scaled(PER_2000["dev_wrapper"], total)
            for i, r in enumerate(devs[::-1][:want_w]):
                fam = klevers.WRAPPERS_HELD_OUT[i % 2]
                sent = pool[fam][i % len(pool[fam])]
                if klevers.lint_wrapper(sent, FAMILY):                    # the lint binds the held-out wrapper families too
                    continue
                row = wrapped_row(r, fam, klevers.WRAP_POS[i % 2], sent, "dev")
                if row:
                    row["split"] = "dev"
                    row["group_id"] = r["group_id"] + "~dev"
                    row["heldout_family"] = fam
                    row["dev_only"] = "split.dev_only"
                    out.append(row)
    return out


def check_lever_row(h):
    """Reasons a derived row is dropped (empty = fine); the full answer checks run on its canonical view in the pipeline."""
    why = []
    a = h.get("a12")
    if a:
        back = klevers.invert(h["rendered"]["context"], [tuple(o) for o in a["ops"]])
        if "\u200b" in back or any(ord(c) > 127 for c in back):
            why.append("xform_inverse")
        allowed = klevers.allowed_nonascii([a["transform"]])        # skeptic fix: the perturbed text holds the characters of ITS transform only
        if any(ord(c) > 127 and c not in allowed for c in h["rendered"]["text"]):
            why.append("non_ascii_off_transform")
        if h.get("heldout_family") is None and a["transform"] in klevers.HELD_OUT:
            why.append("heldout_transform_in_train")
        if h.get("heldout_family") is not None and a["transform"] not in klevers.HELD_OUT:
            why.append("trained_transform_in_dev")
    w = h.get("wrapper")
    if w:
        if h.get("heldout_family") is None and w["family"] in klevers.WRAPPERS_HELD_OUT:
            why.append("heldout_wrapper_in_train")
        if klevers.lint_wrapper(w.get("sentence", ""), FAMILY) or not w.get("sentence"):
            why.append("wrapper_lint")
    if h.get("heldout_family") is not None and h.get("split") != "dev":
        why.append("heldout_not_dev_split")
    return why
