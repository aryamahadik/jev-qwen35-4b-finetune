"""G4 metamorphic tests (G0 section 11) on emitted rows: >= 1,000 rows per training sampler, 100% pass.

Relations (each variant is a test input, never an emitted row):
  MR1 entity rename (fresh card IDs, look-alike pairs kept as pairs; applied everywhere) -> label and gold unchanged
  MR2 statement reorder (facts, rules; a new layout seed for blocks and table rows)    -> label and gold unchanged
  MR3 inert / carrier insertion (I3 background sentence naming c's entity, or V2 topic line) -> unchanged
  MR4 claim negation (yes/no rows): FOLLOWS <-> RULED_OUT (TRUE <-> FALSE), OPEN stays
  MR5 monotonicity (OW, predicate without closure): adding a consistent fact never moves FOLLOWS / RULED_OUT
  MR6 premise removal (OW, predicate without closure): never OPEN -> decided, never FOLLOWS <-> RULED_OUT
  MR8 option shuffle (CH-claim, CH-entity): the gold option's content is unchanged
MR1-MR4 variants are also rendered, parsed back and re-solved by solver B (G3 on the variant). A variant that breaks
2.1 / 2.2 (solver A refuses it: guards, rivals, consistency) is resampled, never counted as a pass or a failure.
Property tests use a seeded random driver (the venv has no Hypothesis; the draws are reproducible from the seed).

  python g4_meta.py <set> [per_sampler] [workers]  -> logs/g4_<set>.json
"""
from __future__ import annotations

import collections
import copy
import json
import multiprocessing as mp
import pickle
import random
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
F4 = HERE.parent
sys.path.insert(0, str(HERE))

import build as BD  # noqa: E402

NAMES = {"cand": "candidates_r1", "qc": "qc_sample", "dev": "mixdev_S5"}
SWAP = {"F": "R", "R": "F", "O": "O"}


def deep_map(obj, fn_str):
    """Copy of obj with every string passed through fn_str (dataclasses, dicts incl. keys, lists, tuples, sets)."""
    if isinstance(obj, str):
        return fn_str(obj)
    if isinstance(obj, dict):
        return {deep_map(k, fn_str): deep_map(v, fn_str) for k, v in obj.items()}
    if isinstance(obj, list):
        return [deep_map(x, fn_str) for x in obj]
    if isinstance(obj, tuple):
        return tuple(deep_map(x, fn_str) for x in obj)
    if isinstance(obj, (set, frozenset)):
        return type(obj)(deep_map(x, fn_str) for x in obj)
    if hasattr(obj, "__dataclass_fields__"):
        new = copy.copy(obj)
        for k in obj.__dataclass_fields__:
            setattr(new, k, deep_map(getattr(obj, k), fn_str))
        return new
    return obj


def a_res(A, rec, card, row, nm):
    try:
        res = A.analyze(rec, card, row, near_miss=nm)
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "why": "exc:" + type(e).__name__}
    return res


def g3_variant(E, RM, cp, card, rec, row, res, dr, lexd, *, unit_seed=None, keep_frame=True):
    """Render the variant, parse it back, solver B: (ok, why, fields)."""
    d = {"rec": rec, "row": row, "res": res}
    try:
        fields, info = E.render_one(cp, card, d, unit_seed=dr["unit_seed"] if unit_seed is None else unit_seed,
                                    row_key=dr["row_key"], style_id=dr["style_id"],
                                    frame=dr["frame"] if keep_frame else None, wording=dr["wording"])
    except ValueError as e:
        return False, "render:" + str(e)[:40], None
    row2 = dict(row)
    row2["gold_canon"] = res["gold"]
    if row["form"] in ("CH-3", "CH-2"):
        row2["opt_labels"] = info["opt_labels"]
    ok, why, _ = RM.g3_check(rec, card, row2, fields, info["style"], lexd, res)
    return ok, why, fields


