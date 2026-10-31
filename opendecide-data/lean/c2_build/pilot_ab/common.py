"""Shared constants for the A42-D item 4 single-family pilots (PREREG_FINAL A42-D 4.1-4.4, A37 (i), 12.6).

Nothing here touches a GPU, a network or any sealed path. Paths containing "ohs" are refused by `refuse_path`.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent            # lean/c2_build/pilot_ab
C2B = HERE.parent                                  # lean/c2_build
LEAN = C2B.parent                                  # lean
FAMILIES = ("T40", "T41", "T42", "T43", "T44", "T45")   # A42-D wave 1 = T40-T43, wave 2 = T44, T45 (item 4 / 9)

# --- the pinned starting point and recipe (A37 (i), spec 9.1, A42-D 4.1) -------------------------------------------------
C1_NAME = "q35_4b_main500k"                        # C1 adapter folder name locally and on the L4
C1_INIT_VOL = "/vol/models/q35_4b_main500k_init"   # same bytes on a Modal volume (extra/fix2_spawn.py::fix2_upload_init)
C1_ADAPTER_SHA = "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078"
BASE = "Qwen/Qwen3.5-4B"
BASE_REV = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
LAYOUT = "schema_branch_mark"
STYLE = "cygnet"
SEED = 20261013                                    # A42-D 4.1
ROWS_PER_PILOT = 1500
EXPECT_TRAINABLE = 32464896
TRAIN_FILE, REL_FILE = "pilot_ab_train.jsonl", "pilot_ab_rel.jsonl"   # names inside the staged data folder only

# --- reads (A18.2 readout = C1's own prompt/layout/readout; choice rows read twice, reversed order) --------------------
SPLITS9 = ("dev_nc", "taskbank_dev", "hard_dev", "dev_negwords", "dev_claims", "pg_dev", "devzs", "devp_card", "dev")
EXCLUDE_SOURCES = ("tb_mixtral",)                  # gate_dev.CONSTRAINT_EXCLUDE: 8,143 rows - 1,087 = the 7,056 retention rows
EXPECT_EXISTING_N = 7056
EXPECT_OWN_N = 300
MIN_GPROXY_ROWS, MIN_GPROXY_PAIRS = 2000, 150
READ_TAG = "_pab"                                  # preds_<split>/<adapter><READ_TAG>.jsonl on the L4
GPROXY_SPLIT = "pab_gproxy"
def own_split(fam: str) -> str:
    return f"pab_own_{fam}"
def pilot_name(fam: str) -> str:
    return f"q35_4b_pab_{fam}"

# --- the bars (A42-D 4.2, 4.3; never loosened) ---------------------------------------------------------------------------
OWN_GAIN_MIN = 2.0          # pt, point
EXISTING_DROP_MAX = 0.5     # pt, point
GPROXY_REJECT_UB = -0.5     # pt: rejected iff the CI upper bound is below this
BOOT = {"resamples": 10000, "seed": 0}
EPS = 1e-9


def refuse_path(p) -> str:
    s = str(p)
    low = s.lower()
    bad = ("ohs", "sealed_nd", "c_spec/sealed_brief", "c_build/preread", "external_quarantine", "longbench_v2", "/.claude/",
           "/private/tmp/")
    hit = [b for b in bad if b in low]
    if hit:
        raise SystemExit(f"REFUSED (never-open path, matches {hit}): {s}")
    return s


def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def read_jsonl(p):
    with open(refuse_path(p)) as f:
        return [json.loads(l) for l in f if l.strip()]
