"""F5 gates on an output set: G3 round trip (structure parse == generator structure, question parse == generator LF and
k, solver B on the parsed structure == stored gold, card parse: printed keys cover the re-computed trigger set, short
cards exact, identical card per base), G15 (fmt1 loader_check under a fresh random permutation + check_rows + unit
rules + real-tokenizer length), negcount quotas, balance report.

  python -m gen.gates --set smoke|candidates|qc|mixdev
"""
from __future__ import annotations

import argparse
import collections
import json
import random
import re
import sys

from . import parse as PZ
from . import solver_b as SB
from .common import OUT, TMP, negc, read_jsonl, write_jsonl


# ---------------------------------------------------------------------------------------------------------------------
# canonical structures (generator side vs parser side)

def canon_s1_gen(M):
    def lit(l):
        if l is None:
            return None
        if l["t"] in ("adj", "out"):
            return ("adj", l["w"], l["pol"])
        if l["t"] == "has":
            return ("has", l["w"], l["pol"])
        if l["t"] == "num":
            return ("num", l["q"], l["op"], l["n"])
        return ("cat", l["c"], l["v"], l["pol"])

    def head(h):
        return ("adj", h["word"], h["pol"]) if h["kind"] == "adj" else ("deon", h["role"], h["modal"], h["verb"])
    rules = sorted((r["id"], r["form"], tuple(lit(c) for c in r["conds"]), lit(r.get("exc")),
                    r.get("exc_kw"), head(r["head"])) for r in M["rules"])
    facts = {}
    for k, f in M["fact_form"].items():
        if f != "omit":
            t, w = k.split(":", 1)
            facts[(t, w)] = f
    if M.get("decoy_text"):
        for w in M["decoy_text"]:
            facts[("adj", w)] = "pos"
    nums = {q: v for q, v in M["nums"].items() if v is not None}
    cats = {c: v for c, v in M["cats"].items() if v is not None}
    table = sorted((c["role"], c["verb"], c["cell"]) for c in M.get("table", []))
    am = None
    if M.get("amount"):
        a = M["amount"]
        am = (a["rid"], a["name"], a["qty"], a["kind"], a["limit"])
    return {"rules": rules, "facts": sorted(facts.items()), "nums": sorted(nums.items()),
            "cats": sorted(cats.items()), "table": table, "amount": am, "subj": M["subj"]}


def canon_s1_parsed(S):
    def lit(l):
        if l is None:
            return None
        if l["t"] == "adj":
            return ("adj", l["w"], l["pol"])
        if l["t"] == "has":
            return ("has", l["w"], l["pol"])
        if l["t"] == "num":
            return ("num", l["q"], l["op"], l["n"])
        return ("cat", l["c"], l["v"], l["pol"])

    def head(h):
        return ("adj", h["word"], h["pol"]) if h["kind"] == "adj" else ("deon", h["role"], h["modal"], h["verb"])
    rules = sorted((r["id"], r["form"], tuple(lit(c) for c in r["conds"]), lit(r.get("exc")),
                    r.get("exc_kw"), head(r["head"])) for r in S["rules"])
    nums = {q: v[0] for q, v in S["nums"].items()}
    am = None
    if S["amount"]:
        a = S["amount"]
        am = (a["rid"], a["name"], a["qty"], a["kind"], a["limit"])
    return {"rules": rules, "facts": sorted(S["facts"].items()), "nums": sorted(nums.items()),
            "cats": sorted(S["cats"].items()), "table": sorted((c["role"], c["verb"], c["cell"]) for c in S["table"]),
            "amount": am, "subj": S["subj"]}


def norm_lf(lf):
    """Canonical LF: double negations kept (they carry k), subjects as given."""
    return json.dumps(lf, sort_keys=True)


# ---------------------------------------------------------------------------------------------------------------------
# trigger re-computation on the parsed text and questions (parser side; trigger table 3.1)

