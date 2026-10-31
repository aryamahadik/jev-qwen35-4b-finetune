"""G4 metamorphic relations (G0 section 7), run through the independent pipeline (G3 parsers + solver B), 100% pass
required on >= 1,000 rows per sampler:

  MR1  insert one contradictory NOT at the outermost scope (framed rows -> "Is it false that ...?"; C2m rows ->
       "Is it true that it is not the case that it is false that ...?")           expected: gold flips
  MR3  swap a cue for another template with the same signature and k (truth frame, C2 phrase, C3 / C5 / C10 / C12
       synonyms)                                                                   expected: unchanged
  MR5  rename every ID consistently (state, card, question) to fresh IDs of the same prefix; reorder the listing of
       rules / statements / log entries / records; change the container (re-render M in another training style)
                                                                                   expected: unchanged
  MR10 inject an attack instruction into the text                                  expected: unchanged
  MR4  (S1) add a sentence with a negation cue that restates a fact of M (closed cards: "<E> is not <w>" for a false
       fact atom)                                                                  expected: unchanged

  python -m gen.gates_mr --set qc
"""
from __future__ import annotations

import argparse
import collections
import copy
import json
import random
import re

from .common import OUT, TMP, read_jsonl  # noqa: I001  (sets sys.path for fmt1 first)
from fmt1 import pool as fpool
from fmt1.render import FormatError, render_state

from . import gates, gen, parse as PZ, parse_more
from .texts import ATTACKS

SWAPS = [("Is it true that ", "Is it the case that "), ("Is it the case that ", "Is it true that "),
         ("Does the record show that ", "Is it true that "), ("Is this assertion true: ", "Is the following statement "
                                                                                          "true: "),
         ("it is not the case that ", "it is false that "), ("it is false that ", "it is not the case that "),
         (" failed to ", " neglected to "), (" neglected to ", " omitted to "), (" omitted to ", " failed to "),
         (" lacks a ", " is without a "), (" is without a ", " lacks a "), (" no later than ", " not after "),
         (" not after ", " no later than "), (" no earlier than ", " not before "), (" not before ", " no earlier than "),
         (" must not ", " may not "), (" may not ", " must not "), (" need not ", " is not required to "),
         (" does not have to ", " need not "), (" hardly any ", " scarcely any "), (" scarcely any ", " hardly any "),
         ("Did ", "Did ")]
ID_RE = re.compile(r"\b([A-Z]{1,4})-([A-Z0-9]{2,6})\b")


def qparse(q, ctx):
    lf, k, fams, outer = PZ.parse_question(q, ctx)
    return lf, k


def ctx_for(sampler, consts, S):
    dp, mp = parse_more.decl_parsers(sampler)
    return {"affixed": consts["affixed"], "value_sets": consts["value_sets"], "decl_parsers": dp,
            "matrix_parsers": mp, "noun": S.get("noun") if isinstance(S, dict) else None,
            "q_graded": S.get("q_graded") if isinstance(S, dict) else None}


def solve(sampler, S, lf):
    return int(gates.solve_b(sampler, S, [lf])[0])


def mr_rows(rows, side, bases, per_sampler=1200, seed=20261005):
    rng = random.Random(seed)
    sid = {s["id"]: s for s in side}
    bmap = {b["base_id"]: b for b in bases}
    by_s = collections.defaultdict(list)
    for r in rows:
        if r["role"] == "attack":
            continue
        b = bmap[sid[r["id"]]["base_id"]]
        by_s["INV" if b.get("inverted") else b["sampler"]].append(r)
    res = collections.Counter()
    errs = []
    for sampler, rs in sorted(by_s.items()):
        rng.shuffle(rs)
        for r in rs[:per_sampler]:
            b = bmap[sid[r["id"]]["base_id"]]
            try:
                out = check_row(sampler, r, b, sid[r["id"]], rng)
            except Exception as e:  # noqa: BLE001
                out = {"error": f"{type(e).__name__}: {str(e)[:120]}"}
            for k, v in out.items():
                if v is True:
                    res[f"{sampler}:{k}:pass"] += 1
                elif v is None:
                    res[f"{sampler}:{k}:n/a"] += 1
                else:
                    res[f"{sampler}:{k}:FAIL"] += 1
                    errs.append((r["id"], k, v))
            res[f"{sampler}:rows"] += 1
    return res, errs


