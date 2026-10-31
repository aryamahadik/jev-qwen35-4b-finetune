"""Independent verifier for gen_evidence_conflict.

For every written row it
  1. rebuilds the case from meta.orig_label.case (a JSON round trip, so nothing is shared with the generator's objects)
     and re-renders the state and the question: both must equal the row text exactly;
  2. recomputes the gold label with a second implementation of the rules (sequential folds over the documents instead
     of the generator's max/filter resolver), under both readings of 'newest', and requires them to agree;
  3. checks every rendered document block for what the label relies on: its header date/time and source, the
     entity it names (the confusable one only for other-entity documents), its value, its effective dates, the date
     of the document a correction or withdrawal refers to (which must be unique for that source), hedge markers for
     speculation, and that the question carries the date and the claimed value.
Returns a list of (rid, reason) for any disagreement.
"""
import json

import ec_render as R
from ec_domains import DOM

YN = ("supported", "refuted", "direct", "enough")
HEDGE_MARKS = ("might", " may ", "could", "not sure", "rumour", "unconfirmed", "wasn't sure", "Provisional",
               "can't confirm", "possible", "not been confirmed")


def _value_at(case, t, cutoff, order):
    """Second implementation: returns (result, ids) where result is ('pos'|'neg', v), 'TIE' or None."""
    drop = case.get("drop")
    docs = [d for d in case["docs"] if d["id"] != drop and (cutoff is None or d["pub"] <= cutoff)]
    withdrawn, fixed = set(), {}
    for d in sorted(docs, key=lambda d: d["pub"]):
        if d["kind"] == "retr":
            withdrawn.add(d["tgt"])
        elif d["kind"] == "corr":
            fixed[d["tgt"]] = d
    rule = case["rule"]
    cands = []
    periods = []  # (start, end, value) of known, counted scheduled / temporary changes (after corrections)
    for d in docs:
        if d["kind"] in ("sched", "temp") and d["mood"] == "def" and d["ent"] == 0 and d["id"] not in withdrawn and \
                not (rule["t"] == "only" and d["src"] not in rule["cnt"]):
            val = fixed[d["id"]]["v"] if d["id"] in fixed else d["v"]
            periods.append((d["start"], d["end"] if d["kind"] == "temp" else float("inf"), val))
        if d["kind"] not in ("stmt", "neg", "sched", "temp") or d["mood"] != "def" or d["ent"] != 0:
            continue
        if d["id"] in withdrawn:
            continue
        start = d["pub"] if d["kind"] in ("stmt", "neg") else d["start"]
        end = d["end"] if d["kind"] == "temp" else float("inf")
        if t < start or t > end:
            continue
        if rule["t"] == "only" and d["src"] not in rule["cnt"]:
            continue
        if d["id"] in fixed:
            c = fixed[d["id"]]
            cands.append({"pub": c["pub"], "start": start, "sig": ("pos", c["v"]), "src": d["src"], "id": c["id"]})
        else:
            cands.append({"pub": d["pub"], "start": start, "sig": ("neg" if d["kind"] == "neg" else "pos", d["v"]),
                          "src": d["src"], "id": d["id"]})
    pre_auth = list(cands)
    if rule["t"] == "auth":
        pos = {s: i for i, s in enumerate(rule["rank"])}
        top = None
        for c in cands:
            if top is None or pos[c["src"]] < top:
                top = pos[c["src"]]
        cands = [c for c in cands if pos[c["src"]] == top]
    keyf = (lambda c: (c["pub"],)) if order == "A" else (lambda c: (c["start"], c["pub"]))
    best, sigs, ids = None, [], []
    for c in sorted(cands, key=keyf):
        k = keyf(c)
        if best is None or k > best:
            best, sigs, ids = k, [tuple(c["sig"])], [c["id"]]
        elif k == best:
            ids.append(c["id"])
            if tuple(c["sig"]) not in sigs:
                sigs.append(tuple(c["sig"]))
    if best is None:
        return None, [], []
    for s0, e0, val in periods:
        if not (s0 <= t <= e0) and ("pos", val) in sigs:
            raise AssertionError("value equals a scheduled/temporary value outside its period")
    if len(sigs) > 1:
        return "TIE", sorted(ids), sorted(sigs, key=repr)
    if sigs[0][0] == "neg":
        alts = sorted({c["sig"][1] for c in pre_auth if c["sig"][0] == "pos" and c["sig"][1] != sigs[0][1]}, key=repr)
        return sigs[0], sorted(ids), [("alts", a) for a in alts]
    return sigs[0], sorted(ids), sigs


def _both(case, t, cutoff):
    a = _value_at(case, t, cutoff, "A")
    b = _value_at(case, t, cutoff, "B")
    if a[0] != b[0] or (a[0] == "TIE" and a[2] != b[2]):
        raise AssertionError("readings disagree")
    return a, b


def _one(vs):
    vs = set(vs)
    return vs.pop() if len(vs) == 1 else "N"


