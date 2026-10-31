"""C2 mixer (C2_DATA_SPEC 5.1-5.5, 3.0, 4.3, 6.1, 6.3, 6.4 step 10, 9.1-9.2; PREREG A37 d/e/f/i/j). CPU only: no
Modal, gcloud, GPU or paid call; no git.

A copy of c_build/mixer.py's logic for C2 (spec 6.1: "a copy with C2 shares and the OHS-4 sha"). mixer.py, mixio.py,
crowd_select.py and replay_sample.py are imported and never edited. Their round-1 helpers are reused as they are
(relation units, refills, G18, E2, the deny-list query, the held-out S7 check, the G15 unit check,
train_decoder.check_rows, G10). The functions that name round-1 files or the round-1 seed are copied here with C2
paths and the A37 seed (20261013).

Shares (spec 5.1, A37 d). New rows = the 17 program families at their spec 2.1 targets (agent tier 13,600, everyday
7,000) + T37b 2,000 + carry-over F5 1,500 (+ F6 <= 1,000, F11 <= 1,000, F4 <= 500 when gated) <= 26,600 (40%).
Replay = floor(1.5 x realised new rows) (60%), always. Total <= 66,500.

Entry (spec 5.3, A37 d). A block enters only when its QC record (data/c2_parts/<B>/qc/QC_REPORT.json) says pass=true,
was passed by the data cutoff (Tue 20 Oct 2026 23:59 UTC) within 2 fix iterations, and records the sha256 of the
files on disk; and its C2 crowd selection (c2_select.py) matches the candidates and passes its checks. A block that
does not enter lowers the total; nothing refills it (A34 c). --leave-out drops a block on purpose (spec 10.2 usage cut
order); T28, T33, T29 and T37b are never cut. Minimum to train: >= 5 of the 6 agent-core families (T28, T33, T29,
T30, T27, T26) and >= 10 program families; otherwise --final refuses (stop and report; no training).

Caps (spec 5.2). One family <= 2,400 rows. The agent tier <= 55% of new rows: when other blocks are missing, the agent
families are re-selected down in proportion (whole units, the same seed and key: c2_select.reselect), so missing
shares lower the total and are never refilled. Free-form rows (meta.c2.author_mode "F") <= 25% per family (T07, T32
<= 40%). Every new row <= 2,000 real tokens (a longer row drops its unit, refilled from the same block's unselected
units), each new block's mean <= 800. New yes/no rows 45-55%. G10 cells 50 +/- 2 (mixer.g10_checks). Easy <= 25% and
hard <= 30% per block. No new ordinal row. Hard 0/1 labels on every new row (no teacher, no gold_probs; the C1 anchor
is on replay rows only). No S5 / dev_only row trains.

Replay (spec 5.4). The C2 draw of replay_sample.py (unchanged; a new seed) and its second pass (C1 read, the A16 p_g
rule, the C1 anchor flags): whole relation units, E2, the round-1 old slice held out, the replay deny-list verdicts,
and logs/decontam_counts/pool_drops_r1.json applied as a G13 drop list on every run.

A42-D / A45 changes (15 Oct 2026; no bar loosened). The 17-family shares above stay; the mix also takes
  - the new families T40-T45 (A42-D 1.1 budgets 1,333 / 1,166 / 1,333 / 1,166 / 833 / 833; T45 restored by A47). They count
    in the agent tier, enter only with a logged pilot verdict (families' qc/PILOT_GATE.json, verdict logged by Mon 19 Oct 23:59 UTC; QC by Wed 21 Oct 23:59 UTC,
    A42-D 1.6 / 3.6 / 4.2) and never count toward the 10 program families;
  - the G-block "GB" (A42-D 5; <= 15,000 rows incl. its twins, no domain above 20%, twins <= 5,000), the metadata block
    "MD" (A42-D 8; 8,000-12,000 incl. twins, source <= 15%, domain <= 20%, >= 8 domains, >= 30% card-free per source,
    twins <= 5,000) and the replay yes/no twins "RTW" (A42-D 7; T37b + RTW <= 10,000, inside the replay budget). All
    use the same data/c2_parts/<B>/out + MANIFEST + qc/QC_REPORT.json + crowd-select (select_<B>.json) interface;
  - replay = floor(1.5 x realised new rows) always (RTW rows are replay-side and count inside it), total <= 125,000.

Entry (spec 5.3, A37 d, A39 g, A42-D 1.6). A block enters only when its QC record (data/c2_parts/<B>/qc/QC_REPORT.json)
says pass=true, was passed by the data cutoff (Wed 21 Oct 2026 23:59 UTC; A39 g moved it from Tue 20 Oct; a new family
by Mon 19 Oct 23:59 UTC, A42-D 3.6) within 2 fix iterations, and records the sha256 of the files on disk; and its C2
crowd selection (c2_select.py) matches the candidates and passes its checks. A block that does not enter lowers the
total; nothing refills it (A34 c). --leave-out drops a block on purpose; T28, T33, T29 and T37b are never cut. Minimum to
train: >= 5 of the 6 agent-core families and >= 10 program families (T40-T45 do not count); otherwise --final refuses.

Caps (spec 5.2, A42-D 1.5), asserted on the realised rows: one family <= 2,400; agent tier (incl. T40-T45) <= 55% of new
rows (T40-T45 scaled down first, in proportion, then the older agent families); free-form <= 25% per family (T07, T32
<= 40%); every new row <= 2,000 real tokens, block mean <= 800; new yes/no 45-55%; G10 cells 50 +/- 2; easy <= 25%, hard
<= 30%; no ordinal row; hard 0/1 labels; no S5 / dev_only row; <= 64 rows per card; new <= 40% / replay >= 60%.

Money and size trim (A42-D 2.3). T_max = min($34, $32 - C2 Modal spend to date) (--spend-to-date, required; replaces
the old $17). The projection is unchanged: real padded tokens through the trainer's own batching, 0.163 ms per padded
token (A28) at $4.09/h, + $2 smoke. If it is above T_max, or the mix is above 125,000 rows, trim in this order, seeded
(20261013) whole-unit removal with the replay following floor(1.5 x new), each step used up before the next:
  1. item 10 rows (none in C2, A45 f; the hook is ITEM10_BLOCKS);  2. wave 2 (T44, T45 in proportion);
  3. metadata rows above 8,000, as whole tasks, keeping the source / domain rules of A42-D 8.2;
  4. spec 5.5's proportional trim of every new block (family shares and balance rules kept).
Below 50,000 rows it stops and asks the owner (SystemExit).

OHS-4 (A37 f, A38). --final refuses until --ohs4-sha equals OHS4_MANIFEST_SHA256 (A38's MANIFEST.json sha256) and
appears in the A38 block of PREREG_FINAL.md. The manifest records it. G13 #3 on the final mix (new targets) and the
orchestrator's counts-only OHS-4 / OHS-AC sealed-side child run after the mix, then preflight (spec 6.4 step 10); the
manifest lists them as pending. No path here opens OHS material (c2io guard) and no training input may be a data/ohs3*,
ohs3_parts/, ohs4_sealed/, ohs_ac_sealed/ path, the G-proxy file or a never-train-manifest anchor (A42-D 13.1).

  ../.venv/bin/python c2_build/mix_c2.py --dry-run --spend-to-date 1.5 [--leave-out T25 ...]
  ../.venv/bin/python c2_build/mix_c2.py --final --spend-to-date <USD> --ohs4-sha <A38 sha> --decontam-drops \
      logs/decontam_counts/c2_*.json --never-train-manifest <file> --gproxy-file <file>
"""
from __future__ import annotations

import argparse
import datetime
import json
import math
import random
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import c2io  # noqa: E402
from c2io import AGENT_CORE, C1, CARRY, PROGRAM, SEED, C2InputLog  # noqa: E402
from c2io import AGENT as AGENT_V1, TARGETS as BASE_TARGETS  # noqa: E402
import c2_select  # noqa: E402
import a49c  # noqa: E402  (A49 c balance checks on the selected rows)

import crowd_select as cs  # noqa: E402  (c_build: imported, never edited)
import mixer as mx  # noqa: E402
from mixio import h64, log_line, sha256_file  # noqa: E402

LEAN, DATA, C2_PARTS = c2io.LEAN, c2io.DATA, c2io.C2_PARTS
WORK = c2io.HERE / "mix_c2"
LOG = c2io.HERE / "progress_c2.log"
OUT_TRAIN, OUT_REL, OUT_MAN = C2_PARTS / "c2_train.jsonl", C2_PARTS / "c2_rel.jsonl", C2_PARTS / "c2_mix_manifest.json"
REPLAY = {                                       # the C2 replay draw and its second pass (inputs; written after A38)
    "shards": DATA / "c2_replay_shards",
    "labels": DATA / "c2_replay_shards" / f"labels_{C1}",
    "pg_anchor": c2io.HERE / "replay_c2_pg_anchor.json",
    "write": c2io.HERE / "replay_c2_write.json",
    "verdicts": c2io.CB / "replay_denylist_verdicts.json",      # the same golden_train pool: the round-1 verdicts
    "golden_rels": DATA / "v14_parts/golden_relations.jsonl",
    "old_slice": DATA / "c_old_slice_shards",                   # spec 5.4: the round-1 old slice
}
POOL_DROPS_R1 = LEAN / "logs/decontam_counts/pool_drops_r1.json"   # spec 5.4: always a G13 drop list
DENYLIST = DATA / "c_parts/denylist.json"
# spec 7.1, frozen before training (gate_c2 reads). c2_t37b_dev removed 16 Oct 2026: T37b is in C3 (PREREG A52 a), so no
# T37b-dev set exists for C2 (gate_c2.py's T37B_DEV label is the dev gate's concern, not a decontamination target).
DEV_SETS = {"c2_mixdev": DATA / "c2_mixdev.jsonl", "c2_transfer_dev": DATA / "c2_transfer_dev.jsonl"}

# ---- spec 5.2 / 5.3 / 5.5 and A42-D constants ---------------------------------------------------------------------------
NEW_FAMILIES = dict(c2io.NEW_FAMILIES)           # A42-D 1.1 budgets; T45 833 restored by A47 (supersedes A45 d)
C3_FAMILIES = ()                                 # A47: T45 is built; it moves to C3 only by the pre-freeze bar / pilot deadline
NEW_FAMILY_ROWS_MAX = 6666                       # A42-D 1.2: new-family rows <= 6,666 (replay <= 10,000)
WAVE2_NEW = ("T44", "T45")                       # A42-D 2.3 step 2 (T45 restored by A47)
ITEM10_BLOCKS = ("I10",)                         # A42-D 2.3 step 1 hook; item 10 is not built for C2 (A45 f)
G_BLOCK, META_BLOCK, REPLAY_TWINS = "GB", "MD", "RTW"
W2_BLOCK = "GW"                                  # A40 + addendum: G-block wave 2 + W8 (general-data tier, like GB)
GENERAL_BLOCKS = (G_BLOCK, W2_BLOCK)             # real-text / general-data blocks: domain cap 20%, spec 5.5 proportional trim
GW_TYPE_MAX = 1200                               # A40 (d): <= 1,200 kept rows per wave-2 type (the domain of a GW row)
BLOCK_TARGETS = dict(c2io.BLOCK_TARGETS)         # selection targets (caps; short = fine)
BLOCK_CAPS = dict(c2io.BLOCK_CAPS)               # A39 e / A42-D 8.2 / A42-D 7.1
TARGETS = {**BASE_TARGETS, **NEW_FAMILIES, **BLOCK_TARGETS}               # every block the mixer knows
AGENT = {**AGENT_V1, **NEW_FAMILIES}             # A42-D 1.5: T40-T45 count in the agent tier
REPLAY_SIDE = ("replay", REPLAY_TWINS)           # A42-D 7.2: replay twins count inside the replay budget
RTW_WITH_T37B_MAX = 10000                        # A42-D 7.1: replay yes/no <= 10,000 including the original T37b
TWIN_CAP = {G_BLOCK: 5000, META_BLOCK: 5000}     # A42-D 7.1 (inside the block caps)
DOMAIN_MAX, SOURCE_MAX, META_MIN_ROWS, META_DOMAINS_MIN = 0.20, 0.15, 8000, 8
CARD_FREE_MIN, META_TASK_ROWS_MAX, META_TASKS_PER_SOURCE = 0.30, 200, (40, 80)
GB_YES_BAND, GB_CARD_MIN_ROWS = (0.40, 0.60), 10 # A42-D 5.5 (per card; a card under 10 rows cannot hold 40-60%)
ROWS_PER_CARD_MAX = 64                           # A42-D 1.5 / spec 3.0 (families)
ROWS_MAX = 125000                                # A40 (d), A42-D 1.4: the whole mix incl. every twin
T_MAX_CAP, T_MAX_BASE = 34.0, 32.0               # A42-D 2.3: T_max = min(34, 32 - C2 Modal spend to date)
FAMILY_MAX = 2400
REPLAY_X = 1.5
AGENT_SHARE_MAX = 0.55                           # A <= 0.55 (A + O)  <=>  9 A <= 11 O (integers)
FREEFORM_MAX, FREEFORM_MAX_FAM = 0.25, {"T07": 0.40, "T32": 0.40}
TOK_MAX, TOK_MEAN_MAX, ROW_TOK_HARD = 2000, 800, mx.MAX_TOK
YESNO_BAND = (0.45, 0.55)
EASY_MAX, HARD_MAX = cs.CAP["easy"], cs.CAP["hard"]
CUTOFF_UTC = "2026-10-21T23:59:00+00:00"         # A39 (g) / A42-D 1.6 (binding): Wed 21 Oct 23:59 UTC (A37 d said Tue 20 Oct)
NEW_FAMILY_DEADLINE_UTC = "2026-10-19T23:59:00+00:00"   # A42-D 1.6 / 3.6: T40-T45 verdict + iteration-2 gates, Mon 19 Oct
FIX_MAX = 2
# A48 (a): the final iteration per family set by A44 (a) / A45 (b, c); every other family keeps FIX_MAX.
FIX_MAX_BY_FAMILY = {"T06": 3, "T31": 3, "T01": 3, "T29": 4, "T35": 4, "T37b": 2, "T19": 2, "T20": 3, "T36": 2}
PILOT_MIN_GAIN_PT, PILOT_MAX_EXISTING_DROP_PT, PILOT_GPROXY_REJECT_PT = 2.0, 0.5, -0.5   # A42-D 4.2 / 4.3
MIN_CORE, MIN_PROGRAM = 5, 10
NEVER_CUT = ("T28", "T33", "T29", "T37b")        # spec 10.2
MS_PER_PADDED, USD_H, OVERHEAD_USD, FLOOR_ROWS = 0.163, 4.09, 2.0, 50000
BATCH, PERM_TWIN, MICRO_TOKENS = 16, 0.3, 8192   # recipe 9.1 (C1's settings)
BUDGET_ROUNDS, BUDGET_MARGIN = 10, 0.995
TRIM_ORDER = ("item10", "wave2", "meta_tail", "proportional")              # A42-D 2.3
REFILL_ROUNDS = 6
OHS4_MANIFEST_SHA256: str | None = "c0217e7739c570b9d22176b68e1c489623dcd5f7c551011606b6ff17e59c09c3"   # Ruling A38
TRAIN_EXCLUDE = ("ohs3", "ohs3_parts", "ohs4_sealed", "ohs_ac_sealed")   # A42-D 13.1: no training glob reads these
PENDING_AFTER_MIX = ("G13 #3: decontam_g13.py refresh on the final mix against the new targets (OHS-4 exports, C2 "
                     "mixdev, transfer dev, T37b-dev), C2 target-registry wrapper", "OHS-4 sealed-side child "
                     "(orchestrator, counts only; spec 8.4)", "preflight (r1_check-style projection and config fill)")