def check_row(sampler, r, b, s, rng):
    keys, consts = PZ.parse_card(r["card"])
    S = gates.parse_structure(sampler, [r], consts)
    ctx = ctx_for(sampler, consts, S)
    q = PZ.extract_question(r["instructions"])
    lf, k = qparse(q, ctx)
    g0 = r["gold"]
    out = {}
    # MR1
    m = re.fullmatch(r"Is it false that (.+)\?", q)
    if m:
        inner = m.group(1)
        for t in PZ.TAILS_P:
            if inner.endswith(t):
                inner = inner[: -len(t)]
        q1 = f"Is it true that it is not the case that it is false that {inner}?"
    else:
        q1 = None
        for pat in PZ.FRAMES_P:
            mm = re.fullmatch(pat, q)
            if mm:
                q1 = f"Is it false that {mm.group(1)}?"
                break
    if q1:
        lf1, k1 = qparse(q1, ctx)
        out["MR1"] = (solve(sampler, S, lf1) == 1 - g0 and k1 == k + 1) or f"MR1 {q1[:80]}"
    else:
        out["MR1"] = None
    # MR3
    sw = [(a, c) for a, c in SWAPS if a in q and a != c]
    if sw:
        a, c = rng.choice(sw)
        q3 = q.replace(a, c, 1)
        lf3, k3 = qparse(q3, ctx)
        out["MR3"] = (solve(sampler, S, lf3) == g0) or f"MR3 {a!r}->{c!r}"
    else:
        out["MR3"] = None
    # MR5: rename IDs (state, card, question), reorder the listing and change the container
    ids = sorted(set(ID_RE.findall(r["state"] + " " + r["card"] + " " + q)))
    ren = {}
    used = {f"{p}-{x}" for p, x in ids}
    for p, x in ids:
        for tries in range(10 ** 6):
            # digits redrawn; an ID with few or no digits gets fresh digits appended (same ID shape, never a loop)
            nx = "".join(rng.choice("0123456789") if ch.isdigit() else ch for ch in x)
            if tries >= 50:
                nx += "".join(rng.choice("0123456789") for _ in range(1 + tries // 200))
            nid = f"{p}-{nx}"
            if nid not in used:
                used.add(nid)
                ren[f"{p}-{x}"] = nid
                break
    H = gen.H_for({"sampler": b["sampler"], "inverted": b.get("inverted")})
    M2 = rename_struct(b["M"], ren)
    reorder(M2, rng)
    doc = H.doc(M2)
    sts = [st for st in fpool.styles() if st["id"] != r["meta"]["format_style"]]
    rng.shuffle(sts)
    new_state = None
    for st in sts[:60]:
        try:
            new_state = render_state(doc, st)
            break
        except FormatError:
            continue
    card2 = ren_text(r["card"], ren)
    q5 = ren_text(q, ren)
    r5 = dict(r, state=new_state, card=card2)
    keys5, consts5 = PZ.parse_card(card2)
    S5 = gates.parse_structure(sampler, [r5], consts5)
    lf5, k5 = qparse(q5, ctx_for(sampler, consts5, S5))
    out["MR5"] = (new_state is not None and solve(sampler, S5, lf5) == g0) or "MR5"
    # MR10: attack injection
    att = rng.choice(ATTACKS).format(X=rng.choice(["Yes", "No"]))
    doc10 = H.doc(b["M"], attack=att)
    try:
        st10 = render_state(doc10, fpool.style(r["meta"]["format_style"]))
        r10 = dict(r, state=st10, role="attack")
        S10 = gates.parse_structure(sampler, [dict(r, role="aff"), r10], consts)
        out["MR10"] = (solve(sampler, S10, lf) == g0) or "MR10"
    except FormatError:
        out["MR10"] = None
    # MR4 (S1): a negated restatement of a false fact atom on a closed card
    if sampler == "S1" and b["M"]["world"] == "closed":
        M4 = copy.deepcopy(b["M"])
        cand = [k_ for k_, x in M4["facts"].items() if x is False and k_.startswith("adj:")
                and M4["fact_form"].get(k_) == "omit"]
        if cand:
            k_ = rng.choice(cand)
            M4["fact_form"][k_] = "not"
            st4 = render_state(H.doc(M4), fpool.style(r["meta"]["format_style"]))
            S4_ = gates.parse_structure(sampler, [dict(r, state=st4)], consts)
            out["MR4"] = (solve(sampler, S4_, lf) == g0) or "MR4"
        else:
            out["MR4"] = None
    return out


def ren_text(t, ren):
    return ID_RE.sub(lambda m: ren.get(m.group(0), m.group(0)), t)


def rename_struct(M, ren):
    s = json.dumps(M)
    s = ID_RE.sub(lambda m: ren.get(m.group(0), m.group(0)), s)
    return json.loads(s)


def reorder(M, rng):
    for key in ("rules", "univ", "facts", "recs", "entries", "cases"):
        if isinstance(M.get(key), list):
            rng.shuffle(M[key])
    if "fact_order" in M:
        rng.shuffle(M["fact_order"])


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", required=True)
    ap.add_argument("--per", type=int, default=1200)
    a = ap.parse_args(argv)
    name = {"candidates": "candidates_r1", "qc": "qc_sample", "mixdev": "mixdev_S5"}.get(a.set, a.set)
    rows = read_jsonl(OUT / f"{name}.jsonl")
    side = read_jsonl(OUT / f"{name}.F5_polarity.jsonl")
    bases = read_jsonl(TMP / f"{name}.bases.jsonl")
    res, errs = mr_rows(rows, side, bases, per_sampler=a.per)
    print(json.dumps(dict(sorted(res.items())), indent=1))
    seen = collections.Counter()
    for e in errs:
        key = (e[1], str(e[2])[:40])
        seen[key] += 1
        if seen[key] <= 2:
            print(json.dumps(e, default=str)[:400])
    json.dump({"set": name, "counts": dict(sorted(res.items())), "errors": errs[:200]},
              open(OUT / f"{name}.G4.json", "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
