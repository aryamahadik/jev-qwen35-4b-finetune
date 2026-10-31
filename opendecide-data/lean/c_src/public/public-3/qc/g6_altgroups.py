#!/usr/bin/env python3
"""Recheck r1 (independent): G6 robustness to the CV grouping. qc/g6.py groups folds by group_id (one record), which
splits v2.0 matched sets across folds and drives many cells far BELOW chance (a held-out set member is predicted with
its training-fold siblings' gold). A below-chance artefact could mask a real above-chance cue, so the same views,
models and spec 8 rule (accuracy <= chance + 2 pp, point estimate, no p-value) are re-run with folds grouped by
(1) meta.match_set (twin set; group_id when absent) and (2) meta.card_id (PREREG A19 'grouped-by-card CV').
Pooled, per dataset on pooled CV, and per dataset own CV, every cell. Writes qc/g6_altgroups.json."""
import json, sys
import g6 as G
import qclib as Q


def run(key):
    rows = [dict(r) for f in G.FILES for r in Q.load(f)]
    for r in rows:
        r["group_id"] = str(key(r))
    yn = [r for r in rows if r["qtype"] == "noul"]
    ch = [r for r in rows if r["qtype"] == "choice"]
    out, prob = {}, []
    for kind, sub, fn in (("yn", yn, G.eval_yn), ("choice", ch, G.eval_choice)):
        for k, (acc, chance, cells, fails) in fn(sub).items():
            out[f"pooled:{k}"] = {"acc": round(acc, 4), "chance": round(chance, 4), "margin_pp": round(100 * (acc - chance), 2),
                                  "per_dataset_pooled_cv": cells}
            if acc > chance + 0.02 or fails:
                prob.append(f"pooled:{k}" + (f" {[f[0] for f in fails]}" if fails else ""))
        for src in sorted({r["source"] for r in sub}):
            part = [r for r in sub if r["source"] == src]
            for k, (acc, chance, cells, fails) in fn(part).items():
                c = cells[src]
                out[f"own_cv:{src}:{k}"] = c
                if c["acc"] > c["chance"] + 0.02:
                    prob.append(f"own_cv:{src}:{k}")
    return out, prob


def main():
    res, allp = {}, []
    for name, key in (("match_set", lambda r: r["meta"].get("match_set") or r["group_id"]),
                      ("card_id", lambda r: r["meta"]["card_id"])):
        G.log(f"grouping {name}")
        out, prob = run(key)
        worst = sorted(((v["margin_pp"], k) for k, v in out.items() if k.startswith("own_cv")), reverse=True)[:5]
        worst2 = sorted(((c["margin_pp"], k, s) for k, v in out.items() if k.startswith("pooled")
                         for s, c in v["per_dataset_pooled_cv"].items()), reverse=True)[:5]
        res[name] = {"pass": not prob, "problems": prob, "worst_own_cv": worst, "worst_pooled_per_dataset": worst2,
                     "cells": out}
        allp += [f"{name}:{p}" for p in prob]
        print(name, "pass", not prob, prob[:6], "worst own", worst[:3], "worst pooled/ds", worst2[:3], flush=True)
    o = {"gate": "G6 grouping robustness", "pass": not allp, "problems": allp,
         "rule": "spec 8 G6: accuracy <= chance + 2 pp (point estimate, no p-value), every view x model, pooled + per dataset",
         **res}
    (Q.HERE / "g6_altgroups.json").write_text(json.dumps(o, indent=1))


if __name__ == "__main__":
    main()