def log(msg):
    try:
        c2io.require_a38()
        log_line(LOG, "mix_c2: " + msg)
    except Exception:  # noqa: BLE001 - before A38 nothing is written
        pass
    print(msg, flush=True)


def is_new(r) -> bool:
    return r["_block"] not in REPLAY_SIDE


# ================================================================== pure rules (unit-tested in memory)

def parse_utc(s) -> datetime.datetime | None:
    try:
        t = datetime.datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except ValueError:
        return None
    return t if t.tzinfo else None


def deadline_for(block: str) -> str:
    """The QC deadline of a block: Wed 21 Oct 23:59 UTC (A39 g, A42-D 1.6) for every block, T40-T45 included. For a new
    family only its PILOT verdict has the earlier time (NEW_FAMILY_DEADLINE_UTC, Mon 19 Oct 23:59 UTC; pilot_problems)."""
    return CUTOFF_UTC


def pilot_problems(block: str, rec: dict | None, deadline: str = NEW_FAMILY_DEADLINE_UTC) -> list[str]:
    """A42-D 1.6 / 4.2 / 4.3: a new family enters only with a logged pilot verdict, by Mon 19 Oct 23:59 UTC, that holds
    all three keep-conditions on the numbers (never on a bare verdict): own-dev gain >= +2.0 pt, existing dev drop
    <= 0.5 pt, G-proxy change not rejected (CI upper bound >= -0.5 pt). [] = it may enter."""
    if not isinstance(rec, dict):
        return [f"{block}: no logged pilot verdict (qc/PILOT_GATE.json; A42-D 1.6)"]
    out = []
    if str(rec.get("verdict")).upper() != "PASS":
        out.append(f"{block}: pilot verdict is {rec.get('verdict')!r}, not PASS (A42-D 4.2)")
    t = parse_utc(rec.get("logged_utc"))
    if t is None:
        out.append(f"{block}: pilot verdict has no logged_utc (ISO 8601 with a UTC offset)")
    elif t > parse_utc(deadline):
        out.append(f"{block}: pilot verdict logged {rec['logged_utc']}, after {deadline} (A42-D 1.6)")

    def num(k):
        v = rec.get(k)
        return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) else None
    gain, drop, gp = num("own_dev_gain_pt"), num("existing_dev_drop_pt"), num("gproxy_change_ci_upper_pt")
    if gain is None or gain < PILOT_MIN_GAIN_PT - 1e-12:
        out.append(f"{block}: own-dev gain {gain} pt < +{PILOT_MIN_GAIN_PT} (A42-D 4.2 i)")
    if drop is None or drop > PILOT_MAX_EXISTING_DROP_PT + 1e-12:
        out.append(f"{block}: existing dev drop {drop} pt > {PILOT_MAX_EXISTING_DROP_PT} (A42-D 4.2 ii)")
    if gp is None or gp < PILOT_GPROXY_REJECT_PT:
        out.append(f"{block}: G-proxy change CI upper bound {gp} pt < {PILOT_GPROXY_REJECT_PT} (A42-D 4.3: rejected)")
    return out


def admission(block: str, qc: dict | None, binding: list[str], selection: str | None = None,
              cutoff: str | None = None, pilot: dict | None = None) -> list[str]:
    """Why a block may NOT enter (spec 5.3; [] = it enters): QC pass, passed by the block's deadline (deadline_for),
    <= 2 fix iterations, the QC record tied to the files on disk, its selection problem (None = the selection passes),
    and for T40-T45 a logged pilot verdict that holds (pilot_problems)."""
    cutoff = cutoff or deadline_for(block)
    if not isinstance(qc, dict):
        return [f"{block}: no QC_REPORT.json"]
    out = []
    if qc.get("pass") is not True:
        out.append(f"{block}: QC pass is not true")
    t = parse_utc(qc.get("passed_utc"))
    if t is None:
        out.append(f"{block}: QC record has no passed_utc (ISO 8601 with a UTC offset)")
    elif t > parse_utc(cutoff):
        out.append(f"{block}: passed {qc['passed_utc']}, after the data cutoff {cutoff} (spec 5.3: no waiting)")
    fi = qc.get("fix_iterations")
    if not isinstance(fi, int) or isinstance(fi, bool) or fi < 0:
        out.append(f"{block}: QC record has no fix_iterations count")
    elif fi > FIX_MAX_BY_FAMILY.get(block, FIX_MAX):
        out.append(f"{block}: {fi} fix iterations (> {FIX_MAX_BY_FAMILY.get(block, FIX_MAX)}: the family is cut, spec 5.3 / A48 a)")
    out += [f"{block}: QC_REPORT.json {p}" for p in binding]
    if selection:
        out.append(f"{block}: {selection}")
    if block in NEW_FAMILIES:
        out += pilot_problems(block, pilot)
    return out


def minimum_to_train(entered) -> tuple[bool, dict]:
    """Spec 5.3: >= 5 of the 6 agent-core families and >= 10 program families, else stop and report (no training)."""
    core = [f for f in AGENT_CORE if f in entered]
    prog = [f for f in PROGRAM if f in entered]
    ok = len(core) >= MIN_CORE and len(prog) >= MIN_PROGRAM
    return ok, {"agent_core": core, "agent_core_n": len(core), "program_families": prog, "program_n": len(prog),
                "rule": f">= {MIN_CORE} of {list(AGENT_CORE)} and >= {MIN_PROGRAM} program families", "ok": ok}


def agent_cap(other: int) -> int:
    """The most agent-tier rows A with A <= 55% of (A + other): 9 A <= 11 other."""
    return (11 * other) // 9


def plan_shares(realised: dict) -> dict:
    """Expected rows per block from the rows each entered block holds now: min(rows, spec target, 2,400 [a family] or
    its block cap [GB, MD, RTW]); T40-T45 together <= 6,666 (A42-D 1.2); the agent tier (incl. T40-T45) cut to 55% of new
    rows (A42-D 1.5: T40-T45 are scaled down first, in proportion, then the older agent families); replay =
    floor(1.5 x new), of which the replay twins RTW (T37b + RTW <= 10,000, A42-D 7.1) are a part; total = new + replay."""
    bad = sorted(set(realised) - set(TARGETS))
    if bad:
        raise ValueError(f"blocks without a spec target: {bad}")
    t = {b: max(0, min(int(n), TARGETS[b], BLOCK_CAPS.get(b, FAMILY_MAX))) for b, n in realised.items()}
    if REPLAY_TWINS in t:
        t[REPLAY_TWINS] = min(t[REPLAY_TWINS], max(0, RTW_WITH_T37B_MAX - t.get("T37b", 0)))
    nf = {b: n for b, n in t.items() if b in NEW_FAMILIES}
    if sum(nf.values()) > NEW_FAMILY_ROWS_MAX:
        t.update(mx.largest_remainder(nf, NEW_FAMILY_ROWS_MAX))
        nf = {b: t[b] for b in nf}
    rtw = t.get(REPLAY_TWINS, 0)
    new_part = {b: n for b, n in t.items() if b != REPLAY_TWINS}
    agent = {b: n for b, n in new_part.items() if b in AGENT}
    other = sum(n for b, n in new_part.items() if b not in AGENT)
    a_now, a_max = sum(agent.values()), agent_cap(other)
    cap = {"agent_rows": a_now, "other_rows": other, "agent_max": a_max, "applied": a_now > a_max}
    if a_now > a_max:
        first = min(a_now - a_max, sum(nf.values()))                    # T40-T45 first, in proportion
        if first > 0:
            cut_nf = mx.largest_remainder(nf, sum(nf.values()) - first)
            cap["new_family_cut"] = {b: [nf[b], cut_nf[b]] for b in sorted(nf)}
            t.update(cut_nf)
            agent.update(cut_nf)
        a_now2 = sum(agent.values())
        if a_now2 > a_max:                                              # then the older agent families
            old = {b: n for b, n in agent.items() if b not in NEW_FAMILIES}
            cut = mx.largest_remainder(old, a_max - sum(n for b, n in agent.items() if b in NEW_FAMILIES))
            cap["by_family"] = {b: [old[b], cut[b]] for b in sorted(old)}
            t.update(cut)
    new = sum(n for b, n in t.items() if b != REPLAY_TWINS)
    rp = math.floor(REPLAY_X * new)
    return {"targets": dict(sorted(t.items())), "new": new, "replay": rp, "replay_twins": rtw,
            "replay_sampler": max(0, rp - rtw), "total": new + rp, "agent_cap": cap}


def scale_plan(realised: dict, f: float) -> dict:
    """Budget trim (spec 5.5): every new block to its share of floor(f x new rows) (largest remainder, so the family
    shares are kept), then the caps of plan_shares again. RTW (replay side) is scaled with the replay budget."""
    new_b = {b: n for b, n in realised.items() if b != REPLAY_TWINS}
    want = math.floor(max(0.0, min(1.0, f)) * sum(new_b.values()))
    out = mx.largest_remainder({b: n for b, n in new_b.items() if n > 0}, want) | {b: 0 for b, n in new_b.items() if n <= 0}
    if REPLAY_TWINS in realised:
        out[REPLAY_TWINS] = math.floor(max(0.0, min(1.0, f)) * realised[REPLAY_TWINS])
    return plan_shares(out)


def a38_block(prereg_text: str) -> str:
    """The text of the 'Ruling A38' block (its quoted lines) in PREREG_FINAL.md, or ''."""
    lines, out, inside = prereg_text.splitlines(), [], False
    for ln in lines:
        if re.match(r"^>\s*\*\*Ruling A38\b", ln):
            inside = True
        elif inside and not ln.startswith(">"):
            break
        if inside:
            out.append(ln)
    return "\n".join(out)


def ohs4_problem(sha: str | None, prereg_text: str, pinned: str | None = None) -> str | None:
    """--final's OHS-4 check: the placeholder must be filled from A38, and --ohs4-sha must equal it and appear in the
    A38 block. Nothing here reads OHS-4 itself (the sha is a recorded number)."""
    pinned = OHS4_MANIFEST_SHA256 if pinned is None else pinned
    if not pinned:
        return "OHS4_MANIFEST_SHA256 is still the placeholder: fill it from Ruling A38 (the OHS-4 freeze) first"
    if not re.fullmatch(r"[0-9a-f]{64}", str(sha or "")):
        return "--ohs4-sha is not a sha256"
    if sha != pinned:
        return "--ohs4-sha is not the A38 manifest sha256 pinned in mix_c2.py"
    blk = a38_block(prereg_text)
    if not blk:
        return "PREREG_FINAL.md has no 'Ruling A38' block (OHS-4 is not frozen)"
    if sha not in blk:
        return "the OHS-4 manifest sha256 does not appear in the Ruling A38 block"
    return None


