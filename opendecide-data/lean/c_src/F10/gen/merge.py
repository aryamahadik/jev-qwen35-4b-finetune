"""Merge the per-card build outputs into the family pools (out/):
  candidates_r1.jsonl (+ .sidecar.jsonl, .relations.jsonl, .cards.jsonl)   from tmp/build/r1 (training samplers only)
  qc_sample.jsonl     (+ same companions)                                   from tmp/build/qc (G6 QC sample, never emitted)
  mixdev_S5.jsonl     (+ .sidecar.jsonl, .cards.jsonl)                      from tmp/build/s5 (400 held-out dev items)
  s7_record_claims.jsonl: every normalized text F10 S7 claims (coded texts and examples; r1 only).
Structural checks here (ids unique, units <= 3 rows sharing one call_id, relations inside one call_id, mixdev
separation from training rows: group_id, normalised state, structure_hash, domain_pack). Gates run in qc/."""
from __future__ import annotations

import glob
import json
import re
from collections import Counter, defaultdict

from common import BUILD, OUT, dump_jsonl, progress, sha256_file


def _load(tag):
    rows, sides, rels, cards, stats, claims, drops = [], [], [], [], Counter(), [], {}
    for f in sorted(glob.glob(str(BUILD / tag / "*.json"))):
        d = json.load(open(f))
        if "cards" in d:          # S7 dataset group
            drops.update(d.get("drops", {}))
            for c in d["cards"]:
                rows += c["rows"]
                sides += c["sides"]
                rels += c["rels"]
                cards.append(c["card"])
                stats.update(c["stats"])
                claims += [{"norm_sha256": n, "kind": f"example:{c['card']['card_id']}"} for n in c["card"]["example_claims"]]
                seen = set()
                for s in c["sides"]:
                    if s["sel_unit"] not in seen:
                        seen.add(s["sel_unit"])
                        claims.append({"norm_sha256": s["record_norm"], "kind": "coded", "group_id": s["sel_unit"]})
        else:
            rows += d["rows"]
            sides += d["sides"]
            rels += d["rels"]
            cards.append(d["card"])
            stats.update(d["stats"])
    return rows, sides, rels, cards, stats, claims, drops


def norm_state(s):
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def check_units(rows, rels):
    probs = []
    ids = Counter(r["id"] for r in rows)
    probs += [f"duplicate id {i}" for i, n in ids.items() if n > 1][:5]
    byid = {r["id"]: r for r in rows}
    units = defaultdict(list)
    for r in rows:
        units[r["call_id"]].append(r["id"])
    big = [u for u, v in units.items() if len(v) > 3]
    if big:
        probs.append(f"{len(big)} units > 3 rows")
    for x in rels:
        a, b = byid.get(x["a"]), byid.get(x["b"])
        if a is None or b is None:
            probs.append(f"relation to a missing row {x}")
        elif a["call_id"] != b["call_id"]:
            probs.append(f"relation across call_ids {x}")
    linked = {x["a"] for x in rels} | {x["b"] for x in rels}
    for u, v in units.items():
        if len(v) > 1 and not all(i in linked for i in v):
            probs.append(f"unit {u} holds a row with no relation")
            break
    return probs, Counter(len(v) for v in units.values())


def _qpara(ins):
    paras = [p for p in ins.strip().split("\n\n") if p.strip()]
    qi = max((i for i, p in enumerate(paras) if "?" in p), default=len(paras) - 1)
    return paras[qi]


def drop_near_dups(rows, sides, rels, stats):
    """G12 "MinHash near-dups: keep one" (repair r1): word 5-gram shingles of question paragraph + state + options;
    a pair outside one planned twin set (same group_id or call_id, or a relation pair) with exact shingle Jaccard
    >= 0.88 keeps the group listed first and does not emit the later group (all its rows and relations)."""
    from datasketch import MinHash, MinHashLSH
    relp = {frozenset((x["a"], x["b"])) for x in rels}
    lsh = MinHashLSH(threshold=0.8, num_perm=128)
    sh, mh = {}, {}
    for r in rows:
        t = (_qpara(r["instructions"]) + " " + r["state"] + " " + " ".join(r["options"] or [])).lower().split()
        sh[r["id"]] = {" ".join(t[i:i + 5]) for i in range(max(1, len(t) - 4))}
        m = MinHash(num_perm=128)
        for x in sh[r["id"]]:
            m.update(x.encode())
        mh[r["id"]] = m
        lsh.insert(r["id"], m)
    by = {r["id"]: r for r in rows}
    gorder = {}
    for r in rows:
        gorder.setdefault(r["group_id"], len(gorder))
    drop = set()
    for r in rows:
        if r["group_id"] in drop:
            continue
        for o in lsh.query(mh[r["id"]]):
            ro = by[o]
            if o == r["id"] or ro["group_id"] in drop or ro["group_id"] == r["group_id"] or ro["call_id"] == r["call_id"] \
                    or frozenset((o, r["id"])) in relp:
                continue
            a, b = sh[r["id"]], sh[o]
            if len(a & b) / max(1, len(a | b)) >= 0.88:
                later = max((r["group_id"], ro["group_id"]), key=lambda g: gorder[g])
                drop.add(later)
                stats["g12_near_dup_group_not_emitted"] += 1
                if later == r["group_id"]:
                    break
    if not drop:
        return rows, sides, rels
    gone = {r["id"] for r in rows if r["group_id"] in drop}
    return ([r for r in rows if r["id"] not in gone], [x for x in sides if x["id"] not in gone],
            [x for x in rels if x["a"] not in gone and x["b"] not in gone])


