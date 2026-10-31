"""Finalize one generated set: G12 checks, cross-set structure-hash separation, trim to the target with whole selection
units (steering the section 6 unit shares and the 2.1 yes/no vs choice 50 / 50), write the outputs.

  python finalize.py cand   -> out/candidates_r1.jsonl (+ .sidecar.jsonl, .relations.jsonl)
  python finalize.py qc     -> out/qc_sample.jsonl (...), structure hashes disjoint from the candidates
  python finalize.py dev    -> out/mixdev_S5.jsonl (...), 400 mix-tuning items + 5 x 60 depth sweep, disjoint from both
Must-show lists for the G15 re-check go to tmp/<name>.must_show.jsonl (scratch, not an output)."""
from __future__ import annotations

import collections
import hashlib
import json
import pickle
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
F4 = HERE.parent
OUT = F4 / "out"
TMP = F4 / "tmp"
sys.path.insert(0, str(HERE))
import build as BD  # noqa: E402

NAMES = {"cand": "candidates_r1", "qc": "qc_sample", "dev": "mixdev_S5"}
TARGET = {"cand": 5400, "qc": 5400}


def read_jsonl(p):
    with open(p) as f:
        return [json.loads(x) for x in f]


def write_jsonl(p, rows):
    with open(p, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")


def surface_key(r):
    return hashlib.sha256(json.dumps([r["state"], r["instructions"], r["options"], r["card"], r["qtype"]],
                                     ensure_ascii=False).encode()).hexdigest()


def trim(rows, side, target, rng):
    sd = {s["id"]: s for s in side}
    groups = collections.OrderedDict()
    for r in rows:
        groups.setdefault(r["group_id"], []).append(r)
    ginfo = {}
    for g, rs in groups.items():
        s0 = sd[rs[0]["id"]]
        ginfo[g] = {"kind": s0["unit"], "side": "Y" if s0["form"].startswith("YN") else "C", "n": len(rs),
                    "card": rs[0]["meta"]["card_id"]}
    alive = set(groups)
    n = len(rows)
    kind_rows = collections.Counter()
    side_rows = collections.Counter()
    card_rows = collections.Counter()
    for g in alive:
        kind_rows[ginfo[g]["kind"]] += ginfo[g]["n"]
        side_rows[ginfo[g]["side"]] += ginfo[g]["n"]
        card_rows[ginfo[g]["card"]] += ginfo[g]["n"]
    removable = ("single", "inert", "attack")

    def feats(r):
        e = r["meta"]["edge"]
        lab = next(x for x in e if x.startswith("L:"))
        return ((lab, "neg" if sd[r["id"]]["claim_neg"] else "pos"), int(any(x.startswith("inert:") for x in e)),
                int(any(x.startswith("carrier:") for x in e)))
    inert_c = collections.defaultdict(lambda: [0, 0])
    car_c = collections.defaultdict(lambda: [0, 0])
    yes_c = collections.defaultdict(lambda: [0, 0])
    ch3 = collections.Counter()
    for g in alive:
        for r in groups[g]:
            if sd[r["id"]]["form"] == "CH-3":
                ch3[sd[r["id"]]["label_c"]] += 1

    def wy(r):
        return next(x for x in r["meta"]["edge"] if x.startswith("world:"))
    for g in alive:
        for r in groups[g]:
            if r["qtype"] != "choice":
                yes_c[wy(r)][0] += r["gold"] == 1
                yes_c[wy(r)][1] += 1
    for g in alive:
        for r in groups[g]:
            t_, ci, cc = feats(r)
            inert_c[t_[0]][0] += ci
            inert_c[t_[0]][1] += 1
            car_c[t_][0] += cc
            car_c[t_][1] += 1

    def gain(rs):
        v = 0.0
        for r in rs:
            t_, ci, cc = feats(r)
            a, b = inert_c[t_[0]]
            dv = a / b - 0.30
            v += dv if ci else -dv * 0.30 / 0.70
            a, b = car_c[t_]
            dv = a / b - 0.25
            v += dv if cc else -dv * 0.25 / 0.75
            if r["qtype"] != "choice":
                a, b = yes_c[wy(r)]
                dv = a / b - 0.5
                v += 2 * (dv if r["gold"] == 1 else -dv)
            if sd[r["id"]]["form"] == "CH-3":
                tot3 = sum(ch3.values())
                v += 30 * (ch3[sd[r["id"]]["label_c"]] / tot3 - 1 / 3)
        return v
    while n > target:
        over = n - target
        exc = {k: kind_rows[k] / n - BD.ROW_SHARE[k] for k in removable}
        tot3 = sum(ch3.values())
        off3 = bool(tot3) and max(abs(v / tot3 - 1 / 3) for v in ch3.values()) > 0.012
        if kind_rows["contrast"] / n > (0.204 if off3 else 0.212):
            exc["contrast"] = kind_rows["contrast"] / n - 0.212
        side_ex = side_rows["Y"] / n - 0.5
        side_ex = (abs(side_ex) - 0.03) * (1 if side_ex > 0 else -1) if abs(side_ex) > 0.03 else 0.0
        pool = [g for g in alive if ginfo[g]["kind"] in exc and exc[ginfo[g]["kind"]] > -0.01 and
                ginfo[g]["n"] <= over and card_rows[ginfo[g]["card"]] - ginfo[g]["n"] >= 12]
        if not pool:
            pool = [g for g in alive if ginfo[g]["n"] <= over and card_rows[ginfo[g]["card"]] - ginfo[g]["n"] >= 8]
        if not pool:
            break
        # among a random handful, drop the unit whose removal best moves the section 6 unit shares, the yes/no share,
        # the per-label inert (30%) and carrier (25%, per claim polarity) shares, the yes rate per world and the
        # CH-3 gold shares toward target (8 / 5.7)
        sample = rng.sample(sorted(pool), min(60, len(pool)))
        if off3:
            # CH-3 units are few: always consider them while the CH-3 gold shares are off
            sample += [g_ for g_ in pool if sd[groups[g_][0]["id"]]["form"] == "CH-3" and g_ not in sample]

        def score(g_):
            gi = ginfo[g_]
            return gain(groups[g_]) + 20 * exc[gi["kind"]] * gi["n"] + \
                20 * gi["n"] * (side_ex if gi["side"] == "Y" else -side_ex)
        g = max(sample, key=score)
        for r in groups[g]:
            t_, ci, cc = feats(r)
            inert_c[t_[0]][0] -= ci
            inert_c[t_[0]][1] -= 1
            car_c[t_][0] -= cc
            car_c[t_][1] -= 1
            if r["qtype"] != "choice":
                yes_c[wy(r)][0] -= r["gold"] == 1
                yes_c[wy(r)][1] -= 1
            if sd[r["id"]]["form"] == "CH-3":
                ch3[sd[r["id"]]["label_c"]] -= 1
        alive.discard(g)
        n -= ginfo[g]["n"]
        kind_rows[ginfo[g]["kind"]] -= ginfo[g]["n"]
        side_rows[ginfo[g]["side"]] -= ginfo[g]["n"]
        card_rows[ginfo[g]["card"]] -= ginfo[g]["n"]
    keep = [r for g in groups if g in alive for r in groups[g]]
    return keep


def pick_sweep(xs, n):
    """Repair r1: the depth sweep keeps n rows per level with the yes/no rows at a 50 / 50 yes rate (the plan draws
    yes / no at 50 / 50, but label-dependent generation retries skewed the kept rows to about 60% yes). Rows are
    taken in the shuffled order; a yes/no row is skipped only while its label already has its half; any shortfall
    is filled in the same order."""
    yn = [r for r in xs if r["qtype"] == "noul"]
    half = (round(n * len(yn) / max(1, len(xs))) + 1) // 2
    got, cnt = [], {0: 0, 1: 0}
    for r in xs:
        if len(got) == n:
            break
        if r["qtype"] == "noul":
            g = int(r["gold"] == 1)
            if cnt[g] >= half:
                continue
            cnt[g] += 1
        got.append(r)
    ids = {id(r) for r in got}
    got += [r for r in xs if id(r) not in ids][: n - len(got)]
    return got


def main():
    set_name = sys.argv[1]
    d = pickle.load(open(TMP / f"rows_{set_name}.pkl", "rb"))
    rows, rels, side, ms = d["rows"], d["rels"], d["side"], d.get("ms", [])
    rng = random.Random(f"f4-finalize-{set_name}")
    report = {"generated_rows": len(rows), "gen_fails": d["fails"]}
    # G12 exact duplicates (surface) and one surface form per structure hash outside a lineage
    seen_s, seen_h, drop_g = {}, {}, set()
    for r in rows:
        k = surface_key(r)
        if k in seen_s:
            drop_g.add(r["group_id"])
        seen_s.setdefault(k, r["group_id"])
        h = r["meta"]["structure_hash"]
        if h in seen_h and seen_h[h] != r["group_id"]:
            drop_g.add(r["group_id"])
        seen_h.setdefault(h, r["group_id"])
    report["g12_dropped_groups"] = len(drop_g)
    # cross-set separation: qc disjoint from candidates; dev disjoint from candidates and qc
    others = []
    if set_name in ("qc", "dev"):
        others.append(OUT / "candidates_r1.jsonl")
    if set_name == "dev":
        others.append(OUT / "qc_sample.jsonl")
    oh, og = set(), set()
    for p in others:
        for r in read_jsonl(p):
            oh.add(r["meta"]["structure_hash"])
            og.add(surface_key(r))
    xdrop = {r["group_id"] for r in rows if r["meta"]["structure_hash"] in oh or surface_key(r) in og}
    report["cross_set_dropped_groups"] = len(xdrop)
    drop_g |= xdrop
    rows = [r for r in rows if r["group_id"] not in drop_g]
    if set_name in TARGET:
        rows = trim(rows, side, TARGET[set_name], rng)
    else:
        # dev: 400 mix-tuning items, 60 per sweep level
        sd = {s["id"]: s for s in side}
        mix = [r for r in rows if sd[r["id"]]["part"] == "mixdev"]
        sweep = collections.defaultdict(list)
        for r in rows:
            if sd[r["id"]]["part"] == "sweep":
                sweep[r["meta"]["depth"]].append(r)
        rng.shuffle(mix)
        keep = trim(mix, side, 400, rng) if len(mix) > 400 else mix
        for dlev in sorted(sweep):
            xs = sweep[dlev]
            rng.shuffle(xs)
            keep += pick_sweep(xs, 60)
        order = {r["id"]: i for i, r in enumerate(rows)}
        rows = sorted(keep, key=lambda r: order[r["id"]])
        report["dev_parts"] = {"mixdev": min(400, len(mix)),
                               **{f"sweep_d{k}": min(60, len(v)) for k, v in sorted(sweep.items())}}
    ids = {r["id"] for r in rows}
    rels = [x for x in rels if x["a"] in ids and x["b"] in ids]
    side = [s for s in side if s["id"] in ids]
    ms = [m for m in ms if m["id"] in ids]
    name = NAMES[set_name]
    OUT.mkdir(exist_ok=True)
    write_jsonl(OUT / f"{name}.jsonl", rows)
    write_jsonl(OUT / f"{name}.sidecar.jsonl", side)
    write_jsonl(OUT / f"{name}.relations.jsonl", rels)
    write_jsonl(TMP / f"{name}.must_show.jsonl", ms)
    report.update({"rows": len(rows), "relations": len(rels)})
    print(json.dumps(report, indent=1, default=str))


if __name__ == "__main__":
    main()
