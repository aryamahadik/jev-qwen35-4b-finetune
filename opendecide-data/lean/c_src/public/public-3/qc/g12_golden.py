#!/usr/bin/env python3
"""Spec 3.1 "unused records only" re-check for public-3 (independent, prep5/B4; counts only, never prints text).

A public-3 record text (qclib.record_texts: the row's state minus its wrap template, or the record options) is USED
when, after loose normalisation (NFKC, casefold, non-word -> space):
  (a) it equals a golden_train state, or a line of a state / instructions / option, in any of the 204 sources; or
  (b) >= 8 words: > 50% of its word 8-grams occur in the 3E-adjacent sources' golden rows (state + instructions +
      options; the union of their 8-grams, a superset of the builder's per-row test, so it can only flag more); or
  (c) 3-7 words: its whole word sequence occurs inside a 3E-adjacent golden row.
Pass = 0 used records in rows_r1 + reserve (and mtdev, reported). Writes qc/g12_golden.json.
Reads data/v14_parts/golden_train.jsonl (C1's training set; an input the builder also used)."""
import json, sys, time
from collections import Counter
from pathlib import Path
import qclib as Q

LEAN = Q.P3.parents[2]
GT = LEAN / "data/v14_parts/golden_train.jsonl"
ADJ = {"binj_offensive", "br_convabuse", "br_edos", "br_emobank", "br_ghc", "br_hatemoji_build", "br_mams_acsa",
       "br_sarcasm_headlines", "br_xed_en", "gd_csc_sarcasm", "gd_edos_sexism", "gd_ghc_hate",
       "gd_hatemoji_build_v14", "std_hate", "toxic_conv"}   # builder's RELEVANT_GT list (build_records.py), re-typed


def grams(words, n=8):
    return [" ".join(words[i:i + n]) for i in range(len(words) - n + 1)]


def main():
    t0 = time.time()
    full, g8, adj_txt, n_rows, n_adj, srcs = set(), set(), [], 0, 0, set()
    with open(GT, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            n_rows += 1
            srcs.add(r.get("source"))
            parts = [r.get("state") or "", r.get("instructions") or ""] + [str(o) for o in (r.get("options") or [])]
            full.add(Q.h(Q.loose(parts[0])))
            for p in parts:
                for ln in p.split("\n"):
                    lz = Q.loose(ln)
                    if lz:
                        full.add(Q.h(lz))
            if r.get("source") in ADJ:
                n_adj += 1
                lz = Q.loose("\n".join(parts))
                adj_txt.append(lz)
                for g in grams(lz.split()):
                    g8.add(Q.h(g))
    joined = " " + " | ".join(adj_txt) + " "
    print(f"golden rows {n_rows} sources {len(srcs)} adjacent rows {n_adj} in {time.time() - t0:.0f}s", flush=True)
    res, prob = {}, []
    for name in Q.MIXED + ("public3_mtdev.jsonl",):
        c = Counter()
        for r in Q.load(name):
            for t in Q.record_texts(r)[0]:
                lz = Q.loose(t)
                w = lz.split()
                c["texts"] += 1
                if Q.h(lz) in full:
                    c["used_exact_or_line"] += 1
                elif len(w) >= 8:
                    gs = grams(w)
                    if sum(Q.h(g) in g8 for g in gs) / len(gs) > 0.5:
                        c["used_8gram_gt50pct"] += 1
                elif len(w) >= 3:
                    if " " + lz + " " in joined:
                        c["used_short_seq_in_adjacent"] += 1
                else:
                    c["lt3_words"] += 1
        used = c["used_exact_or_line"] + c["used_8gram_gt50pct"] + c["used_short_seq_in_adjacent"]
        res[name] = dict(c) | {"used_total": used}
        if used and name in Q.MIXED:
            prob.append(f"{name}: {used} used records")
    # control: formats-2's independent record parse of the same 3E sets carries its own in_golden_train flag (the
    # builder-side rule); this detector must flag the flagged records and leave most unflagged ones alone.
    F2 = LEAN / "c_src/formats/formats-2/records"
    ctl = Counter()
    for f in ("xed", "ghc", "edos", "mams_acsa", "mams_atsa"):
        for line in open(F2 / f"{f}.jsonl", encoding="utf-8"):
            x = json.loads(line)
            fl = bool((x.get("flags") or {}).get("in_golden_train"))
            if ctl[f"n_{fl}"] >= 2000:
                continue
            lz = Q.loose(x.get("text") or "")
            w = lz.split()
            hit = Q.h(lz) in full or (len(w) >= 8 and sum(Q.h(g) in g8 for g in grams(w)) / max(1, len(grams(w))) > 0.5) \
                or (3 <= len(w) < 8 and " " + lz + " " in joined)
            ctl[f"n_{fl}"] += 1
            ctl[f"hit_{fl}"] += hit
    control = {"formats2_flagged_records": ctl["n_True"], "detected": ctl["hit_True"],
               "formats2_unflagged_records": ctl["n_False"], "detected_unflagged": ctl["hit_False"]}
    out = {"check": "spec 3.1 unused records vs golden_train", "control": control, "golden_train": str(GT.relative_to(LEAN)),
           "golden_rows": n_rows, "golden_sources": len(srcs), "adjacent_rows": n_adj, "pass": not prob,
           "problems": prob, "files": res, "secs": round(time.time() - t0)}
    (Q.HERE / "g12_golden.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out)[:1500])


if __name__ == "__main__":
    main()
