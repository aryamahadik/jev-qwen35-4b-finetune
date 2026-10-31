"""f5_carry_qc.py: the C2 re-gate record of the F5 carry-over pool (C2_DATA_SPEC 2.1 / 3.19; c2io CARRY contract).
CPU only, counts and shas only, no model call, no G13. Ruling A66 (a): a block-specific QC-record writer is a program fix
that implements the pre-registered admission fields; it re-derives every binding non-G13 gate from the files on disk at
UNCHANGED bars, writes pass=true only when all pass, records file sha256s, lists the pending gates, writes only this
block's QC_REPORT.json and backs up any existing record first.

  data/c2_parts/F5/qc/QC_REPORT.json = {"pass", "passed_utc", "fix_iterations", "files": {name: {"sha256", "rows"}}, ...}
  bound to the round-1 candidates file c_src/F5/out/candidates_r1.jsonl (+ relations): the contract of qc_full_c2.finalize.

What it re-checks now (spec 3.19: "existing gates + G13 against the new targets"; G13 is NOT run here):
  R1  the round-1 record c_src/F5/qc/QC_REPORT.json (sha recorded): pass true, failed_gates [], mixer.qc_binding [] against
      the files on disk, every recorded pool sha256 equals the file on disk, every recorded gate has pass true.
  R2  the live C2 checks on the candidates: c2io.candidate_problems, the round-1 MANIFEST + sha checks, relation endpoints,
      G-TW 100%, units whole (size 1..3), exact duplicate count 0, formats-1 strict refuse_held_out, the shard set's
      candidates sha = the file, every row has a C1 crowd label of the one C1 view, no choice rows.
  R3  the selectable pool (complement and equiv units of the round-1 selection) holds the 1,500 target (counts reported).
  R4  (A66 a) the binding gates G2 G3 G4 G5 G6 G7 G10 G11 G12 G15 G18 re-derived from their gate-output FILES (each sha256
      recorded) against the bars written below, which are the pre-registered bars copied from the F5 gate scripts
      (c_src/F5/qc/g*.py, solverB) and never read from the files; the files' row counts, sampler / gold / unit / relation /
      card / pack counts are cross-checked against the LIVE candidates, so an edited or stale gate file bites. G8 is
      report-only for yes/no parts (PREREG_FINAL A19.1); that F5 has no choice rows is checked live. The round-1
      `sealed_check` boolean is only carried (its file lies on the never-open side, so this tool cannot re-derive it): it is
      listed as pending inside the G13 / OHS-AC path.
Pending (listed in `gates_pending`): G13 incl. the OHS-AC / sealed-side path, the sealed_check re-run, crowd selection (G9).
Usage (from c2_build):  ../../.venv/bin/python -B zed_orch/f5_carry_qc.py [--write]
Without --write nothing is written (report only). With --write an existing record is copied to
c2_build/_backup_a66/F5/ first (a failed backup stops the write).
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

import c2io  # noqa: E402
from mixio import sha256_file  # noqa: E402

LEAN = c2io.LEAN
F5 = LEAN / "c_src" / "F5"
R1_QC = F5 / "qc" / "QC_REPORT.json"
OUTQ = c2io.C2_PARTS / "F5" / "qc" / c2io.QC
BACKUP_DIR = HERE / "_backup_a66" / "F5"
FAM = "F5"

# ---------------------------------------------------------------------------------------------------------------------
# The unchanged bars (copied from the F5 gate scripts; never read from the gate files)
# ---------------------------------------------------------------------------------------------------------------------
G6_BAR = 0.52                                   # g6.py: every gated grouped accuracy <= 0.52
G6_GATED = ("a_question.lr_grouped", "a_question.gbt_grouped", "c_card_noq.lr_grouped", "c_card_noq.gbt_grouped",
            "d_meta.lr_grouped", "d_meta.gbt_grouped")
G15_TOKEN_CAP = 1900                            # F5 served-prompt cap (g15_g18.py rows_gt_1900_F5_cap)
G5_MAX_AMBIGUOUS = 3                            # "<= 1% (3 of 300)"; clearly_wrong 0 confirmed
G5_N = 300
G10_B_TARGET_ROWS = 3600                        # g10.py: keep >= 3600
# g10.py part A cells: key -> (tolerance, n_min); report-only keys are not gated
G10_A_CELLS = {"row_type": (0.02, 1), "k_neg": (0.02, 1), "k_all": (0.02, 1), "j_q": (0.02, 1), "j_t": (0.03, 1),
               "t_txt": (0.03, 1), "sampler": (0.02, 1), "wording": (0.02, 1), "cue_family": (0.03, 200),
               "world": (0.03, 1), "location": (0.03, 1), "sem_key": (0.03, 1), "A_rows_op_x_world": (0.03, 200)}
G10_OVERALL_TOL = 0.02
# g10.py part A quotas: key -> (lo, hi) on "v" (None = open)
G10_Q_RANGE = {"yes_is_bad_share": (0.45, 0.55), "no_polarity_share": (None, 0.05), "double_negation_k_all>=2": (0.25, None),
               "k_syn>=1_share": (0.10, None), "k_syn>=2_with_affirmative_twin": (0.02, None),
               "attack_rows_share": (0.04, 0.06), "contrast_set_share": (0.20, 0.25), "deep_rows": (None, 0.10),
               "depth>=3_bases": (None, 0.04), "decoy_rows": (0.10, None), "text_side_negation": (0.30, None),
               "label_check_form_rows": (None, 0), "cards": (80, None), "inverted_cards": (0.10, 0.15),
               "fewshot_cards": (0.05, 0.10), "short_card_bases": (0.12, 0.18)}
G10_ATTACK_P_MIN = 0.01                         # chi2 p > 0.01 (strict)
G10_VERBATIM_MIN_SHARE, G10_VERBATIM_YES_TOL = 0.15, 0.03
G11_MAX_SAMPLER_ROWS, G11_MIN_PACKS, G11_MIN_TRAIN_SAMPLERS = 2500, 30, 4
G11_TWO_PCT = 0.02
G12_ZERO = ("exact_dup_model_view", "exact_dup_raw_fields")
SETS = ("candidates_r1", "qc_sample", "mixdev_S5")
# gate files are read by name relative to c_src/F5; a name on the never-open side (OHS, sealed side, quarantine, Jev) is refused here
# in addition to c2io.refusal, which does not know the F5 `sealed_check` file name
GATE_NEVER_RE = re.compile(r"ohs|sealed|preread|quarantine|longbench|jev", re.I)


# ---------------------------------------------------------------------------------------------------------------------
# JSONL helpers: split on "\n" only (never str.splitlines / universal newlines)
# ---------------------------------------------------------------------------------------------------------------------
def jsonl_lines(path) -> list[bytes]:
    return [x for x in Path(path).read_bytes().split(b"\n") if x.strip()]


def count_jsonl_rows(path) -> int:
    return len(jsonl_lines(path))


class GateReader:
    """Reads gate-output JSON files under `root`, refusing never-open paths (c2io.refusal) and recording the sha256 and
    byte size of every file it opens."""

    def __init__(self, root: Path, guard=None):
        self.root = Path(root)
        self.guard = guard or c2io.refusal
        self.files: dict[str, dict] = {}

    def path(self, rel: str) -> Path:
        p = self.root / rel
        why = self.guard(p) or (f"gate file name on the never-open side ({GATE_NEVER_RE.search(rel).group(0)!r})"
                                if GATE_NEVER_RE.search(rel) else None)
        if why:
            raise c2io.C2Refused(f"gate file refused: {rel}: {why}")
        return p

    def record(self, rel: str) -> Path:
        p = self.path(rel)
        if not p.is_file():
            raise FileNotFoundError(rel)
        if rel not in self.files:
            self.files[rel] = {"sha256": sha256_file(p), "bytes": p.stat().st_size}
        return p

    def json(self, rel: str):
        p = self.record(rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    def count_rows(self, rel: str) -> int:
        return count_jsonl_rows(self.record(rel))


def _num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _eq(p: list, what: str, got, want) -> None:
    if got != want:
        p.append(f"{what}: {got!r} != {want!r}")


def _zero(p: list, what: str, got) -> None:
    if got != 0 or isinstance(got, bool):
        p.append(f"{what}: {got!r} != 0")


def _get(d, *keys):
    for k in keys:
        if not isinstance(d, dict) or k not in d:
            return None
        d = d[k]
    return d


# ---------------------------------------------------------------------------------------------------------------------
# One checker per gate. Each takes the parsed gate files and the live stats and returns a list of problems.
# ---------------------------------------------------------------------------------------------------------------------
def live_set_rows(live: dict) -> dict:
    return {"candidates_r1": live["rows"], "qc_sample": live["qc_sample_rows"], "mixdev_S5": live["mixdev_rows"]}


def chk_g2(sol: dict, live: dict) -> list[str]:
    p: list[str] = []
    want = {"candidates_r1.jsonl": live["rows"], "qc_sample.jsonl": live["qc_sample_rows"], "mixdev_S5.jsonl": live["mixdev_rows"]}
    _eq(p, "G2 files", sol.get("files"), want)
    total = sum(want.values())
    _eq(p, "G2 rows_checked", sol.get("rows_checked"), total)
    _eq(p, "G2 agree", sol.get("agree"), total)
    _eq(p, "G2 agree_pct", sol.get("agree_pct"), 100.0)
    for k in ("n_mismatch", "n_undetermined", "n_unparsed"):
        _zero(p, f"G2 {k}", sol.get(k))
    _eq(p, "G2 mismatches", sol.get("mismatches"), [])
    _eq(p, "G2 unparsed", sol.get("unparsed"), [])
    by = sol.get("by_sampler") or {}
    if not by or any(not k.endswith(":agree") for k in by) or sum(v for v in by.values() if _num(v)) != total:
        p.append(f"G2 by_sampler does not sum to rows_checked: {by}")
    return p


def chk_g3(gates: dict, live: dict) -> list[str]:
    """gates = {set: parsed out/<set>.gates.json}; the G3 half."""
    p: list[str] = []
    for s, n in live_set_rows(live).items():
        d = gates.get(s)
        if not isinstance(d, dict):
            p.append(f"G3 {s}: no gates file")
            continue
        g = d.get("G3") or {}
        _eq(p, f"G3 {s} set", d.get("set"), s)
        _eq(p, f"G3 {s} rows", g.get("rows"), n)
        _eq(p, f"G3 {s} rows_ok", g.get("rows_ok"), n)
        _eq(p, f"G3 {s} errors", g.get("errors"), [])
    return p


def chk_g15_builder(gates: dict, live: dict) -> list[str]:
    """The builder's G15 half of out/<set>.gates.json: whole units, token cap."""
    p: list[str] = []
    for s, n in live_set_rows(live).items():
        g = (gates.get(s) or {}).get("G15") or {}
        _eq(p, f"G15 {s} ok rows", g.get("ok"), n)
        _zero(p, f"G15 {s} unit_over_3", g.get("unit_over_3"))
        _zero(p, f"G15 {s} rel_split", g.get("rel_split"))
        _eq(p, f"G15 {s} errors", g.get("errors"), [])
        _eq(p, f"G15 {s} token_cap", g.get("token_cap"), G15_TOKEN_CAP)
        st = g.get("served_tokens") or {}
        if not (_num(st.get("max")) and st["max"] <= G15_TOKEN_CAP and _num(st.get("min")) and st["min"] > 0):
            p.append(f"G15 {s} served_tokens {st} not within 1..{G15_TOKEN_CAP}")
    c = (gates.get("candidates_r1") or {}).get("G15") or {}
    _eq(p, "G15 candidates_r1 units vs live units", c.get("units"), live["units"])
    return p


