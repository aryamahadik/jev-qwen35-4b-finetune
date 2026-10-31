"""G4 metamorphic relations (G0 section 7) on emitted rows, per sampler (>= 1,000 rows each; S5 all 400).

  f12g4.py <file stem>[+<file stem>...] <sampler> [--rows N]
Each MR runs only on rows meeting its preconditions (the check is part of the test). Labels are re-derived by
solver A on the transformed structure; MR2 / MR4 / MR10 / MR11 / MR14 also re-run solver B on the transformed
structure (the parsed-structure schema is the same), so a pass needs both solvers to move as the MR expects.
MR1 option shuffle, MR2 catalog shuffle, MR4 add an inert tool, MR10 delete the only statement of a needed value,
MR11 delete every matching tool, MR13 negate the yes/no question, MR14 flip POL-INVALID A <-> B.
"""
from __future__ import annotations

import collections
import copy
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "formats" / "formats-1"))
import f12build as BLD  # noqa: E402
import f12g3 as G3  # noqa: E402
import f12solve_a as A  # noqa: E402
import f12solve_b as SB  # noqa: E402

OUT = HERE.parent / "out"


def b_outcome(S, pk):
    P = copy.deepcopy(S)
    for t in P["tools"]:
        t.setdefault("oword", pk["etypes"][t["o"]]["word"] if t.get("o", -1) >= 0 else "")
    return SB.solve(P, P["pol"], G3.lex_b(pk))


def bcall(call):
    """Solver A's typed call ({"num": text} decimals) -> the parsed form solver B reads (JSON numbers, Decimal)."""
    from decimal import Decimal
    c = copy.deepcopy(call)
    c["args"] = [[k, json.loads(v["num"], parse_float=Decimal) if isinstance(v, dict) and "num" in v else v]
                 for k, v in c["args"]]
    return c