def cap_checks(rows, ntok: dict, final: bool = True) -> tuple[dict, list[str]]:
    """Spec 3.0 / 4.3 / 5.2 caps on the new rows. Returns (report, problem lines)."""
    new = [r for r in rows if is_new(r)]
    by = defaultdict(list)
    for r in new:
        by[r["_block"]].append(r)
    rep, probs = {}, []
    for b, rr in sorted(by.items()):
        n = len(rr)
        tok = [ntok.get(r["id"], 0) for r in rr]
        bins = Counter((r.get("meta") or {}).get("difficulty_bin") or "na" for r in rr)
        ff = sum(1 for r in rr if ((r.get("meta") or {}).get("c2") or {}).get("author_mode") == "F")
        ordi = sum(1 for r in rr if isinstance((r.get("meta") or {}).get("option_level"), dict))
        soft = sum(1 for r in rr if mx.own_target(r.get("meta") or {}))
        dev = sum(1 for r in rr if (r.get("meta") or {}).get("dev_only") or (r.get("meta") or {}).get("sampler") == "S5")
        yn = sum(1 for r in rr if r["qtype"] == "noul")
        x = {"rows": n, "tok_mean": round(sum(tok) / max(1, n), 1), "tok_max": max(tok, default=0),
             "rows_over_2000": sum(1 for t in tok if t > TOK_MAX), "yes_no_share": round(yn / max(1, n), 4),
             "freeform_share": round(ff / max(1, n), 4), "bins": dict(bins),
             "easy_share": round(bins["easy"] / max(1, n), 4), "hard_share": round(bins["hard"] / max(1, n), 4),
             "ordinal_rows": ordi, "soft_label_rows": soft, "dev_only_or_s5_rows": dev}
        if b in PROGRAM or b in NEW_FAMILIES:                       # A42-D 1.5 / spec 3.0: rows per card <= 64
            cards = Counter(card_of(r) for r in rr if card_of(r))
            x["max_rows_per_card"] = max(cards.values(), default=0)
            if x["max_rows_per_card"] > ROWS_PER_CARD_MAX:
                probs.append(f"{b}: a card holds {x['max_rows_per_card']} rows > {ROWS_PER_CARD_MAX} (A42-D 1.5)")
        x["twin_rows"] = sum(1 for r in rr if is_twin(r))
        rep[b] = x
        if x["rows_over_2000"]:
            probs.append(f"{b}: {x['rows_over_2000']} new rows over {TOK_MAX} tokens (spec 3.0)")
        if x["tok_mean"] > TOK_MEAN_MAX:
            probs.append(f"{b}: mean {x['tok_mean']} tokens per row > {TOK_MEAN_MAX} (spec 3.0)")
        cap = FREEFORM_MAX_FAM.get(b, FREEFORM_MAX)
        if ff / max(1, n) > cap + 1e-12 and b not in BLOCK_TARGETS:      # spec 3.0 / 5.2 bind per FAMILY; blocks (GB, GW, MD, RTW) are real-text / routed: report only
            probs.append(f"{b}: free-form rows {x['freeform_share']:.3f} > {cap} (spec 3.0 / 5.2)")
        if bins.get("na") and final:
            probs.append(f"{b}: {bins['na']} rows without a crowd difficulty bin (G9)")
        if bins["easy"] / max(1, n) > EASY_MAX + 1e-9 or bins["hard"] / max(1, n) > HARD_MAX + 1e-9:
            probs.append(f"{b}: difficulty easy {x['easy_share']} / hard {x['hard_share']} outside easy <= "
                         f"{EASY_MAX}, hard <= {HARD_MAX} (spec 3.0 / 5.2)")
        if ordi:
            probs.append(f"{b}: {ordi} new ordinal rows (spec 5.2: none; T20 is not trained)")
        if soft:
            probs.append(f"{b}: {soft} new rows with a soft target (spec 4.3: hard 0/1 labels on every new row)")
        if dev:
            probs.append(f"{b}: {dev} S5 / dev_only rows in training (mixdev / transfer dev only)")
    yn = sum(1 for r in new if r["qtype"] == "noul")
    share = yn / max(1, len(new))
    rep["_new_yes_no_share"] = round(share, 4)
    if new and not YESNO_BAND[0] - 1e-9 <= share <= YESNO_BAND[1] + 1e-9:
        probs.append(f"new yes/no rows {share:.3f} outside {YESNO_BAND[0]}-{YESNO_BAND[1]} (spec 5.2)")
    return rep, probs


def share_checks(by: Counter, plan: dict) -> tuple[dict, list[str]]:
    """Realised vs planned rows (spec 5.1 / 5.2, A42-D 1.2 / 1.4 / 1.5): no block above its plan (a block short after
    drops it could not refill is reported: missing shares lower the total), replay side (replay + RTW) = floor(1.5 x
    realised new), new <= 40% of the mix, total <= 125,000, T40-T45 <= 6,666, the agent tier (incl. T40-T45) <= 55% of
    new, one family <= 2,400 (GB / MD / RTW: their block caps), no unplanned block."""
    newb = {b: n for b, n in by.items() if b not in REPLAY_SIDE}
    new = sum(newb.values())
    rside = by.get("replay", 0) + by.get(REPLAY_TWINS, 0)
    probs = []
    above = {b: [n, plan["targets"].get(b, 0)] for b, n in {**newb, **({REPLAY_TWINS: by[REPLAY_TWINS]}
                                                                         if REPLAY_TWINS in by else {})}.items()
             if n > plan["targets"].get(b, 0)}
    if above:
        probs.append(f"blocks above their planned rows: {above}")
    short = {b: [by.get(b, 0), t] for b, t in plan["targets"].items() if by.get(b, 0) < t}
    rp_want = math.floor(REPLAY_X * new)
    if rside != rp_want:
        probs.append(f"replay {rside:,} rows vs floor(1.5 x {new:,} new) = {rp_want:,} (spec 5.3)")
    tot = new + rside
    if 3 * new > 2 * rside + 1:
        probs.append(f"new rows {new:,} are {new / max(1, tot):.4f} of the mix > 40% (spec 5.1; replay >= 60%)")
    if tot > ROWS_MAX:
        probs.append(f"total {tot:,} > {ROWS_MAX:,} (A40 d / A42-D 1.4)")
    nfr = sum(n for b, n in newb.items() if b in NEW_FAMILIES)
    if nfr > NEW_FAMILY_ROWS_MAX:
        probs.append(f"T40-T45 hold {nfr:,} rows > {NEW_FAMILY_ROWS_MAX:,} (A42-D 1.2)")
    a = sum(n for b, n in newb.items() if b in AGENT)
    if 9 * a > 11 * (new - a):
        probs.append(f"agent tier {a:,} rows = {a / max(1, new):.3f} of new rows > {AGENT_SHARE_MAX} (spec 5.2)")
    big = {b: n for b, n in newb.items() if b not in BLOCK_CAPS and n > FAMILY_MAX}
    if big:
        probs.append(f"families above {FAMILY_MAX:,} rows: {big} (spec 5.2)")
    bigb = {b: n for b, n in by.items() if b in BLOCK_CAPS and n > BLOCK_CAPS[b]}
    if bigb:
        probs.append(f"blocks above their cap {BLOCK_CAPS}: {bigb} (A39 e / A42-D 7, 8)")
    if REPLAY_TWINS in by and by[REPLAY_TWINS] + by.get("T37b", 0) > RTW_WITH_T37B_MAX:
        probs.append(f"replay yes/no rows (T37b + RTW) {by[REPLAY_TWINS] + by.get('T37b', 0):,} > {RTW_WITH_T37B_MAX:,} "
                     "(A42-D 7.1)")
    return {"by_block": {b: [by.get(b, 0), plan["targets"].get(b, 0)] for b in sorted(set(by) | set(plan["targets"]))},
            "short_after_drops": short, "new": new, "replay": [rside, rp_want], "replay_sampler": by.get("replay", 0),
            "replay_twins": by.get(REPLAY_TWINS, 0), "total": tot, "agent_share": round(a / max(1, new), 4),
            "new_share": round(new / max(1, tot), 4)}, probs


# ================================================================== the cost projection (spec 5.5)

def config_fill(rows, rels, seed: int = SEED) -> dict:
    """mixer.config_fill with the C2 seed (A37 i): epochs = 16 / measured rows per step (a CPU dry run of
    train_decoder.batches() on the final rows, seeded as the run), the expect_* values."""
    sys.path.insert(0, str(LEAN))
    import train_decoder as td
    clean = [{k: v for k, v in r.items() if k != "_block"} for r in rows]
    if len(clean) < 2 * BATCH:
        raise ValueError(f"config_fill: {len(clean)} rows; batches() never yields a step below {BATCH} rows")
    units, merged = td.make_units(clean, rels)
    st = random.getstate()
    try:
        random.seed(seed)
        gen = td._BATCHES(list(units), BATCH)
        n_steps = math.ceil(len(clean) / BATCH)
        drawn = sum(len(next(gen)) for _ in range(n_steps))
    finally:
        random.setstate(st)
    per_step = drawn / max(1, n_steps)
    kd_rows = [r for r in clean if td.kd_target(r) is not None and (r.get("meta") or {}).get("teacher_src")
               not in mx.KD_SKIP_SRC]
    return {"epochs": round(BATCH / per_step, 4), "measured_rows_per_step": round(per_step, 4),
            "dry_run_steps": n_steps, "units": len(units), "inv_merged": merged,
            "expect_ord_rows": sum(1 for r in clean if td.is_ordinal(r)), "expect_kd_targets": len(kd_rows),
            "expect_kd_full": sum(1 for r in kd_rows if r["source"] in mx.KD_FULL_SRC and r["qtype"] == "noul"),
            "seed": seed}