def chk_g4(g4: dict, live: dict) -> list[str]:
    p: list[str] = []
    for s in SETS:
        d = g4.get(s)
        if not isinstance(d, dict):
            p.append(f"G4 {s}: no file")
            continue
        _eq(p, f"G4 {s} set", d.get("set"), s)
        _eq(p, f"G4 {s} errors", d.get("errors"), [])
        counts = d.get("counts") or {}
        n_pass = 0
        for k, v in counts.items():
            last = k.rsplit(":", 1)[-1]
            if last == "rows":
                continue
            if last not in ("pass", "n/a"):
                if not _num(v) or v != 0:
                    p.append(f"G4 {s}: outcome {k} = {v}")
            elif last == "pass" and _num(v):
                n_pass += v
        if n_pass <= 0:
            p.append(f"G4 {s}: no passing checks recorded")
        for k, v in counts.items():
            if not _num(v) or v < 0:
                p.append(f"G4 {s}: bad count {k}={v!r}")
        # per sampler "<S>:rows" cannot exceed the live rows of that sampler (INV rows are the planned inverse rows)
        for k, v in counts.items():
            pre, _, last = k.rpartition(":")
            if last == "rows" and pre in live["samplers"] and _num(v) and v > live["samplers"][pre] and s == "candidates_r1":
                p.append(f"G4 {s}: {k}={v} above the live sampler rows {live['samplers'][pre]}")
    return p