def triggers_s1(S, qfams):
    keys = {"SEM-01", "SEM-02" if S["world"] == "closed" else "SEM-03"}
    for r in S["rules"]:
        if r["form"] == "if":
            keys.add("SEM-07")
            if r.get("exc"):
                keys.add("SEM-15")
        elif r["form"] == "unless":
            keys.add("SEM-05")
        elif r["form"] == "onlyif":
            keys.add("SEM-06")
        elif r.get("exc"):
            keys.add("SEM-15")
        if r["head"]["kind"] == "deon":
            keys.add("SEM-24")
        if r["head"]["kind"] == "adj" and r["head"]["pol"] == "aff":
            keys.add("SEM-18")
        for l in r["conds"] + ([r["exc"]] if r.get("exc") else []):
            if l["t"] == "num":
                keys |= {"SEM-08", "SEM-12", "SEM-14"}
            if l["t"] == "adj" and l["pol"] == "aff":
                keys.add("SEM-18")
            if l["t"] == "has" and l["pol"] == "lacks":
                keys.add("SEM-19")
    if S["table"]:
        keys.add("SEM-24")
    if S["amount"]:
        keys |= {"SEM-08", "SEM-12", "SEM-14"}
    if any(v[0] != "NR" for v in S["nums"].values()):
        keys |= {"SEM-12", "SEM-14"}
    if any(v[0] == "NR" for v in S["nums"].values()) or any(v == "NR" for v in S["cats"].values()):
        keys.add("SEM-04")
    if S["cats"]:
        keys.add("SEM-17")
    if any(f == "aff" for f in S["facts"].values()):
        keys.add("SEM-18")
    if any(f == "lacks" for f in S["facts"].values()):
        keys.add("SEM-19")
    if S["decoys"]:
        keys.add("SEM-28")
    keys |= qfam_keys(qfams)
    return keys


QFAM = {"C13": {"SEM-10"}, "C16": {"SEM-28"}, "C12": {"SEM-24"}, "C9": {"SEM-08", "SEM-12", "SEM-14"},
        "C5": {"SEM-19"}, "C3": {"SEM-19", "SEM-27"}, "C8": {"SEM-22"}, "C11": {"SEM-23"}, "C14": {"SEM-25"},
        "C15": {"SEM-26", "SEM-27"}, "C10": {"SEM-11"}, "C7": {"SEM-20"}, "C6": {"SEM-18"}}


def qfam_keys(fams):
    out = set()
    for f in fams:
        out |= QFAM.get(f, set())
    return out


# ---------------------------------------------------------------------------------------------------------------------
# G3