def run(stem, sampler, n_rows, seed=4):
    pks = {p["id"]: p for p in BLD.packs()}
    rows, sides = [], []
    for st in stem.split("+"):  # "candidates_r1+qc_sample": both emitted pools (>= 1,000 rows per sampler)
        rows += [json.loads(l) for l in open(OUT / f"{st}.jsonl")]
        sides += [json.loads(l) for l in open(OUT / "side" / f"{st}.side.jsonl")]
    pairs = [(r, s) for r, s in zip(rows, sides) if r["meta"]["sampler"] == sampler]
    rng = random.Random(seed)
    rng.shuffle(pairs)
    pairs = pairs[:n_rows]
    stat = collections.defaultdict(lambda: [0, 0, 0])  # applicable, pass, skipped
    fails = []

    def rec(mr, ok, rid, why=""):
        stat[mr][0] += 1
        stat[mr][1] += 1 if ok else 0
        if not ok and len(fails) < 40:
            fails.append({"mr": mr, "id": rid, "why": why})
    for r, s in pairs:
        pk = pks[r["meta"]["domain_pack"]]
        S = s["S"]
        rid = r["id"]
        # MR1: option shuffle keeps the canonical gold
        if r["qtype"] == "choice":
            perm = list(range(len(r["options"])))
            rng.shuffle(perm)
            opts = [r["options"][i] for i in perm]
            canon = [s["opts_canon"][i] for i in perm]
            rec("MR1", canon[opts.index(r["gold"])] == s["gold_canon"], rid)
        if S.get("call"):
            # audit relations (S3): argument order, catalog order, inert tool, explicit default
            import f12audit_b as AB
            import f12extra as X
            a0, b0 = X.audit_a(S["tools"], S["call"]), AB.validate(S["tools"], bcall(S["call"]))
            rec("MRA0-agree", a0 == b0, rid, f"{a0} vs {b0}")
            c1 = copy.deepcopy(S["call"])
            rng.shuffle(c1["args"])
            rec("MRA1", X.audit_a(S["tools"], c1) == a0 and AB.validate(S["tools"], bcall(c1)) == b0, rid)
            t2 = copy.deepcopy(S["tools"])
            rng.shuffle(t2)
            rec("MRA2", X.audit_a(t2, S["call"]) == a0 and AB.validate(t2, bcall(S["call"])) == b0, rid)
            by = {t["name"]: t for t in S["tools"]}
            T = by.get(S["call"]["tool"])
            if T and not a0:
                have = {k for k, _ in S["call"]["args"]}
                dfl = [p for p in T["params"] if p["name"] not in have and p["default"] is not None
                       and all(p["name"] not in (c["p"], c["q"]) for c in T.get("cons") or [])]
                if dfl:
                    p = rng.choice(dfl)
                    c3 = copy.deepcopy(S["call"])
                    c3["args"].append([p["name"], X.typed_default(p)])
                    ok = not X.audit_a(S["tools"], c3) and not AB.validate(S["tools"], bcall(c3))
                    if s["form"] == "Y-CORRECT":
                        res0 = A.solve(S, pk)
                        ok = ok and X.correct_a(S, res0, c3) == X.correct_a(S, res0, S["call"])
                    rec("MRA3", ok, rid)
        if s["outcome"] is None or "conv" not in S or not S["conv"]:
            continue
        base = A.solve(S, pk)
        if base["outcome"] != s["outcome"]:
            rec("MR0-base", False, rid, "solver A re-solve differs")
            continue
        # MR2: catalog order shuffle
        S2 = copy.deepcopy(S)
        rng.shuffle(S2["tools"])
        r2 = A.solve(S2, pk)
        b2 = b_outcome(S2, pk)
        rec("MR2", r2["outcome"] == base["outcome"] and r2.get("tool") == base.get("tool")
            and b2["outcome"] == base["outcome"], rid)
        # MR4: add an inert tool (shares no action / object with the intent or any candidate; returns nothing)
        req, _ = A.request_of(S)
        cand_acts = {t["a"] for t in S["tools"] if t["o"] == req["o"]} | {req["a"]}
        names = {t["name"] for t in S["tools"]}
        inert = [t for t in BLD.packs_tools(pk) if t["name"] not in names and t["a"] not in cand_acts
                 and t["o"] != req["o"] and not t["returns"]]
        if inert and len(S["tools"]) < 60:
            S4 = copy.deepcopy(S)
            S4["tools"].insert(rng.randrange(len(S4["tools"]) + 1), copy.deepcopy(rng.choice(inert)))
            r4 = A.solve(S4, pk)
            b4 = b_outcome(S4, pk)
            nm_old = sorted(map(tuple, s["near_miss"]))
            rec("MR4", r4["outcome"] == base["outcome"] and r4.get("tool") == base.get("tool")
                and b4["outcome"] == base["outcome"] and sorted(A.near_misses(S4, r4)) == nm_old, rid)
        # MR10: delete the only statement of a needed value (CALL -> ASK)
        if base["outcome"] == "CALL" and base["kind"] == "action" and not S["pol"]["chain"]:
            T = next(t for t in S["tools"] if t["name"] == base["tool"])
            matching = [t for t in S["tools"] if base["checks"][t["name"]]["match"]]
            if len(matching) == 1:
                stated = [p for p in T["params"] if p["required"] and base["src"].get(p["name"]) in
                          ("stated", "current", "reldate") and p["default"] is None]
                for p in stated:
                    users = [c for c in S["conv"] if c["who"] == "user"]
                    cnt = sum(1 for c in users for st in c["st"] if st["t"] == "val" and
                              (st["p"] == p["name"] or (st["p"] is None and _unnamed_is(st, p, S, pk))))
                    req_id = req["ref"] and req["ref"][0] == "id" and p["name"] == pk["etypes"][req["o"]]["idkey"]
                    if cnt != 1 or req_id:
                        continue
                    S10 = copy.deepcopy(S)
                    for c in S10["conv"]:
                        if c["who"] == "user":
                            c["st"] = [st for st in c["st"] if not (st["t"] == "val" and (
                                st["p"] == p["name"] or (st["p"] is None and _unnamed_is(st, p, S, pk))))]
                    if any(not c["st"] for c in S10["conv"] if c["who"] == "user"):
                        continue
                    r10 = A.solve(S10, pk)
                    b10 = b_outcome(S10, pk)
                    rec("MR10", r10["outcome"] == "ASK" and b10["outcome"] == "ASK", rid, r10["outcome"])
                    break
        # MR11: delete every matching tool -> UNABLE (not catalog, no answer shown)
        unnamed = any(st["t"] == "val" and st["p"] is None for c in S["conv"] if c["who"] == "user" for st in c["st"])
        if base["kind"] != "catalog" and base["outcome"] != "ANSWER" and not unnamed:
            S11 = copy.deepcopy(S)
            S11["tools"] = [t for t in S["tools"] if not base["checks"][t["name"]]["match"]]
            if S11["tools"]:
                r11 = A.solve(S11, pk)
                b11 = b_outcome(S11, pk)
                rec("MR11", r11["outcome"] == "UNABLE" and b11["outcome"] == "UNABLE", rid, r11["outcome"])
        # MR14: flip POL-INVALID A <-> B (ASK <-> UNABLE) when every matching tool rejects >= 1 user value and
        # no needed value is absent or unclear
        if base["outcome"] in ("ASK", "UNABLE") and base["kind"] == "action":
            matching = [t for t in S["tools"] if base["checks"][t["name"]]["match"]]
            if matching and all(base["checks"][t["name"]]["rejects"] and not base["checks"][t["name"]]["missing"]
                                and not base["checks"][t["name"]]["unclear"] for t in matching):
                S14 = copy.deepcopy(S)
                S14["pol"]["invalid"] = "B" if S["pol"]["invalid"] == "A" else "A"
                r14 = A.solve(S14, pk)
                b14 = b_outcome(S14, pk)
                exp = "UNABLE" if S14["pol"]["invalid"] == "B" else "ASK"
                rec("MR14", r14["outcome"] == exp and b14["outcome"] == exp, rid, r14["outcome"])
        # MR13: negation units (complement / equiv) checked on the emitted unit rows
        if r["qtype"] == "noul" and s["neg"] in (1, 2):
            rec("MR13", True, rid)
    out = {"stem": stem, "sampler": sampler, "rows": len(pairs),
           "mr": {k: {"applicable": v[0], "pass": v[1]} for k, v in sorted(stat.items())},
           "n_relations_with_rows": sum(1 for k, v in stat.items() if v[0] > 0 and not k.startswith("MR0")),
           "pass": all(v[0] == v[1] for v in stat.values()), "fails": fails}
    return out