def g5_counts(d: dict) -> tuple[int, int, int]:
    """(clearly_wrong, ambiguous, n) of a G5 file of either schema."""
    if isinstance(d.get("total"), dict):
        t = d["total"]
        return t.get("clearly_wrong"), t.get("ambiguous"), t.get("n")
    return d.get("n_clearly_wrong"), d.get("n_ambiguous"), d.get("n_answered")


def chk_g5(g5: dict, live: dict) -> list[str]:
    """g5 = {"wording": final file, "pre": qc/g5_wording_pre_g10fix.json, "a32": ..., "r2": ...}."""
    p: list[str] = []
    w = g5["wording"]
    _eq(p, "G5 final file sha256 vs live candidates sha", w.get("sha256"), live["cand_sha"])
    _eq(p, "G5 final file pass", w.get("pass"), True)
    t, c, f = w.get("total") or {}, w.get("carried") or {}, w.get("fresh") or {}
    _eq(p, "G5 sample n", _get(w, "sample", "n"), G5_N)
    _eq(p, "G5 total n", t.get("n"), G5_N)
    _eq(p, "G5 carried + fresh n", (c.get("n") or 0) + (f.get("n") or 0), G5_N)
    _eq(p, "G5 carried + fresh agree", (c.get("agree") or 0) + (f.get("agree") or 0), t.get("agree"))
    if _num(t.get("agree")) and _num(t.get("n")) and t["n"]:
        _eq(p, "G5 agreement", t.get("agreement"), round(t["agree"] / t["n"], 4))
    _zero(p, "G5 total clearly_wrong", t.get("clearly_wrong"))
    _zero(p, "G5 carried clearly_wrong", c.get("clearly_wrong"))
    _zero(p, "G5 fresh clearly_wrong", f.get("clearly_wrong"))
    amb = (c.get("ambiguous") or 0) + (f.get("ambiguous") or 0)
    if amb > G5_MAX_AMBIGUOUS or (t.get("ambiguous") or 0) > G5_MAX_AMBIGUOUS:
        p.append(f"G5 ambiguous {amb} / {t.get('ambiguous')} > {G5_MAX_AMBIGUOUS}")
    for name in ("pre", "a32", "r2"):
        d = g5.get(name)
        if not isinstance(d, dict):
            p.append(f"G5 {name}: no file")
            continue
        _eq(p, f"G5 {name} pass", d.get("pass"), True)
        cw, am, n = g5_counts(d)
        _zero(p, f"G5 {name} clearly_wrong", cw)
        if not (_num(am) and am <= G5_MAX_AMBIGUOUS):
            p.append(f"G5 {name} ambiguous {am!r} > {G5_MAX_AMBIGUOUS}")
        _eq(p, f"G5 {name} n", n, G5_N)
    return p


def chk_g6(g6: dict, live: dict) -> list[str]:
    p: list[str] = []
    _eq(p, "G6 set", g6.get("set"), "qc_sample")
    _eq(p, "G6 n", g6.get("n"), live["qc_sample_rows"])
    gated = g6.get("gated") or {}
    if tuple(sorted(gated)) != tuple(sorted(G6_GATED)):
        p.append(f"G6 gated keys {sorted(gated)} != the pre-registered six")
    for k in G6_GATED:
        v = gated.get(k)
        if not _num(v):
            p.append(f"G6 {k} missing")
        elif v > G6_BAR:
            p.append(f"G6 {k} = {v} > bar {G6_BAR}")
    vals = [v for v in gated.values() if _num(v)]
    if vals:
        _eq(p, "G6 max_gated", g6.get("max_gated"), max(vals))
    return p


def chk_g7(g7: dict, live: dict) -> list[str]:
    p: list[str] = []
    for s in ("candidates_r1", "qc_sample"):
        d = g7.get(s)
        if not isinstance(d, dict):
            p.append(f"G7 {s}: no file")
            continue
        _eq(p, f"G7 {s} set", d.get("set"), s)
        _eq(p, f"G7 {s} rows", d.get("rows"), live_set_rows(live)[s])
        _zero(p, f"G7 {s} n_fail", d.get("n_fail"))
        _eq(p, f"G7 {s} fails", d.get("fails"), [])
        _zero(p, f"G7 {s} n_fail_at_50k_denominator", d.get("n_fail_at_50k_denominator"))
        _zero(p, f"G7 {s} n_fail_text", d.get("n_fail_text"))
        _zero(p, f"G7 {s} n_fail_meta", d.get("n_fail_meta"))
        if not (_num(d.get("features_tested")) and d["features_tested"] > 0):
            p.append(f"G7 {s}: no features tested")
    return p