def project_cost(rows, rels, ntok: dict, seed: int = SEED) -> dict:
    """Spec 5.5: the run's steps from the config fill (n_steps = ceil(rows / 16 x epochs), as train()); per step the
    trainer's own draws (global random seeded as the run, perms, twins from random.Random(seed + 1)) and micro-batches;
    padded tokens = sequences x the micro-batch's longest real token count rounded up to PAD_MULTIPLE (rows and
    their perm twins; a twin has its row's length). Time = 0.163 ms per padded token (A28); $4.09/h; + $2 overhead."""
    sys.path.insert(0, str(LEAN))
    import decoder_io as dio
    import train_decoder as td
    fill = config_fill(rows, rels, seed)
    clean = [{k: v for k, v in r.items() if k != "_block"} for r in rows]
    n_steps = math.ceil(len(clean) / BATCH * fill["epochs"])
    units, _ = td.make_units(clean, rels)
    uid = {r["id"]: k for k, u in enumerate(units) for r in u}
    pad = max(1, dio.PAD_MULTIPLE)

    def padded(n):
        return -(-min(int(n), dio.MAX_LEN) // pad) * pad
    st = random.getstate()
    padded_total = real_total = micro = twins = 0
    try:
        random.seed(seed)
        twin_rng = random.Random(seed + 1)
        gen = td._BATCHES(list(units), BATCH)
        for _ in range(n_steps):
            b = next(gen)
            perms = [random.sample(range(len(r["options"])), len(r["options"])) if r["qtype"] == "choice"
                     else random.sample([0, 1], 2) for r in b]
            tw = td.pick_twins(b, perms, PERM_TWIN, twin_rng)
            twins += len(tw)
            for g in td._micro_groups(b, uid, tw, MICRO_TOKENS):
                gs = set(g)
                lens = [ntok[b[i]["id"]] for i in g] + [ntok[b[i]["id"]] for i, _ in tw if i in gs]
                padded_total += len(lens) * padded(max(lens))
                real_total += sum(lens)
                micro += 1
    finally:
        random.setstate(st)
    sec = padded_total * MS_PER_PADDED / 1000
    train_usd = sec / 3600 * USD_H
    return {"rows": len(clean), "steps": n_steps, "epochs": fill["epochs"],
            "rows_per_step": fill["measured_rows_per_step"],
            "padded_tokens_per_step": round(padded_total / max(1, n_steps), 1),
            "real_tokens_per_step": round(real_total / max(1, n_steps), 1),
            "micro_batches_per_step": round(micro / max(1, n_steps), 2), "twins_per_step": round(twins / max(1, n_steps), 2),
            "s_per_step": round(sec / max(1, n_steps), 3), "hours": round(sec / 3600, 3), "train_usd": round(train_usd, 2),
            "overhead_usd": OVERHEAD_USD, "total_usd": round(train_usd + OVERHEAD_USD, 2),
            "model": f"{MS_PER_PADDED} ms per padded token (A28), ${USD_H}/h, + ${OVERHEAD_USD} smoke and overhead "
                     f"(spec 9.2); pad {pad}, micro_tokens {MICRO_TOKENS}, perm_twin {PERM_TWIN}, seed {seed}"}


def t_max_usd(spend_to_date) -> float:
    """A42-D 2.3: T_max = min($34, $32 - C2 Modal spend to date), fixed at the training GO ($32 = $40 - $4 evaluation -
    $2 SPEED-3 - $2 reserve). The spend is the owner-confirmed C2 Modal total on every account (A42-D 2.1)."""
    try:
        sp = float(spend_to_date)
    except (TypeError, ValueError):
        raise SystemExit("--spend-to-date must be a number (USD of C2 Modal spend to date, A42-D 2.3)") from None
    if not math.isfinite(sp) or sp < 0:
        raise SystemExit(f"--spend-to-date {spend_to_date!r} is not a finite non-negative USD amount")
    t = min(T_MAX_CAP, T_MAX_BASE - sp)
    if t <= OVERHEAD_USD:
        raise SystemExit(f"T_max = ${t:.2f} leaves no training budget after the ${OVERHEAD_USD} smoke (spend to date "
                         f"${sp}): stop and ask the owner (A42-D 2.3)")
    return round(t, 4)


def budget_factor(proj: dict, rnd: int = 0, t_max: float = T_MAX_CAP, rows: int = 0) -> float:
    """The share of rows kept so the projected total meets T_max (training cost ~ rows at a fixed composition) and the
    mix is within 125,000 rows (rows > 0); a small extra margin per repeated round."""
    room = t_max - OVERHEAD_USD
    f = min(1.0, room / max(1e-9, proj["total_usd"] - OVERHEAD_USD))
    if rows > ROWS_MAX:
        f = min(f, ROWS_MAX / rows)
    return f * BUDGET_MARGIN ** rnd


# ================================================================== round-1 functions with C2 paths / seed (copies)

def load_replay(ilog, rep: dict, P: dict | None = None):
    """mixer.load_replay with the C2 replay draw: kept rows of its second pass (C1 read + the A16 p_g rule), whole
    relation units. Returns rows, light rows, units, kept unit indices, relations, flags, C1 probs."""
    P = REPLAY if P is None else P
    rs = mx.rs_mod()
    sys.path.insert(0, str(LEAN))
    import shard_golden as sg
    pa = ilog.json(P["pg_anchor"])
    if pa.get("pg_rule", {}).get("amendment") != "A16":
        raise SystemExit(f"{Path(P['pg_anchor']).name}: unexpected p_g rule {pa.get('pg_rule')}")
    rows = [r for p in sg.shard_files(P["shards"]) for r in ilog.jsonl(p)]
    for p in sorted(Path(P["labels"]).glob("shard_*")):
        ilog.record(p)
    probs, view = sg.load_labels(P["labels"], P["shards"], return_view=True)
    if (view or {}).get("settings", {}).get("name") != C1 or view["settings"] != pa["read"]:
        raise SystemExit("C2 replay labels are not the C1 read recorded by its second pass")
    flags = pa["flags"]
    miss = [r["id"] for r in rows if r["id"] not in flags or r["id"] not in probs]
    if miss:
        raise SystemExit(f"{len(miss)} replay rows without second-pass flags or C1 labels, e.g. {miss[:3]}")
    ids = {r["id"] for r in rows}
    rels = [x for x in ilog.jsonl(P["golden_rels"]) if x["a"] in ids and x["b"] in ids]
    lt = [mx.light(r, rs) for r in rows]
    units = rs.build_units(lt, rels)
    kept = [u for u, x in enumerate(units) if not any(flags[lt[i]["id"]]["drop_pg"] for i in x["rows"])]
    rep["replay_read"] = {"rows_read": len(rows), "units": len(units), "relations": len(rels),
                          "rows_kept": sum(len(units[u]["rows"]) for u in kept), "second_pass_counts": pa.get("counts")}
    return rows, lt, units, kept, rels, flags, probs


def old_slice_clash(ilog, rows, units, kept, P: dict | None = None):
    """mixer.old_slice_clash on the round-1 old slice (spec 5.4: the same slice, so the snapshot reads compare)."""
    P = REPLAY if P is None else P
    rs = mx.rs_mod()
    sys.path.insert(0, str(LEAN))
    import shard_golden as sg
    od = Path(P["old_slice"])
    old = [r for p in sg.shard_files(od) for r in ilog.jsonl(p)] if od.exists() else []
    groups, states = {r["group_id"] for r in old}, {rs.norm_state(r.get("state")) for r in old}
    bad = {u for u in kept if any(rows[i]["group_id"] in groups or rs.norm_state(rows[i].get("state")) in states
                                  for i in units[u]["rows"])}
    return [u for u in kept if u not in bad], {"old_slice_rows": len(old), "clash_units_removed": len(bad)}


def trim_replay(ilog, lt, units, kept, rep, total: int, P: dict | None = None):
    """mixer.trim_replay with the C2 draw's quotas, always scaled to `total` (A34 c: the per-source quota
    proportions kept): each source's prefix of the sampler's seeded stratified unit order; deficits pass to sources
    with margin; exact total by the last single-row units."""
    P = REPLAY if P is None else P
    rs = mx.rs_mod()
    q1 = {s: v["q1"] for s, v in ilog.json(P["write"])["quota_by_source"].items()}
    q1 = mx.largest_remainder(q1, total)
    by_src = defaultdict(list)
    for u in kept:
        by_src[units[u]["source"]].append(u)
    order = {s: rs.unit_order(lt, units, uis) for s, uis in by_src.items()}
    size = lambda us: sum(len(units[u]["rows"]) for u in us)  # noqa: E731
    take = {s: rs.prefix(order[s], units, q1.get(s, 0)) for s in order}
    deficit, rounds = total - sum(size(t) for t in take.values()), 0
    while deficit > 0 and rounds < 50:
        donors = {s: q1.get(s, 0) or 1 for s in order if len(take[s]) < len(order[s])}
        if not donors:
            break
        for s, k in mx.largest_remainder(donors, deficit).items():
            if k > 0:
                take[s] = rs.prefix(order[s], units, size(take[s]) + k)
        deficit = total - sum(size(t) for t in take.values())
        rounds += 1
    take = mx.exact_total(take, q1, units, total)
    sel = [u for s in sorted(take) for u in take[s]]
    chosen = set(sel)
    pool = [u for s in sorted(order) for u in order[s] if u not in chosen]
    rep["replay_trim"] = {"total": total, "rows": size(sel), "units": len(sel), "sources": len(take),
                          "margin_units_left": len(pool), "deficit_rounds": rounds}
    return sel, pool


def replay_denylist_check(ilog, rows, rep, P: dict | None = None):
    P = REPLAY if P is None else P
    ver = ilog.json(P["verdicts"])["verdicts"]
    srcs = Counter(r["source"] for r in rows)
    v = {s: (ver.get(s) or {}).get("verdict") for s in srcs}
    bad = sorted(s for s, x in v.items() if x is None or x == "drop")
    rep["denylist_replay"] = {"sources": len(srcs), "verdicts": dict(Counter(v.values())), "refused": bad}
    return bad


def run_denylist(ilog, query: dict, rep, final=False) -> set:
    """mixer.run_denylist with C2 paths: denylist.py check in its own process; returns the denied query keys."""
    WORK.mkdir(parents=True, exist_ok=True)
    qp, vp = WORK / "denylist_query_mix_c2.json", WORK / "denylist_verdicts_mix_c2.json"
    vp.unlink(missing_ok=True)
    undeclared = sorted(k for k, v in query.items() if "parents" not in v)
    if not final:
        query = {k: v for k, v in query.items() if "parents" in v}
    c2io.write_json(qp, {"purpose": "C2 mixer (C2_DATA_SPEC 6.1; C spec 3.H.2): every new-row source and real-text "
                                    "source", "datasets": query})
    ilog.record(DENYLIST)
    p = subprocess.run([str(mx.PY), str(LEAN / "c_src/common/denylist.py"), "check", "--query", str(qp), "--out",
                        str(vp), "--run", "mixer_c2", "--denylist", str(DENYLIST)], capture_output=True, text=True,
                       cwd=str(LEAN), timeout=600)
    if p.returncode not in (0, 3) or not vp.exists():
        raise SystemExit(f"denylist.py check failed (exit {p.returncode}): {p.stderr[-400:]}")
    ver = ilog.json(vp)["verdicts"]
    denied = {k for k, v in ver.items() if v.get("verdict") in ("deny", "no_new_rows")}
    rep["denylist_new"] = {"checked": len(ver), "denied": sorted(denied),
                           "verdicts": dict(Counter(v.get("verdict") for v in ver.values())),
                           "not_checked_parents_undeclared": undeclared}
    return denied


def part_key(block: str, unit_rows) -> str:
    """The selection key a unit of `block` was selected under (c2_select): the family key; F11: '|pref' for an
    all-XED / MAMS unit, else '|rest'."""
    k = c2_select.sel_key(block)
    if block in c2_select.CARRY_PREFER:
        return k + ("|pref" if all(c2_select.preferred(block, r) for r in unit_rows) else "|rest")
    return k


def own_pool(block, rows, rels, units, chosen, bins, pg, seed: int = SEED) -> mx.Pool:
    """mixer.own_pool with the C2 seed and selection keys: a block's unselected whole units for refills, never an
    all-easy unit the selection's seeded 30% keep thinned out (its own key), never a unit without a crowd bin."""
    uid = {rows[i]["id"]: u for u, x in enumerate(units) for i in x}
    used = {uid[i] for i in chosen if i in uid}
    cands = []
    for u, x in enumerate(units):
        if u in used or (pg and any(rows[i]["id"] not in pg for i in x)):
            continue
        if pg and cs.easy_thinned(rows, [x], bins, part_key(block, [rows[i] for i in x]), seed):
            continue
        cands.append(u)
    cands.sort(key=lambda u: h64(seed, block, "refill", rows[units[u][0]]["id"]))
    ri = mx.rel_index(rels)

    def rows_of(u, tally=None):
        out = []
        for i in units[u]:
            m = dict(rows[i].get("meta") or {})
            if pg:
                m["crowd_pg"], m["difficulty_bin"] = pg[rows[i]["id"]], bins[rows[i]["id"]]
            out.append(rows[i] | {"meta": m, "_block": block})
        return out
    return mx.Pool(block, uid, lambda r: "", {"": cands}, lambda u: [rows[i] for i in units[u]], rows_of,
                   lambda r: mx.own_keys(r, bins.get(r["id"], "na")),
                   lambda ids: [x for a in ids for x in ri.get(a, []) if x["b"] in ids], {r["source"] for r in rows})


def current_parts(block: str, rows, rels, parts: list[dict]) -> list[dict]:
    """The block's rows now, split into its selection parts (c2_select records): ids kept from each part, plus every
    refilled unit under the part its key belongs to."""
    have = {r["id"] for r in rows}
    out = [{"key": p["key"], "ids": [i for i in p["ids"] if i in have]} for p in parts]
    placed = {i for p in out for i in p["ids"]}
    left = [r for r in rows if r["id"] not in placed]
    if left:
        units = cs.units_of(left, [x for x in rels if x["a"] in have and x["b"] in have])
        by_key = {p["key"]: p for p in out}
        for x in units:
            ur = [left[i] for i in x]
            k = part_key(block, ur)
            if k not in by_key:
                by_key[k] = {"key": k, "ids": []}
                out.append(by_key[k])
            by_key[k]["ids"] += [r["id"] for r in ur]
    return out


def apply_targets(rows, rels, targets: dict, parts: dict, seed: int = SEED) -> tuple[list, list, dict]:
    """Re-select every new block holding more rows than its target (agent-tier cap, budget trim): c2_select.reselect
    on its rows with its parts' keys and the C2 seed. Whole units; balance rules as in the selection."""
    by = defaultdict(list)
    for r in rows:
        by[r["_block"]].append(r)
    drop, info = set(), {}
    for b, t in targets.items():
        rr = by.get(b, [])
        if len(rr) <= t:
            continue
        ids = {r["id"] for r in rr}
        if b == META_BLOCK:                          # whole tasks, source shares kept (A42-D 2.3 step 4 / 8.2)
            rows, rels = reduce_meta(rows, rels, t, seed)
            rows, rels, fi = fit_block(b, rows, rels, seed)
            info[b] = {"rows_before": len(rr), "target": t, "rows_after": sum(1 for r in rows if r["_block"] == b),
                       "fit": fi}
            by[b] = [r for r in rows if r["_block"] == b]
            continue
        brel = [x for x in rels if x["a"] in ids and x["b"] in ids]
        pg = {r["id"]: float((r.get("meta") or {}).get("crowd_pg") if (r.get("meta") or {}).get("crowd_pg") is not None else 0.5) for r in rr}
        res = c2_select.reselect(rr, brel, pg, current_parts(b, rr, brel, parts.get(b) or
                                                             [{"key": c2_select.sel_key(b), "ids": list(ids)}]), t, seed)
        keep = set(res["selected_ids"])
        drop |= ids - keep
        parts[b] = res["parts"]
        info[b] = {"rows_before": len(rr), "target": t, "rows_after": len(keep),
                   "checks_pass": all(x.get("pass") for x in res["reports"] if x.get("target"))}
    rows, rels = mx.drop_rows(rows, rels, drop)
    for b in GENERAL_BLOCKS:                         # reselection keeps the balance rules; the block caps are re-fitted
        if b in targets and any(r["_block"] == b for r in rows):
            rows, rels, fi = fit_block(b, rows, rels, seed)
            info.setdefault(b, {})["fit"] = fi
    return rows, rels, info


def dev_items(ilog, blocks, dev_sets: dict | None = None) -> tuple[dict, list[str]]:
    """{block: [(dev row, pack_check)]} for mixer.HeldOut: the frozen C2 mixdev (each row under its meta.family, held-out
    packs checked against that block), transfer dev and T37b-dev, and each carry-over pool's round-1 dev parts."""
    out, miss = defaultdict(list), []
    for name, p in (DEV_SETS if dev_sets is None else dev_sets).items():
        if not Path(p).exists():
            miss.append(f"frozen dev set {name} missing ({Path(p).name}; spec 7.1: built before training)")
            continue
        for r in ilog.jsonl(p):
            fam = (r.get("meta") or {}).get("family") or name
            out[fam if name == "c2_mixdev" else name].append((r, name == "c2_mixdev"))
    for b in blocks:
        if b in BLOCK_TARGETS:                       # A39 h: a block's own report-only mixdev (GB: 1,650 rows) is never trained
            f = c2io.fam_files(b)["mixdev"]
            if f.exists():
                out[b] += [(r, False) for r in ilog.jsonl(f)]
        if b in CARRY:
            d = cs.fam_dir(b) / "out"
            for n in ("mixdev_S5.jsonl",) + mx.DEV_EXTRA:
                if (d / n).exists():
                    out[b] += [(r, n == "mixdev_S5.jsonl") for r in ilog.jsonl(d / n)]
    return out, miss


def refuse_held_out(ilog, blocks: dict, rep) -> list[str]:
    """formats-1 refuse_held_out on every training block (held-out style ids, sampler S5): strict on the carry-over
    pools (round-1 formats-1 ids), not strict on C2 blocks (their format_style is '<register>/<escape>'; their own
    held-out rule is meta.dev_only, checked in cap_checks)."""
    sys.path.insert(0, str(LEAN / "c_src/formats/formats-1"))
    from fmt1 import pool
    ilog.record(LEAN / "c_src/formats/formats-1/fmt1/pool.py")
    out = {}
    for name, rows in blocks.items():
        strict = name in CARRY
        try:
            out[name] = pool.refuse_held_out(rows, strict_unknown=strict) | {"strict_unknown": strict}
        except pool.HeldOutStyleError as e:
            out[name] = {"refused": str(e).split("; first ids")[0], "strict_unknown": strict}
    rep["fmt1_refuse_held_out"] = out
    return [n for n, v in out.items() if "refused" in v]


# ================================================================== A42-D blocks: groups, caps, trim steps

# A42-D 8.2 (16 Oct ruling): OpenAlex (scholarly_publishing) and ROR (research_organisations) are ONE domain for the 20% cap.
DOMAIN_GROUP = {"scholarly_publishing": "scholarly", "research_organisations": "scholarly"}


def dom_of(r) -> str:
    m = r.get("meta") or {}
    d = str(m.get("domain") or r.get("domain") or m.get("domain_pack") or "na")
    return DOMAIN_GROUP.get(d, d)


def card_of(r):
    return (r.get("meta") or {}).get("card_id") or r.get("card_id")


def task_of(r):
    return (r.get("meta") or {}).get("task_id")


def is_twin(r) -> bool:
    """A negation-twin row of a G-block / metadata block (A42-D 7): meta.twin_of names its base row."""
    return bool((r.get("meta") or {}).get("twin_of"))


def card_free(r) -> bool:
    return not str(r.get("card") or "").strip()


def groups(rows, rels, by_task: bool = False) -> list[list[int]]:
    """Whole units of `rows` (relation units, cs.units_of); by_task: units sharing a meta.task_id are one group (a whole
    task of the metadata block, twins included)."""
    units = cs.units_of(rows, rels)
    if not by_task:
        return units
    parent = list(range(len(units)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    first = {}
    for k, u in enumerate(units):
        for i in u:
            t = task_of(rows[i])
            if t is None:
                continue
            if t in first:
                parent[find(k)] = find(first[t])
            else:
                first[t] = k
    comp = defaultdict(list)
    for k, u in enumerate(units):
        comp[find(k)] += u
    return [sorted(v) for v in comp.values()]


def remove_groups(rows, rels, scope, pred, need: int, tag: str, seed: int = SEED, by_task: bool = False):
    """Seeded whole-group removal (A42-D 2.3): among the rows of the blocks in `scope`, groups holding a `pred` row go in
    the order of h64(seed, tag, first row id) until `need` pred rows are gone (a group may overshoot). Returns rows,
    rels, pred rows removed, rows removed."""
    if need <= 0:
        return rows, rels, 0, 0
    sub = [r for r in rows if r["_block"] in scope]
    ids = {r["id"] for r in sub}
    gs = [g for g in groups(sub, [x for x in rels if x["a"] in ids and x["b"] in ids], by_task)
          if any(pred(sub[i]) for i in g)]
    gs.sort(key=lambda g: h64(seed, tag, sub[g[0]]["id"]))
    gone, got = set(), 0
    for g in gs:
        if got >= need:
            break
        gone |= {sub[i]["id"] for i in g}
        got += sum(1 for i in g if pred(sub[i]))
    rows, rels = mx.drop_rows(rows, rels, gone)
    return rows, rels, got, len(gone)


def recorded_deviations(block: str) -> list:
    """Deviation records of the block's qc/QC_REPORT.json (a list of dicts; [] when the file or the key is missing)."""
    try:
        j = json.loads((C2_PARTS / block / "qc" / "QC_REPORT.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    d = j.get("deviations") if isinstance(j, dict) else None
    return [x for x in d if isinstance(x, dict)] if isinstance(d, list) else []


def task_floor_accepted(source: str, n_tasks: int, deviations) -> bool:
    """A51 (c): a source under the 8.2 task floor after the noise gate keeps its tasks. Accepted only when the block's QC record
    holds a deviation that cites A51 (c), names this source, and whose recorded counts match what is on disk
    (tasks_in - tasks_dropped_by_gate == tasks_kept == n_tasks). Any other shortfall stays a problem."""
    for d in deviations or ():
        try:
            if ("A51 (c)" in str(d.get("ruling")) and d.get("block_source") == source and d.get("tasks_kept") == n_tasks
                    and d["tasks_in"] - d["tasks_dropped_by_gate"] == n_tasks and n_tasks < META_TASKS_PER_SOURCE[0]):
                return True
        except (KeyError, TypeError):
            continue
    return False


def block_rules(block: str, rows, loaded: bool = False, proportional_trim: bool = False, deviations=None) -> tuple[dict, list[str]]:
    """The A42-D rules of the G-block (5.5, 7.1, A39 e) and the metadata block (8.2, 7.1) on its rows, twins included.
    loaded: the block as it came from its selection (also asserts the 40-80 tasks per source design); the 8,000-row
    floor is waived only after spec 5.5's proportional step (A42-D 2.3 step 4) has trimmed it."""
    rep, p = {"rows": len(rows)}, []
    if block not in (G_BLOCK, W2_BLOCK, META_BLOCK):
        return rep, p
    n = len(rows)
    tw = sum(1 for r in rows if is_twin(r))
    rep["twins"] = tw
    if n > BLOCK_CAPS[block]:
        p.append(f"{block}: {n:,} rows > {BLOCK_CAPS[block]:,} incl. twins")
    if block in TWIN_CAP and tw > TWIN_CAP[block]:
        p.append(f"{block}: {tw:,} negation-twin rows > {TWIN_CAP[block]:,} (A42-D 7.1)")
    dc = Counter(dom_of(r) for r in rows)
    rep["domains"] = len(dc)
    rep["max_domain_share"] = round(max(dc.values(), default=0) / max(1, n), 4)
    if max(dc.values(), default=0) > DOMAIN_MAX * n + 1e-9:
        p.append(f"{block}: domain {max(dc, key=dc.get)} holds {rep['max_domain_share']} of the block > {DOMAIN_MAX}")
    if block == W2_BLOCK:                            # A40 (d) per-type cap; no twins, no card band (constructed items)
        pt = max(dc.values(), default=0)
        rep["max_rows_per_type"] = pt
        if pt > GW_TYPE_MAX:
            p.append(f"{block}: a wave-2 type holds {pt:,} rows > {GW_TYPE_MAX:,} (A40 d)")
        return rep, p
    if block == G_BLOCK:
        bad, small = [], 0
        for c, rr in _by(rows, card_of).items():
            yn = [r for r in rr if r["qtype"] == "noul"]
            if c is None or len(yn) < GB_CARD_MIN_ROWS or len(yn) != len(rr):
                small += 1
                continue
            y = sum(1 for r in yn if r["gold"] == 1) / len(yn)
            if not GB_YES_BAND[0] - 1e-9 <= y <= GB_YES_BAND[1] + 1e-9:
                bad.append((c, round(y, 3)))
        rep["yes_share_cards_outside_band"], rep["cards_not_checked"] = len(bad), small
        if bad:
            p.append(f"{block}: {len(bad)} yes/no cards with a yes share outside {GB_YES_BAND} (A42-D 5.5), e.g. {bad[:3]}")
        return rep, p
    sc = Counter(r["source"] for r in rows)
    rep["sources"] = len(sc)
    rep["max_source_share"] = round(max(sc.values(), default=0) / max(1, n), 4)
    if max(sc.values(), default=0) > SOURCE_MAX * n + 1e-9:
        p.append(f"{block}: source {max(sc, key=sc.get)} holds {rep['max_source_share']} of the block > {SOURCE_MAX}")
    if len(dc) < META_DOMAINS_MIN:
        p.append(f"{block}: {len(dc)} domains < {META_DOMAINS_MIN}")
    free = {s: sum(1 for r in rows if r["source"] == s and card_free(r)) / c for s, c in sc.items()}
    rep["card_free_min"] = round(min(free.values(), default=1.0), 4)
    low = {s: round(v, 3) for s, v in free.items() if v < CARD_FREE_MIN - 1e-9}
    if low:
        p.append(f"{block}: card-free share below {CARD_FREE_MIN} for sources {low}")
    tasks = _by(rows, task_of)
    big = {t: len(v) for t, v in tasks.items() if t is not None and len(v) > META_TASK_ROWS_MAX}
    if big:
        p.append(f"{block}: {len(big)} tasks above {META_TASK_ROWS_MAX} rows")
    tps = Counter()
    for t, v in tasks.items():
        if t is not None:
            tps[v[0]["source"]] += 1
    rep["tasks_per_source"] = dict(sorted(tps.items()))
    devs = recorded_deviations(block) if (loaded and deviations is None) else (deviations or [])
    short = {s for s, v in tps.items() if v < META_TASKS_PER_SOURCE[0]}
    ok = {s for s in short if task_floor_accepted(s, tps[s], devs)}
    if ok:
        rep["task_floor_accepted_A51c"] = {s: tps[s] for s in sorted(ok)}
    if any(v > META_TASKS_PER_SOURCE[1] for v in tps.values()) or (loaded and short - ok):
        p.append(f"{block}: tasks per source outside {META_TASKS_PER_SOURCE} {dict(tps)} (A42-D 8.2)")
    if n < META_MIN_ROWS and not proportional_trim:
        p.append(f"{block}: {n:,} rows < {META_MIN_ROWS:,} (A42-D 8.2; waived only after spec 5.5's proportional trim)")
    return rep, p


def _by(rows, key) -> dict:
    out = defaultdict(list)
    for r in rows:
        out[key(r)].append(r)
    return out


def fit_block(block: str, rows, rels, seed: int = SEED):
    """Bring a G-block / metadata / RTW block inside its own caps by seeded whole-unit (metadata: whole-task) removal
    only: twins <= 5,000, size cap, no domain above 20%, (metadata) no source above 15%. Nothing is added or relabelled."""
    info = {"before": len(rows), "steps": []}
    if block not in BLOCK_CAPS:
        return rows, rels, info
    for _ in range(80):
        n = len(rows)
        tw = sum(1 for r in rows if is_twin(r))
        need = pred = None
        if block in TWIN_CAP and tw > TWIN_CAP[block]:
            need, pred, tag = tw - TWIN_CAP[block], is_twin, "twins"
        elif n > BLOCK_CAPS[block]:
            need, pred, tag = n - BLOCK_CAPS[block], (lambda r: True), "size"
        elif block in (G_BLOCK, W2_BLOCK, META_BLOCK):
            for lim, key, tg in ((DOMAIN_MAX, dom_of, "domain"), (SOURCE_MAX if block == META_BLOCK else 9, lambda r: r["source"], "source")):
                c = Counter(key(r) for r in rows)
                if not c:
                    continue
                v, k = max(c.items(), key=lambda x: (x[1], str(x[0])))
                if k > lim * n + 1e-9:
                    need, pred, tag = math.ceil((k - lim * n) / (1 - lim)), (lambda r, v=v, key=key: key(r) == v), f"{tg}:{v}"
                    break
        if need is None:
            break
        rows, rels, got, _ = remove_groups(rows, rels, {block}, pred, need, f"fit|{block}|{tag}", seed,
                                           by_task=block == META_BLOCK)
        info["steps"].append({"rule": tag, "need": need, "removed": got})
        if got == 0:
            info["unfixable"] = tag
            break
    info["after"] = len(rows)
    return rows, rels, info


def reduce_meta(rows, rels, target: int, seed: int = SEED):
    """Spec 5.5 proportional step for the metadata block: whole tasks, quotas per source by largest remainder over the
    rows each source holds (so the source shares are kept), seeded order inside a source."""
    blk = [r for r in rows if r["_block"] == META_BLOCK]
    drop = len(blk) - target
    if drop <= 0:
        return rows, rels
    sc = Counter(r["source"] for r in blk)
    q = mx.largest_remainder(dict(sc), drop)
    for s, k in sorted(q.items()):
        rows, rels, _, _ = remove_groups(rows, rels, {META_BLOCK}, lambda r, s=s: r["source"] == s, k,
                                         f"prop|{META_BLOCK}|{s}", seed, by_task=True)
    return rows, rels


def trim_blocks(rows, rels, blocks, need: int, tag: str, seed: int = SEED):
    """A42-D 2.3 steps 1-2: remove up to `need` rows from the blocks in `blocks` (in proportion to the rows each holds,
    largest remainder), seeded whole units. Returns rows, rels, removed rows, info (left = rows still available)."""
    have = Counter(r["_block"] for r in rows if r["_block"] in blocks)
    avail = sum(have.values())
    take = min(max(0, need), avail)
    out = 0
    if take:
        q = mx.largest_remainder(dict(have), take)
        for b, k in sorted(q.items()):
            rows, rels, got, _ = remove_groups(rows, rels, {b}, lambda r: True, k, f"{tag}|{b}", seed)
            out += got
    return rows, rels, out, {"available_before": avail, "need": need, "removed": out, "left": avail - out}


def trim_meta_tail(rows, rels, need: int, seed: int = SEED):
    """A42-D 2.3 step 3: metadata-block rows above 8,000, as whole tasks in seeded order. A task is skipped when removing it
    would break item 8.2: a source above 15% of the block, a domain above 20%, fewer than 8 domains, a source with less
    than 30% card-free rows or a source emptied, or when the block would fall below 8,000 rows."""
    blk = [r for r in rows if r["_block"] == META_BLOCK]
    n = len(blk)
    room = max(0, n - META_MIN_ROWS)
    take = min(max(0, need), room)
    info = {"available_before": room, "need": need, "removed": 0}
    if take <= 0:
        info["left"] = room
        return rows, rels, 0, info
    ids = {r["id"] for r in blk}
    gs = groups(blk, [x for x in rels if x["a"] in ids and x["b"] in ids], by_task=True)
    gs.sort(key=lambda g: h64(seed, "meta_tail", blk[g[0]]["id"]))
    N = n
    src, dom = Counter(r["source"] for r in blk), Counter(dom_of(r) for r in blk)
    free = Counter(r["source"] for r in blk if card_free(r))
    gone, removed, skipped = set(), 0, 0
    for g in gs:
        if removed >= take:
            break
        rr = [blk[i] for i in g]
        if N - len(rr) < META_MIN_ROWS:
            skipped += 1
            continue
        ds, dd, df = Counter(r["source"] for r in rr), Counter(dom_of(r) for r in rr), Counter(
            r["source"] for r in rr if card_free(r))
        N2 = N - len(rr)
        s2 = {s: src[s] - ds.get(s, 0) for s in src}
        d2 = {d: dom[d] - dd.get(d, 0) for d in dom}

        def holds(v2, v1, lim):                      # the rule holds after, or (a block that starts outside it) it is not worse
            return v2 <= lim * N2 + 1e-9 or v2 * N <= v1 * N2 + 1e-9
        nd1, nd2 = sum(1 for v in dom.values() if v > 0), sum(1 for v in d2.values() if v > 0)
        ok = (all(v > 0 for v in s2.values()) and all(holds(s2[s], src[s], SOURCE_MAX) for s in s2)
              and all(holds(d2[d], dom[d], DOMAIN_MAX) for d in d2) and (nd2 >= META_DOMAINS_MIN or nd2 >= nd1)
              and all((free[s] - df.get(s, 0)) >= CARD_FREE_MIN * s2[s] - 1e-9
                      or (free[s] - df.get(s, 0)) * src[s] >= free[s] * s2[s] - 1e-9 for s in s2))
        if not ok:
            skipped += 1
            continue
        gone |= {r["id"] for r in rr}
        N, removed = N2, removed + len(rr)
        src, dom, free = Counter(s2), Counter({d: v for d, v in d2.items() if v > 0}), free - df
    rows, rels = mx.drop_rows(rows, rels, gone)
    info |= {"removed": removed, "skipped_tasks": skipped, "left": max(0, N - META_MIN_ROWS) if removed >= take else 0}
    return rows, rels, removed, info


# ---- the never-train guard (A42-D 13.1) -----------------------------------------------------------------------------

def train_path_problem(path, blocked_paths=(), blocked_sha=(), sha: str | None = None) -> str | None:
    """Why a path may not be a training input (None = fine): any part holding 'ohs' (data/ohs3*, ohs3_parts/,
    ohs4_sealed/, ohs_ac_sealed/), the G-proxy file, a never-train-manifest file or a file with a manifest sha256."""
    parts = [x.lower() for x in Path(str(path)).parts]
    if any("ohs" in x for x in parts) or any(x.startswith(e) for x in parts for e in TRAIN_EXCLUDE):
        return "OHS path (data/ohs3*, ohs3_parts/, ohs4_sealed/, ohs_ac_sealed/)"
    try:
        rp = str(Path(path).resolve())
    except OSError:
        rp = str(path)
    if rp in {str(Path(b).resolve()) for b in blocked_paths}:
        return "the G-proxy file or a never-train-manifest anchor"
    if sha and sha in set(blocked_sha):
        return "its sha256 is a G-proxy / never-train-manifest file"
    return None


def load_never_train(manifest: Path | None, gproxy: Path | None) -> dict:
    """{paths, sha256, names} to exclude: the G-proxy file (path + sha256) and every path, sha256 and dataset name in
    the never-train manifest (any json: strings under path/paths/file/files/ keys, 64-hex strings, name/names/source(s)/
    dataset(s) keys)."""
    paths, shas, names = set(), set(), set()
    if gproxy and Path(gproxy).is_file():
        paths.add(str(Path(gproxy).resolve()))
        shas.add(sha256_file(Path(gproxy)))
    if manifest and Path(manifest).is_file():
        def walk(x, key=""):
            if isinstance(x, dict):
                for k, v in x.items():
                    walk(v, str(k).lower())
            elif isinstance(x, list):
                for v in x:
                    walk(v, key)
            elif isinstance(x, str):
                if re.fullmatch(r"[0-9a-f]{64}", x):
                    shas.add(x)
                elif key in ("path", "paths", "file", "files"):
                    paths.add(str(Path(x).resolve()) if Path(x).is_absolute() else str((c2io.LEAN / x).resolve()))
                elif key in ("name", "names", "source", "sources", "dataset", "datasets", "anchor", "anchors"):
                    names.add(x.lower())
        walk(json.loads(Path(manifest).read_text(encoding="utf-8")))
    return {"paths": paths, "sha256": shas, "names": names}


def filter_train_globs(items) -> tuple[list, list]:
    """Expand glob patterns (the --decontam-drops lists) and drop every path train_path_problem refuses."""
    import glob
    kept, out = [], []
    for it in items or []:
        for p in (sorted(glob.glob(str(it))) if any(c in str(it) for c in "*?[") else [str(it)]):
            (out if train_path_problem(p) else kept).append(p)
    return kept, out


def anchor_row_problems(rows, names) -> list[str]:
    """Training rows whose source / text-source dataset is a never-train-manifest anchor name."""
    if not names:
        return []
    bad = Counter()
    for r in rows:
        src = str(r.get("source", "")).lower()
        ds = str(((r.get("meta") or {}).get("text_source") or {}).get("dataset", "")).lower()
        for n in names:
            if src == n or src.startswith(n + ":") or src.startswith(n + "_") or ds == n:
                bad[n] += 1
    return [f"never-train anchors among the training rows: {dict(bad)} (A42-D 13.1)"] if bad else []


class MixInputLog(C2InputLog):
    """C2InputLog + the A42-D 13.1 training-input guard (OHS globs, the G-proxy file, never-train-manifest anchors)."""

    def __init__(self, never: dict | None = None):
        super().__init__()
        self.never = never or {"paths": set(), "sha256": set(), "names": set()}

    def check(self, path) -> Path:
        why = train_path_problem(path, self.never["paths"])
        if why:
            raise c2io.C2Refused(f"input refused: {path}: {why}")
        return super().check(path)

    def record(self, path):
        p = super().record(path)
        if p.is_file() and self.never["sha256"]:
            why = train_path_problem(p, (), self.never["sha256"], sha256_file(p))
            if why:
                raise c2io.C2Refused(f"input refused: {path}: {why}")
        return p


# ================================================================== blocks

def units_removed(ex) -> int:
    """G13-removed units recorded by a select file (one part, or the F11 two-part form)."""
    if not isinstance(ex, dict):
        return 0
    if "units_removed" in ex:
        return int(ex.get("units_removed") or 0)
    return sum(units_removed(v) for v in ex.values() if isinstance(v, dict))


def selection_problem(s: dict | None, cand_sha: str, target: int, at_most: bool = False) -> str | None:
    """A crowd selection record that may not be mixed (None = fine): another candidates file, another target, or a
    failed check. Short of its target passes when that is the only failed check AND either G13 removed units (the A34
    e rule) or the block's spec size is an upper bound (at_most: F6 / F11 / F4 '<='); it then enters with its rows."""
    if s is None:
        return "no C2 crowd selection file (G9 not run)"
    if s.get("candidates_sha256") != cand_sha:
        return "the crowd selection was made on another candidates file (re-run the crowd)"
    if s.get("target") != target:
        return f"crowd selection target {s.get('target')} != spec target {target}"
    rep = s.get("report") or {}
    bad = [k for k, v in (rep.get("checks") or {}).items() if v is not True]
    short = len(s.get("selected_ids") or []) < target
    if bad == ["total_eq_target"] and short and (at_most or units_removed(s.get("exclude_ids")) > 0):
        return None
    if rep.get("pass") is not True or bad:
        return f"crowd selection fails its checks (G9 / spec 2.1): {bad or ['pass is not true']}"
    return None


def load_block(ilog, b: str, final: bool, rep: dict, probs: list):
    """One block's selected rows + relations + parents + refill pool + selection parts. A selection that fails
    (selection_problem) cuts the block in --final (SystemExit, caught by build: the block is left out, spec 5.3);
    --dry-run then uses a provisional selection (no crowd; counts only) and lists the problem."""
    rows, rels, shas = c2_select.family_inputs(ilog, b)
    units = cs.units_of(rows, rels)
    target = TARGETS[b]
    sf = c2_select.OUT / f"select_{b}.json"
    s = ilog.json(sf) if sf.exists() else None
    info = {"candidates": len(rows), "target": target, "relations_loaded": len(rels)}
    why = selection_problem(s, shas["candidates_sha256"], target,
                            at_most=b in c2io.CARRY_CONDITIONAL or b in BLOCK_TARGETS)
    if why and final:
        raise SystemExit(f"{b}: {why}")
    if s is None or why:
        res = cs.select(rows, units, None, target, key=c2_select.sel_key(b), seed=SEED)
        chosen = {rows[i]["id"] for u in res["sel"] for i in units[u]}
        pg, bins, parts = {}, {r["id"]: "na" for r in rows}, [{"key": c2_select.sel_key(b), "ids": sorted(chosen)}]
        info |= {"selection": f"provisional ({why})", "report": res["report"]}
        probs.append(f"{b}: {why}")
    else:
        chosen, pg, bins = set(s["selected_ids"]), s["crowd_pg"], s["difficulty_bin"]
        parts = s.get("parts") or [{"key": c2_select.sel_key(b), "ids": list(chosen)}]
        info |= {"selection": "crowd (C1 only)", "report": s["report"]}
    out = []
    for r in rows:
        if r["id"] in chosen:
            m = dict(r.get("meta") or {})
            if pg:
                m["crowd_pg"], m["difficulty_bin"] = pg[r["id"]], bins[r["id"]]
            out.append(r | {"meta": m, "_block": b})
    keep_rels = [x for x in rels if x["a"] in chosen and x["b"] in chosen]
    if b in BLOCK_CAPS:                              # A42-D 5.5 / 7.1 / 8.2: the block's own caps, whole units / tasks only
        out, keep_rels, info["fit"] = fit_block(b, out, keep_rels)
        if b in (G_BLOCK, W2_BLOCK, META_BLOCK):
            info["block_rules"], bp = block_rules(b, out, loaded=True)
            probs += bp
    f = c2io.fam_files(b)
    man = ilog.json(f["manifest"]) if f["manifest"].exists() else {}
    parents = mx.manifest_parents(man)
    info |= {"rows": len(out), "relations": len(keep_rels), "parents_declared": parents is not None}
    if parents is None:
        probs.append(f"{b}: MANIFEST declares no parents (G1; the deny-list check cannot run on it)")
    rep.setdefault("blocks", {})[b] = info
    return out, keep_rels, parents, own_pool(b, rows, rels, units, chosen, bins, pg), parts


def admit_blocks(ilog, leave_out, rep) -> list[str]:
    """Spec 5.3: the blocks with candidates on disk that pass admission(); the rest are left out (reported)."""
    for b in leave_out or []:
        if b not in TARGETS:
            raise SystemExit(f"--leave-out: {b} is not a C2 block")
        if b in NEVER_CUT:
            raise SystemExit(f"--leave-out: {b} is never cut (spec 10.2: never cut T28, T33, T29 or T37b)")
    entered, left = [], {}
    for b in TARGETS:
        if b in (leave_out or []):
            left[b] = ["left out on purpose (--leave-out; spec 10.2 cut order)"]
            continue
        f = c2io.fam_files(b)
        if not f["cand"].exists():
            left[b] = ["no candidates on disk"]
            continue
        qc = ilog.json(f["qc"]) if f["qc"].exists() else None
        pg_file = f["qc"].parent / "PILOT_GATE.json"
        pilot = ilog.json(pg_file) if b in NEW_FAMILIES and pg_file.exists() else None
        files = {f["cand"].name: f["cand"]} | ({f["rel"].name: f["rel"]} if f["rel"] and f["rel"].exists() else {})
        binding = mx.qc_binding(qc, files) if isinstance(qc, dict) else []
        why = admission(b, qc, binding, pilot=pilot)
        if why:
            left[b] = why
        else:
            entered.append(b)
    rep["entry"] = {"entered": entered, "left_out": left, "cutoff_utc": CUTOFF_UTC, "fix_max": FIX_MAX,
                    "new_family_deadline_utc": NEW_FAMILY_DEADLINE_UTC,
                    "waves": {b: c2io.wave(b) for b in entered},
                    "rule": "spec 5.3: a block enters only if it passed every gate by the cutoff; missing shares lower "
                            "the total and are never refilled (A34 c)"}
    return entered


# ================================================================== build

def build(a) -> dict:
    t0 = time.time()
    c2io.require_a38()
    tmax = t_max_usd(getattr(a, "spend_to_date", None))
    never = load_never_train(getattr(a, "never_train_manifest", None), getattr(a, "gproxy_file", None))
    ilog = MixInputLog(never)
    rep, probs = {"mode": "final" if a.final else "dry-run", "seed": SEED, "targets": TARGETS,
                  "spend_to_date_usd": float(a.spend_to_date), "t_max_usd": tmax, "rows_max": ROWS_MAX,
                  "never_train": {"paths": len(never["paths"]), "sha256": len(never["sha256"]),
                                  "names": len(never["names"]),
                                  "excluded_globs": list(getattr(a, "excluded_globs", []) or [])}}, []
    if a.final:
        for what, v in (("--never-train-manifest", getattr(a, "never_train_manifest", None)),
                        ("--gproxy-file", getattr(a, "gproxy_file", None))):
            if not v or not Path(v).is_file():
                raise SystemExit(f"--final needs {what} (A42-D 13.1: the G-proxy file and every public anchor are excluded)")
        why = ohs4_problem(a.ohs4_sha, c2io.PREREG.read_text(encoding="utf-8"))
        if why:
            raise SystemExit(f"--final: OHS-4 sha refused ({why})")
    entered = admit_blocks(ilog, a.leave_out, rep)
    blocks, parents, pools, parts = {}, {}, {}, {}
    for b in entered:
        try:
            br, brel, par, bpool, bparts = load_block(ilog, b, a.final, rep, probs)
        except SystemExit as e:             # a refused relation file or a failed selection: the block is cut
            rep["entry"]["left_out"][b] = [f"{b}: {e}"]
            if not a.final:
                probs.append(f"{b} left out: {e}")
            continue
        blocks[b] = (br, brel)
        pools[b], parts[b] = bpool, bparts
        if par is not None:
            for s in {r["source"] for r in br} | bpool.sources:
                parents[s] = par
    rep["entry"]["entered"] = sorted(blocks)
    ok, rep["minimum_to_train"] = minimum_to_train(blocks)
    if not ok:
        msg = (f"minimum to train not met (spec 5.3): agent core {rep['minimum_to_train']['agent_core_n']}/6, program "
               f"families {rep['minimum_to_train']['program_n']}: stop and report to the owner; no training")
        if a.final:
            raise SystemExit(msg)
        probs.append(msg)
    if not blocks:
        rep |= {"problems": probs, "shares": {"new": 0, "replay": [0, 0], "total": 0}, "inputs": ilog.entries}
        return dry_report(rep)
    # plan: spec targets, the agent-tier cap, replay = floor(1.5 x new)
    plan = plan_shares({b: len(v[0]) for b, v in blocks.items()})
    rep["plan"] = rep["plan_final"] = plan
    rows = [r for v in blocks.values() for r in v[0]]
    rels = [x for v in blocks.values() for x in v[1]]
    rows, rels, rep["agent_cap_reselect"] = apply_targets(rows, rels, plan["targets"], parts)
    # replay
    rs = mx.rs_mod()
    rows_r, lt, units, kept, rels_r, flags, c1p = load_replay(ilog, rep)
    kept, rep["old_slice"] = old_slice_clash(ilog, rows_r, units, kept)
    sel, pool = trim_replay(ilog, lt, units, kept, rep, plan["replay_sampler"])
    sel, pool, sticky = mx.e2_restratify(lt, units, sel, pool, rep)
    rpool = mx.replay_pool(rows_r, lt, units, pool, rels_r, flags, c1p)
    cnt = Counter()
    pos = {lt[i]["id"]: i for u in sel for i in units[u]["rows"]}
    replay = sorted((r for u in sel for r in rpool.rows_of(u, cnt)), key=lambda r: pos[r["id"]])
    rpool.tried |= set(sel)
    rid = {r["id"] for r in replay}
    rels += [x for x in rels_r if x["a"] in rid and x["b"] in rid]
    rep["replay_targets"] = {k: v for k, v in cnt.items() if not k.startswith("option_level:")}
    ctx = {"lt": lt, "units": units, "sticky": sticky}
    rows = list(replay) + rows
    pools["replay"] = rpool
    dup = [k for k, v in Counter(r["id"] for r in rows).items() if v > 1]
    if dup:
        probs.append(f"{len(dup)} duplicate row ids across blocks, e.g. {dup[:3]}")
    log(f"assembled {len(rows):,} rows ({time.time() - t0:.0f}s)")
    return finish(a, ilog, rep, probs, rows, rels, parents, pools, parts, ctx, plan, t0, rs)


def finish(a, ilog, rep, probs, rows, rels, parents, pools, parts, ctx, plan, t0, rs) -> dict:
    """Drops (G13 incl. pool_drops_r1 and the deny-list: whole units; G18 and tokens), refills from each block's pool,
    replay to floor(1.5 x new), the budget trim, then the gates."""
    ho_dev, miss = dev_items(ilog, [b for b in plan["targets"]])
    probs += miss
    ho = mx.HeldOut(ho_dev, rs)
    drops = list(a.decontam_drops or [])
    if POOL_DROPS_R1 not in [Path(p) for p in drops]:
        drops.append(POOL_DROPS_R1)
    dids, rep["g13_decontam_inputs"] = mx.decontam_drop_ids(ilog, drops)
    pool_rows = [r for p in pools.values() if p.block != "replay" for c in p.cands.values() for u in c
                 for r in p.raw_of(u)]
    denied = run_denylist(ilog, mx.denylist_query([r for r in rows if is_new(r)] + pool_rows, parents), rep, a.final)

    def bad_row(r) -> bool:
        if r["id"] in dids:
            return True
        if not is_new(r):
            return False
        ts = (r.get("meta") or {}).get("text_source") or {}
        return r["source"] in denied or "text:" + str(ts.get("dataset")) in denied
    ever = {r["id"]: (r["_block"], r) for r in rows}
    rows, rels, rep["g13_rows_dropped"] = mx.drop_units(rows, rels, dids)
    rows, rels, n = mx.drop_units(rows, rels, {r["id"] for r in rows if bad_row(r)})
    rep["denylist_rows_dropped"] = n
    rb = replay_denylist_check(ilog, [r for r in rows if not is_new(r)], rep)
    if rb:
        probs.append(f"replay sources without a keep verdict: {rb}")
    g18, gone, out = {}, set(), []
    for b in sorted({r["_block"] for r in rows}):
        kept, d = mx.g18_lint([r for r in rows if r["_block"] == b], b, g18)
        out += kept
        gone |= d
    order = {r["id"]: i for i, r in enumerate(rows)}
    rows, rels = mx.drop_rows(sorted(out, key=lambda r: order[r["id"]]), rels, gone)
    log(f"tokenizing {len(rows):,} rendered prompts ({time.time() - t0:.0f}s)")
    ntok = dict(zip((r["id"] for r in rows), mx.token_counts(ilog, rows)))
    long_new = {r["id"] for r in rows if is_new(r) and ntok[r["id"]] > TOK_MAX}
    rows, rels, n_long = mx.drop_units(rows, rels, long_new)
    over = {r["id"] for r in rows if ntok[r["id"]] > ROW_TOK_HARD}
    rows, rels = mx.drop_rows(rows, rels, over)
    rep["drops_before_refill"] = {"g13": rep["g13_rows_dropped"], "denylist": n, "g18": len(gone),
                                  "new_units_over_2000_tokens": n_long, "rows_over_7900": len(over)}

    def accept(pool, u, tally):
        rr = pool.rows_of(u, tally)
        if any(r["id"] in ever or bad_row(r) or ho.clash(r) for r in rr):
            return None
        rr, d = mx.g18_lint(rr, pool.block, {})
        if d:
            return None
        tk = mx.token_counts(ilog, rr)
        if any(t > (TOK_MAX if pool.block != "replay" else ROW_TOK_HARD) for t in tk):
            return None
        ntok.update(zip((r["id"] for r in rr), tk))
        return rr
    handled, rep["refill"] = set(), {}
    for rnd in range(REFILL_ROUNDS):
        add, arels = mx.refill(pools, rows, ever, handled, accept, rep["refill"])
        if not add:
            break
        rows += add
        rels += arels
        ever.update({r["id"]: (r["_block"], r) for r in add})
    # the caps again on what the drops left (a block its pool could not refill lowers the total; the agent tier is
    # re-selected down when that pushes it above 55% of new rows)
    plan2 = plan_shares(dict(Counter(r["_block"] for r in rows if r["_block"] != "replay")))
    if plan2["agent_cap"]["applied"]:
        rows, rels, rep["agent_cap_after_refills"] = apply_targets(rows, rels, plan2["targets"], parts)
    rep["plan_final"] = plan2
    rows, rels = replay_to_rule(rows, rels, pools, ctx, rep, "after_refills")
    rows, rels = budget_trim(a, rows, rels, ntok, pools, parts, ctx, rep, probs)
    probs += mx.e2_final(ctx, rows, rep)
    rep["g18"] = {"rows_checked": sum(c[0] for v in g18.values() for c in v.values()),
                  "fell_back": sum(c[1] for v in g18.values() for c in v.values()), "dropped": len(gone),
                  "pass_after_fix": all(mx.g18_ok(r) for r in rows
                                        if isinstance((r.get("meta") or {}).get("option_level"), dict))}
    if not rep["g18"]["pass_after_fix"]:
        probs.append("G18 ordinal target lint is not 100% on the final targets")
    return gates(a, ilog, rep, probs, rows, rels, ntok, ho, plan, t0)


def replay_to_rule(rows, rels, pools, ctx, rep, tag) -> tuple[list, list]:
    """Replay side = floor(1.5 x realised new rows) (spec 5.3; the replay twins RTW count inside it, A42-D 7.2): the
    sampler's replay is cut by mixer.shrink_replay (whole units, E2 order); a replay below it is reported by
    share_checks."""
    by = Counter(r["_block"] for r in rows)
    new = sum(n for b, n in by.items() if b not in REPLAY_SIDE)
    want = max(0, math.floor(REPLAY_X * new) - by.get(REPLAY_TWINS, 0))
    cut = by.get("replay", 0) - want
    info = rep.setdefault("replay_rule", {})
    info[tag] = {"new": new, "replay_twins": by.get(REPLAY_TWINS, 0), "replay_before": by.get("replay", 0),
                 "cut": max(0, cut)}
    if cut > 0:
        x = {}
        rows, rels = mx.shrink_replay(rows, rels, pools, ctx, cut, x)
        info[tag] |= x
    return rows, rels


def budget_trim(a, rows, rels, ntok, pools, parts, ctx, rep, probs) -> tuple[list, list]:
    """A42-D 2.3 (replaces spec 5.5's $17 rule). Project from real padded tokens; while the projection is above T_max =
    min($34, $32 - spend to date) or the mix is above 125,000 rows, remove rows in FINAL_PLAN's order, each step used up
    before the next: (1) item 10 rows, (2) wave 2 (T44, T45 in proportion), (3) metadata rows above 8,000 as whole tasks,
    (4) spec 5.5's proportional trim of every new block. Seeded (20261013) whole units; the replay follows floor(1.5 x
    new) after every step. Below 50,000 rows it stops and asks the owner."""
    tmax = t_max_usd(getattr(a, "spend_to_date", None))
    rounds, exhausted, used4 = [], set(), False
    for rnd in range(BUDGET_ROUNDS + 1):
        proj = project_cost(rows, rels, ntok)
        proj["t_max_usd"] = tmax
        rounds.append(proj)
        if (proj["total_usd"] <= tmax + 1e-9 and len(rows) <= ROWS_MAX) or rnd == BUDGET_ROUNDS:
            break
        f = budget_factor(proj, rnd, tmax, len(rows))
        n_now = len(rows)
        remove_total = n_now - math.floor(f * n_now)
        if n_now - remove_total < FLOOR_ROWS:
            msg = (f"budget trim (A42-D 2.3): T_max ${tmax} / {ROWS_MAX:,} rows needs {n_now - remove_total:,} rows, below "
                   f"the {FLOOR_ROWS:,} floor: stop and ask the owner (projection ${proj['total_usd']}, {n_now:,} rows)")
            rep["budget"] = {"rounds": rounds, "stopped": msg, "final_total_usd": proj["total_usd"], "trimmed": False,
                             "t_max_usd": tmax}
            if a.final:
                raise SystemExit(msg)
            probs.append(msg)
            return rows, rels
        left = math.ceil(remove_total / (1 + REPLAY_X))               # new rows to remove (each takes 1.5 replay rows)
        done = []
        for step in TRIM_ORDER:
            if left <= 0:
                break
            if step in exhausted:
                continue
            if step == "proportional":
                by = Counter(r["_block"] for r in rows if r["_block"] != "replay")
                new_now = sum(n for b, n in by.items() if b not in REPLAY_SIDE)
                plan = scale_plan(dict(by), max(0.0, (new_now - left) / max(1, new_now)))
                rows, rels, info = apply_targets(rows, rels, plan["targets"], parts)
                rows, rels = replay_to_rule(rows, rels, pools, ctx, rep, f"budget_round_{rnd + 1}_prop")
                done.append({"step": step, "plan": plan, "reselect": info})
                rep["plan_final"], used4, left = plan, True, 0
                break
            if step == "item10":
                rows, rels, got, info = trim_blocks(rows, rels, set(ITEM10_BLOCKS), left, "item10", SEED)
            elif step == "wave2":
                rows, rels, got, info = trim_blocks(rows, rels, set(WAVE2_NEW), left, "wave2", SEED)
            else:
                rows, rels, got, info = trim_meta_tail(rows, rels, left, SEED)
            if info["left"] <= 0 or got < min(left, info["available_before"]):
                exhausted.add(step)
            done.append({"step": step} | info)
            left -= got
            rows, rels = replay_to_rule(rows, rels, pools, ctx, rep, f"budget_round_{rnd + 1}_{step}")
        rounds[-1]["trim"] = {"factor": round(f, 4), "remove_total_rows": remove_total, "steps": done}
    final = rounds[-1]
    rep["budget"] = {"rounds": rounds, "final_total_usd": final["total_usd"], "trimmed": len(rounds) > 1,
                     "t_max_usd": tmax, "spend_to_date_usd": float(a.spend_to_date), "rows_max": ROWS_MAX,
                     "order": list(TRIM_ORDER), "exhausted_steps": sorted(exhausted), "proportional_used": used4,
                     "rule": "A42-D 2.3: real padded tokens x 0.163 ms (A28), $4.09/h, + $2; T_max = min(34, 32 - spend); "
                             "<= 125,000 rows; floor 50,000 rows"}
    if final["total_usd"] > tmax + 1e-9:
        probs.append(f"budget: projection ${final['total_usd']} > T_max ${tmax} after {len(rounds) - 1} trim rounds")
    if len(rows) > ROWS_MAX:
        probs.append(f"mix {len(rows):,} rows > {ROWS_MAX:,} after {len(rounds) - 1} trim rounds")
    return rows, rels


def block_mixdev_ids(ilog, blocks) -> dict:
    """{block: ids} of every block mixdev on disk (A39 h; GB: out/mixdev_S5.jsonl). They are report-only and never trained."""
    out = {}
    for b in blocks:
        if b in BLOCK_TARGETS:
            f = c2io.fam_files(b)["mixdev"]
            if f.exists():
                out[b] = {r["id"] for r in ilog.jsonl(f)}
    return out


def mixdev_id_problems(rows, mixdev: dict, rep) -> list[str]:
    """No block-mixdev id may be a training row id (A39 h); also reported per block."""
    ids = {i: b for b, v in mixdev.items() for i in v}
    hit = Counter(ids[r["id"]] for r in rows if r["id"] in ids)
    rep["block_mixdev_never_train"] = {"mixdev_ids": {b: len(v) for b, v in mixdev.items()}, "training_rows_hit": dict(hit)}
    return [f"block mixdev ids among training rows: {dict(hit)} (A39 h: report-only mixdev is never trained)"] if hit else []


A49C_BLOCKS = tuple(PROGRAM) + tuple(NEW_FAMILIES) + ("T37b",)


def a49c_assert(rows, rels, ntok: dict) -> tuple[dict, list[str]]:
    """A49 (c): the balance checks of a49c.family_checks on the SELECTED rows, per family (program families, T37b, T40-T45);
    a 'fail' is a problem. Blocks and carry pools are computed and reported only (their own A42-D / round-1 rules bind)."""
    by = defaultdict(list)
    for r in rows:
        if is_new(r):
            by[r["_block"]].append(r)
    rep, probs = {}, []
    for b, rr in sorted(by.items()):
        ids = {r["id"] for r in rr}
        ck = a49c.family_checks(b, rr, [x for x in rels if x["a"] in ids and x["b"] in ids], ntok)
        bad = a49c.failing(ck)
        rep[b] = {"binding": b in A49C_BLOCKS, "failing": bad, "checks": ck}
        if b in A49C_BLOCKS:
            probs += [f"A49 c {b}: {k} {ck[k]['value']} vs {ck[k]['bar']}" for k in bad]
    return rep, probs


def gates(a, ilog, rep, probs, rows, rels, ntok, ho, plan, t0) -> dict:
    nolic = Counter(r["_block"] for r in rows if not mx.licence_ok(r))
    rep["licence_missing_by_block"] = dict(nolic)
    if nolic:
        probs.append(f"licence join: rows without meta.licence {dict(nolic)}")
    blocks = defaultdict(list)
    for r in rows:
        blocks[r["_block"]].append(r)
    refused = refuse_held_out(ilog, {b: v for b, v in blocks.items() if b not in REPLAY_SIDE}, rep)
    if refused:
        probs.append(f"fmt1 refuse_held_out refused blocks {refused}")
    probs += ho.check(rows, rep)
    rels = mx.split_replay_call_ids(rows, rels, ntok, rep)
    probs += mx.unit_check(rows, rels, ntok, rep)
    probs += mx.check_rows(rows, rep)
    g10p = mx.g10_checks(rows, rep, a.final, side={})
    sup = [x for x in g10p if x.startswith("G10 gold position not uniform")]     # A49 b: row-level chi-square is superseded by the cell-level count
    probs += [x for x in g10p if x not in sup]
    rep["g10_superseded_by_a49b"] = sup
    rep["caps"], cp = cap_checks(rows, ntok, a.final)
    probs += cp
    rep["a49c"], ap = a49c_assert(rows, rels, ntok)
    probs += ap
    probs += mixdev_id_problems(rows, block_mixdev_ids(ilog, [b for b in plan["targets"]]), rep)
    rep["a42d_blocks"] = {}
    for b in (G_BLOCK, W2_BLOCK, META_BLOCK):
        if blocks.get(b):
            rep["a42d_blocks"][b], bp = block_rules(b, blocks[b], proportional_trim=bool(
                (rep.get("budget") or {}).get("proportional_used")))
            probs += bp
    probs += anchor_row_problems(rows, getattr(ilog, "never", {}).get("names"))
    by = Counter(r["_block"] for r in rows)
    rep["shares"], sp = share_checks(by, rep.get("plan_final") or plan)   # after refills / a trim: the final plan
    rep["shares"]["short_vs_first_plan"] = {b: [by.get(b, 0), t] for b, t in plan["targets"].items()
                                            if by.get(b, 0) < t}
    probs += sp
    import hashlib
    ids = sorted(str(r["id"]) for r in rows)
    rep["selection_digest"] = {"rows": len(ids), "ids_sha256": hashlib.sha256("\n".join(ids).encode()).hexdigest(),
                               "relations": len(rels), "rows_by_block": dict(sorted(by.items()))}
    rep["config_fill"] = config_fill(rows, rels)
    rep["problems"] = probs
    rep["inputs"] = ilog.entries
    rep["seconds"] = round(time.time() - t0, 1)
    return write_outputs(a, rep, rows, rels) if a.final else dry_report(rep)


def write_outputs(a, rep, rows, rels) -> dict:
    if rep["problems"]:
        c2io.write_json(WORK / "final_refused_c2.json", rep)
        raise SystemExit("--final refused (no training file written):\n  " + "\n  ".join(rep["problems"]))
    clean = [{k: v for k, v in r.items() if k != "_block"} for r in rows]
    rel_out = [{"a": x["a"], "b": x["b"], "type": x["type"]} for x in rels]
    sha_t = c2io.write_jsonl(OUT_TRAIN, clean)
    sha_r = c2io.write_jsonl(OUT_REL, rel_out)
    man = {"what": "C2 training mix (C2_DATA_SPEC 5; PREREG A37)", "written_utc":
           time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "ohs4_manifest_sha256": a.ohs4_sha, "seed": SEED,
           "files": {OUT_TRAIN.name: {"sha256": sha_t, "rows": len(clean)},
                     OUT_REL.name: {"sha256": sha_r, "rows": len(rel_out)}},
           "counts": {"by_block": dict(Counter(r["_block"] for r in rows)),
                      "relations": dict(Counter(x["type"] for x in rel_out))},
           "config_fill": rep["config_fill"], "budget_final_usd": rep["budget"]["final_total_usd"],
           "t_max_usd": rep["t_max_usd"], "spend_to_date_usd": rep["spend_to_date_usd"], "rows_max": ROWS_MAX,
           "never_train": rep["never_train"],
           "mix_c2_sha256": sha256_file(Path(__file__)), "c2_select_sha256": sha256_file(c2io.HERE / "c2_select.py"),
           "mixer_sha256": sha256_file(c2io.CB / "mixer.py"), "crowd_select_sha256": sha256_file(c2io.CB /
                                                                                                "crowd_select.py"),
           "pending_after_mix": list(PENDING_AFTER_MIX), "report": "c2_build/mix_c2/mix_report_c2.json"}
    c2io.write_json(OUT_MAN, man)
    c2io.write_json(WORK / "config_fill_c2.json", {**rep["config_fill"], "train_file_sha256": sha_t,
                                                   "rel_file_sha256": sha_r})
    c2io.write_json(WORK / "mix_report_c2.json", rep)
    log(f"FINAL written: {len(clean):,} rows sha {sha_t[:12]}, {len(rel_out):,} relations; "
        f"projection ${rep['budget']['final_total_usd']} (T_max ${rep['t_max_usd']})")
    return rep


def dry_report(rep) -> dict:
    c2io.write_json(WORK / "dryrun_c2.json", rep)
    log("DRY RUN (no training file written): " + json.dumps({k: rep["shares"][k] for k in ("new", "replay", "total")},
                                                           default=str) + f"; problems {len(rep['problems'])}")
    return rep


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", dest="dry_run", action="store_true")
    g.add_argument("--final", action="store_true")
    ap.add_argument("--ohs4-sha", dest="ohs4_sha", default=None, help="the OHS-4 manifest sha256 of Ruling A38")
    ap.add_argument("--decontam-drops", dest="decontam_drops", nargs="*", default=[])
    ap.add_argument("--leave-out", dest="leave_out", nargs="*", default=[],
                    help="blocks left out on purpose (spec 10.2 cut order); never T28, T33, T29 or T37b")
    ap.add_argument("--spend-to-date", dest="spend_to_date", type=float, required=True,
                    help="C2 Modal spend to date in USD, every account (A42-D 2.1); T_max = min(34, 32 - this)")
    ap.add_argument("--never-train-manifest", dest="never_train_manifest", default=None,
                    help="the never-train manifest (public anchors, A42-D 13.3); required with --final")
    ap.add_argument("--gproxy-file", dest="gproxy_file", default=None, help="the G-proxy file (A42-D 12); required with --final")
    a = ap.parse_args(argv)
    a.decontam_drops, a.excluded_globs = filter_train_globs(a.decontam_drops)      # A42-D 13.1: no OHS glob is read
    if a.final and not a.decontam_drops:
        raise SystemExit("--final needs the G13 counts-only decontamination drop lists (--decontam-drops)")
    rep = build(a)
    print(json.dumps({"t_max_usd": rep.get("t_max_usd"), "shares": rep["shares"], "budget_usd": rep.get("budget", {}).get("final_total_usd"),
                      "entry": rep["entry"], "problems": rep["problems"]}, indent=1, default=str))


if __name__ == "__main__":
    main()
