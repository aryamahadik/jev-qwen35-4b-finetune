"""make_probe_body.py: write ONE real SGLang /generate body (input_ids + sampling params) for a dev decision, for the
cold-start and keep-alive probes. CPU, tokenizer only; no model is called. Uses the round-2 harness read-only (oc1 from the
round-2 stage folder, or ~/opt_r2 on the VM) and the same body builder the S1 path uses (sglang_host.build_generate_body).

  make_probe_body.py --tokenizer DIR --work-dir DIR_WITH_N.jsonl --index 0 --out out/probe_body.json [--oc1-parent DIR]
  (VM: --oc1-parent ~/opt_r2 --work-dir ~/opt_r2/data --tokenizer ~/lean/models/q35_4b_main500k)
Dev data only (N.jsonl of the SPEED-2 workloads); a path containing 'ohs' is refused. The body holds token ids only.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

DEFAULT_OC1 = C.LEAN / "speed" / "opt_c1_round2_20261017" / "stage"
DEFAULT_WORK = C.LEAN / "speed" / "workloads"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--tokenizer", required=True)
    ap.add_argument("--work-dir", default=str(DEFAULT_WORK))
    ap.add_argument("--oc1-parent", default=str(DEFAULT_OC1))
    ap.add_argument("--name", default="N")
    ap.add_argument("--index", type=int, default=0)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    for p in (a.tokenizer, a.work_dir, a.oc1_parent):
        C.refuse_ohs(p)
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    for p in (a.oc1_parent, str(C.LEAN / "hosting"), str(C.LEAN)):      # on the VM: ~/lean/hosting and ~/lean
        if Path(p).exists() and p not in sys.path:
            sys.path.insert(0, p)
    from oc1 import items as I  # noqa: E402
    R, SH = I.readout_mod(), I.sglang_host_mod()
    tok, ro, _ = I.load_c1(a.tokenizer)
    its = C.read_jsonl(Path(a.work_dir) / f"{a.name}.jsonl")
    prep = I.prepare_one(its[a.index], R, ro, tok)
    body = SH.build_generate_body(prep.items, "ld-probe")
    C.write_json(a.out, body)
    print(f"{a.name}[{a.index}] {prep.n_tokens} tokens, {len(prep.items)} sequence(s) -> {a.out} (sha256 {C.sha256_file(a.out)[:16]})")


if __name__ == "__main__":
    main()
