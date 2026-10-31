"""GW remediation (16 Oct 2026, task W7 of the Zed orchestration): DROPS ONLY, seeded (20261013). Never relabels, never edits text.

Reads the ORIGINAL packaged pool (c2_build/_backup_w7/GW_candidates_c2.jsonl.orig) so it is idempotent, and writes the
remediated pool to data/c2_parts/GW/out/candidates_c2.jsonl plus qc/GW_w7_drops.json (ids, per type and round).

Per binding type (W1, W3, W4, W5, W7, W8; W2 and W6 are report-only and untouched):
  (1) feature drops: every feature the G7-style screen flags (same statistic as gw_g7.screen: pilot._pb_test / binom, Bonferroni
      alpha 0.01) is brought back to p >= P_TARGET by dropping, from the over-represented side only, the rows that carry it
      (yes/no: majority-label carriers; choice: gold-hit rows for an over-represented option feature). Rows carrying several
      flagged features are dropped first. A feature that cannot be fixed without dropping nearly all its carriers loses them all.
  (2) label rebalance: yes/no gold classes are down-sampled to equal size (expected share 50%); choice gold classes are
      handled by the option-feature rule above (a class over-represented against its expected share sum(1/k) is a flagged
      feature).
  rounds repeat until the screen passes or MAX_ROUNDS.
  (3) a type that still fails, or has < 300 rows, leaves GW.
"""
from __future__ import annotations

import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

CB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CB))
sys.path.insert(0, str(CB / "gblock" / "tools"))
import pilot as P  # noqa: E402
import gw_g7  # noqa: E402
from scipy.stats import binom, norm  # noqa: E402

GW = CB.parent / "data" / "c2_parts" / "GW"
ORIG = CB / "_backup_w7" / "GW_candidates_c2.jsonl.orig"
SEED = 20261013
P_TARGET = 0.05
MAX_ROUNDS = 12
MIN_ROWS = 300
BINDING = ["W1", "W3", "W4", "W5", "W7", "W8"]


def feature_tables(rows):
    """Same features and tests as gw_g7.screen, but returning everything needed to act on a flag."""
    yn = [i for i, r in enumerate(rows) if r["qtype"] == "noul"]
    ch = [i for i, r in enumerate(rows) if r["qtype"] == "choice"]
    out = {}  # feature -> dict(kind, p, carriers ...)
    feats = defaultdict(list)
    for n, i in enumerate(yn):
        r = rows[i]
        for f in P.ngrams(r["instructions"] + "\n" + r["state"]) | gw_g7.meta_feats(r):
            feats[f].append(i)
    for f, ix in feats.items():
        if len(ix) < P.N_MIN or len(ix) > len(yn) - P.N_MIN:
            continue
        k = sum(int(rows[j]["gold"]) for j in ix)
        x = max(k, len(ix) - k)
        out[("yn", f)] = dict(carriers=ix, k=k, p=float(min(1.0, binom.sf(x - 1, len(ix), 0.5))))
    units = defaultdict(lambda: defaultdict(list))
    for i in ch:
        r = rows[i]
        kinds = sorted(gw_g7.meta_feats(r))
        for j, o in enumerate(r["options"]):
            g = int(o == r["gold"])
            for f in {"opt:" + t for t in P.ngrams(o)} | {"optpos=%d" % j}:
                units[f][i].append(g)
                for m in kinds:
                    if m.startswith(("meta:wording", "meta:task")):
                        units[f + "&" + m][i].append(g)
    for f, per in units.items():
        ps, x, hits = [], 0, []
        for i, gs in per.items():
            k = len(rows[i]["options"])
            if len(gs) == k:
                continue
            ps.append((i, len(gs) / k))
            x += sum(gs)
            if sum(gs):
                hits.append(i)
        if len(ps) < P.N_MIN:
            continue
        p, mu = P._pb_test([q for _, q in ps], x)
        out[("ch", f)] = dict(rows=[i for i, _ in ps], pk=dict(ps), x=x, mu=mu, hits=set(hits), p=p)
    return out


def zstat(x, mu, var):
    return 0.0 if var <= 0 else (abs(x - mu) - 0.5) / math.sqrt(var)


