"""A20 (d) / A21 (c) pipeline pre-smoke INPUT: a sample of the current partial dry-run mix (CPU only; decides nothing).

Runs c_build/mixer.py's own --dry-run build (unchanged code, imported) with its work folder and log redirected to
c_build/endgame/presmoke/, captures the final-form rows and relations at the point where the mixer computes its config
fill (after drops, refills, targets, G18, token caps, check_rows and the other gates), and writes a seeded sample:
whole relation units, every block present (replay, each family, public, commits).

  .venv/bin/python c_build/endgame/presmoke_mix.py            (from lean/; ~15-20 min on the loaded Mac)

Outputs:
  data/c_presmoke_r1.jsonl, data/c_presmoke_rel_r1.jsonl     (top level of data/, so modal_od's image uploads them;
                                                               DELETE both after the pre-smoke; copies are kept below)
  c_build/endgame/presmoke/c_presmoke_r1.jsonl (+ _rel), presmoke_mix.json (counts, sha256, mixer problems)
"""
from __future__ import annotations

import json
import random
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent            # c_build/endgame
CB = HERE.parent
LEAN = CB.parent
sys.path.insert(0, str(CB))
import mixer  # noqa: E402
from mixio import sha256_file, write_json, write_jsonl  # noqa: E402

OUT = HERE / "presmoke"
SEED = 20261006
PER_BLOCK = {"replay": 420, "public": 120, "COMMIT": 60}
PER_FAMILY = 60


class Captured(Exception):
    pass


def local_check(rows) -> dict:
    """train_decoder.check_rows on the sample, on the Mac (the trainer runs it again on the GPU)."""
    sys.path.insert(0, str(LEAN))
    import train_decoder as td
    try:
        td.check_rows(rows, mixer.KD)
        return {"rows": len(rows), "ok": True}
    except ValueError as e:
        return {"rows": len(rows), "ok": False, "error": str(e)[:400]}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    mixer.WORK = OUT / "work"
    mixer.LOG = HERE / "logs" / "presmoke_mixer.log"
    mixer.cs.LOG = mixer.LOG
    cap = {}
    real_check = mixer.check_rows

    def check_rows(rows, rep):
        out = real_check(rows, rep)
        cap["mixer_check_rows"] = rep.get("check_rows")
        return out

    def config_fill(rows, rels):
        cap["rows"], cap["rels"], cap["stage"] = rows, rels, "config_fill (after every mixer gate)"
        raise Captured

    real_finish = mixer.finish

    def finish(a, ilog, rep, probs, rows, rels, parents, *rest):
        bad = sorted(k for k, v in parents.items() if not all(isinstance(x, str) for x in (v or [])))
        cap["parents_not_str"] = {k: sorted({type(x).__name__ for x in parents[k]}) for k in bad}
        if bad:   # mixer.denylist_query would crash (TypeError: unhashable dict): capture at assembly instead
            cap["rows"], cap["rels"], cap["stage"] = rows, rels, "assembly (mixer.finish entry; drops/gates not run)"
            raise Captured
        return real_finish(a, ilog, rep, probs, rows, rels, parents, *rest)

    mixer.check_rows, mixer.config_fill, mixer.finish = check_rows, config_fill, finish
    a = mixer.argparse.Namespace(dry_run=True, final=False, sealed_sha=None, decontam_drops=[])
    try:
        mixer.build(a)
        raise SystemExit("mixer build returned without reaching config_fill")
    except Captured:
        pass
    rows, rels = cap["rows"], cap["rels"]
    adj = defaultdict(set)
    for x in rels:
        adj[x["a"]].add(x["b"])
        adj[x["b"]].add(x["a"])
    by = defaultdict(list)
    for r in rows:
        by[r["_block"]].append(r["id"])
    rng = random.Random(SEED)
    keep = set()
    for b, ids in sorted(by.items()):
        n = PER_BLOCK.get(b, PER_FAMILY)
        for i in rng.sample(ids, min(n, len(ids))):
            stack = [i]
            while stack:                       # whole relation unit (closure; units are <= 3 rows)
                j = stack.pop()
                if j not in keep:
                    keep.add(j)
                    stack += list(adj[j])
    out_rows = [{k: v for k, v in r.items() if k != "_block"} for r in rows if r["id"] in keep]
    out_rels = [{"a": x["a"], "b": x["b"], "type": x["type"]} for x in rels if x["a"] in keep and x["b"] in keep]
    blocks = Counter(r["_block"] for r in rows if r["id"] in keep)
    tr, rl = OUT / "c_presmoke_r1.jsonl", OUT / "c_presmoke_rel_r1.jsonl"
    sha_t, sha_r = write_jsonl(tr, out_rows), write_jsonl(rl, out_rels)
    data = LEAN / "data"
    shutil.copyfile(tr, data / tr.name)
    shutil.copyfile(rl, data / rl.name)
    rep = {"what": "A20 (d) pipeline pre-smoke input (sample of the partial dry-run mix); decides nothing",
           "seed": SEED, "mix_rows_captured": len(rows), "mix_relations_captured": len(rels),
           "sample_rows": len(out_rows), "sample_relations": len(out_rels), "by_block": dict(blocks),
           "relation_types": dict(Counter(x["type"] for x in out_rels)),
           "train_file_sha256": sha_t, "rel_file_sha256": sha_r,
           "mixer_check_rows_on_full_partial_mix": cap.get("mixer_check_rows"),
           "capture_stage": cap.get("stage"), "parents_not_str_by_source": cap.get("parents_not_str"),
           "trainer_check_rows_on_sample": local_check(out_rows),
           "mixer_sha256": sha256_file(CB / "mixer.py"),
           "data_copies": [f"data/{tr.name}", f"data/{rl.name}"]}
    write_json(OUT / "presmoke_mix.json", rep)
    print(json.dumps({k: rep[k] for k in ("sample_rows", "sample_relations", "by_block", "train_file_sha256",
                                          "capture_stage", "parents_not_str_by_source",
                                          "trainer_check_rows_on_sample")}))


if __name__ == "__main__":
    main()