def write_part(name, rows, sides, rels, cards):
    n = dump_jsonl(OUT / f"{name}.jsonl", rows)
    dump_jsonl(OUT / f"{name}.sidecar.jsonl", sides)
    if rels is not None:
        dump_jsonl(OUT / f"{name}.relations.jsonl", rels)
    dump_jsonl(OUT / f"{name}.cards.jsonl", cards)
    return n


def main():
    OUT.mkdir(exist_ok=True)
    report = {}
    for tag, name in (("r1", "candidates_r1"), ("qc", "qc_sample")):
        rows, sides, rels, cards, stats, claims, drops = _load(tag)
        rows, sides, rels = drop_near_dups(rows, sides, rels, stats)
        probs, usz = check_units(rows, rels)
        n = write_part(name, rows, sides, rels, cards)
        report[name] = {"rows": n, "cards": len(cards), "relations": dict(Counter(x["type"] for x in rels)),
                        "unit_sizes": dict(usz), "problems": probs, "gen_stats": {k: v for k, v in stats.items()},
                        "s7_drops": drops}
        if tag == "r1":
            c = Counter(x["norm_sha256"] for x in claims)
            dup = sum(1 for v in c.values() if v > 1)
            dump_jsonl(OUT / "s7_record_claims.jsonl", claims)
            report[name]["s7_claims"] = {"claims": len(claims), "texts_claimed_twice": dup}
    # S5 dev: anchors only, meta.sampler S5, exactly 400 items (card order, then row order)
    rows, sides, rels, cards, stats, _, _ = _load("s5")
    keep, per = [], Counter()
    ncard = len(cards)
    quota = {c["card_id"]: 400 // ncard + (1 if i < 400 % ncard else 0) for i, c in enumerate(cards)}
    sd = {s["id"]: s for s in sides}
    pool = [r for r in rows if r["id"].endswith("-a")]
    for r in pool:
        cid = r["meta"]["card_id"]
        if per[cid] < quota[cid]:
            per[cid] += 1
            keep.append(r)
    if len(keep) < 400:          # a short card: fill from the other cards' spare anchors, in order
        have = {r["id"] for r in keep}
        for r in pool:
            if len(keep) >= 400:
                break
            if r["id"] not in have:
                keep.append(r)
    keep = keep[:400]
    for r in keep:
        r["meta"]["sampler"] = "S5"
        r["call_id"] = r["group_id"] + "-u"
    dsides = [sd[r["id"]] for r in keep]
    for s in dsides:
        s["sampler"] = "S5"
    write_part("mixdev_S5", keep, dsides, None, cards)
    # separation of mixdev from every training row
    tr = [json.loads(l) for l in open(OUT / "candidates_r1.jsonl")]
    sep = {"group_id": len({r["group_id"] for r in tr} & {r["group_id"] for r in keep}),
           "norm_state": len({norm_state(r["state"]) for r in tr} & {norm_state(r["state"]) for r in keep}),
           "structure_hash": len({r["meta"]["structure_hash"] for r in tr} & {r["meta"]["structure_hash"] for r in keep}),
           "domain_pack": len({r["meta"]["domain_pack"] for r in tr} & {r["meta"]["domain_pack"] for r in keep}),
           "format_style": len({r["meta"]["format_style"] for r in tr} & {r["meta"]["format_style"] for r in keep})}
    report["mixdev_S5"] = {"rows": len(keep), "cards": ncard, "per_card": dict(per), "separation_overlaps": sep,
                           "gen_stats": dict(stats)}
    report["files"] = {p.name: sha256_file(p) for p in sorted(OUT.glob("*.jsonl"))}
    (OUT / "merge_report.json").write_text(json.dumps(report, indent=1))
    progress(f"merge: candidates {report['candidates_r1']['rows']}, qc {report['qc_sample']['rows']}, "
             f"mixdev {len(keep)}; problems {sum(len(report[k]['problems']) for k in ('candidates_r1', 'qc_sample'))}; "
             f"mixdev overlaps {sep}")
    print(json.dumps({k: (v if k != "files" else len(v)) for k, v in report.items()}, default=str)[:3000])


if __name__ == "__main__":
    main()