def g3(rows, side, bases):
    sid = {s["id"]: s for s in side}
    bmap = {b["base_id"]: b for b in bases}
    by_base = collections.defaultdict(list)
    for r in rows:
        by_base[sid[r["id"]]["base_id"]].append(r)
    res = collections.Counter()
    errs = []
    for bid, rs in by_base.items():
        b = bmap[bid]
        sampler = "INV" if b.get("inverted") else b["sampler"]
        cards = {r["card"] for r in rs}
        if len(cards) != 1:
            res["card_not_identical"] += 1
            errs.append((bid, "card differs across rows"))
        keys, consts = PZ.parse_card(rs[0]["card"])
        from . import parse_more
        dp, mp = parse_more.decl_parsers(sampler)
        ctx = {"affixed": consts["affixed"], "value_sets": consts["value_sets"], "decl_parsers": dp,
               "matrix_parsers": mp}
        qf_all = []
        try:
            S = parse_structure(sampler, rs, consts)
        except Exception as e:  # noqa: BLE001
            res["structure_parse_fail"] += 1
            errs.append((bid, f"structure: {e}"))
            continue
        ctx["noun"] = S.get("noun") if isinstance(S, dict) else None
        ctx["q_graded"] = S.get("q_graded") if isinstance(S, dict) else None
        lfs_parsed = []
        if canon_gen(sampler, b["M"]) != canon_parsed(sampler, S):
            res["structure_mismatch"] += 1
            errs.append((bid, "structure mismatch", canon_gen(sampler, b["M"]), canon_parsed(sampler, S)))
            continue
        for r in rs:
            s = sid[r["id"]]
            try:
                q = PZ.extract_question(r["instructions"])
                lf, k, fams, outer = PZ.parse_question(q, ctx)
            except Exception as e:  # noqa: BLE001
                res["question_parse_fail"] += 1
                errs.append((r["id"], f"question: {e}"))
                continue
            qf_all += fams
            lfs_parsed.append(lf)
            if norm_lf(lf) != norm_lf(s["lf"]):
                res["lf_mismatch"] += 1
                errs.append((r["id"], "lf", lf, s["lf"]))
                continue
            if k != s["k_neg"]:
                res["k_mismatch"] += 1
                errs.append((r["id"], "k", k, s["k_neg"]))
                continue
            S_row = S if s["row_type"] != "Vp" else S
            try:
                (gb,) = solve_b(sampler, S_row, [lf])
            except Exception as e:  # noqa: BLE001
                res["solver_b_fail"] += 1
                errs.append((r["id"], f"solver B: {e}"))
                continue
            if int(gb) != r["gold"]:
                res["gold_mismatch"] += 1
                errs.append((r["id"], "gold", int(gb), r["gold"]))
                continue
            res["rows_ok"] += 1
        trig = triggers(sampler, S, qf_all)
        if sampler == "S4":
            from . import parse_s4
            for lf in lfs_parsed:
                trig |= parse_s4.lf_triggers(lf)
        if not trig <= keys:
            res["trigger_not_printed"] += 1
            errs.append((bid, "triggered keys not printed", sorted(trig - keys)))
        if sid[rs[0]["id"]]["card_form"] == "short":
            world = {"SEM-02", "SEM-03"} & keys
            if keys != trig | world | {"SEM-01"}:
                res["short_card_not_exact"] += 1
                errs.append((bid, "short card", sorted(keys ^ (trig | world | {"SEM-01"}))))
    return res, errs


def parse_structure(sampler, rs, consts):
    if sampler == "S1":
        # the attack twin's state has one extra (attack) sentence; parse a non-attack row
        r = next((x for x in rs if x["role"] != "attack"), rs[0])
        S = PZ.s1_parse(r["state"], consts)
        for x in rs:
            if x["role"] == "attack":
                S2 = PZ.s1_parse(x["state"], consts)
                if len(S2["attack"]) != 1 or canon_s1_parsed(S2) != canon_s1_parsed(S):
                    raise ValueError("attack twin state differs beyond one attack sentence")
        return S
    from . import parse_more
    return parse_more.parse_structure(sampler, rs, consts)


def canon_gen(sampler, M):
    if sampler == "S1":
        return canon_s1_gen(M)
    from . import parse_more
    return parse_more.canon_gen(sampler, M)


def canon_parsed(sampler, S):
    if sampler == "S1":
        return canon_s1_parsed(S)
    from . import parse_more
    return parse_more.canon_parsed(sampler, S)


def solve_b(sampler, S, lfs):
    if sampler == "S1":
        return SB.s1_solve(S, lfs)
    from . import parse_more
    return parse_more.solve_b(sampler, S, lfs)


def triggers(sampler, S, qf):
    if sampler == "S1":
        return triggers_s1(S, qf)
    from . import parse_more
    return parse_more.triggers(sampler, S, qf) | qfam_keys(qf)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", required=True)
    ap.add_argument("--g15", action="store_true")
    a = ap.parse_args(argv)
    name = {"candidates": "candidates_r1", "qc": "qc_sample", "mixdev": "mixdev_S5"}.get(a.set, a.set)
    rows = read_jsonl(OUT / f"{name}.jsonl")
    side = read_jsonl(OUT / f"{name}.F5_polarity.jsonl")
    bases = read_jsonl(TMP / f"{name}.bases.jsonl")
    res, errs = g3(rows, side, bases)
    print(json.dumps(dict(res), indent=1))
    for e in errs[:12]:
        print(json.dumps(e, default=str)[:900])
    out = {"set": name, "G3": {"rows": len(rows), **dict(res), "pass": res.get("rows_ok", 0) == len(rows) and
                               len(res) == 1, "errors": [str(e)[:300] for e in errs[:50]]}}
    if a.g15:
        rels = read_jsonl(OUT / f"{name}.relations.jsonl")
        r15, e15, stats = g15(rows, rels)
        out["G15"] = {**dict(r15), "pass": r15.get("ok", 0) == len(rows) and not r15.get("unit_over_3") and
                      not r15.get("rel_split") and r15.get("check_rows_all") == 1, "served_tokens": stats,
                      "token_cap": 1900, "token_method": "tokenizers Qwen3.5-4B tokenizer.json over the Qwen chat "
                      "template text (system + user, thinking off) of decoder_io.user_msg (cygnet, "
                      "schema_branch_mark; instructions printed twice)", "errors": [str(e)[:200] for e in e15[:30]]}
        print(json.dumps(out["G15"], indent=1)[:1500])
    json.dump(out, open(OUT / f"{name}.gates.json", "w"), indent=1)