def _claim_verdict(case, res, tied=None):
    c = case["claim"]
    if res == "TIE":
        return _one(_claim_verdict(case, s) for s in tied)
    if res is None:
        return "N"
    pol, v = res
    if c["t"] == "cmp":
        if pol != "pos":
            return "N"
        x, op = c["thr"], c["op"]
        ok = (v < x) if op == "lt" else (v <= x) if op == "le" else (v > x) if op == "gt" else (v >= x)
        return "T" if ok else "F"
    holds_eq = None
    if pol == "pos":
        holds_eq = v == c["v"]
    elif v == c["v"]:
        holds_eq = False
    if holds_eq is None:
        return "N"
    if c["t"] == "eq":
        return "T" if holds_eq else "F"
    return "F" if holds_eq else "T"


def independent_gold(case):
    qid = case["qid"]
    mode = case["mode"]
    c = case.get("claim")
    if c and c["t"] == "diff":
        (r2, _, t2), _ = _both(case, case["D"], case["D"])
        (r1, _, t1), _ = _both(case, c["D2"], c["D2"])

        def dv(a, b):
            if a is None or b is None:
                return "N"
            if a[0] == "pos" and b[0] == "pos":
                return "T" if a[1] != b[1] else "F"
            if a[0] != b[0]:
                return "T" if a[1] == b[1] else "N"
            return "N"
        for rr, tt in ((r1, t1), (r2, t2)):
            if rr not in (None, "TIE") and rr[0] == "neg" and tt:
                raise AssertionError("negative report with alternatives in a comparison")
        o1 = t1 if r1 == "TIE" else [r1]
        o2 = t2 if r2 == "TIE" else [r2]
        verdict = _one(dv(a, b) for a in o1 for b in o2)
        res, ids_a, ids_b = r2, None, None
    else:
        cutoff = case["D"] if mode == "known" else (None if mode == "hind" else case["K"])
        (res, ids_a, tied), (_, ids_b, _) = _both(case, case["D"], cutoff)
        verdict = _claim_verdict(case, res, tied) if c else None
        if res not in (None, "TIE") and res[0] == "neg" and tied:
            if not c:
                raise AssertionError("negative report with alternatives in a value question")
            for _, a in tied:
                if _claim_verdict(case, ("pos", a)) != verdict:
                    raise AssertionError("negative report: verdict depends on falling back to an older report")
    if qid == "supported":
        return "yes" if verdict == "T" else "no"
    if qid == "refuted":
        return "yes" if verdict == "F" else "no"
    if qid == "enough":
        return "yes" if verdict in ("T", "F") else "no"
    if qid == "direct":
        assert verdict in ("T", "F")
        return "yes" if verdict == "T" else "no"
    if qid == "choice3":
        return {"T": "supported", "F": "refuted", "N": "not enough information"}[verdict]
    if qid == "pick":
        opts = case["pick_opts"]
        tgt = "NEI" if (res is None or res == "TIE" or res[0] == "neg") else res[1]
        return "ABCDEF"[opts.index(tgt)]
    if qid == "source":
        if res is None or res == "TIE":
            return "none"
        assert res[0] == "pos" and ids_a == ids_b and len(ids_a) == 1
        return str(case["order"].index(ids_a[0]) + 1)
    raise ValueError(qid)


def _blocks(case, state):
    """Split the state at the rendered headers (which must appear in order, once each)."""
    byid = {d["id"]: d for d in case["docs"]}
    heads = [R.header(case, byid[i], n) for n, i in enumerate(case["order"], 1)]
    pos = []
    at = 0
    for h in heads:
        k = state.find(h + "\n", at)
        assert k >= 0, f"header missing: {h}"
        assert state.count(h + "\n") == 1, f"header repeated: {h}"
        pos.append(k)
        at = k + len(h)
    out = []
    for j, i in enumerate(case["order"]):
        end = pos[j + 1] if j + 1 < len(pos) else len(state)
        out.append((byid[i], heads[j], state[pos[j] + len(heads[j]) + 1:end]))
    return out