def _cell_problems(name: str, block: dict, tol: float, nmin: int) -> list[str]:
    p = []
    cells = (block or {}).get("cells")
    if not isinstance(cells, dict) or not cells:
        return [f"G10 {name}: no cells"]
    for k, v in cells.items():
        if not (isinstance(v, dict) and _num(v.get("n")) and _num(v.get("yes"))):
            p.append(f"G10 {name}[{k}] malformed")
        elif v["n"] >= nmin and abs(v["yes"] - 0.5) > tol:
            p.append(f"G10 {name}[{k}] yes {v['yes']} n {v['n']} outside 0.5 +/- {tol}")
    return p


def chk_g10(g10: dict, live: dict) -> list[str]:
    p: list[str] = []
    for s in ("candidates_r1", "qc_sample"):
        d = g10.get(s)
        if not isinstance(d, dict):
            p.append(f"G10 {s}: no file")
            continue
        n = live_set_rows(live)[s]
        _eq(p, f"G10 {s} set", d.get("set"), s)
        _eq(p, f"G10 {s} rows", d.get("rows"), n)
        A, Q = d.get("A_construction") or {}, d.get("A_quotas") or {}
        ov = A.get("overall") or {}
        _eq(p, f"G10 {s} overall n", ov.get("n"), n)
        if not (_num(ov.get("yes")) and abs(ov["yes"] - 0.5) <= G10_OVERALL_TOL):
            p.append(f"G10 {s} overall yes {ov.get('yes')!r} outside 0.5 +/- {G10_OVERALL_TOL}")
        for key, (tol, nmin) in G10_A_CELLS.items():
            p += [f"{s}: {x}" for x in _cell_problems(key, A.get(key), tol, nmin)]
        for key, (lo, hi) in G10_Q_RANGE.items():
            v = _get(Q, key, "v")
            if not _num(v):
                p.append(f"G10 {s} quota {key} missing")
                continue
            if (lo is not None and v < lo) or (hi is not None and v > hi):
                p.append(f"G10 {s} quota {key} = {v} outside [{lo}, {hi}]")
        pv = _get(Q, "attack_present_vs_label", "chi2_p")
        if not (_num(pv) and pv > G10_ATTACK_P_MIN):
            p.append(f"G10 {s} attack_present_vs_label chi2_p {pv!r} not > {G10_ATTACK_P_MIN}")
        vo = Q.get("verbatim_overlap") or {}
        if not (_num(vo.get("share_of_jq>=1")) and vo["share_of_jq>=1"] >= G10_VERBATIM_MIN_SHARE
                and _num(vo.get("yes")) and abs(vo["yes"] - 0.5) <= G10_VERBATIM_YES_TOL):
            p.append(f"G10 {s} verbatim_overlap {vo}")
        _zero(p, f"G10 {s} per_card_rate_vs_r_card n_off", _get(Q, "per_card_rate_vs_r_card", "n_off"))
        B = d.get("B_wording_bin_kall") or {}
        _zero(p, f"G10 {s} B n_fail_raw", B.get("n_fail_raw"))
        if not (_num(B.get("feasible_rows_after_exact_balancing")) and B["feasible_rows_after_exact_balancing"] >= G10_B_TARGET_ROWS):
            p.append(f"G10 {s} B feasible rows {B.get('feasible_rows_after_exact_balancing')!r} < {G10_B_TARGET_ROWS}")
        # live cross-binding: overall and per-sampler yes rate and size
        if s == "candidates_r1":
            _eq(p, "G10 candidates_r1 overall yes vs live", ov.get("yes"), round(live["gold_yes"] / n, 4))
            sc = _get(A, "sampler", "cells") or {}
            _eq(p, "G10 sampler cells (n) vs live", {k: v.get("n") for k, v in sc.items()}, dict(live["samplers"]))
            _eq(p, "G10 sampler cells (yes) vs live", {k: v.get("yes") for k, v in sc.items()},
                {k: round(live["gold_by_sampler"][k] / live["samplers"][k], 4) for k in live["samplers"]})
            _eq(p, "G10 cards vs live", _get(Q, "cards", "v"), live["cards"])
    return p


def chk_g11(g11: dict, live: dict) -> list[str]:
    p: list[str] = []
    _eq(p, "G11 rows", g11.get("rows"), live["rows"])
    c = g11.get("counts") or {}
    if not (isinstance(c.get("training_samplers"), list) and len(c["training_samplers"]) >= G11_MIN_TRAIN_SAMPLERS):
        p.append(f"G11 training_samplers {c.get('training_samplers')!r} < {G11_MIN_TRAIN_SAMPLERS}")
    _zero(p, "G11 S5_rows", c.get("S5_rows"))
    if not (_num(c.get("max_sampler_rows")) and c["max_sampler_rows"] <= G11_MAX_SAMPLER_ROWS):
        p.append(f"G11 max_sampler_rows {c.get('max_sampler_rows')!r} > {G11_MAX_SAMPLER_ROWS}")
    if not (_num(c.get("packs")) and c["packs"] >= G11_MIN_PACKS):
        p.append(f"G11 packs {c.get('packs')!r} < {G11_MIN_PACKS}")
    _zero(p, "G11 held_out_style_rows", c.get("held_out_style_rows"))
    _eq(p, "G11 cards_with_one_sampler_pack == cards", c.get("cards_with_one_sampler_pack"), c.get("cards"))
    t2 = g11.get("two_pct") or {}
    for k in ("frame_x_template", "question_skeleton"):
        v = _get(t2, k, "max_share")
        if not (_num(v) and v <= G11_TWO_PCT):
            p.append(f"G11 two_pct {k} max_share {v!r} > {G11_TWO_PCT}")
    _zero(p, "G11 seeds wordings pairs_ge_0.7", _get(g11, "seeds_rouge_l", "wordings", "pairs_ge_0.7"))
    _eq(p, "G11 by_sampler vs live", c.get("by_sampler"), dict(live["samplers"]))
    _eq(p, "G11 cards vs live", c.get("cards"), live["cards"])
    _eq(p, "G11 packs vs live", c.get("packs"), live["packs"])
    _eq(p, "G11 S5 rows vs live", c.get("S5_rows"), live["samplers"].get("S5", 0))
    return p


