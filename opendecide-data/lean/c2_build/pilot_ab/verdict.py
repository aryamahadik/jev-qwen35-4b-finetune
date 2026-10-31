"""verdict.py: the A42-D item 4 pilot verdict for ONE family (PREREG_FINAL A42-D 4.2, 4.3, 4.4, 12.6). CPU only.

Reads the L4 predictions of C1 and of the family's pilot adapter (same job, A18.2 readout, choice rows read twice in
reversed order) and decides KEEP or MOVE_TO_C3:
  (i)   own-dev gain (pilot - C1, 300 rows, point) >= +2.0 pt
  (ii)  existing-dev change (pilot - C1, the 9 gate dev splits without tb_mixtral = 7,056 rows, pooled accuracy as the
        pre-gate D1 reads it, point) >= -0.5 pt, i.e. the drop is <= 0.5 pt
  (iii) G-proxy change (pilot - C1, paired by item): REJECTED iff the 95% paired bootstrap CI upper bound < -0.5 pt;
        clusters = source documents, a complement pair is ONE cluster (union-find), 10,000 resamples, seed 0 (the same
        gate_dev.group_boot the pre-gate uses)
There is no 0.5-pt point rule on the G-proxy and no re-pilot (an existing verdict file is never overwritten).

  cd lean/c2_build && ../../.venv/bin/python -B pilot_ab/verdict.py --family T40 --reads-dir pilot_ab/reads/T40 \
      --own-rows <own dev jsonl> --gproxy-rows <gproxy jsonl> --gproxy-rel <gproxy relations jsonl> [--gproxy-sha256 H]
Reads layout: <reads-dir>/preds_<split>/<adapter><_pab>.jsonl (+ .meta.json), <reads-dir>/adapters.sha256.
Writes families/<FAM>/pilot_ab/PILOT_AB_VERDICT.json. Exit 0 = a decision was computed, 2 = REFUSED (nothing written).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import common as C  # noqa: E402

sys.path.insert(0, str(C.LEAN))
import gate_dev as g  # noqa: E402  (lean/gate_dev.py, read-only: score, group_boot, pipe_sig, PIPE_MATCH)

DOC_KEYS = ("source_doc", "doc_id", "document_id", "source_document", "doc")


class Refused(Exception):
    pass


@dataclass(frozen=True)
class Spec:
    """The pre-registered sizes and bars. The CLI never exposes them; only tests build another Spec."""
    own_n: int = C.EXPECT_OWN_N
    existing_n: int = C.EXPECT_EXISTING_N
    min_gproxy_rows: int = C.MIN_GPROXY_ROWS
    min_gproxy_pairs: int = C.MIN_GPROXY_PAIRS
    own_gain_min: float = C.OWN_GAIN_MIN
    existing_drop_max: float = C.EXISTING_DROP_MAX
    gproxy_reject_ub: float = C.GPROXY_REJECT_UB
    splits9: tuple = C.SPLITS9
    exclude_sources: tuple = C.EXCLUDE_SOURCES
    require_pipeline: bool = True
    require_adapter_sha: bool = True


def _load_preds(reads, split, name):
    f = Path(reads) / f"preds_{split}" / f"{name}.jsonl"
    if not f.exists():
        raise Refused(f"missing prediction file {f}")
    d = {}
    for l in open(f):
        if l.strip():
            x = json.loads(l)
            d[x["id"]] = x["probs"]
    return d, f


def _meta(reads, split, name):
    f = Path(reads) / f"preds_{split}" / f"{name}.meta.json"
    return json.loads(f.read_text()) if f.exists() else None


def paired_rows(split, rows, p_c1, p_pilot):
    """Per-row paired outcomes. Missing prediction of either model = refusal (the comparison must be complete)."""
    out, missing = [], []
    for r in rows:
        a, b = p_c1.get(r["id"]), p_pilot.get(r["id"])
        if a is None or b is None:
            missing.append(r["id"])
            continue
        out.append({"split": split, "id": r["id"], "group_id": r.get("group_id", r["id"]), "source": r.get("source"),
                    "qtype": r["qtype"], "ok_r": g.score(r, a)[0], "ok_c": g.score(r, b)[0]})
    if missing:
        raise Refused(f"{split}: {len(missing)} row(s) without a prediction from C1 or the pilot (first: {missing[0]})")
    return out


def point_pt(rows):
    n = len(rows)
    c, r = int(sum(x["ok_c"] for x in rows)), int(sum(x["ok_r"] for x in rows))
    return {"n": n, "pilot_ok": c, "c1_ok": r, "pilot": 100.0 * c / n, "c1": 100.0 * r / n, "diff_pt": 100.0 * (c - r) / n}


def doc_key(r):
    """(key, used_fallback): the source document of a row."""
    m = r.get("meta") or {}
    for k in DOC_KEYS:
        if m.get(k) not in (None, ""):
            return f"{k}:{m[k]}", False
    return f"group:{r.get('group_id', r['id'])}", True


def clusters(rows, rels):
    """Union-find over source documents and complement-pair links: row id -> cluster label, plus counts."""
    parent = {}
    def find(x):
        while parent.setdefault(x, x) != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)
    fallback = 0
    for r in rows:
        k, fb = doc_key(r)
        fallback += fb
        union(("row", r["id"]), ("doc", k))
    ids = {r["id"] for r in rows}
    pairs = [x for x in rels if x.get("type") == "complement"]
    for x in pairs:
        if x["a"] not in ids or x["b"] not in ids:
            raise Refused(f"complement pair {x['a']}/{x['b']} has an endpoint outside the G-proxy rows")
        union(("row", x["a"]), ("row", x["b"]))
    lab = {r["id"]: f"c{hash_label(find(('row', r['id'])))}" for r in rows}
    return lab, {"pairs": len(pairs), "clusters": len(set(lab.values())), "rows_with_group_id_fallback": fallback}


def hash_label(node):
    import hashlib
    return hashlib.sha1(repr(node).encode()).hexdigest()[:12]


def check_pipeline(reads, names, splits, spec):
    """C1 and the pilot must come from one od_gcp predict job class: same base, host, GPU, torch, CUDA, revision and chat
    template; tta_choice on (two views for choice rows), nothing else; layout E; pinned base revision; no forced override."""
    issues, sigs = [], {}
    for n in names:
        for sp in splits:
            m = _meta(reads, sp, n)
            if m is None:
                issues.append(f"{n}/{sp}: no .meta.json")
                continue
            s = sigs[(n, sp)] = g.pipe_sig(m)
            if s["path"] != "predict" or not s["has_load"]:
                issues.append(f"{n}/{sp}: not an od_gcp predict read with a load record")
            if s["forced"] is None or s["forced"]:
                issues.append(f"{n}/{sp}: forced overrides {s['forced']}")
            if s["revision"] != C.BASE_REV:
                issues.append(f"{n}/{sp}: base revision {s['revision']}")
            if s["layout"] != C.LAYOUT:
                issues.append(f"{n}/{sp}: layout {s['layout']}")
            if s["tta"] != ["tta_choice"] or not m.get("tta_choice") or m.get("tta") or m.get("tta_noul"):
                issues.append(f"{n}/{sp}: read must be --tta-choice only (got {s['tta']})")
            if s["perm_seed"] is not None:
                issues.append(f"{n}/{sp}: perm_seed {s['perm_seed']} (standard order needed)")
    for k in g.PIPE_MATCH:
        vals = {str(s[k]) for s in sigs.values()}
        if len(vals) > 1:
            issues.append(f"{k} is not one value over all reads of C1 and the pilot: {sorted(vals)}")
        if any(s[k] in (None, "") for s in sigs.values()):
            issues.append(f"{k} missing in a read's meta")
    return issues


def read_adapter_shas(reads):
    f = Path(reads) / "adapters.sha256"
    if not f.exists():
        raise Refused(f"missing {f} (l4_reads.sh read writes sha256 of both adapters on the VM)")
    out = {}
    for l in open(f):
        if l.strip():
            sha, name = l.split(maxsplit=1)
            out[Path(name.strip()).parts[-2] if "/" in name.strip() else name.strip()] = sha
    return out


def decide(own, existing, gp, spec=Spec()):
    crit = {
        "i_own_dev": {"rule": f"pilot - C1 >= +{spec.own_gain_min} pt (point)", "value_pt": own["diff_pt"],
                      "pass": own["diff_pt"] >= spec.own_gain_min - C.EPS},
        "ii_existing_dev": {"rule": f"drop <= {spec.existing_drop_max} pt (point)", "value_pt": existing["diff_pt"],
                            "pass": existing["diff_pt"] >= -spec.existing_drop_max - C.EPS},
        "iii_gproxy": {"rule": f"rejected iff CI upper bound < {spec.gproxy_reject_ub} pt", "value_pt": gp["diff"],
                       "ci": [gp["lo"], gp["hi"]], "pass": not (gp["hi"] < spec.gproxy_reject_ub)},
    }
    failed = [k for k, v in crit.items() if not v["pass"]]
    return {"verdict": "KEEP" if not failed else "MOVE_TO_C3", "failed": failed, "criteria": crit}


def compute(fam, reads, own_rows, gp_rows, gp_rels, dev_dir=None, spec=Spec(), c1_name=None, pilot_name=None,
            gproxy_sha=None, files=None):
    c1_name = c1_name or C.C1_NAME + C.READ_TAG
    pilot_name = pilot_name or C.pilot_name(fam) + C.READ_TAG
    dev_dir = Path(dev_dir) if dev_dir else C.LEAN / "data"
    for r_ in (own_rows, gp_rows):
        ids = [r["id"] for r in r_]
        if len(set(ids)) != len(ids):
            raise Refused("duplicate row ids in a dev file")
    if len(own_rows) != spec.own_n:
        raise Refused(f"own dev has {len(own_rows)} rows, A42-D 4.4 fixes {spec.own_n}")
    if len(gp_rows) < spec.min_gproxy_rows:
        raise Refused(f"G-proxy has {len(gp_rows)} rows, needs >= {spec.min_gproxy_rows}")
    own_split, gp_split = C.own_split(fam), C.GPROXY_SPLIT
    ex_splits = list(spec.splits9)
    read_splits = [own_split, gp_split] + ex_splits
    if spec.require_pipeline:
        issues = check_pipeline(reads, (c1_name, pilot_name), read_splits, spec)
        if issues:
            raise Refused("pipeline: " + "; ".join(issues[:8]) + (f" (+{len(issues) - 8} more)" if len(issues) > 8 else ""))
    shas = {}
    if spec.require_adapter_sha:
        shas = read_adapter_shas(reads)
        if shas.get(c1_name) != C.C1_ADAPTER_SHA and shas.get(C.C1_NAME) != C.C1_ADAPTER_SHA:
            raise Refused("the C1 adapter read by the L4 job is not sha256 507d1c29...")
        if pilot_name not in shas and C.pilot_name(fam) not in shas:
            raise Refused("no sha256 recorded for the pilot adapter")
    prov = {"reads": {}}
    def pair(split, rows):
        a, fa = _load_preds(reads, split, c1_name)
        b, fb = _load_preds(reads, split, pilot_name)
        prov["reads"][split] = {c1_name: C.sha256_file(fa), pilot_name: C.sha256_file(fb)}
        return paired_rows(split, rows, a, b)
    own = pair(own_split, own_rows)
    gp = pair(gp_split, gp_rows)
    ex, per_split = [], {}
    for sp in ex_splits:
        rows = C.read_jsonl(dev_dir / f"{sp}.jsonl")
        pr = pair(sp, rows)
        per_split[sp] = point_pt(pr)
        ex += [x for x in pr if x["source"] not in spec.exclude_sources]
    if len(ex) != spec.existing_n:
        raise Refused(f"existing dev has {len(ex)} rows after excluding {spec.exclude_sources}, expected {spec.existing_n}")
    lab, cinfo = clusters(gp_rows, gp_rels)
    if cinfo["pairs"] < spec.min_gproxy_pairs:
        raise Refused(f"G-proxy has {cinfo['pairs']} complement pairs, needs >= {spec.min_gproxy_pairs}")
    gp_cl = [{**x, "group_id": lab[x["id"]]} for x in gp]
    own_p, ex_p = point_pt(own), point_pt(ex)
    gpb = g.group_boot(gp_cl, g.BOOTS, g.SEED)
    if (g.BOOTS, g.SEED) != (C.BOOT["resamples"], C.BOOT["seed"]):
        raise Refused("gate_dev bootstrap constants differ from 10,000 / seed 0")
    d = decide(own_p, ex_p, gpb, spec)
    qt = lambda rows: {q: point_pt([x for x in rows if x["qtype"] == q]) for q in sorted({x["qtype"] for x in rows})}
    fallback = cinfo["rows_with_group_id_fallback"]
    return {
        "family": fam, "verdict": d["verdict"], "failed": d["failed"], "criteria": d["criteria"],
        "own_dev": {**own_p, "by_qtype": qt(own), "report_ci_by_group": {k: v for k, v in g.group_boot(own).items()
                                                                           if k in ("lo", "hi", "groups")}},
        "existing_dev": {**ex_p, "by_qtype": qt(ex), "per_split_incl_excluded": per_split,
                         "report_ci_by_group": {k: v for k, v in g.group_boot(ex).items() if k in ("lo", "hi", "groups")}},
        "gproxy": {"n": gpb["n"], "clusters": gpb["groups"], "pilot": gpb["cand"], "c1": gpb["ref"], "diff_pt": gpb["diff"],
                   "ci95": [gpb["lo"], gpb["hi"]], "resamples": g.BOOTS, "seed": g.SEED, "complement_pairs": cinfo["pairs"],
                   "rows_with_group_id_fallback": fallback, "by_qtype": qt(gp)},
        "warnings": ([f"{fallback} G-proxy row(s) carry no source-document field {DOC_KEYS}; clustered by group_id "
                      "(a CI clustered by a finer unit is too narrow)"] if fallback else []),
        "inputs": {"c1_read": c1_name, "pilot_read": pilot_name, "adapter_sha256": shas, "gproxy_sha256_pinned": gproxy_sha,
                   **(files or {}), **prov},
        "readout": "A18.2 (C1's prompt, layout schema_branch_mark, od_gcp predict), choice rows two views (--tta-choice)",
        "spec": "PREREG_FINAL A42-D 4.2 / 4.3 / 4.4 / 12.6", "written_unix": time.time(),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--family", required=True)
    ap.add_argument("--reads-dir", required=True)
    ap.add_argument("--own-rows", required=True)
    ap.add_argument("--gproxy-rows", required=True)
    ap.add_argument("--gproxy-rel", required=True, help="G-proxy relations (complement pairs), jsonl {a,b,type}")
    ap.add_argument("--gproxy-sha256", default="", help="the hash recorded before C1's first read (12.2); must match")
    ap.add_argument("--dev-data-dir", default="", help="folder with the 9 gate dev splits (default lean/data)")
    ap.add_argument("--out-dir", default="")
    ap.add_argument("--no-write", action="store_true")
    a = ap.parse_args(argv)
    try:
        for p in (a.reads_dir, a.own_rows, a.gproxy_rows, a.gproxy_rel, a.dev_data_dir or "x", a.out_dir or "x"):
            C.refuse_path(p)
        if a.family not in C.FAMILIES:
            raise Refused(f"unknown family {a.family}")
        out_dir = Path(a.out_dir) if a.out_dir else C.C2B / "families" / a.family / "pilot_ab"
        out = out_dir / "PILOT_AB_VERDICT.json"
        if out.exists() and not a.no_write:
            raise Refused(f"{out} exists: there is no re-pilot (A42-D 4.1)")
        gsha = C.sha256_file(a.gproxy_rows)
        if a.gproxy_sha256 and gsha != a.gproxy_sha256:
            raise Refused(f"G-proxy file sha256 {gsha[:12]} differs from the recorded {a.gproxy_sha256[:12]}")
        files = {"own_rows_sha256": C.sha256_file(a.own_rows), "gproxy_rows_sha256": gsha,
                 "gproxy_rel_sha256": C.sha256_file(a.gproxy_rel)}
        res = compute(a.family, a.reads_dir, C.read_jsonl(a.own_rows), C.read_jsonl(a.gproxy_rows),
                      C.read_jsonl(a.gproxy_rel), a.dev_data_dir or None, gproxy_sha=a.gproxy_sha256 or None, files=files)
    except (Refused, SystemExit) as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 2
    if not a.no_write:
        out_dir.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(res, indent=2, default=float) + "\n")
    c = res["criteria"]
    print(json.dumps({"family": res["family"], "verdict": res["verdict"], "failed": res["failed"],
                      "own_pt": round(c["i_own_dev"]["value_pt"], 2), "existing_pt": round(c["ii_existing_dev"]["value_pt"], 2),
                      "gproxy_pt": round(c["iii_gproxy"]["value_pt"], 2),
                      "gproxy_ci": [round(x, 2) for x in c["iii_gproxy"]["ci"]], "written": None if a.no_write else str(out)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
