"""grid_elig.py: per-candidate eligibility for the 18 grid candidates (PREREG A42-D 9.4; C2_DATA_SPEC 7.2 (a)-(d); item 4.3). CPU only.

gate_c2.py runs ONE pre-gate (CANDIDATE_C2.json) and has no per-candidate mode. This wrapper calls gate_c2's own functions
(check_dev, load_d2_set, split_rows, evaluate, the rules, the 10,000-resample seed-0 group bootstrap) unchanged on the reads
of each grid candidate and maps their verdicts to the 11 booleans select_candidate.py needs:

  a_learning      gate_c2 rule a    mixdev gain >= +8.0 pp and paired LB > 0
  b_transfer      rule b            transfer dev gain >= +3.0 pp and LB > 0
  c1_D1           rule c1           dev full set LB > -1.5
  c2_D2           rule c2           D2 re-derived unseen set: not (point < -1.0 and UB < 0)
  c3_D3           rules c3.yes/no and c3.choice   each >= C1 - 1.0 pp
  c4_D4           rule c4           calibrated yes/no Brier <= C1 + 0.005
  c5_D5           rules c5.equiv and c5.perm      each <= C1 + 2 pp
  c6_D6           rules c6.jagged and c6.opi      not above max(C1 + 2 pp, 3%) with LB of the increase > 0
  c7_D9           rule c7           p50 latency <= 1.05 x C1 (needs the candidate's own latency record)
  d_complement    rule d            T37b-dev complement violation: candidate < C1 (point)
  gproxy_rule_4_3                   G-proxy change vs C1 (paired by item, clusters = source documents with complement pairs
                                    as ONE cluster, 10,000 resamples, seed 0) is NOT rejected: CI upper bound >= -0.5 pt

A booleans is True only on a PASS. A missing read, a non-finite number, a missing latency record, a stale or wrong dev JSON
is a REFUSAL (exit 2, nothing written for that candidate): no value is ever filled in, no bar is changed, and no check is skipped.
The output <out-dir>/<candidate>.json is exactly what select_candidate.py reads (items per component, eligibility, S inputs).

Safeguards on top of gate_c2's own: the grid record (grid_plan.py record) is present and was written before the first grid read;
the d2-set was written before the first read of ANY grid candidate or of the reference; the stop rule did not fire and the 25/50/75%
snapshot reads exist; the reference's refparity look passed; candidate and reference are one clean predict job (gate_dev.pipeline_check
for the gate sets, a same-job meta comparison for the G-proxy / own-dev reads, which use the pilot A/B two-view convention).

  grid_elig.py status --cfg GRID_CFG.json              which inputs exist, per candidate (reads nothing else, computes nothing)
  grid_elig.py one  --cfg GRID_CFG.json --cand last3_a07 --out-dir DIR
  grid_elig.py all  --cfg GRID_CFG.json --out-dir DIR     (the 18; writes every candidate that does not refuse; exit 2 if any refused)
The gate dev JSON of each candidate: gate_dev.py <read name> <ref> --mode ship --size 4b --json <ship_tpl> --no-log.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2B = HERE.parent
LEAN = C2B.parent
for _p in (str(HERE), str(C2B), str(LEAN)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import gate_c2 as gc  # noqa: E402
import gate_dev as g  # noqa: E402
import grid_plan as gp  # noqa: E402
import select_candidate as sc  # noqa: E402

Refused = gc.Refused
GPROXY_REJECT_UB = -0.5                       # item 4.3: rejected iff the CI upper bound is below this (pt)
DOC_KEYS = ("source_doc", "doc_id", "document_id", "source_document", "doc")     # pilot_ab/verdict.py

# eligibility key -> the gate_c2 rule ids that must ALL be PASS
RULE_MAP = {"a_learning": ("a",), "b_transfer": ("b",), "c1_D1": ("c1",), "c2_D2": ("c2",),
            "c3_D3": ("c3.yes/no", "c3.choice"), "c4_D4": ("c4",), "c5_D5": ("c5.equiv", "c5.perm"),
            "c6_D6": ("c6.jagged", "c6.opi"), "c7_D9": ("c7",), "d_complement": ("d",)}
ELIG_KEYS = tuple(RULE_MAP) + ("gproxy_rule_4_3",)
assert ELIG_KEYS == sc.ELIG_KEYS


# ------------------------------------------------------------------------------------------------ pure parts
def booleans(rules: list, gproxy: dict) -> dict:
    """The 11 eligibility booleans from gate_c2's rule list and the G-proxy result. Anything but PASS is False; a rule that is
    absent or UNMEASURED is a refusal (the read is incomplete)."""
    by = {r["id"]: r["status"] for r in rules}
    out = {}
    for key, ids in RULE_MAP.items():
        for i in ids:
            if i not in by:
                raise Refused(f"gate_c2 produced no rule {i!r} (eligibility {key})")
            if by[i] == "UNMEASURED":
                raise Refused(f"rule {i} is UNMEASURED: the reads are incomplete (eligibility {key})")
        out[key] = all(by[i] == "PASS" for i in ids)
    if gproxy.get("status") == "UNMEASURED":
        raise Refused("the G-proxy change is UNMEASURED")
    out["gproxy_rule_4_3"] = gproxy["status"] == "PASS"
    return out


def doc_key(r: dict) -> tuple:
    m = r.get("meta") or {}
    for k in DOC_KEYS:
        if m.get(k) not in (None, ""):
            return f"{k}:{m[k]}", False
    return f"group:{r.get('group_id', r['id'])}", True


def _hash_label(node) -> str:
    return hashlib.sha1(repr(node).encode()).hexdigest()[:12]


def gproxy_clusters(rows: list, rels: list) -> tuple:
    """pilot_ab/verdict.py clusters(): union-find over source documents and complement pairs (a pair is ONE cluster).
    Returns ({row id: label}, {pairs, clusters, fallback})."""
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
    lab = {r["id"]: f"c{_hash_label(find(('row', r['id'])))}" for r in rows}
    return lab, {"pairs": len(pairs), "clusters": len(set(lab.values())), "rows_with_group_id_fallback": fallback}


def gproxy_result(rows: list, rels: list, pc: dict, pr: dict) -> dict:
    """Item 4.3 for one candidate. rows = G-proxy rows; pc / pr = {id: probs} of the candidate and the C1 reference."""
    miss = [r["id"] for r in rows if r["id"] not in pc or r["id"] not in pr]
    if miss:
        raise Refused(f"G-proxy: {len(miss)} row(s) without a candidate or reference prediction (first {miss[0]})")
    lab, info = gproxy_clusters(rows, rels)
    paired = [{"id": r["id"], "group_id": lab[r["id"]], "ok_c": g.score(r, pc[r["id"]])[0], "ok_r": g.score(r, pr[r["id"]])[0]}
              for r in rows]
    b = g.group_boot(paired, gc.DEV_BOOT["resamples"], gc.DEV_BOOT["seed"])
    if not gc.fin(b.get("diff"), b.get("lo"), b.get("hi")):
        return {"status": "UNMEASURED", "detail": "no finite G-proxy interval", "items": None, **info}
    ok = not (b["hi"] < GPROXY_REJECT_UB - gc.EPS)
    return {"status": "PASS" if ok else "FAIL", "n": b["n"], "clusters": b["groups"], "cand": b["cand"], "ref": b["ref"],
            "diff_pt": b["diff"], "ci95": [b["lo"], b["hi"]], "rule": f"rejected iff the CI upper bound < {GPROXY_REJECT_UB} pt (4.3)",
            "detail": f"{b['cand']:.2f} vs {b['ref']:.2f}: diff {b['diff']:+.2f} [{b['lo']:+.2f}, {b['hi']:+.2f}] "
                      f"(n={b['n']}, {b['groups']} clusters, {info['pairs']} complement pairs)",
            "items": {"id": [x["id"] for x in paired], "cluster": [x["group_id"] for x in paired],
                      "correct": [int(x["ok_c"]) for x in paired]}, **info}


def items_of(rows: list) -> dict:
    """select_candidate's item block from gate_c2.split_rows() rows (cluster = group_id, correct = the candidate's)."""
    return {"id": [x["id"] for x in rows], "cluster": [str(x["group_id"]) for x in rows], "correct": [int(x["ok_c"]) for x in rows]}


def make_record(cand: str, read_name: str, ref: str, rules: list, gproxy: dict, items: dict, extra: dict) -> dict:
    el = booleans(rules, gproxy)
    return {"candidate": cand, "read_name": read_name, "ref": ref, "eligibility": el, "eligible": all(el.values()),
            "failed_checks": [k for k in ELIG_KEYS if not el[k]], "items": items,
            "rules": [{k: r[k] for k in ("id", "status", "detail")} for r in rules],
            "gproxy_4_3": {k: v for k, v in gproxy.items() if k != "items"}, **extra}


# ------------------------------------------------------------------------------------------------ IO
def _abs(root: Path, x):
    q = Path(x)
    return q if q.is_absolute() else Path(root) / q


def load_cfg(path: Path) -> dict:
    gc.refuse_inputs([path])
    cfg = json.loads(Path(path).read_text())
    for k in ("root", "run_name", "ref", "name_tpl", "grid", "grid_record", "ship_tpl", "latency_tpl", "d2_set", "gproxy"):
        if k not in cfg:
            raise Refused(f"config lacks {k!r}")
    return cfg


def jsonl(path: Path) -> list:
    gc.refuse_inputs([path])
    try:
        return [json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()]
    except OSError as e:
        raise Refused(f"cannot read {path} ({type(e).__name__})") from None


def preds_of(root: Path, split: str, name: str) -> dict:
    gc.refuse_inputs([Path(root) / f"preds_{split}"], [split, name])
    with gc.at_root(root):
        p = g.load(split, name)
    if p is None:
        raise Refused(f"no preds_{split}/{name}.jsonl")
    return p


def meta_of(root: Path, split: str, name: str) -> dict:
    f = Path(root) / f"preds_{split}" / f"{name}.meta.json"
    try:
        return json.loads(f.read_text())
    except (OSError, ValueError):
        raise Refused(f"preds_{split}/{name}.meta.json missing or not JSON") from None


SAME_JOB_KEYS = ("base", "host", "gpu", "torch", "cuda")


def same_job_issues(root: Path, splits: list, cand: str, ref: str, want_tta_choice: bool = True) -> list:
    """The G-proxy / own-dev reads use the pilot A/B readout (choice rows two views). Not the gate_dev pipeline_check (that
    refuses TTA): here candidate and reference must carry one value for each field, the same readout, a pinned revision and no forced
    override. Returns the problems."""
    probs = []
    for sp in splits:
        ms = {n: meta_of(root, sp, n) for n in (cand, ref)}
        for n, m in ms.items():
            ld = m.get("load") or {}
            if not (ld.get("revision") or m.get("revision")):
                probs.append(f"{sp}/{n}: no pinned base revision")
            if ld.get("forced") is None or ld.get("forced"):
                probs.append(f"{sp}/{n}: forced overrides {ld.get('forced')}")
            if bool(m.get("tta_choice")) != want_tta_choice or m.get("tta") or m.get("tta_noul"):
                probs.append(f"{sp}/{n}: readout tta={m.get('tta')} tta_choice={m.get('tta_choice')} tta_noul={m.get('tta_noul')}")
            if m.get("perm_seed") is not None:
                probs.append(f"{sp}/{n}: perm_seed {m.get('perm_seed')}")
        for k in (*SAME_JOB_KEYS, "layout", "style"):
            a, b = ms[cand].get(k), ms[ref].get(k)
            if a != b or not a:
                probs.append(f"{sp}: {k} differs or is missing ({a!r} vs {b!r})")
        ld_c, ld_r = ms[cand].get("load") or {}, ms[ref].get("load") or {}
        for k in ("revision", "chat_template_sha"):
            if ld_c.get(k) != ld_r.get(k) or not ld_c.get(k):
                probs.append(f"{sp}: load.{k} differs or is missing")
    return probs


class Run:
    """Everything that is the same for the 18 candidates: checked once."""

    def __init__(self, cfg: dict, root: Path | None = None):
        self.cfg = cfg
        self.root = Path(root or cfg["root"])
        self.ref, self.run = cfg["ref"], cfg["run_name"]
        gc.refuse_inputs([self.root], [self.ref, self.run])
        self.grid_path = _abs(self.root, cfg["grid"])
        self.grid = json.loads(self.grid_path.read_text())
        self.names = [c["name"] for c in self.grid["candidates"]]
        self.rec_path = _abs(self.root, cfg["grid_record"])
        self.read_names = {n: cfg["name_tpl"].format(cand=n) for n in self.names}
        self.problems = []

    def check_once(self, snap=None) -> dict:
        v = gp.verify_record(self.rec_path, self.grid_path, self.root)
        if not v["ok"]:
            raise Refused("grid record: " + "; ".join(v["problems"][:4]))
        info = {"grid_record": {"grid_sha256": v["grid_sha256"]}}
        if snap is None:
            import snap_monitor_c2 as sm
            snap = (Path(sm.STATE), Path(sm.STOPREC), Path(sm.ESCREC))
        info["stop_rule"] = gc.check_stop_rule(snap[0], snap[1], snap[2], self.run)
        info["refparity"] = gc.check_refparity(self.root, self.ref)
        d2 = gc.jload(_abs(self.root, self.cfg["d2_set"]), "D2 set")
        reads = gp.grid_read_files(self.root, [*self.read_names.values(), self.ref])
        first = min((f.stat().st_mtime for f in reads), default=None)
        if first is not None and float(d2.get("written_unix", 1e18)) > first + gp.SLACK:
            raise Refused("the D2 set was written after the first grid read (a D2 set written after a look is refused)")
        info["d2_set_sha256"] = d2.get("sources_sha256")
        return info

    def inputs_for(self, cand: str) -> dict:
        name = self.read_names[cand]
        ship = _abs(self.root, self.cfg["ship_tpl"].format(cand=cand))
        lat = _abs(self.root, self.cfg["latency_tpl"].format(cand=cand))
        return {"name": name, "ship": ship, "latency": lat}

    def evaluate(self, cand: str) -> dict:
        root, ref = self.root, self.ref
        io = self.inputs_for(cand)
        name = io["name"]
        gc.refuse_inputs([io["ship"], io["latency"]], [name])
        dev = gc.jload(io["ship"], f"gate_dev ship JSON of {cand}")
        gc.check_dev(dev, name, ref)
        d2set = gc.load_d2_set(_abs(root, self.cfg["d2_set"]), root, name)
        with gc.at_root(root):
            try:
                dev_rows = g.complete_rows(gc.SPLITS9, name, ref)
            except SystemExit as e:
                raise Refused(str(e)) from None
        d2 = gc.boot(gc.d2_rows(dev_rows, d2set["sources"]))
        gate_reads = g.std_reads(gc.SPLITS9) + [(sp, f"preds_{sp}", "", None, "dev") for sp in (gc.MIXDEV, gc.TRANSFER, gc.T37B_DEV)]
        with gc.at_root(root):
            issues, _ = g.pipeline_check([name, ref], gate_reads)
        if issues:
            raise Refused(f"{cand}: the reads are not one clean predict job: {issues[:3]}")
        mix = gc.split_rows(gc.MIXDEV, name, ref, root)
        tr = gc.split_rows(gc.TRANSFER, name, ref, root)
        t37 = gc.split_rows(gc.T37B_DEV, name, ref, root)
        rels = gc.relations(gc.T37B_DEV, root)
        lat = gc.jload(io["latency"], f"latency record of {cand}")
        # A80 (c): the learning rule (a) and the R term of S read only the mixdev rows of the families the final mix TRAINED on (the written mix manifest);
        # the rows of a family that left the mix are report-only ("family not trained in C2"). The pre-gate (gate_c2.pregate) does the same.
        tf = gc.trained_families(_abs(root, self.cfg["mix_manifest"]) if self.cfg.get("mix_manifest") else Path(root) / gc.MIX_MANIFEST, root)
        res = gc.evaluate(dev, d2, mix, tr, t37, rels, lat, dev_rows, trained=set(tf["trained"]))
        mix_trained, _mix_off = gc.split_trained(mix, tf["trained"])
        # G-proxy (item 4.3) and the pooled own dev (9.3 third component)
        gpc = self.cfg["gproxy"]
        prob = same_job_issues(root, [gpc["split"], *[o["split"] for o in self.cfg.get("own_dev", [])]], name, ref)
        if prob:
            raise Refused(f"{cand}: G-proxy / own-dev reads are not one clean job: {prob[:3]}")
        gp_rows_path = _abs(root, gpc["rows"])
        if gpc.get("sha256") and gp.sha_file(gp_rows_path) != gpc["sha256"]:
            raise Refused("the G-proxy rows file differs from the recorded sha256 (12.2: never edited after C1's first read)")
        gprows, gprels = jsonl(gp_rows_path), jsonl(_abs(root, gpc["rel"]))
        gpres = gproxy_result(gprows, gprels, preds_of(root, gpc["split"], name), preds_of(root, gpc["split"], ref))
        items = {"gproxy": gpres["items"], "rmixdev": items_of(mix_trained)}
        own = [gc.split_rows(o["split"], name, ref, root) for o in self.cfg.get("own_dev", [])]
        if own:
            flat = [x for rows in own for x in rows]
            items["own_dev"] = items_of(flat)
        if gpres["items"] is None:
            raise Refused("the G-proxy change is UNMEASURED")
        inputs_sha = gc.canon_sha({"ship": gp.sha_file(io["ship"]), "lat": gc.canon_sha(lat), "d2": d2set["sources_sha256"], "trained": tf["trained"],
                                   "grid": self.grid["grid_sha256"],
                                   "preds": {f"{p.parent.name}/{p.name}": gp.sha_file(p) for p in
                                             gp.grid_read_files(root, [name, ref])}})
        return make_record(cand, name, ref, res["rules"], gpres, items,
                           {"inputs_sha256": inputs_sha, "grid_sha256": self.grid["grid_sha256"],
                            "adapter_sha256": next(c["adapter_sha256"] for c in self.grid["candidates"] if c["name"] == cand),
                            "report_only": {"mixdev_diff": res["mixdev"].get("diff"), "transfer_diff": res["transfer"].get("diff"),
                                            "complement": res["report_only"]["complement_t37b_dev"],
                                            "mixdev_trained_families": res["report_only"].get("mixdev_trained_families")},
                            "trained_families": tf["trained"],
                            "caveat": "A61 (f): every G-proxy use carries the label 'A42-D 12.2 unmet'; eligibility is searched on the "
                                      "same dev reads as the pre-gate, so the pre-gate result is optimistic (analysis L5)",
                            "written_unix": time.time()})


def write_once(out_dir: Path, rec: dict) -> str:
    """Write <out_dir>/<candidate>.json once; the same inputs repeat harmlessly, other inputs are refused."""
    gc.refuse_inputs([out_dir])
    f = Path(out_dir) / f"{rec['candidate']}.json"
    if f.exists():
        old = json.loads(f.read_text())
        if old.get("inputs_sha256") != rec["inputs_sha256"]:
            raise Refused(f"{f.name} exists with other inputs (one eligibility record per candidate)")
        return "unchanged"
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(rec, indent=1, default=str) + "\n")
    return "written"


def status(run: Run) -> list:
    """Which inputs exist for each candidate (names only; no value is read)."""
    rows = []
    splits = [*gc.SPLITS9, "eval_jagged", "eval_opi", gc.MIXDEV, gc.TRANSFER, gc.T37B_DEV, run.cfg["gproxy"]["split"],
              *[o["split"] for o in run.cfg.get("own_dev", [])]]
    for n in [*run.names]:
        io = run.inputs_for(n)
        have = [s for s in splits if (run.root / f"preds_{s}" / f"{io['name']}.jsonl").exists()]
        perm = [s for s in gc.SPLITS9 if (run.root / f"preds_{s}" / f"{io['name']}_perm.jsonl").exists()]
        rows.append({"candidate": n, "reads": f"{len(have)}/{len(splits)}", "perm": f"{len(perm)}/9", "ship_json": io["ship"].exists(),
                     "latency": io["latency"].exists(),
                     "missing_reads": [s for s in splits if s not in have]})
    return rows


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("status", "one", "all"))
    ap.add_argument("--cfg", required=True)
    ap.add_argument("--cand", default=None)
    ap.add_argument("--out-dir", default=None)
    a = ap.parse_args(argv)
    try:
        run = Run(load_cfg(Path(a.cfg)))
        if a.cmd == "status":
            print(json.dumps(status(run), indent=1))
            return 0
        if not a.out_dir:
            raise Refused("--out-dir is required")
        out_dir = _abs(run.root, a.out_dir)
        cands = [a.cand] if a.cmd == "one" else list(run.names)
        if a.cmd == "one" and a.cand not in run.read_names:
            raise Refused(f"{a.cand!r} is not a grid candidate")
        info = run.check_once()
    except Refused as e:
        print(f"REFUSED: {e}")
        return 2
    refused = {}
    for c in cands:
        try:
            rec = run.evaluate(c)
            how = write_once(out_dir, rec)
            print(f"  {c:<14} {'ELIGIBLE' if rec['eligible'] else 'not eligible':<12} {how}"
                  + ("" if rec["eligible"] else f"  failed: {', '.join(rec['failed_checks'])}"))
        except Refused as e:
            refused[c] = str(e)
            print(f"  {c:<14} REFUSED {e}")
    print(json.dumps({"checked_once": info, "refused": list(refused)}, default=str))
    return 2 if refused else 0


if __name__ == "__main__":
    sys.exit(main())