def chk_g12(g12: dict, live: dict) -> list[str]:
    p: list[str] = []
    for s in ("candidates_r1", "qc_sample"):
        d = g12.get(s)
        if not isinstance(d, dict):
            p.append(f"G12 {s}: no file")
            continue
        _eq(p, f"G12 {s} rows", d.get("rows"), live_set_rows(live)[s])
        for k in G12_ZERO:
            _zero(p, f"G12 {s} {k}", d.get(k))
        mh = d.get("minhash_question_plus_record") or {}
        _zero(p, f"G12 {s} non_twin_pairs", mh.get("non_twin_pairs"))
        _zero(p, f"G12 {s} minhash_record_only non_pair_base_pairs", _get(d, "minhash_record_only_info", "non_pair_base_pairs"))
        _zero(p, f"G12 {s} hashes_spanning_bases", _get(d, "structure_hash_generator", "hashes_spanning_bases"))
        _zero(p, f"G12 {s} keys_spanning_non_twin_bases", _get(d, "structure_hash_independent", "keys_spanning_non_twin_bases"))
    _eq(p, "G12 live exact duplicates (candidates_r1)", live["dups"], 0)
    return p


def chk_g15_g18(g15: dict, live: dict) -> list[str]:
    p: list[str] = []
    for s in ("candidates_r1", "qc_sample"):
        d = g15.get(s)
        if not isinstance(d, dict):
            p.append(f"G15 {s}: no file")
            continue
        _eq(p, f"G15 {s} rows", d.get("rows"), live_set_rows(live)[s])
        for k in ("loader_check_fail", "roundtrip_gold_fail", "relations_split_call_id", "relations_missing_rows",
                  "relations_gold_inconsistent", "units_gt3", "units_long_gt2"):
            _zero(p, f"G15 {s} {k}", d.get(k))
        tk = d.get("tokens_full_chat_prompt") or {}
        if not (_num(tk.get("max")) and tk["max"] <= G15_TOKEN_CAP):
            p.append(f"G15 {s} max prompt tokens {tk.get('max')!r} > {G15_TOKEN_CAP}")
        _zero(p, f"G15 {s} rows_gt_1900_F5_cap", tk.get("rows_gt_1900_F5_cap"))
        _zero(p, f"G15 {s} rows_gt_7900", tk.get("rows_gt_7900"))
        g18 = d.get("G18") or {}
        _zero(p, f"G18 {s} ordinal_rows", g18.get("ordinal_rows"))
        _eq(p, f"G18 {s} applies", g18.get("applies"), False)
    c = g15.get("candidates_r1") or {}
    _eq(p, "G15 candidates_r1 relations vs live", c.get("relations"), live["relations"])
    _eq(p, "G15 candidates_r1 relation_types vs live", c.get("relation_types"), live["relation_kinds"])
    _eq(p, "G15 candidates_r1 call_units vs live", c.get("call_units"), live["units"])
    _eq(p, "G15 candidates_r1 unit_size_hist vs live", c.get("unit_size_hist"), {str(k): v for k, v in live["unit_sizes"].items()})
    return p


def chk_g8_report_only(g8: dict, live: dict) -> list[str]:
    """PREREG_FINAL A19.1: G8 gates choice parts only; yes/no parts are report-only. F5 has no choice rows (checked live)."""
    p: list[str] = []
    if live["choice_rows"] != 0:
        p.append(f"G8 would gate: {live['choice_rows']} live rows carry an options list (choice rows)")
    _eq(p, "G8 rows (report file)", g8.get("rows"), live["rows"])
    return p


def chk_r1_consistency(r1gates: dict, d: dict) -> list[str]:
    """The round-1 record's recorded numbers must equal what the gate files say now."""
    p: list[str] = []
    g2, g6, g7, g11 = r1gates.get("G2") or {}, r1gates.get("G6") or {}, r1gates.get("G7") or {}, r1gates.get("G11") or {}
    _eq(p, "round-1 G2.agree vs solver file", g2.get("agree"), _get(d, "G2", "agree"))
    _eq(p, "round-1 G6.max_gated vs file", g6.get("max_gated_grouped_by_card"), _get(d, "G6", "max_gated"))
    _eq(p, "round-1 G7.features_tested vs files", g7.get("features_tested"),
        [_get(d, "G7", s, "features_tested") for s in ("candidates_r1", "qc_sample")])
    _eq(p, "round-1 G11 max_sampler_rows vs file", _get(g11, "counts", "max_sampler_rows"), _get(d, "G11", "counts", "max_sampler_rows"))
    _eq(p, "round-1 G5 total vs file", _get(r1gates, "G5", "total"), _get(d, "G5", "wording", "total"))
    return p


GATE_FILES = {
    "G2": {"sol": "solverB/mismatch.json"},
    "G3_G15b": {s: f"out/{s}.gates.json" for s in SETS},
    "G4": {s: f"out/{s}.G4.json" for s in SETS},
    "G5": {"wording": "qc/g5_wording.json", "pre": "qc/g5_wording_pre_g10fix.json", "a32": "qc/g5_a32.json", "r2": "qc/g5_r2.json"},
    "G6": {"f": "qc/g6_qc_sample.json"},
    "G7": {s: f"qc/g7_{s}.json" for s in ("candidates_r1", "qc_sample")},
    "G8": {"f": "qc/g8_candidates_r1.json"},
    "G10": {s: f"qc/g10_{s}.json" for s in ("candidates_r1", "qc_sample")},
    "G11": {"f": "qc/g11_candidates_r1.json"},
    "G12": {s: f"qc/g12_{s}.json" for s in ("candidates_r1", "qc_sample")},
    "G15_G18": {s: f"qc/g15_g18_{s}.json" for s in ("candidates_r1", "qc_sample")},
}
ROW_FILES = {"qc_sample": "out/qc_sample.jsonl", "mixdev_S5": "out/mixdev_S5.jsonl"}