def check_text(case, row):
    dom = DOM[case["dom"]]
    state, q = row["state"], row["instructions"]
    assert state == R.render_state(case), "state does not re-render"
    assert q == R.question(case), "question does not re-render"
    assert "\n" not in q and q.endswith("?") and q.count("?") == 1, "question is not one sentence"
    E, C = case["ent"]["E"], case["ent"]["C"]
    assert E.lower() not in C.lower() and C.lower() not in E.lower(), ("confusable", E, C)
    byid = {d["id"]: d for d in case["docs"]}
    for d, head, blk in _blocks(case, state):
        assert R.hdr_when(case, d["pub"]) in head, ("header date", head)
        if d["kind"] == "inject":
            assert any(s in head for s in R.INJ_SRC), ("inject header", head)
            continue
        assert dom["sources"][d["src"]]["sg"].lower() in head.lower(), ("source header", head)
        if d["kind"] in ("stmt", "neg", "sched", "temp"):
            want, avoid = (E, C) if d["ent"] == 0 else (C, E)
            lb = blk.lower()
            assert want.lower() in lb, (want, blk)
            assert avoid.lower() not in lb or (d.get("inj") and d["ent"] == 0), (avoid, blk)
            vtxt = [R.vn(case, d["v"]), R.rv(case, d["v"]), R.fval(case, d["v"]), R.interrog(case, d["v"], d["ent"], "doc")]
            if dom["vtype"] == "bin":
                vtxt += [R.pres(case, d["v"], d["ent"])] + [R.base(case, d["v"], a, d["ent"]) for a in ("will",) + tuple(R.HEDGE_AUX)]
                if d.get("surf") == "negpres":
                    vtxt.append(R.negpres(case, d["v"], d["ent"]))
            assert any(x.lower() in lb for x in vtxt), ("value", d["v"], blk)
            if d["mood"] == "hedge":
                assert any(m in blk for m in HEDGE_MARKS), blk
            if d["mood"] == "ask":
                assert "?" in blk or "asked" in blk or "checking" in blk, blk
            if d["mood"] == "def":
                assert not any(m in blk.split("(Note")[0].split("[")[0] for m in ("might", "rumour", "not sure")), blk
        if d["kind"] in ("sched", "temp") and d["mood"] == "def":
            assert R.eff_text(case, d, "S") in blk, ("start", blk)
            if d["kind"] == "temp":
                assert R.eff_text(case, d, "F") in blk, ("end", blk)
        if d["kind"] in ("corr", "retr"):
            tg = byid[d["tgt"]]
            assert R.ref_when(case, tg["pub"]) in blk, ("ref", blk)
            same = [o for o in case["docs"] if o["kind"] != "inject" and o["src"] == tg["src"] and o["id"] != tg["id"]
                    and R.ref_when(case, o["pub"]) == R.ref_when(case, tg["pub"])]
            assert not same, "ambiguous reference"
            if d["kind"] == "corr":
                assert any(x in blk for x in (R.vn(case, d["v"]), R.rv(case, d["v"]), R.pres(case, d["v"]),
                                              R.base(case, d["v"], "will"))), ("corr value", blk)
    c = case.get("claim")
    Dtxt = R.when(case, case["D"])
    if not (dom["event"] and case["mode"] == "hind"):
        assert Dtxt in q, ("date not in question", Dtxt, q)
    if c and c["t"] in ("eq", "neq"):
        ql = q.lower()
        assert R.fval(case, c["v"], "q").lower() in ql or R.vn(case, c["v"], "q").lower() in ql or \
            (dom["vtype"] == "bin" and (R.pres(case, c["v"]).lower() in ql or R.interrog(case, c["v"]).lower() in ql or
                                        R.negc(case, c["v"]).lower() in ql)), ("claim value", q)
    if c and c["t"] == "cmp":
        assert R.fval(case, c["thr"], "q") in q, ("threshold", q)
    if c and c["t"] == "diff":
        assert R.when(case, c["D2"]) in q, ("D2", q)
    if case["mode"] == "pk":
        assert R.when(case, case["K"]) in q, ("K", q)


DOC_DEFAULTS = {"mood": "def", "ent": 0, "v": None, "start": None, "end": None, "rel": None, "tgt": None, "inj": None,
                "surf": "pos"}
CASE_DEFAULTS = {"claim": None, "drop": None, "person": None, "pick_opts": None, "K": None}


def restore_case(stored):
    case = json.loads(json.dumps(stored))
    for k, v in CASE_DEFAULTS.items():
        case.setdefault(k, v)
    for d in case["docs"]:
        for k, v in DOC_DEFAULTS.items():
            d.setdefault(k, v)
    if isinstance(case.get("win"), list):
        case["win"] = tuple(case["win"])
    return case


def verify_rows(rows):
    bad = []
    twins = {}
    for r in rows:
        case = restore_case(r["meta"]["orig_label"]["case"])
        try:
            g = independent_gold(case)
        except AssertionError as e:  # noqa: PERF203
            bad.append((r["rid"], f"independent resolver: {e}"))
            continue
        if g != r["gold"]:
            bad.append((r["rid"], f"gold {r['gold']} vs independent {g}"))
            continue
        if g not in r["options"]:
            bad.append((r["rid"], "gold not in options"))
            continue
        try:
            check_text(case, r)
        except AssertionError as e:  # noqa: PERF203
            bad.append((r["rid"], f"text check: {e}"))
            continue
        if r["meta"].get("twin_of"):
            twins[r["meta"]["twin_of"]] = r
    by_rid = {r["rid"]: r for r in rows}
    for base_rid, tw in twins.items():
        b = by_rid.get(base_rid)
        if b is None or b["gold"] == tw["gold"] or b["meta"]["defs"] != tw["meta"]["defs"]:
            bad.append((tw["rid"], "twin does not flip the gold"))
    return bad