def plan_round(rows, rng):
    tab = feature_tables(rows)
    thr = P.ALPHA / max(1, len(tab))
    nch = sum(1 for r in rows if r["qtype"] == "choice")
    # also flagged: a gold class (an option feature present in every row) above its expected share at nominal p < 0.05
    fails = sorted([(v["p"], key) for key, v in tab.items()
                    if v["p"] < thr or (key[0] == "ch" and len(v["rows"]) == nch and v["p"] < 0.05 and v["x"] > v["mu"])])
    if not fails:
        return set(), fails, thr
    drop = set()
    # how many flagged features each row carries on its over-represented side (greedy priority)
    prio = defaultdict(int)
    for _, key in fails:
        v = tab[key]
        if key[0] == "yn":
            maj = 1 if v["k"] * 2 >= len(v["carriers"]) else 0
            for j in v["carriers"]:
                if int(rows[j]["gold"]) == maj:
                    prio[j] += 1
        elif v["x"] > v["mu"]:
            for j in v["hits"]:
                prio[j] += 1
    for _, key in fails:
        v = tab[key]
        if key[0] == "yn":
            maj = 1 if v["k"] * 2 >= len(v["carriers"]) else 0
            alive = [j for j in v["carriers"] if j not in drop]
            k = sum(int(rows[j]["gold"]) for j in alive)
            n = len(alive)
            cand = [j for j in alive if int(rows[j]["gold"]) == maj]
            cand.sort(key=lambda j: (-prio[j], rng.random()))
            for j in cand:
                x = max(k, n - k)
                if n < P.N_MIN or binom.sf(x - 1, n, 0.5) >= P_TARGET:
                    break
                drop.add(j)
                n -= 1
                k -= int(maj == 1)
        else:
            pk = v["pk"]
            alive = [j for j in v["rows"] if j not in drop]
            x = sum(1 for j in alive if j in v["hits"] and _hit(rows[j], key[1]))
            mu = sum(pk[j] for j in alive)
            var = sum(pk[j] * (1 - pk[j]) for j in alive)
            if x > mu:  # over-represented: drop gold-hit rows
                cand = [j for j in alive if j in v["hits"]]
                cand.sort(key=lambda j: (-prio[j], rng.random()))
                for j in cand:
                    if len(alive) < P.N_MIN or x - mu <= 0.5:  # stricter than P_TARGET: no gold class above its expected share
                        break
                    drop.add(j)
                    alive.remove(j)
                    x -= 1
                    mu -= pk[j]
                    var -= pk[j] * (1 - pk[j])
            else:  # under-represented: drop rows where the feature is present and not gold, small k first
                cand = [j for j in alive if j not in v["hits"]]
                cand.sort(key=lambda j: (len(rows[j]["options"]), rng.random()))
                for j in cand:
                    if len(alive) < P.N_MIN or norm.sf(max(0.0, zstat(x, mu, var))) >= P_TARGET:
                        break
                    drop.add(j)
                    alive.remove(j)
                    mu -= pk[j]
                    var -= pk[j] * (1 - pk[j])
    return drop, fails, thr


def _hit(r, feat):
    return True  # hits set already holds only rows whose option set contains a gold hit for this feature


def rebalance_yn(rows, rng):
    by = {0: [], 1: []}
    for i, r in enumerate(rows):
        by[int(r["gold"])].append(i)
    big = 0 if len(by[0]) > len(by[1]) else 1
    n_drop = len(by[big]) - len(by[1 - big])
    return set(rng.sample(by[big], n_drop)) if n_drop > 0 else set()


def remediate_type(t, rows0):
    rng = random.Random(f"{SEED}:{t}")
    rows = list(rows0)
    log = []
    for rd in range(MAX_ROUNDS):
        drop, fails, thr = plan_round(rows, rng)
        nfail = len(fails)
        if rows and rows[0]["qtype"] == "noul":
            kept = [r for i, r in enumerate(rows) if i not in drop]
            drop |= {i for i in range(len(rows)) if i not in drop and False}
            rb = rebalance_yn(kept, rng)
            kept_idx = [i for i in range(len(rows)) if i not in drop]
            drop |= {kept_idx[j] for j in rb}
        log.append({"round": rd, "rows_in": len(rows), "flagged_features": nfail, "dropped": len(drop),
                    "top_flags": [k[1] for _, k in fails[:6]]})
        if not drop and not fails:
            break
        if not drop:
            break
        rows = [r for i, r in enumerate(rows) if i not in drop]
        if len(rows) < MIN_ROWS:
            log.append({"round": rd + 1, "rows_in": len(rows), "note": "below MIN_ROWS"})
            break
    return rows, log


def main():
    allr = [json.loads(l) for l in ORIG.open(encoding="utf-8")]
    by = defaultdict(list)
    for r in allr:
        by[r["meta"]["wave2"]["type"]].append(r)
    kept_ids, report = set(), {}
    for t in sorted(by):
        rows0 = by[t]
        if t not in BINDING:
            kept_ids |= {r["id"] for r in rows0}
            report[t] = {"before": len(rows0), "after": len(rows0), "action": "report-only type, untouched"}
            continue
        scr0 = gw_g7.screen(rows0)
        if scr0["verdict"] == "pass":
            kept_ids |= {r["id"] for r in rows0}
            report[t] = {"before": len(rows0), "after": len(rows0), "action": "G7 pass, untouched"}
            continue
        rows, log = remediate_type(t, rows0)
        scr = gw_g7.screen(rows) if rows else {"verdict": "fail"}
        ok = scr["verdict"] == "pass" and len(rows) >= MIN_ROWS
        report[t] = {"before": len(rows0), "after": len(rows), "g7_after": scr["verdict"], "kept": ok, "rounds": log}
        if ok:
            kept_ids |= {r["id"] for r in rows}
        print(t, len(rows0), "->", len(rows), scr["verdict"], "kept" if ok else "OUT", flush=True)
    out = [r for r in allr if r["id"] in kept_ids]
    (GW / "out" / "candidates_c2.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out), encoding="utf-8")
    dropped = {t: sorted(r["id"] for r in by[t] if r["id"] not in kept_ids) for t in by}
    (GW / "qc" / "GW_w7_drops.json").write_text(json.dumps({"seed": SEED, "p_target": P_TARGET, "report": report,
                                                            "dropped_ids": dropped}, indent=1) + "\n", encoding="utf-8")
    print("total", len(allr), "->", len(out))


if __name__ == "__main__":
    main()