def rederive_gates(reader: GateReader, live: dict, r1gates: dict | None = None) -> tuple[dict, list[str]]:
    """Read every gate-output file and apply the unchanged bars. Returns ({gate: {"pass", "problems", "files"}}, problems).
    A missing, refused or unparsable file is a problem for its gate (never a pass)."""
    names = ("G2", "G3", "G4", "G5", "G6", "G7", "G8", "G10", "G11", "G12", "G15", "G18")
    problems_by: dict[str, list[str]] = {g: [] for g in names}
    loaded: dict[str, dict] = {}
    for key, mapping in GATE_FILES.items():
        gate = key.split("_")[0]
        loaded[key] = {}
        for k, rel in mapping.items():
            try:
                loaded[key][k] = reader.json(rel)
            except Exception as e:
                problems_by[gate].append(f"{rel}: {type(e).__name__}: {e}")

    def evaluate(gate: str, key: str, fn, single: str | None = None) -> list[str]:
        d = loaded[key]
        if set(d) != set(GATE_FILES[key]):
            return [f"{gate}: gate file(s) missing, not evaluated"]
        return fn(d[single] if single else d, live)

    problems_by["G2"] += evaluate("G2", "G2", chk_g2, "sol")
    problems_by["G3"] += evaluate("G3", "G3_G15b", chk_g3)
    problems_by["G4"] += evaluate("G4", "G4", chk_g4)
    problems_by["G5"] += evaluate("G5", "G5", chk_g5)
    problems_by["G6"] += evaluate("G6", "G6", chk_g6, "f")
    problems_by["G7"] += evaluate("G7", "G7", chk_g7)
    problems_by["G8"] += evaluate("G8", "G8", chk_g8_report_only, "f")
    problems_by["G10"] += evaluate("G10", "G10", chk_g10)
    problems_by["G11"] += evaluate("G11", "G11", chk_g11, "f")
    problems_by["G12"] += evaluate("G12", "G12", chk_g12)
    problems_by["G15"] += evaluate("G15", "G3_G15b", chk_g15_builder)          # the builder's G15 half (out/<set>.gates.json)
    for x in evaluate("G15", "G15_G18", chk_g15_g18):                           # the checker's G15 + G18 files
        problems_by["G18" if x.startswith("G18") else "G15"].append(x)

    cons: list[str] = []
    if r1gates is not None:
        if all(set(loaded[k]) == set(GATE_FILES[k]) for k in ("G2", "G5", "G6", "G7", "G11")):
            cons = chk_r1_consistency(r1gates, {"G2": loaded["G2"]["sol"], "G5": loaded["G5"], "G6": loaded["G6"]["f"],
                                                "G7": loaded["G7"], "G11": loaded["G11"]["f"]})
        else:
            cons = ["round-1 consistency not evaluated: a gate file is missing"]
    files_by_gate = {"G2": GATE_FILES["G2"].values(), "G3": GATE_FILES["G3_G15b"].values(), "G4": GATE_FILES["G4"].values(),
                     "G5": GATE_FILES["G5"].values(), "G6": GATE_FILES["G6"].values(), "G7": GATE_FILES["G7"].values(),
                     "G8": GATE_FILES["G8"].values(), "G10": GATE_FILES["G10"].values(), "G11": GATE_FILES["G11"].values(),
                     "G12": GATE_FILES["G12"].values(), "G15": list(GATE_FILES["G15_G18"].values()) + list(GATE_FILES["G3_G15b"].values()),
                     "G18": GATE_FILES["G15_G18"].values()}
    gates: dict = {}
    for g in names:
        gates[g] = {"pass": not problems_by[g], "problems": problems_by[g],
                    "files": {rel: reader.files[rel]["sha256"] for rel in files_by_gate[g] if rel in reader.files}}
    gates["G8"] |= {"gated": False, "rule": "PREREG_FINAL A19.1: yes/no parts report-only; the raw old-rule verdict in "
                                            "qc/g8_candidates_r1.json is not a gate for F5 (no choice rows, checked live)"}
    gates["round1_consistency"] = {"pass": not cons, "problems": cons}
    all_problems = [x for v in gates.values() for x in v["problems"]]
    return gates, all_problems


# ---------------------------------------------------------------------------------------------------------------------
# Live stats from the candidates / relations / units
# ---------------------------------------------------------------------------------------------------------------------
def live_stats(rows: list, rels: list, units: list, reader: GateReader, cand_sha: str, mixdev_path: Path) -> dict:
    sam = Counter((r.get("meta") or {}).get("sampler") for r in rows)
    by_s: Counter = Counter()
    for r in rows:
        by_s[(r.get("meta") or {}).get("sampler")] += int(r["gold"])
    kinds: Counter = Counter()
    by = {r["id"] for r in rows}
    for x in rels:
        if x["a"] in by and x["b"] in by:
            kinds[x["type"]] += 1
    return {"rows": len(rows), "samplers": dict(sam), "gold_yes": sum(int(r["gold"]) for r in rows),
            "gold_by_sampler": dict(by_s), "relations": len(rels), "relation_kinds": dict(kinds),
            "units": len(units), "unit_sizes": dict(Counter(len(u) for u in units)),
            "cards": len({(r.get("meta") or {}).get("card_id") for r in rows}),
            "packs": len({(r.get("meta") or {}).get("domain_pack") for r in rows}),
            "choice_rows": sum(1 for r in rows if r.get("options")),
            "qc_sample_rows": reader.count_rows(ROW_FILES["qc_sample"]),
            "mixdev_rows": count_jsonl_rows(mixdev_path), "cand_sha": cand_sha, "dups": 0}


