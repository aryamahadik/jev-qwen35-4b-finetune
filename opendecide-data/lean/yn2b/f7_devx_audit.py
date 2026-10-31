"""Audit of the blind F7 devx v2 (yn2b/f7_devx_build.py outputs). CPU only; prints counts, never row text from
dev / eval / OHS / JevBench files; never opens OHS-3 data.

It runs, on the devx files alone:
  A. the ship audit's own row-level checks (yn2b/f7_precheck.py functions, imported read-only): schema, LF contract,
     cue <-> LF consistency, own-evaluator gold, distractor deletion, bivalence lines, non-presupposing distractors,
     choice LFs, tag rules (3.3), devx balance (4.1c / 4.2c), yes/no restatement (5.l), EXCLUDE X1-X12 (7.1), ladder
     integrity / relations / rung semantics (9.x), the SPEC 7.3 cue-share rule (8.9);
  B. every checklist section-3 target, computed on devx (the ship audit computes most of them on train and dev only);
  C. twin integrity (each yes/no question appears once per twin with opposite golds; twins share source, kind, state
     format and state negation);
  D. with --decontam: the ship audit's decontamination checks 8.1-8.8, 8.11, 8.12, 8.14, 8.15 on devx (about 30 s).

Usage (from opendecide-data/lean):
  ../.venv/bin/python yn2b/f7_devx_audit.py [--dir DIR] [--decontam]
Writes yn2b/f7_devx_audit.json (or DIR/f7_devx_audit.json for a dry dir).
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

LEAN = Path(__file__).resolve().parents[1]
for _p in (str(LEAN), str(LEAN / "yn2b"), str(LEAN / "extra")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.dont_write_bytecode = True
import f7_precheck as F  # noqa: E402  (the ship audit; read-only import)


def share(k, n):
    return round(k / n, 4) if n else None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(LEAN / "data/v14_parts"))
    ap.add_argument("--decontam", action="store_true")
    a = ap.parse_args(argv)
    D = Path(a.dir)
    rows = F.load_rows(D / "f7_devx.jsonl")
    metas = F.load_rows(D / "f7_devx_meta.jsonl")
    rels = F.load_rows(D / "f7_devx_relations.jsonl")
    ctx = F.Ctx({"train": [], "probe": [], "devx": rows}, metas, {"devx": rels}, F.Opts(), log=lambda s: None)
    out, fails = {}, []

    def rec(key, ok, value):
        out[key] = {"pass": bool(ok), "value": value}
        if not ok:
            fails.append(key)

    # ------------------------------------------------------------------ A. ship-audit row-level checks
    rec("A.valid_rows", len(ctx.devx) == len(rows), {"valid": len(ctx.devx), "rows": len(rows),
                                                      "errors": [(R["row"]["id"], R["an"]["errors"][:2])
                                                                 for R in ctx.R if not R["an"]["ok"]][:6]})
    for fn in (F.check_schema, F.check_gold, F.check_ladders):
        for s in fn(ctx):
            if s.id in ("2.3", "2.3b"):   # decide2 is run separately (golden_src/gen3/v3_nested_negation.py)
                continue
            if s.id == "9.4":             # R0 share is over train / dev ladders; devx is checked in C below
                continue
            rec(f"A.{s.id}", s.status == "PASS", s.value)
    mism = collections.defaultdict(list)
    for R in ctx.ok:
        for it in set(R["m"]["phen"]):
            if F.tag_rule(it, R) is False:
                mism[it].append(R["row"]["id"])
    rec("A.3.3", not mism, {k: v[:3] for k, v in mism.items()})
    bc, br, bs, ncell, nstr, n = F.balance_set(ctx.devx, "devx")
    rec("A.4.1c", not bc and not br, {"bad_cells": bc, "bad_rungs": br, "cells": ncell, "yes_no_rows": n})
    rec("A.4.2c", not bs, {"bad_strata": dict(list(bs.items())[:10]), "strata": nstr})
    s5 = F.yn_restates(ctx)
    rec("A.5.l", s5.status == "PASS", s5.value)
    xs = collections.Counter()
    for R in ctx.ok:
        for x in F.exclude_hits(ctx, R):
            xs[x] += 1
    rec("A.7.1", not xs, dict(xs))
    import check_yn2b as cy
    cs = cy.cue_shares([("F7X", "instruction", R["row"]["instructions"], bool(R["an"]["depth"] % 2))
                        for R in ctx.ok])
    rec("A.8.9", all(v["pass"] for v in cs.values()), cs)

    # ------------------------------------------------------------------ B. section-3 targets on devx
    dv = ctx.devx
    yn = [R for R in dv if R["an"]["yn"]]
    ch = [R for R in dv if not R["an"]["yn"]]
    N = len(dv)
    dc = collections.Counter(R["an"]["depth"] for R in dv)
    mix_ok = all(F.within(dc[d], N, t, F.DEPTH_MIX_TOL) for d, t in F.DEPTH_MIX.items()) and \
        sum(v for k, v in dc.items() if k >= 4) / N <= F.DEPTH4_MAX + 1e-12
    rec("B.depth_mix", mix_ok, {d: [dc[d], share(dc[d], N)] for d in sorted(dc)})
    odd = sum(v for k, v in dc.items() if k % 2)
    rec("B.parity", F.share_ok(odd, N, *F.PARITY_SHARE), share(odd, N))
    cells = collections.defaultdict(lambda: [0, 0])
    for R in yn:
        cells[R["m"]["rung"]][0] += R["row"]["gold"]
        cells[R["m"]["rung"]][1] += 1
    tp = collections.defaultdict(lambda: [0, 0])
    for R in dv:
        tp["rung=" + R["m"]["rung"]][0] += R["an"]["truth_P"]
        tp["rung=" + R["m"]["rung"]][1] += 1
        if R["an"]["yn"]:
            tp["depth=%d" % R["an"]["depth"]][0] += R["an"]["truth_P"]
            tp["depth=%d" % R["an"]["depth"]][1] += 1
    bad = {k: v for k, v in tp.items() if not F.share_ok(v[0], v[1], *F.TRUTHP_RUNG_DEPTH)}
    rec("B.truthP_rung_depth", not bad, {"bad": bad, "R0_ladders": [sum(R["an"]["truth_P"] for R in dv
                                                                       if R["m"]["rung"] == "R0"),
                                                                   sum(1 for R in dv if R["m"]["rung"] == "R0")]})
    ql = collections.defaultdict(lambda: [0, 0])
    for R in dv:
        if R["an"]["qlabel"]:
            ql[R["an"]["qlabel"]][0] += R["an"]["truth_P"]
            ql[R["an"]["qlabel"]][1] += 1
    bad = {k: v for k, v in ql.items() if not F.share_ok(v[0], v[1], *F.TRUTHP_LABEL)}
    rec("B.truthP_label", not bad, bad)
    neg = sum(1 for R in ch if R["an"]["select_false"])
    oc = collections.Counter(len(R["row"]["options"]) for R in ch)
    pos_bad = []
    for k in oc:
        rk = [R for R in ch if len(R["row"]["options"]) == k]
        pc = collections.Counter(R["m"]["gold"] for R in rk)
        pos_bad += [f"k={k} pos={p}" for p in range(k) if not F.within(pc[p], len(rk), 1 / k, F.CHOICE_POS_TOL)]
    rec("B.choice", F.share_ok(len(ch), N, *F.CHOICE_SHARE) and F.share_ok(neg, len(ch), *F.CHOICE_NEGSEL)
        and not pos_bad and all(3 <= k <= 5 for k in oc),
        {"share": share(len(ch), N), "negated_selection": share(neg, len(ch)), "option_counts": dict(oc),
         "position_misses": pos_bad, "depths": dict(collections.Counter(R["an"]["depth"] for R in ch))})
    per = {d: [sum(1 for R in dv if R["an"]["depth"] == d and R["an"]["n_dist"]), dc[d]] for d in range(4)}
    kk = sum(1 for R in dv if R["an"]["n_dist"])
    rec("B.distractors", kk / N >= F.DIST_ANY_MIN - 1e-12 and all(b and a / b >= F.DIST_PER_DEPTH_MIN - 1e-12
                                                                  for a, b in per.values()),
        {"overall": share(kk, N), "per_depth": {d: share(a, b) for d, (a, b) in per.items()}})
    mm = sum(1 for R in dv if (R["an"]["n_all"] % 2) != (R["an"]["depth"] % 2))
    rec("B.parity_mismatch", mm / N >= F.PARITY_MISMATCH_MIN - 1e-12, share(mm, N))
    oddr = [R for R in dv if R["an"]["depth"] % 2]
    arlex = sum(1 for R in oddr if R["m"]["rung"] == "AR" or (R["an"]["scoping"] and all(
        c["cls"] == "lexical" for c in R["an"]["scoping"])))
    rec("B.ar_lexical_only", arlex / len(oddr) >= F.AR_LEXONLY_MIN - 1e-12, share(arlex, len(oddr)))
    toks, lex_tok = collections.Counter(), collections.Counter()
    for R in dv:
        for c in R["m"]["cues"]:
            if c["cls"] != "lookalike":
                toks[F.CLASS5[c["cls"]]] += 1
                lex_tok[c["lexeme"].lower()] += 1
    nt = sum(toks.values())
    rec("B.cue_mix", all(F.share_ok(toks[k], nt, lo, hi) for k, (lo, hi) in F.CUE_MIX.items()),
        {k: share(toks[k], nt) for k in F.CUE_MIX})
    notnt = lex_tok["not"] + lex_tok["n't"]
    top = lex_tok.most_common(1)[0]
    rec("B.not_and_top_lexeme", notnt / nt <= F.NOT_NT_MAX + 1e-12 and top[1] / nt <= F.LEXEME_MAX + 1e-12,
        {"not_nt": share(notnt, nt), "top": [top[0], share(top[1], nt)]})
    pc = collections.Counter()
    for R in dv:
        for c in R["an"]["scoping"]:
            pc["yn_key+answer_map" if c["position"] in ("yn_key", "answer_map") else c["position"]] += 1
    npos = sum(pc.values())
    rec("B.positions", all(F.share_ok(pc[k], npos, lo, hi) for k, (lo, hi) in F.POSITION_MIX.items())
        and not pc.get("state"), {k: share(pc[k], npos) for k in F.POSITION_MIX})
    st_tot = collections.Counter(R["m"]["card_style"] for R in yn)
    sbad = {}
    for st, nst in st_tot.items():
        for key, f in (("depth", lambda R: R["an"]["depth"]), ("gold", lambda R: R["row"]["gold"])):
            grp = collections.defaultdict(list)
            for R in yn:
                grp[f(R)].append(R)
            for g, rs in grp.items():
                k = sum(1 for R in rs if R["m"]["card_style"] == st)
                if not F.within(k, len(rs), nst / len(yn), F.CARD_STYLE_TOL):
                    sbad[f"{st}:{key}={g}"] = [k, len(rs)]
    nc_frame = [R["row"]["id"] for R in yn if not (R["row"].get("card") or "").strip()
                and not F.CARDLESS_OK_RE.search(R["row"]["instructions"])]
    rec("B.card_style_and_cardless", not sbad and not nc_frame,
        {"styles": {k: share(v, len(yn)) for k, v in st_tot.items()}, "bad": sbad, "cardless_bad_frame": nc_frame})
    a_ = [R for R in yn if R["an"]["state_neg"]]
    b_ = [R for R in yn if not R["an"]["state_neg"]]
    ya, yb = sum(F.gold_yes(R) for R in a_) / len(a_), sum(F.gold_yes(R) for R in b_) / len(b_)
    rec("B.state_negation", abs(ya - yb) <= F.STATE_NEG_TOL + max(0.5 / len(a_), 0.5 / len(b_)),
        {"with": [round(ya, 4), len(a_)], "without": [round(yb, 4), len(b_)]})
    y = [R["row"]["gold"] for R in yn]
    preds = collections.defaultdict(list)
    for R in yn:
        for k, v in F.comp_preds(R).items():
            preds[k].append(v)
    res = {k: round(F.acc(v, y), 4) for k, v in preds.items()}
    c2d = {}
    for d in sorted({R["an"]["depth"] for R in yn}):
        idx = [i for i, R in enumerate(yn) if R["an"]["depth"] == d]
        c2d[d] = round(F.acc([preds["C2 count all cues"][i] for i in idx], [y[i] for i in idx]), 4)
    big_d = {d: v for d, v in c2d.items() if sum(1 for R in yn if R["an"]["depth"] == d) >= 10}
    it21 = [R for R in yn if 21 in R["m"]["phen"]]
    c7 = sum(1 for R in it21 if int(bool(R["m"]["antonym_gold"])) != R["row"]["gold"]) / len(it21)
    comp_ok = (F.C1_BAND[0] <= res["C1 ignore negation"] <= F.C1_BAND[1] and res["C2 count all cues"] <= F.C2_MAX
               and all(v <= F.C2_DEPTH_MAX for v in big_d.values()) and res["C3 count syntactic cues"] <= F.C3_MAX
               and res["C4 outer cue only"] <= F.C4_MAX and res["C5 inner cue only"] <= F.C5_MAX
               and all(res[f"C6 counter ignoring {c}"] <= F.C6_MAX for c in ("affixal", "lexical", "cross-sentence"))
               and c7 >= F.C7_WRONG_MIN)
    rec("B.composition", comp_ok, {**{k: v for k, v in res.items() if not k.startswith("C6i")},
                                   "C2_per_depth": c2d, "C7_antonym_wrong": round(c7, 4)})
    par = collections.defaultdict(lambda: [0, 0])
    for R in yn:
        for lx in {c["lexeme"].lower() for c in R["m"]["cues"]}:
            par[lx][0] += R["an"]["depth"] % 2
            par[lx][1] += 1
    bad = {k: v for k, v in par.items() if v[1] >= 10 and not F.share_ok(v[0], v[1], *F.LEXEME_ODD)}
    rec("B.lexeme_odd_share(>=10 rows)", not bad, bad)
    items = collections.Counter()
    for R in dv:
        for p in set(R["m"]["phen"]):
            items[p] += 1
    items[19] = sum(1 for R in dv if R["an"]["state_neg"])
    caps = {it: share(items[it], N) for it in F.ITEM_CAP}
    rec("B.items_present_and_caps", all(items[i] for i in range(1, 39))
        and all(caps[it] <= F.ITEM_CAP[it][0] + 1e-12 for it in caps),
        {"rows_per_item": {i: items[i] for i in range(1, 39)}, "caps": caps})
    lk = collections.Counter(m["ladder_kind"] for m in {R["m"]["ladder_id"]: R["m"] for R in dv}.values())
    nl = sum(lk.values())
    rec("B.ladder_kinds", lk["card"] / nl >= F.CARD_LADDER_MIN and F.share_ok(lk["multitext"], nl,
                                                                              *F.MULTITEXT_LADDERS), dict(lk))
    rec("B.devx_size", len(rows) >= F.DEVX_ROWS_MIN, len(rows))
    gold = [R["m"]["gold"] for R in ch]
    cp = {}
    for name, f in (("longest", lambda R: max(range(len(R["row"]["options"])),
                                              key=lambda i: len(R["row"]["options"][i]))),
                    ("most_cues", lambda R: max(range(len(R["row"]["options"])),
                                                key=lambda i: ctx.full_cue_count(R["row"]["options"][i]))),
                    ("fewest_cues", lambda R: min(range(len(R["row"]["options"])),
                                                  key=lambda i: ctx.full_cue_count(R["row"]["options"][i]))),
                    ("overlap", lambda R: max(range(len(R["row"]["options"])), key=lambda i: len(
                        set(F.words(R["row"]["options"][i])) & set(F.words(R["row"]["instructions"])))))):
        cp[name] = round(F.acc([f(R) for R in ch], gold), 4)
    rec("B.choice_probes", all(v <= F.PROBE_MAX for v in cp.values()), cp)
    gp = [R["m"]["gold"] / max(1, len(R["row"]["options"]) - 1) for R in ch]
    cr = {k: round(F.corr(x, gp) or 0.0, 4) for k, x in (
        ("negated_selection", [1 if R["an"]["select_false"] else 0 for R in ch]),
        ("depth", [R["an"]["depth"] for R in ch]), ("option_count", [len(R["row"]["options"]) for R in ch]),
        ("cue_count", [R["an"]["n_all"] for R in ch]))}
    cr.update({k: round(F.corr(x, y) or 0.0, 4) for k, x in (
        ("yes~cue_count", [R["an"]["n_all"] for R in yn]), ("yes~cue_parity", [R["an"]["n_all"] % 2 for R in yn]),
        ("yes~has_distractor", [1 if R["an"]["n_dist"] else 0 for R in yn]))})
    rec("B.correlations", all(abs(v) < F.CORR_MAX for v in cr.values()), cr)

    # ------------------------------------------------------------------ C. twin integrity
    byq = collections.defaultdict(list)
    for r in rows:
        if r["qtype"] == "noul":
            byq[(r["meta"]["pair"], r["instructions"], r["card"])].append(r["gold"])
    tw_bad = [k[:2] for k, v in byq.items() if sorted(v) != [0, 1]]
    lads = collections.defaultdict(list)
    for R in dv:
        lads[R["m"]["ladder_id"]].append(R)
    pairs = collections.defaultdict(list)
    for lid, rs in lads.items():
        pairs[rs[0]["m"]["pair"]].append(rs[0])
    p_bad = [p for p, (x, z) in pairs.items() if (x["m"]["source"], x["m"]["ladder_kind"], x["an"]["state_format"],
                                                  x["an"]["state_neg"]) != (z["m"]["source"], z["m"]["ladder_kind"],
                                                                            z["an"]["state_format"],
                                                                            z["an"]["state_neg"])]
    r0 = sum(1 for rs in lads.values() if any(R["m"]["rung"] == "R0" for R in rs))
    rec("C.twins", not tw_bad and not p_bad and len(pairs) * 2 == len(lads) and r0 == len(lads),
        {"pairs": len(pairs), "ladders": len(lads), "R0_ladders": r0, "question_mismatch": tw_bad[:5],
         "pair_strata_mismatch": p_bad})
    texts = collections.Counter(o for r in rows for o in [r["state"]])
    rec("C.state_reuse", True, {"distinct_states": len(texts), "ladders": len(lads)})

    # ------------------------------------------------------------------ D. decontamination (optional)
    if a.decontam:
        for s in F.check_decontam(ctx):
            if s.id in ("8.10", "8.13", "8.9"):
                continue
            rec(f"D.{s.id}", s.status == "PASS", s.value)
    out["_verdict"] = {"pass": not fails, "failed": fails, "checks": len([k for k in out if not k.startswith("_")])}
    dest = (LEAN / "yn2b/f7_devx_audit.json") if D.resolve() == (LEAN / "data/v14_parts").resolve() \
        else D / "f7_devx_audit.json"
    dest.write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps(out["_verdict"]))
    for k, v in out.items():
        if not k.startswith("_"):
            print(f"{'PASS' if v['pass'] else 'FAIL'}  {k}  {json.dumps(v['value'], default=str)[:150]}")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
