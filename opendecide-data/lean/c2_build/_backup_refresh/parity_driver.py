"""Real-data parity check for refresh-dev (one block, a reduced engine target set, a private dev tree and vector cache).

  A  = full candidates run of the block on dev state A      -> out_A/        (the "older log")
  B  = the dev files change (a block's own mixdev appears, another file shrinks, one more appears)
  Bf = full candidates run on dev state B                   -> out_Bfull/
  Br = refresh-dev from the older log on dev state B        -> out_Bref/
  Br2 = refresh-dev again with nothing changed              -> out_Bref2/   (must equal Br)
Compared: Bf vs Br, field for field, apart from wall_s / unix / embed_stats / refreshed.

Counts, hashes and C2 ids only are printed. No ohs / sealed / Jev path is in the reduced target list (asserted below); the real
sealed checkers and the real hash exports run exactly as in a full run (RUN only). The dev files are copies of the real
c2_mixdev / c2_transfer_dev files in a private folder under lean/; the real dev files, logs and vector cache are never written.
Run: nice -n 10 env G13_STREAM_WORKERS=4 G13_BIGPAT_STREAM=1 G13_BIGPAT_LOCAL=$HOME/.cache/opendecide_ext/bigpat_full \
     ../.venv/bin/python -B c2_build/_backup_refresh/parity_driver.py   (from lean/)
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN / "c2_build"))
NEXT = Path(os.environ.get("G13_MODULE_PATH") or LEAN / "c2_build" / "g13_c2.py")
_spec = importlib.util.spec_from_file_location("g13_c2", NEXT)
G = importlib.util.module_from_spec(_spec)
sys.modules["g13_c2"] = G
_spec.loader.exec_module(G)
g = G.g

BLOCK = os.environ.get("PARITY_BLOCK", "T31")
W = LEAN / "c2_build" / "_backup_refresh" / "parity_work"
BOOK = ("wall_s", "unix", "embed_stats", "refreshed")
T_NAMES = ["dev:taskbank_dev", "dev:hard_dev", "dev:dev_claims", "dev:dev", "mixdev", "eval_opi", "eval_jagged",
           "mixdev_structure", "templates_m8"]


def say(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def strip_book(x):
    if isinstance(x, dict):
        return {k: strip_book(v) for k, v in x.items() if k not in BOOK}
    if isinstance(x, list):
        return [strip_book(v) for v in x]
    return x


def first_diff(a, b, path=""):
    if type(a) is not type(b):
        return f"{path}: type {type(a).__name__} vs {type(b).__name__}"
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                return f"{path}/{k}: only in {'refresh' if k in a else 'full run'}"
            d = first_diff(a[k], b[k], f"{path}/{k}")
            if d:
                return d
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return f"{path}: length {len(a)} vs {len(b)}"
        for i, (x, y) in enumerate(zip(a, b)):
            d = first_diff(x, y, f"{path}[{i}]")
            if d:
                return d
        return None
    return None if a == b else f"{path}: values differ"


def sha(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()


def main() -> int:
    t00 = time.time()
    real = {n: G.dev_files(n) for n in G.C2_DEV}                       # the real dev files, before the specs are moved
    mix = {Path(p).parent.parent.name: Path(p) for p in real["c2_mixdev"]}
    transfer = real["c2_transfer_dev"][0]
    say(f"real dev files: c2_mixdev {len(mix)} (families {sorted(mix)}), c2_transfer_dev {len(real['c2_transfer_dev'])}")
    own = BLOCK
    other_gone = "T33" if "T33" in mix and own != "T33" else sorted(set(mix) - {own})[0]
    shrunk = "GB" if "GB" in mix else sorted(set(mix) - {own, other_gone})[0]
    say(f"state A lacks {own} (the block's own mixdev) and {other_gone}; state B has both, and {shrunk} loses its last 100 rows")

    if W.exists():
        shutil.rmtree(W)
    dev = W / "dev"
    rel_dev = dev.relative_to(LEAN).as_posix()
    G.C2_DEV["c2_mixdev"]["paths"] = [f"lean:{rel_dev}/c2_parts/*/out/mixdev_S5.jsonl"]
    G.C2_DEV["c2_transfer_dev"]["paths"] = [f"lean:{rel_dev}/c2_transfer_dev.jsonl"]

    def set_state(state: str) -> None:
        if dev.exists():
            shutil.rmtree(dev)
        for fam, src in mix.items():
            if state == "A" and fam in (own, other_gone):
                continue
            dst = dev / "c2_parts" / fam / "out" / "mixdev_S5.jsonl"
            dst.parent.mkdir(parents=True, exist_ok=True)
            if state == "B" and fam == shrunk:
                lines = src.read_text().splitlines(keepends=True)
                dst.write_text("".join(lines[:-100]))
            else:
                shutil.copyfile(src, dst)
        (dev).mkdir(parents=True, exist_ok=True)
        shutil.copyfile(transfer, dev / "c2_transfer_dev.jsonl")
        say(f"dev state {state}: {len(G.dev_files('c2_mixdev'))} mixdev files, {len(G.dev_files('c2_transfer_dev'))} transfer")

    by = {t["name"]: t for t in g.targets()}
    red = [by[n] for n in T_NAMES]
    for t in red:
        assert not re.search(r"ohs|sealed|jev|longbench|quarantine|preread", " ".join(t["paths"]), re.I), t["name"]
    tgs = red + G.c2_dev_targets()
    say("reduced engine targets:", [t["name"] for t in tgs])
    g.EMB_DIR = W / "emb"                                              # a private vector cache (the real one is not written)

    ev = {}
    # ---- A: the older log
    set_state("A")
    G.OUT = W / "out_A"
    t0 = time.time()
    recA = G.run("candidates", [BLOCK], embed=True, side=False, tgs=tgs, write=True)[f"c2_cand_{BLOCK}"]
    ev["wall_full_A_s"] = round(time.time() - t0, 1)
    say(f"A done {ev['wall_full_A_s']} s: complete {recA['complete']}, drop units {recA['drop_units']}, "
        f"c2_mixdev {recA['c2_dev_targets']['structure'].get('c2_mixdev')}")
    # ---- B: the mixdev change; the full run on the new files
    set_state("B")
    G.OUT = W / "out_Bfull"
    t0 = time.time()
    recBf = G.run("candidates", [BLOCK], embed=True, side=False, tgs=tgs, write=True)[f"c2_cand_{BLOCK}"]
    ev["wall_full_B_s"] = round(time.time() - t0, 1)
    say(f"Bf done {ev['wall_full_B_s']} s: complete {recBf['complete']}, drop units {recBf['drop_units']}")
    # ---- Br: refresh-dev from the older log
    G.OUT = W / "out_Bref"
    t0 = time.time()
    try:
        recBr = G.refresh_dev([BLOCK], tgs=tgs, log_dir=W / "out_A", write=True)[f"c2_cand_{BLOCK}"]
    except G.RefreshRefused as e:
        for k, v in e.problems.items():
            for w in v:
                say(f"REFUSED [{k}] {w}")
        return 2
    ev["wall_refresh_s"] = round(time.time() - t0, 1)
    ev["refresh_engine_wall_s"] = recBr["refreshed"][-1]["engine_wall_s"]
    say(f"Br done {ev['wall_refresh_s']} s (engine part {ev['refresh_engine_wall_s']} s): complete {recBr['complete']}")
    # ---- Br2: refresh again, nothing changed
    G.OUT = W / "out_Bref2"
    t0 = time.time()
    recBr2 = G.refresh_dev([BLOCK], tgs=tgs, log_dir=W / "out_Bref", write=True)[f"c2_cand_{BLOCK}"]
    ev["wall_refresh2_s"] = round(time.time() - t0, 1)
    say(f"Br2 done {ev['wall_refresh2_s']} s")

    # ---- compare what was WRITTEN (re-read from disk)
    def load(d):
        return json.loads((W / d / f"c2_cand_{BLOCK}.json").read_text())

    A, Bf, Br, Br2 = load("out_A"), load("out_Bfull"), load("out_Bref"), load("out_Bref2")
    sBf, sBr, sBr2, sA = (strip_book(x) for x in (Bf, Br, Br2, A))
    d1, d2 = first_diff(sBr, sBf), first_diff(sBr2, sBr)
    ev.update({
        "parity_refresh_vs_full_identical": d1 is None, "first_difference": d1,
        "canonical_sha256_full_B": sha(sBf), "canonical_sha256_refresh_B": sha(sBr),
        "identity_second_refresh_identical": d2 is None, "first_difference_identity": d2,
        "old_log_differs_from_B_in_drop_ids": sA["drop_ids"] != sBf["drop_ids"],
        "old_log_differs_from_B_in_counts": sA["counts_by_target_and_method"] != sBf["counts_by_target_and_method"],
        "old_log_differs_from_B_in_inputs_at_start": sA["inputs_at_start"] != sBf["inputs_at_start"],
        "drop_units_A": A["drop_units"], "drop_units_B": Bf["drop_units"], "drop_rows_B": len(Bf["drop_ids"]),
        "a53_waived_A": A["a53"].get("waived_units"), "a53_waived_B": Bf["a53"].get("waived_units"),
        "counts_B_c2_dev": {k: {m: c["units"] for m, c in v.items()} for k, v in Bf["counts_by_target_and_method"].items()
                            if k in ("c2_mixdev", "c2_transfer_dev", G.C2_STRUCT)},
        "counts_A_c2_dev": {k: {m: c["units"] for m, c in v.items()} for k, v in A["counts_by_target_and_method"].items()
                            if k in ("c2_mixdev", "c2_transfer_dev", G.C2_STRUCT)},
        "complete_A_B_Bf_Br": [A["complete"], Bf["complete"], Br["complete"]],
        "key_order_identical_apart_from_bookkeeping": json.dumps(sBr) == json.dumps(sBf),
        "bytes_log_full_B": (W / "out_Bfull" / f"c2_cand_{BLOCK}.json").stat().st_size,
        "status_problems_refreshed_log": G.log_problems([W / "out_Bref" / f"c2_cand_{BLOCK}.json"]),
        "status_problems_full_B_log": G.log_problems([W / "out_Bfull" / f"c2_cand_{BLOCK}.json"]),
        "tool_sha256": Br["tool_sha256"], "engine_sha256": Br["engine_sha256"],
        "refreshed_entry": Br["refreshed"],
        "wall_total_s": round(time.time() - t00, 1),
    })
    (W / "evidence.json").write_text(json.dumps(ev, indent=1, default=str))
    say("EVIDENCE", json.dumps(ev, indent=1, default=str))
    return 0 if d1 is None and d2 is None else 1


if __name__ == "__main__":
    sys.exit(main())