def id_rename(cp, seed):
    import packs_f4 as P
    n_base = len(cp.ids) - len(cp.looks)
    new_ids, new_looks = P.ids_for_card(f"{cp.card_id}#mr1#{seed}", n_base, len(cp.looks))
    new_all = new_ids + [v for _, v in new_looks]
    m = dict(zip(cp.ids, new_all))
    rx = re.compile(r"(?<![A-Za-z0-9])(" + "|".join(re.escape(i) for i in sorted(m, key=len, reverse=True)) +
                    r")(?![A-Za-z0-9])")
    cp2 = copy.copy(cp)
    cp2.ids = new_all
    cp2.looks = new_looks
    return cp2, (lambda s: rx.sub(lambda mo: m[mo.group(1)], s)), m


def claim_atoms(rec):
    return {(s.pred, s.e) for s in rec.stmts if s.kind == "lit"}


def test_row(args):
    """All applicable relations on one emitted row. Returns {mr: (status, why)} with status pass | fail | resample."""
    dr, cp, seed = args
    import core as C
    import emit as E
    import f4lex as L
    import render_f4 as R
    import rowmake as RM
    import solve_a as A
    card = BD.card_of(cp)
    lexd = RM.lexicon_for(cp)
    rng = random.Random(seed)
    rec, row, res0, nm = dr["rec"], dict(dr["row"]), dr["res"], dr["near_miss"]
    W = card.world or "OW"
    out = {}
    form = row["form"]
    base = a_res(A, rec, card, row, nm)
    if not base.get("ok") or str(base["gold"]) != str(res0["gold"]) or base["label_c"] != res0["label_c"]:
        return {"base": ("fail", "base_resolve:" + str(base.get("why")))}
    lab = base["label_c"]
    gold = base["gold"]

    def opt_content(row_, g):
        if g == "NONE" or not isinstance(g, int):
            return g
        return row_["options"][g]

    # MR1 entity rename
    cp2 = None
    for k in range(4):
        cp2, fn, m = id_rename(cp, f"{seed}:{k}")
        if len(cp2.looks) == len(cp.looks):
            break
    else:
        cp2 = None
    if cp2 is None:
        out["MR1"] = ("resample", "id_pool")
    else:
        rec1, row1, nm1 = deep_map(rec, fn), deep_map(row, fn), deep_map(nm, fn)
        r1 = a_res(A, rec1, card, row1, nm1)
        if not r1.get("ok"):
            out["MR1"] = ("fail", "a_refused:" + str(r1.get("why")))
        elif r1["label_c"] != lab or deep_map(opt_content(row, gold), fn) != opt_content(row1, r1["gold"]):
            out["MR1"] = ("fail", "label_changed")
        else:
            ok, why, _ = g3_variant(E, RM, cp2, card, rec1, row1, r1, dr, RM.lexicon_for(cp2))
            out["MR1"] = ("pass", None) if ok else ("fail", "g3:" + str(why))
    # MR2 statement reorder (and a new layout seed)
    rec2 = copy.deepcopy(rec)
    rng.shuffle(rec2.stmts)
    rng.shuffle(rec2.rules)
    r2 = a_res(A, rec2, card, row, nm)
    if not r2.get("ok"):
        out["MR2"] = ("fail", "a_refused:" + str(r2.get("why")))
    elif r2["label_c"] != lab or str(r2["gold"]) != str(gold):
        out["MR2"] = ("fail", "label_changed")
    else:
        ok, why, _ = g3_variant(E, RM, cp, card, rec2, row, r2, dr, lexd, unit_seed=rng.random())
        out["MR2"] = ("pass", None) if ok else ("fail", "g3:" + str(why))
    # MR3 inert / carrier insertion (I3 background naming c's entity, or a V2 topic line)
    rec3 = copy.deepcopy(rec)
    c = row["c"]
    if form == "CH-entity" or not c:
        out["MR3"] = ("resample", "no_c")
    else:
        if rec3.extras.get("topic") or rng.random() < 0.6:
            t = rec3.ents[c[1]]
            tpl = rng.choice(L.BACKGROUND_TEMPLATES)
            doc = rng.choice(cp.pack["docs"]) if cp.pack["docs"] else "file"
            rec3.extras["background"] = list(rec3.extras.get("background", [])) + \
                [tpl.format(X=c[1], doc=doc, types=cp.types[t][1])]
            kind3 = "I3"
        else:
            rec3.extras["topic"] = R.topic_line(rng.choice(L.TOPIC_LABELS), tuple(c))
            kind3 = "V2"
        r3 = a_res(A, rec3, card, row, nm)
        if not r3.get("ok"):
            out["MR3"] = ("fail", "a_refused:" + str(r3.get("why")))
        elif r3["label_c"] != lab or str(r3["gold"]) != str(gold):
            out["MR3"] = ("fail", "label_changed")
        else:
            ok, why, _ = g3_variant(E, RM, cp, card, rec3, row, r3, dr, lexd)
            out["MR3"] = ("pass", None) if ok else ("fail", f"g3:{kind3}:" + str(why))
    # MR4 claim negation (yes/no rows; label of not-c is the swap of the label of c)
    if form.startswith("YN") and c:
        row4 = dict(row)
        row4["c"] = (c[0], c[1], not c[2])
        if row.get("claim"):
            cl = row["claim"]
            row4["claim"] = (cl[0], cl[1], not cl[2])
        r4 = a_res(A, rec, card, row4, nm)
        if not r4.get("ok"):
            out["MR4"] = ("resample", "a_refused:" + str(r4.get("why")))
        elif r4["label_c"] != SWAP[lab]:
            out["MR4"] = ("fail", f"{lab}->{r4['label_c']}")
        else:
            ok, why, _ = g3_variant(E, RM, cp, card, rec, row4, r4, dr, lexd)
            out["MR4"] = ("pass", None) if ok else ("resample", "render_or_parse:" + str(why))
    closed = {p for (p, t, f_, tid) in rec.closures}
    if W == "OW" and form != "CH-entity" and c and c[0] not in closed:
        # MR5 monotonicity: one consistent fact about an open atom of a predicate with no closure
        stated = claim_atoms(rec)
        cands = [(p, e) for e, t in rec.ents.items() for p, tp in rec.preds.items()
                 if tp == t and p not in closed and p not in rec.exc_preds and (p, e) not in stated and
                 (p, e) != (c[0], c[1])]
        rng.shuffle(cands)
        st5 = ("resample", "no_candidate")
        for (p, e) in cands[:6]:
            rec5 = copy.deepcopy(rec)
            rec5.stmts.append(C.Stmt(sid=f"mr5_{p}_{e}", kind="lit", e=e, pred=p, pos=rng.random() < 0.5))
            r5 = a_res(A, rec5, card, row, nm)
            if not r5.get("ok"):
                continue
            if lab in ("F", "R") and r5["label_c"] != lab:
                st5 = ("fail", f"{lab}->{r5['label_c']}")
            else:
                st5 = ("pass", None)
            break
        out["MR5"] = st5
        # MR6 premise removal: one stated fact of a predicate with no closure
        lits = [s for s in rec.stmts if s.kind == "lit" and s.pred not in closed and s.pos is not None and
                s.pred not in rec.exc_preds]
        rng.shuffle(lits)
        st6 = ("resample", "no_candidate")
        for s in lits[:6]:
            rec6 = copy.deepcopy(rec)
            rec6.stmts = [x for x in rec6.stmts if x.sid != s.sid]
            r6 = a_res(A, rec6, card, row, nm)
            if not r6.get("ok"):
                continue
            l6 = r6["label_c"]
            bad = (lab == "O" and l6 != "O") or (lab == "F" and l6 == "R") or (lab == "R" and l6 == "F")
            st6 = ("fail", f"{lab}->{l6}") if bad else ("pass", None)
            break
        out["MR6"] = st6
    # MR8 option shuffle, display level, every row: re-render the row and show its options in a random order; the
    # option under the gold letter must be the gold option (yes/no rows: "Yes" / "No")
    from fmt1 import card as fcard
    try:
        fields8, _ = E.render_one(cp, card, {"rec": rec, "row": row, "res": base}, unit_seed=dr["unit_seed"],
                                  row_key=dr["row_key"], style_id=dr["style_id"], frame=dr["frame"],
                                  wording=dr["wording"])
        n8 = len(fields8["options"]) if fields8["options"] else 2
        perm = list(range(n8))
        while n8 > 1 and perm == list(range(n8)):
            rng.shuffle(perm)
        chk = fcard.loader_check({"id": dr["id"], **fields8}, perm=perm)
        out["MR8"] = ("pass", None) if chk["ok"] else ("fail", "loader:" + chk["problems"][0][:40])
    except ValueError as e:
        out["MR8"] = ("fail", "render:" + str(e)[:40])
    # MR8 option shuffle, structure level (CH-claim, CH-entity): solver A on the shuffled option list
    if form in ("CH-claim", "CH-entity") and out["MR8"][0] == "pass":
        row8 = dict(row)
        opts = list(row["options"])
        rng.shuffle(opts)
        row8["options"] = opts
        r8 = a_res(A, rec, card, row8, nm)
        if not r8.get("ok"):
            out["MR8"] = ("fail", "a_refused:" + str(r8.get("why")))
        elif opt_content(row8, r8["gold"]) != opt_content(row, gold):
            out["MR8"] = ("fail", "gold_content_changed")
        else:
            out["MR8"] = ("pass", None)
    return out