# ---------------------------------------------------------------------------------------------------------------------
# G15: loader round trip under a fresh random permutation, check_rows, unit rules, real-tokenizer length

_TOK = None


def tokenizer():
    global _TOK
    if _TOK is None:
        from tokenizers import Tokenizer
        from .common import CSRC
        _TOK = Tokenizer.from_file(str(CSRC / "public" / "public-3" / "tmp" / "tokenizer.json"))
    return _TOK


def served_tokens(row):
    """Real-tokenizer length of the served prompt: Qwen3.5 chat template (system + user, thinking off), decoder_io
    cygnet style, schema_branch_mark layout (instructions printed twice), identity option order."""
    from fmt1 import card as fc
    dio = fc._dio()
    with fc._serving(dio, 2):
        user = dio.user_msg(row, [0, 1])
        system = dio.CYGNET_SYSTEM
    txt = (f"<|im_start|>system\n{system}<|im_end|>\n<|im_start|>user\n{user}<|im_end|>\n"
           f"<|im_start|>assistant\n<think>\n\n</think>\n\n")
    return len(tokenizer().encode(txt, add_special_tokens=False).ids)


def g15(rows, rels, *, cap=1900, seed=20261004):
    from fmt1 import card as fc
    rng = random.Random(seed)
    res = collections.Counter()
    errs = []
    lens = []
    for r in rows:
        perm = [0, 1]
        rng.shuffle(perm)
        out = fc.loader_check(r, perm=perm)
        if not out["ok"]:
            res["loader_fail"] += 1
            errs.append((r["id"], out["problems"][:3]))
            continue
        gl = out["gold_letter"]
        shown = "Yes" if (perm.index(0) == "AB".index(gl)) else "No"
        if (shown == "Yes") != (r["gold"] == 1):
            res["gold_letter_map_fail"] += 1
            errs.append((r["id"], "gold letter"))
            continue
        n = served_tokens(r)
        lens.append(n)
        if n >= cap:
            res["over_cap"] += 1
            errs.append((r["id"], f"{n} tokens"))
            continue
        res["ok"] += 1
    # units: every relation pair shares a call_id; <= 3 rows per call_id; no row >= 2000 tokens (F5 has no long units)
    by_call = collections.Counter(r["call_id"] for r in rows)
    cid = {r["id"]: r["call_id"] for r in rows}
    res["units"] = len(by_call)
    res["unit_over_3"] = sum(1 for v in by_call.values() if v > 3)
    res["rel_split"] = sum(1 for x in rels if cid.get(x["a"]) != cid.get(x["b"]))
    from fmt1 import card as fc2
    try:
        fc2._td().check_rows(rows)
        res["check_rows_all"] = 1
    except Exception as e:  # noqa: BLE001
        res["check_rows_all"] = 0
        errs.append(("check_rows", str(e)[:300]))
    lens.sort()
    stats = {"max": lens[-1] if lens else None, "median": lens[len(lens) // 2] if lens else None,
             "p95": lens[int(len(lens) * 0.95)] if lens else None, "min": lens[0] if lens else None}
    return res, errs, stats


if __name__ == "__main__":
    main()