# ---------------------------------------------------------------------------------------------------------------------
# Writing: backup first
# ---------------------------------------------------------------------------------------------------------------------
def backup_existing(out: Path, backup_dir: Path, stamp: str) -> dict | None:
    """Copy an existing record to backup_dir before it is replaced. Returns {"path", "sha256"} or None when there is none.
    Raises (and nothing is written) when the copy cannot be made or does not verify."""
    out = Path(out)
    if not out.exists():
        return None
    backup_dir = Path(backup_dir)
    backup_dir.mkdir(parents=True, exist_ok=True)
    dest = backup_dir / f"QC_REPORT.pre_write_{stamp}.json"
    n = 1
    while dest.exists():
        dest = backup_dir / f"QC_REPORT.pre_write_{stamp}_{n}.json"
        n += 1
    shutil.copy2(out, dest)
    if sha256_file(dest) != sha256_file(out):
        raise RuntimeError(f"backup {dest} does not match {out}")
    return {"path": str(dest), "sha256": sha256_file(dest)}


def write_record(rec: dict, out: Path, backup_dir: Path, stamp: str, writer=None) -> dict:
    """Backup-before-write. `writer(path, obj) -> sha` defaults to c2io.write_json. The only file written (besides the
    backup copy) is `out`."""
    bk = backup_existing(out, backup_dir, stamp)
    sha = (writer or c2io.write_json)(out, rec)
    return {"written": str(out), "sha256": sha, "backup": bk}