def main():
    set_name = sys.argv[1]
    per = int(sys.argv[2]) if len(sys.argv) > 2 else 1100
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 9
    pl = pickle.load(open(F4 / "tmp" / "cards_r1.pkl", "rb"))
    cards = pl["dev"] if set_name == "dev" else pl["cards"]
    final = {}
    with open(F4 / "out" / f"{NAMES[set_name]}.jsonl") as f:
        for x in f:
            r = json.loads(x)
            final[r["id"]] = r["meta"]["sampler"]
    drafts = [d for d in pickle.load(open(F4 / "tmp" / f"drafts_{set_name}.pkl", "rb")) if d["id"] in final]
    by = collections.defaultdict(list)
    for d in drafts:
        by[final[d["id"]]].append(d)
    rng = random.Random(f"f4-g4-{set_name}")
    jobs = []
    for smp in sorted(by):
        xs = by[smp]
        rng.shuffle(xs)
        for d in xs[:per]:
            jobs.append((d, cards[d["card_no"]], f"g4:{d['id']}"))
    t0 = time.time()
    agg = collections.defaultdict(collections.Counter)
    reasons = collections.Counter()
    fails = []
    with mp.get_context("fork").Pool(workers) as pool:
        for (d, cp, sd_), res in zip(jobs, pool.imap(test_row, jobs, chunksize=8)):
            smp = final[d["id"]]
            for mr, (st, why) in res.items():
                agg[(smp, mr)][st] += 1
                agg[("all", mr)][st] += 1
                if st != "pass":
                    reasons[(mr, st, (why or "")[:50])] += 1
                if st == "fail" and len(fails) < 40:
                    fails.append({"id": d["id"], "mr": mr, "why": why})
    rows_tested = collections.Counter(final[d["id"]] for d, _, _ in jobs)
    out = {"set": set_name, "rows_tested": dict(rows_tested), "seconds": round(time.time() - t0),
           "relations": {f"{k[0]}:{k[1]}": dict(v) for k, v in sorted(agg.items())},
           "non_pass_reasons": [[list(k), v] for k, v in reasons.most_common(40)], "fail_examples": fails,
           "n_fail": sum(v.get("fail", 0) for k, v in agg.items() if k[0] == "all")}
    with open(F4 / "logs" / f"g4_{set_name}.json", "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({"rows_tested": out["rows_tested"], "n_fail": out["n_fail"],
                      "all": {k: v for k, v in out["relations"].items() if k.startswith("all:")}}, indent=1))


if __name__ == "__main__":
    main()