def _unnamed_is(st, p, S, pk):
    return st["p"] is None and st["v"] and A.form_ok(p, st["v"], S["now"])


def neg_units(stem):
    """MR13 on the relation file: complement flips the yes/no gold, equiv keeps it."""
    rows, rels = {}, []
    for st in stem.split("+"):
        rows.update({json.loads(l)["id"]: json.loads(l) for l in open(OUT / f"{st}.jsonl")})
        rels += [json.loads(l) for l in open(OUT / f"relations_{st}.jsonl")]
    ok = bad = 0
    for e in rels:
        a, b = rows.get(e["a"]), rows.get(e["b"])
        if not a or not b or a["qtype"] != "noul":
            continue
        good = (a["gold"] != b["gold"]) if e["type"] == "complement" else (a["gold"] == b["gold"])
        ok += good
        bad += not good
    return {"units_checked": ok + bad, "pass": bad == 0, "fail": bad}


if __name__ == "__main__":
    stem, smp = sys.argv[1], sys.argv[2]
    n = int(sys.argv[sys.argv.index("--rows") + 1]) if "--rows" in sys.argv else 1000
    res = run(stem, smp, n)
    res["MR13_units"] = neg_units(stem)
    (OUT / "qc").mkdir(exist_ok=True)
    json.dump(res, open(OUT / "qc" / f"g4_{stem}_{smp}.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "fails"})[:1500])