GATES_PENDING = [
    "G13 decontamination against the new targets: g13_c2.py carry --block F5 (orchestrator batch; includes the OHS-AC / "
    "sealed-side checkers, drops are whole units)",
    "sealed_check re-run inside that G13 / OHS-AC path: the round-1 sealed_check boolean is carried only, its file is on the "
    "never-open side and was not read by this tool",
    "crowd selection (G9) on the G13 drops: c2_select.py carry --fam F5 --exclude-ids <c2_carry_F5.json>",
]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args(argv)
    c2io.require_a38()
    import c2_select as sel  # noqa: E402
    import crowd_select as cs  # noqa: E402
    problems: list[str] = []
    rec: dict = {"family": FAM, "stage": "C2 carry-over re-gate (spec 3.19)", "tool": "c2_build/zed_orch/f5_carry_qc.py",
                 "tool_sha256": sha256_file(Path(__file__).resolve()), "ruling": "A66 (a): block-specific QC-record writer"}

    # ---- R1: the round-1 record
    r1 = json.loads(R1_QC.read_bytes().decode("utf-8"))
    f = c2io.fam_files(FAM)
    cand, relf = f["cand"], f["rel"]
    sys.path.insert(0, str(LEAN / "c_build"))
    import mixer as mx  # noqa: E402
    bind = mx.qc_binding(r1, {cand.name: cand, relf.name: relf})
    gates1 = r1.get("gates", {})
    bad_gates = sorted(g for g, v in gates1.items() if not (isinstance(v, dict) and v.get("pass") is True))
    pool_bad = []
    for name, sha in (r1.get("pool_sha256") or {}).items():
        p = F5 / "out" / name
        if not p.exists() or sha256_file(p) != sha:
            pool_bad.append(name)
    r1_ok = r1.get("pass") is True and not r1.get("failed_gates") and not bind and not bad_gates and not pool_bad
    rec["round1_record"] = {"file": "c_src/F5/qc/QC_REPORT.json", "sha256": sha256_file(R1_QC), "pass": r1.get("pass"),
                            "written_utc": r1.get("written_utc"), "failed_gates": r1.get("failed_gates"),
                            "gates": {g: v.get("pass") for g, v in gates1.items()}, "qc_binding_problems": bind,
                            "gates_not_pass_true": bad_gates, "pool_files_checked": len(r1.get("pool_sha256") or {}),
                            "pool_files_differing": pool_bad}
    if not r1_ok:
        problems.append(f"round-1 record: binding {bind}, gates {bad_gates}, pool files {pool_bad}")

    # ---- R2: live checks
    ilog = sel.LinkGuardedInputLog()
    rows, rels, shas = sel.family_inputs(ilog, FAM)          # cs.load_family: MANIFEST + sha checks, raises on a mismatch
    cp = c2io.candidate_problems(FAM, rows)
    by = {r["id"]: r for r in rows}
    miss = [x for x in rels if x["a"] not in by or x["b"] not in by]
    twbad = 0
    kinds = Counter()
    for x in rels:
        if x["a"] in by and x["b"] in by:
            ga, gb = by[x["a"]]["gold"], by[x["b"]]["gold"]
            kinds[x["type"]] += 1
            if x["type"] == "complement" and ga == gb:
                twbad += 1
            elif x["type"] == "equiv" and ga != gb:
                twbad += 1
            elif x["type"] not in ("complement", "equiv", "inv"):
                twbad += 1
    units = cs.units_of(rows, rels)
    sizes = Counter(len(u) for u in units)
    seen, dups = set(), 0
    for r in rows:
        k = json.dumps([r.get("state"), r.get("instructions"), r.get("options"), r.get("card")], sort_keys=True)
        dups += k in seen
        seen.add(k)
    import mix_c2  # noqa: E402
    ho_rep: dict = {}
    refused = mix_c2.refuse_held_out(ilog, {FAM: rows}, ho_rep)
    shard_meta = json.loads((sel.R1_SHARDS / FAM / "shards.json").read_bytes().decode("utf-8"))
    ilog.record(sel.R1_SHARDS / FAM / "shards.json")
    shard_ok = shard_meta.get("candidates_sha256") == shas["candidates_sha256"]
    sd = sel.R1_SHARDS / FAM
    pg, view = sel.load_c1(ilog, rows, sd / f"labels_{c2io.C1}", sd)
    r1sel = ilog.json(sel.R1_SELECT / f"select_{FAM}.json")
    # the independent line count of the candidates (split on "\n" only) must equal the loader's row count
    n_lines, n_rel_lines = count_jsonl_rows(cand), count_jsonl_rows(relf)
    live = {"candidate_problems": cp, "rows": len(rows), "relations": len(rels), "relation_kinds": dict(kinds),
            "relation_endpoint_missing": len(miss), "g_tw_violations": twbad, "unit_sizes": dict(sizes),
            "exact_duplicate_rows": dups, "formats1_refuse_held_out_strict": ho_rep["fmt1_refuse_held_out"][FAM],
            "formats1_refused": refused, "shard_set_candidates_sha_equal": shard_ok,
            "c1_labels": len(pg), "c1_labels_missing": sum(1 for r in rows if r["id"] not in pg), "c1_view": view,
            "round1_select_candidates_sha_equal": r1sel.get("candidates_sha256") == shas["candidates_sha256"],
            "gold": dict(Counter(r["gold"] for r in rows)), "sampler": dict(Counter((r.get("meta") or {}).get("sampler") for r in rows)),
            "jsonl_lines_candidates": n_lines, "jsonl_lines_relations": n_rel_lines}
    rec["live_checks"] = live
    if cp or miss or twbad or dups or refused or not shard_ok or live["c1_labels_missing"] or not live["round1_select_candidates_sha_equal"]:
        problems.append(f"live checks failed: {live}")
    if n_lines != len(rows) or n_rel_lines != len(rels):
        problems.append(f"JSONL line counts (split on \\n) {n_lines}/{n_rel_lines} != loader rows {len(rows)}/{len(rels)}")
    if any(k not in (1, 2, 3) for k in sizes):
        problems.append(f"units not whole / too large: sizes {dict(sizes)}")

    # ---- R3: the selectable pool
    pool, prel, info = sel.carry_pool(FAM, rows, rels, set(r1sel["selected_ids"]))
    rec["selectable_pool"] = info | {"target": c2io.CARRY[FAM], "units": len(cs.units_of(pool, prel)),
                                     "room_for_g13_drops_rows": len(pool) - c2io.CARRY[FAM]}
    if len(pool) < c2io.CARRY[FAM]:
        problems.append(f"selectable pool {len(pool)} < target {c2io.CARRY[FAM]}")

    # ---- R4: the binding gates re-derived from their gate-output files at the unchanged bars (A66 a)
    reader = GateReader(F5)
    stats = live_stats(rows, rels, units, reader, shas["candidates_sha256"], f["mixdev"])
    stats["dups"] = dups
    reader.record(ROW_FILES["qc_sample"])
    ilog.record(f["mixdev"])
    gate_rec, gate_problems = rederive_gates(reader, stats, gates1)
    rec["gates_rederived"] = gate_rec
    rec["gate_files_sha256"] = dict(sorted(reader.files.items()))
    rec["gate_bars"] = {"G6": G6_BAR, "G15_token_cap": G15_TOKEN_CAP, "G5_max_ambiguous": G5_MAX_AMBIGUOUS,
                        "G10_B_target_rows": G10_B_TARGET_ROWS, "G11_max_sampler_rows": G11_MAX_SAMPLER_ROWS,
                        "G11_min_packs": G11_MIN_PACKS, "G11_two_pct": G11_TWO_PCT, "source": "c_src/F5/qc/g*.py, solverB (unchanged)"}
    rec["sealed_check"] = {"re_derived": False, "round1_boolean": (gates1.get("sealed_check") or {}).get("pass"),
                           "reason": "its file is on the never-open side; carried from the round-1 record (sha-bound above) and "
                                     "listed in gates_pending"}
    problems += [f"gate re-derivation: {x}" for x in gate_problems]

    ok = not problems
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    rec |= {"pass": ok, "passed_utc": now.isoformat() if ok else None,
            "fix_iterations": 0,
            "fix_iterations_note": "C2 re-gate fix iterations (spec 5.3): none, the pool is unchanged since the round-1 pass; "
                                   "round-1 repair history (A32 regen, wording fix, G10 fix) is in c_src/F5/qc/QC_REPORT.json",
            "reasons_not_passed": problems,
            "files": {cand.name: {"sha256": shas["candidates_sha256"], "rows": len(rows)},
                      relf.name: {"sha256": shas["relations_sha256"], "rows": len(rels)}},
            "mixdev": {"mixdev_S5.jsonl": {"sha256": sha256_file(f["mixdev"]), "rows": stats["mixdev_rows"],
                                           "layout": "round-1 (carry-over)"}},
            "inputs_sha256": dict(sorted(ilog.entries.items())),
            "gates_pending": GATES_PENDING,
            "crowd": "round-1 C1 labels (data/c_crowd_r1_shards/F5/labels_q35_4b_main500k, one view of C1, same settings; "
                     "label and shard files are sha-bound in inputs_sha256); no new read (the candidates file is "
                     "byte-identical to the one that was read)"}
    print(json.dumps({k: rec[k] for k in ("pass", "passed_utc", "fix_iterations", "reasons_not_passed", "files")}, indent=1))
    print(json.dumps(rec["live_checks"], default=str)[:1800])
    print(json.dumps(rec["selectable_pool"]))
    print(json.dumps({g: v["pass"] for g, v in gate_rec.items()}))
    if a.write:
        res = write_record(rec, OUTQ, BACKUP_DIR, now.strftime("%Y%m%dT%H%M%SZ"))
        probs = mx.qc_binding(json.loads(OUTQ.read_bytes().decode("utf-8")), {cand.name: cand, relf.name: relf})
        print("written", res, "qc_binding", probs)
    else:
        print("dry run: nothing written; would write", OUTQ, "(existing record, if any, is copied to", BACKUP_DIR, "first)")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
