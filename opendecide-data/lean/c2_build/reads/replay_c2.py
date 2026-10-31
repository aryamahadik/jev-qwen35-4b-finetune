"""reads/replay_c2.py: the C2 replay inputs the mixer needs (spec 5.4), made with c_build/replay_sample.py UNCHANGED
(imported and run in-process, as replay_screen/draw.py does) and the C2 seed 20261013 (= c2io.SEED = the A46 draw seed).
Nothing under lean/c_build or lean/*.py is edited; the sampler's own output files go to reads/replay_work/ (its module
global HERE is pointed there), never into c_build/.

  PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
  cd c2_build/reads
  nice -n 10 $PY -B replay_c2.py draw          # --write-shards at --r1 75000 --r2 150000 --margin 0.10 (the A46 size):
                                               #   data/c2_replay_shards/ (read shards), c2_build/replay_c2_write.json,
                                               #   reads/replay_work/replay_draw.json, the C2-seed old slice (kept apart)
  $PY -B replay_c2.py old-slice                # data/c_old_slice_shards/ = the ROUND-1 old slice (spec 5.4: "the same
                                               #   slice as round 1"), rebuilt from c_build/replay_draw.json and checked
                                               #   against the sha256s recorded in c_build/replay_r1_write.json
  $PY -B replay_c2.py verify                   # the draw == replay_screen/pool/draw_75000.json (the A46 screen's draw);
                                               #   replay_screen/screen.py coverage on the shards
  ... C1 read of data/c2_replay_shards (fast_read.py label, or od_gcp.py label) -> data/c2_replay_shards/labels_q35_4b_main500k
  $PY -B replay_c2.py second-pass              # p_g rule (A16) + C1 anchor flags -> c2_build/replay_c2_pg_anchor.json
  $PY -B replay_c2.py reuse-r1-labels          # (optional, before the read) copy round-1 HF labels of rows that are
                                               #   byte-identical read inputs; the rest is read

The deny inputs (replay_screen/REPLAY_DENY_A46.json + REPLAY_UNSCREENED_A46.json, logs/decontam_counts/pool_drops_r1.json)
are mixer inputs (`mix_c2.py --decontam-drops`), not sampler inputs: the sampler has no row-id input. The shards are the
sampler's raw draw (rows of dropped units are read too: mix_c2.load_replay needs a label for every shard row).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2 = HERE.parent
LEAN = C2.parent
DATA = LEAN / "data"
WORK = HERE / "replay_work"
C2_SEED = 20261013
VERDICTS = LEAN / "c_build/replay_denylist_verdicts.json"
A46_DRAW = C2 / "replay_screen/pool/draw_75000.json"
R1_WRITE = LEAN / "c_build/replay_r1_write.json"
R1_DRAW = LEAN / "c_build/replay_draw.json"
SHARDS = DATA / "c2_replay_shards"
OLD_R1 = DATA / "c_old_slice_shards"
OLD_C2SEED = DATA / "c2_seed_old_slice_shards"
SEALED_SHA = "f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68"  # the A15 suite sha in PREREG_FINAL.md
C1 = "q35_4b_main500k"


def sha(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def sampler():
    sys.path.insert(0, str(LEAN / "c_build"))
    sys.path.insert(0, str(LEAN))
    import replay_sample as rs
    WORK.mkdir(parents=True, exist_ok=True)
    rs.SEED = C2_SEED
    rs.HERE = WORK
    rs.LOG = WORK / "progress_prep.log"
    return rs


def cmd_draw(a):
    rs = sampler()
    import shard_golden as sg
    orig = sg.write_shards

    def redirect(keep, out_dir, shard_rows, source_info, overwrite=False):
        out_dir = Path(out_dir)
        if out_dir.name == "c_old_slice_shards":  # the C2-seed old slice must not take the round-1 slice's place
            out_dir = OLD_C2SEED
        return orig(keep, out_dir, shard_rows, source_info, overwrite)

    sg.write_shards = redirect
    t = time.time()
    rep = rs.main(["--write-shards", "--r1", str(a.r1), "--r2", str(a.r2), "--margin", str(a.margin),
                   "--old-slice", "2000", "--denylist-verdicts", str(VERDICTS), "--sealed-sha", SEALED_SHA,
                   "--shards-dir", str(SHARDS)])
    w = rep["write"]
    w["old_slice_shards"]["dir"] = str(OLD_C2SEED.relative_to(LEAN))
    w["old_slice_shards"]["note"] = ("the C2-seed old slice (held out of this draw by the sampler); NOT the mixer's old "
                                     "slice: data/c_old_slice_shards is the round-1 slice (replay_c2.py old-slice)")
    rep["reads_replay_c2"] = {"seed": C2_SEED, "r1": a.r1, "r2": a.r2, "margin": a.margin, "sec": round(time.time() - t),
                              "wrapper_sha256": sha(__file__), "sealed_sha_source": "A15 suite sha256 in PREREG_FINAL.md",
                              "replay_draw_json": {"path": "c2_build/reads/replay_work/replay_draw.json",
                                                   "sha256": sha(WORK / "replay_draw.json")}}
    out = C2 / "replay_c2_write.json"
    out.write_text(json.dumps(rep, indent=1))
    print("wrote", out, sha(out))


def cmd_old_slice(a):
    """Round-1 old slice -> data/c_old_slice_shards, rebuilt from the recorded round-1 ids and checked by sha."""
    sys.path.insert(0, str(LEAN))
    import shard_golden as sg
    r1w = json.loads(R1_WRITE.read_text())["write"]
    want = r1w["old_slice_shards"]
    ids = set(json.loads(R1_DRAW.read_text())["old_slice_ids"])
    keep = []
    with open(LEAN / "data/v14_parts/golden_train.jsonl") as f:
        for line in f:
            r = json.loads(line)
            if r["id"] in ids:
                keep.append(r)
    if len(keep) != want["rows"] or {r["id"] for r in keep} != ids:
        raise SystemExit(f"old slice: found {len(keep)} of {len(ids)} ids (recorded rows {want['rows']})")
    info = {"purpose": "C old slice (monitor)", "seed": 20261003, "from": "data/v14_parts/golden_train.jsonl",
            "rebuilt_for": "C2 (spec 5.4: the same slice as round 1)", "round1_record": "c_build/replay_r1_write.json"}
    man = sg.write_shards(keep, OLD_R1, 2500, info)
    ok = {"ids_sha256": man["ids_sha256"] == want["ids_sha256"], "rows_sha256": man["rows_sha256"] == want["rows_sha256"],
          "files": {s["file"]: s["sha256"] == want["files"].get(s["file"]) for s in man["shards"]}}
    print(json.dumps({"rows": man["rows"], "match_round1_record": ok}, indent=1))
    if not (ok["ids_sha256"] and ok["rows_sha256"]):
        print("NOTE: rows differ from the round-1 shards byte-wise (ids match); record kept for the orchestrator")


def cmd_verify(a):
    sys.path.insert(0, str(LEAN))
    import shard_golden as sg
    rows = [r for p in sg.shard_files(SHARDS) for r in sg.read_jsonl(p)]
    ids = sorted(r["id"] for r in rows)
    a46 = json.loads(A46_DRAW.read_text())
    same = ids == sorted(a46["draw_r1_ids"])
    rep = {"shard_rows": len(rows), "a46_draw_rows": len(a46["draw_r1_ids"]), "identical_id_set": same,
           "only_in_shards": len(set(ids) - set(a46["draw_r1_ids"])), "only_in_a46": len(set(a46["draw_r1_ids"]) - set(ids)),
           "manifest_sha256": sha(SHARDS / "shards.json")}
    print(json.dumps(rep, indent=1))


def cmd_second_pass(a):
    rs = sampler()
    rs.main(["--second-pass", str(SHARDS / f"labels_{C1}"), "--shards-dir", str(SHARDS), "--attacked-pg-rule",
             "clean_partner", "--pg-rule-amendment", "A16"])
    out = C2 / "replay_c2_pg_anchor.json"
    shutil.copyfile(WORK / "replay_r1_pg_anchor.json", out)
    d = json.loads(out.read_text())
    print(json.dumps({"counts": d["counts"], "units_dropped_pg": d["units_dropped_pg"], "pg_rule": d["pg_rule"],
                      "sha256": sha(out)}, indent=1))


def row_key(r) -> str:
    return hashlib.sha1(json.dumps([r.get("state"), r.get("instructions"), r.get("qtype"), r.get("options"),
                                    r.get("card")]).encode()).hexdigest()


def cmd_reuse(a):
    """Copy round-1 HF labels (same C1, same A5 readout) for rows whose read inputs are identical; write a partial label
    set into reads/replay_work/reuse_labels.jsonl keyed by id (the fast read skips them: fast_read label --reuse)."""
    sys.path.insert(0, str(LEAN))
    import shard_golden as sg
    r1d = DATA / "c_replay_r1_shards"
    lab, _ = sg.load_labels(r1d / f"labels_{C1}", r1d, return_view=True)
    old = {}
    for p in sg.shard_files(r1d):
        for r in sg.read_jsonl(p):
            old[row_key(r)] = r["id"]
    n = hit = 0
    out = open(WORK / "reuse_labels.jsonl", "w")
    for p in sg.shard_files(SHARDS):
        for r in sg.read_jsonl(p):
            n += 1
            oid = old.get(row_key(r))
            if oid is not None and set(lab[oid]) == set(
                    (r["options"] if r["qtype"] == "choice" else ["yes", "no"])):
                hit += 1
                out.write(json.dumps({"id": r["id"], "from": oid, "probs": lab[oid]}) + "\n")
    out.close()
    print(json.dumps({"rows": n, "reusable": hit, "share": round(hit / max(1, n), 4),
                      "sha256": sha(WORK / "reuse_labels.jsonl")}))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("draw")
    d.add_argument("--r1", type=int, default=75000)
    d.add_argument("--r2", type=int, default=150000)
    d.add_argument("--margin", type=float, default=0.10)
    for n in ("old-slice", "verify", "second-pass", "reuse-r1-labels"):
        sub.add_parser(n)
    a = ap.parse_args()
    {"draw": cmd_draw, "old-slice": cmd_old_slice, "verify": cmd_verify, "second-pass": cmd_second_pass,
     "reuse-r1-labels": cmd_reuse}[a.cmd](a)


if __name__ == "__main__":
    main()
