"""F13 emission: merge build parts into out/<name>.jsonl (+ side/<name>.f13_meta.jsonl, relations_<name>.jsonl), cut
to quota keeping each selection set (base + twins, one group_id) whole, check S5 disjointness (MIXER_NOTE 4), and
write out/MANIFEST.json + qc/QC_REPORT.json (pool and relation sha256s, gate files). Usage:
  f13_emit.py cut <name> <quota_json|N> <part.jsonl> [<part.jsonl> ...]
  f13_emit.py manifest
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

F13 = Path(__file__).resolve().parent.parent
OUT = F13 / "out"
QC = F13 / "qc"
NAMES = ("candidates_r1", "qc_sample", "mixdev_S5")
PARENTS = [
    "gd_onet_occupation (O*NET occupation codes as persona seeds via the packs; role titles only)",
    "c_src/packs/packs-1 (Claude-written domain packs)",
    "c_src/packs/packs-2 (Claude-written domain packs)",
    "c_src/packs/packs-3 (Claude-written domain packs)",
    "c_src/formats/formats-1 (fmt1 format styles, card styles and card layout; decoder_io cygnet / schema_branch_mark)",
    "c_src/formats/formats-2/wordings/family_pools.jsonl (F13 wording pool)",
    "Qwen/Qwen3.5-4B tokenizer @851bf6e8 (length measurement only)",
]


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


MAX_PER_CARD = 128


def cut(name, quota, parts):
    rows, side, rel = [], {}, []
    for p in parts:
        p = Path(p)
        rows += [json.loads(x) for x in open(p)]
        for x in open(str(p).replace(".jsonl", ".side.jsonl")):
            d = json.loads(x)
            side[d["id"]] = d
        rp = Path(str(p).replace(".jsonl", ".rel.jsonl"))
        if rp.exists():
            rel += [json.loads(x) for x in open(rp)]
    groups = defaultdict(list)
    for r in rows:
        groups[r["group_id"]].append(r)
    by_s = defaultdict(list)
    for g, rs in sorted(groups.items()):
        by_s[rs[0]["meta"]["sampler"]].append(rs)
    keep = []
    for s, gl in sorted(by_s.items()):
        q = quota.get(s, quota.get("*")) if isinstance(quota, dict) else quota
        n = 0
        # round-robin over cards so every card contributes evenly
        per_card = defaultdict(list)
        for rs in gl:
            per_card[rs[0]["meta"]["card_id"]].append(rs)
        order = []
        while any(per_card.values()):
            for c in sorted(per_card):
                if per_card[c]:
                    order.append(per_card[c].pop(0))
        pc = Counter()
        for rs in order:
            if q is not None and n + len(rs) > q:
                continue
            cid = rs[0]["meta"]["card_id"]
            if pc[cid] + len(rs) > MAX_PER_CARD:
                continue  # repair r2 (G11 counts): spec 2.1 rows per card max 128, every pool
            keep += rs
            n += len(rs)
            pc[cid] += len(rs)
    ids = {r["id"] for r in keep}
    rel = [x for x in rel if x["a"] in ids and x["b"] in ids]
    (OUT / "side").mkdir(parents=True, exist_ok=True)
    with open(OUT / f"{name}.jsonl", "w") as f:
        for r in keep:
            f.write(json.dumps(r) + "\n")
    with open(OUT / "side" / f"{name}.f13_meta.jsonl", "w") as f:
        for r in keep:
            f.write(json.dumps(side[r["id"]]) + "\n")
    with open(OUT / f"relations_{name}.jsonl", "w") as f:
        for x in rel:
            f.write(json.dumps({"a": x["a"], "b": x["b"], "type": x["type"]}) + "\n")
    print(json.dumps({"name": name, "rows": len(keep), "by_sampler": dict(Counter(r["meta"]["sampler"] for r in keep)),
                      "relations": len(rel)}))


def _load(name):
    p = OUT / f"{name}.jsonl"
    return [json.loads(x) for x in open(p)] if p.exists() else []


def s5_disjoint():
    s5 = _load("mixdev_S5")
    import re
    norm = lambda t: re.sub(r"\s+", " ", t.lower()).strip()  # noqa: E731
    keys = {k: set() for k in ("group_id", "state", "structure_hash", "domain_pack")}
    for r in s5:
        keys["group_id"].add(r["group_id"])
        keys["state"].add(hashlib.sha256(norm(r["state"]).encode()).hexdigest())
        keys["structure_hash"].add(r["meta"]["structure_hash"])
        keys["domain_pack"].add(r["meta"]["domain_pack"])
    out = {}
    for name in ("candidates_r1", "qc_sample"):
        hit = Counter()
        for r in _load(name):
            hit["group_id"] += r["group_id"] in keys["group_id"]
            hit["state"] += hashlib.sha256(norm(r["state"]).encode()).hexdigest() in keys["state"]
            hit["structure_hash"] += r["meta"]["structure_hash"] in keys["structure_hash"]
            hit["domain_pack"] += r["meta"]["domain_pack"] in keys["domain_pack"]
            hit["no_format_style"] += not r["meta"].get("format_style")
        out[name] = dict(hit)
    out["pass"] = all(v == 0 for d in out.values() if isinstance(d, dict) for v in d.values())
    return out


def manifest():
    files, counts, cov = {}, {}, {}
    for name in NAMES:
        p = OUT / f"{name}.jsonl"
        if not p.exists():
            continue
        rows = _load(name)
        rp = OUT / f"relations_{name}.jsonl"
        sp = OUT / "side" / f"{name}.f13_meta.jsonl"
        rel = [json.loads(x) for x in open(rp)] if rp.exists() else []
        files[name] = {"rows": len(rows), "sha256": sha(p), "side_sha256": sha(sp) if sp.exists() else None,
                       "relations": len(rel), "relations_sha256": sha(rp) if rp.exists() else None,
                       "relation_types": dict(Counter(x["type"] for x in rel))}
        counts[name] = {"by_sampler": dict(Counter(r["meta"]["sampler"] for r in rows)),
                        "by_card": len({r["meta"]["card_id"] for r in rows}),
                        "qtype": dict(Counter(r["qtype"] for r in rows)),
                        "aggregate": sum(1 for r in rows if r["meta"].get("subtype") == "aggregate"),
                        "twin_kind": dict(Counter(r["meta"]["twin_kind"] for r in rows))}
        cov[name] = {"domain_packs": len({r["meta"]["domain_pack"] for r in rows}),
                     "format_styles": len({r["meta"]["format_style"] for r in rows}),
                     "wordings": len({r["meta"]["wording_id"] for r in rows})}
    g0 = json.load(open(F13 / "G0_FROZEN.json"))
    gates = {}
    for name in NAMES:
        gp = QC / f"gates_{name}.json"
        if gp.exists():
            g = json.load(open(gp))
            gates[name] = {"pool_sha256": g["pool_sha256"], "G2": g.get("G2_G3", {}).get("G2_pass"),
                           "G3": g.get("G2_G3", {}).get("G3_pass"), "G15": g["G15_G18"]["G15_pass"],
                           "G18": g["G15_G18"]["G18"]["pass"], "negcount": g["negcount"]["pass"],
                           "length": g["length"]["pass"], "sealed": (g.get("sealed") or {}).get("pass"),
                           "current": g["pool_sha256"] == files.get(name, {}).get("sha256")}
    g4p = QC / "g4.json"
    if g4p.exists():
        g4 = json.load(open(g4p))
        gates["G4"] = {"pass": g4.get("pass"), "rows": g4.get("rows"), "rows_per_sampler": g4.get("rows_per_sampler"),
                       "files": g4.get("files"), "method": g4.get("method"), "summary": g4.get("summary")}
    s5 = s5_disjoint()
    m = {"family": "F13", "spec_id": g0["spec_id"], "g0_sha256": g0["sha256"], "files": files, "counts": counts,
         "coverage": cov, "gates": gates, "s5_disjoint": s5, "parents": PARENTS}
    (OUT / "MANIFEST.json").write_text(json.dumps(m, indent=1))
    qc = {"family": "F13", "pools": {n: {"sha256": f["sha256"], "relations_sha256": f["relations_sha256"]}
                                     for n, f in files.items()}, "gates": gates, "s5_disjoint": s5}
    # keep other keys of an existing report; attach the independent solver-B G2 summary when it is current
    qp = QC / "QC_REPORT.json"
    prev = json.load(open(qp)) if qp.exists() else {}
    sbp = F13 / "solverB" / "mismatch.json"
    if sbp.exists():
        sb = json.load(open(sbp))["summary"]
        cur = all(sb.get("pool_sha256", {}).get(n) == f["sha256"] for n, f in files.items())
        qc["G2_solverB"] = {"rows": sb.get("rows"), "mismatches": sb.get("mismatches"), "current": cur,
                            "pool_sha256": sb.get("pool_sha256"), "spec_sha256_prefix": sb.get("spec_sha256_prefix")}
    (QC / "QC_REPORT.json").write_text(json.dumps({**prev, **qc}, indent=1))
    print(json.dumps({"files": {k: v["rows"] for k, v in files.items()}, "s5_pass": s5["pass"]}))


if __name__ == "__main__":
    if sys.argv[1] == "cut":
        q = sys.argv[3]
        quota = json.loads(q) if q.startswith("{") else int(q)
        cut(sys.argv[2], quota, sys.argv[4:])
    else:
        manifest()
