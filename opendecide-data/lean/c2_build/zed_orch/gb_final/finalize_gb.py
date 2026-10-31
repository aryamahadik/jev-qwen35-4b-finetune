"""finalize_gb.py: the GB QC-record writer (Ruling A66 a, 17 Oct 2026). Dry run by default; --write only after a skeptic review and an
orchestrator OK. Modelled on zed_orch/md_final/finalize_md.py.

GB (the routed real-text G-block) has no pre-registered tool that writes QC `pass` / `passed_utc` / `fix_iterations`, so mix admission
(mix_c2.admission) refuses it although its non-G13 gates ran. This tool re-derives every binding non-G13 GB gate from the files on
disk, at the unchanged bars, and only then (with --write) records pass=true. It never loosens a bar, never waives a gate and never
touches any file but data/c2_parts/GB/qc/QC_REPORT.json (a timestamped backup of the old record goes to c2_build/_backup_gb_final/
first). Output is counts, shas and gate names only: no row text.

  cd lean/c2_build && ../../.venv/bin/python -B zed_orch/gb_final/finalize_gb.py            # dry run (default)
  cd lean/c2_build && ../../.venv/bin/python -B zed_orch/gb_final/finalize_gb.py --write    # only after the orchestrator says so

Gates re-derived (all must hold, else no write; the dry run lists every problem):
  files      MANIFEST == candidate / relation / mixdev files on disk; the QC record's recorded shas == disk (mixer.qc_binding);
             MANIFEST input shas (routed_block.jsonl, mixdev_ids.json) == the gblock files
  schema     c2_kit.rows.validate_row (training) clean on every row (meta.licence excepted, as at packaging); c2io.candidate_problems empty
  block      mix_c2.block_rules('GB', rows, loaded=True) empty: rows <= 15,000, twins <= 5,000, no domain > 20%, every yes/no card of
             >= 10 rows inside the 40-60% yes band (A42-D 5.5)
  labels     A39 / A42-D 5.1-5.2: the base rows are exactly gblock/route_a42d/routed_block.jsonl, gold == the routed label, routed
             confidence >= 0.80 (Haiku) / >= 0.85 (Opus), and no routed row is in the mixdev; the A39 counts in the QC record equal
             the population / accepted / Opus-finalize files; the 5% Opus audit re-counted (no domain over 6% disagreement) and its
             sampled-vs-read shortfall recorded (A39 audit sampled 565, read 493: 72 never answered; the 6% bar is unchanged)
  routing    A42-D 5.2-5.4 re-derived from route_a42d/classes.jsonl (C1 read of the 18,773 rows): every row's class re-computed from
             its C1 argmax / p (AGREE-HIGH p >= 0.9, AGREE-LOW p < 0.9, DISAGREE); the 35% AGREE-HIGH anchors re-drawn (seed 20261013,
             stratified card x label) and equal to the stored anchors; every routed row sits in a consistent class/source pair
             (anchor / agree-low / opus-kept / opus_disagree at conf >= 0.85); no mixdev or A39-dropped row is routed; the funnel counts
             re-counted from the class file equal routed_block_stats.json and the QC record
  mixdev     1,650 rows, 150 per domain, ids = population mixdev flags = mixdev_ids.json, disjoint from the candidates by id, by
             group / call id and by text
  source     A39 (b) source-level gates, cached upstream, sha-bound here: gblock/checks/denylist_verdicts_final.json (11 datasets, 0
             hits, 0 taint, canonical, bound to the deny-list / query / program shas), c1_overlap.json (every domain's list empty),
             final_sources.json and summary.json agree on the domains; >= 8 domains on the rows; every row's text licence is recorded
             and permissive. The files' sha256 go into the record (finalize.inputs_sha256); a changed file is a new run
  programs   A42-D 7.3 / A43 f / A48 h per-twin program checks re-run on every live twin with negtwins.rtw.twin_checks (check_pair:
             exactly one predicate changed, edit-site, modal scope, pattern class, polarity A / B); the trained catalogue has >= 300
  G-TW       mix_c2-side recompute on the live twin rows: negtwins.checks.g_tw 100%, every twin has its base in the rows, every twin
             pattern is in the frozen trained catalogue and none is a pattern the pooled audit dropped, relations == twin links
  A60        the pooled spec 3.18 shares recomputed over the complement twins of GB + MD + RTW on disk (mix_c2.a60_shares): no problem,
             counts equal the recorded pooled_after; the hold file's sha / row counts equal the A60 record; kept + held == rows_before
  audit      the pooled-audit record (QC negtwin_audit and negtwins/stage3/POOLED_AUDIT_REPORT.json) names the same twin / row counts
             as the file; the QC negtwin_gates.g_tw pass is recorded
  crowd      reads/verify_crowd_labels.check_family('GB'): exactly one C1 label per candidate row, rows identical to the rows read, one
             C1 view, every probability set a distribution
  admission  the would-be record passes mix_c2.admission('GB', ...) (pass, passed_utc before the cutoff, fix_iterations <= max, shas)

negtwin_gates in the record is REFRESHED from the live recompute (101 twins today); the packaged block (224 twins, W6 rebalance numbers)
is kept verbatim under negtwin_gates_superseded with the 224 -> 197 -> 101 history, never silently dropped.

Still pending after --write (never waived; listed in gates_pending): G13 decontamination on the candidates (incl. the OHS-AC path) and
the C1 crowd selection. Mix admission still needs the binding G13 log and the selection record (A66 c).
fix_iterations: the packaged record's count (0) is carried unchanged; this tool does not change it.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime
import hashlib
import json
import math
import os
import random
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent.parent
sys.path.insert(0, str(BUILD))
sys.path.insert(0, str(BUILD / "reads"))
import c2io  # noqa: E402
import c2_select as sel  # noqa: E402
import mix_c2  # noqa: E402
import verify_crowd_labels as vcl  # noqa: E402
from c2_kit import rows as R  # noqa: E402
from negtwins import checks as K  # noqa: E402
from negtwins import core as NC  # noqa: E402
from negtwins import frozen as FZ  # noqa: E402
from negtwins import rtw as RTW  # noqa: E402

AUDIT_MAX_DISAGREE = 0.06                    # A39: re-read a domain's Haiku-accepted rows if the 5% audit disagreement exceeds 6%
HAIKU_MIN_CONF, OPUS_MIN_CONF = 0.80, 0.85   # A39: Haiku accepted conf >= 0.80, Opus kept conf >= 0.85
MIXDEV_ROWS, MIXDEV_PER_DOMAIN = 1650, 150
P_HIGH, KEEP_HIGH, ROUTE_SEED = 0.90, 0.35, 20261013   # A42-D 5.2 / 5.3 (and the routing seed of gblock/tools/route_a42d.py)
ANCHOR_RATE_TOL = 0.01                       # the realised anchor rate may differ from 35% by the per-stratum rounding only
MIN_DOMAINS, MIN_PATTERNS = 8, 300           # A39 b: at least 8 domains; A42-D 7.3 / A48: at least 300 trained patterns
SCHEMA_EXCEPT = {"meta.licence"}             # real-text rows carry the upstream licence (as at packaging, package_gb.py)
PENDING = ["G13 decontamination on the candidates (A42-D 5.7 / 8.6; g13_c2.py candidates --block GB, incl. the OHS-AC path; orchestrator batch): drops are whole units",
           "C1 crowd selection for GB (c2_select.py select --fam GB --exclude-ids <complete G13 log>; target 15,000, short is allowed)"]


class Paths:
    """Every file the tool reads or writes; tests point it at a fixture tree."""

    def __init__(self, parts=None, shards=None, gblock=None, stage3=None, backup=None, denylist_program=None):
        self.parts = Path(parts or c2io.C2_PARTS)
        self.shards = Path(shards or sel.SHARDS)
        self.gblock = Path(gblock or BUILD / "gblock")
        self.stage3 = Path(stage3 or BUILD / "negtwins" / "stage3")
        self.backup = Path(backup or BUILD / "_backup_gb_final")
        gb = self.parts / "GB"
        self.cand, self.rel = gb / "out" / c2io.CAND, gb / "out" / c2io.REL
        self.man, self.qc = gb / "out" / "MANIFEST.json", gb / "qc" / "QC_REPORT.json"
        self.mixdev = gb / "out" / "mixdev_S5.jsonl"
        self.route = self.gblock / "route_a42d"
        self.label = self.gblock / "label"
        self.checks = self.gblock / "checks"
        self.denylist_program = Path(denylist_program or BUILD.parent / "c_src" / "common" / "denylist.py")


def sha_b(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha(p: Path) -> str:
    return sha_b(Path(p).read_bytes())


def jl(p: Path) -> list:
    # split on "\n" only: str.splitlines() also breaks on U+2028 / U+0085 / \x0b inside a JSON string (real-text rows carry them)
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").split("\n") if x.strip()]


def jf(p: Path):
    return json.loads(Path(p).read_text(encoding="utf-8"))


# ------------------------------------------------------------------------------------------------ pure checks (each returns problems)

def label_problems(base, routed, pop, accepted_n, opus_kept_n, mixdev_ids, qc_labels, qc_audit) -> tuple[dict, list]:
    """A39 / A42-D 5.1-5.2 on the base rows. base: non-twin candidate rows; routed: routed_block.jsonl rows; pop: population.jsonl rows."""
    p, rep = [], {}
    rb = {r["id"]: r for r in routed}
    if len(rb) != len(routed):
        p.append("routed_block.jsonl has duplicate ids")
    ids = {r["id"] for r in base}
    if ids != set(rb):
        p.append(f"base rows != routed block ({len(ids - set(rb))} not routed, {len(set(rb) - ids)} routed but absent)")
    bad_gold = bad_conf = bad_card = 0
    for r in base:
        x = rb.get(r["id"])
        if x is None:
            continue
        want = (1 if x["label"] == "yes" else 0 if x["label"] == "no" else None) if r["qtype"] == "noul" else x["label"]
        if want is None or r["gold"] != want or isinstance(r["gold"], bool):
            bad_gold += 1
        need = OPUS_MIN_CONF if str(x["source"]).startswith("opus") else HAIKU_MIN_CONF
        if not isinstance(x.get("conf"), (int, float)) or x["conf"] < need - 1e-9:
            bad_conf += 1
        if (r.get("meta") or {}).get("card_id") != x["card_id"] or r["qtype"] != x["qtype"]:
            bad_card += 1
    for n, k in ((bad_gold, "gold differs from the routed label"), (bad_conf, "routed confidence under its A39 floor"),
                 (bad_card, "card / qtype differs from the routed row")):
        if n:
            p.append(f"{n} base rows: {k}")
    pb = {r["id"]: r for r in pop}
    if len(pb) != len(pop):
        p.append("population.jsonl has duplicate ids")
    miss = [i for i in rb if i not in pb or pb[i]["status"] not in ("haiku_accepted", "opus_kept") or pb[i]["mixdev"]]
    if miss:
        p.append(f"{len(miss)} routed rows are not kept-pool rows outside the mixdev")
    if set(rb) & mixdev_ids:
        p.append(f"{len(set(rb) & mixdev_ids)} routed rows are in the mixdev")
    st = Counter(r["status"] for r in pop)
    rep["population"] = {"rows": len(pop), "haiku_accepted": st["haiku_accepted"], "opus_kept": st["opus_kept"], "a39_dropped": st["a39_dropped"]}
    if st["haiku_accepted"] != accepted_n:
        p.append(f"population haiku_accepted {st['haiku_accepted']} != accepted_haiku.jsonl rows {accepted_n}")
    if st["opus_kept"] != opus_kept_n:
        p.append(f"population opus_kept {st['opus_kept']} != opus_finalize_A39 opus_kept {opus_kept_n}")
    got = {"haiku_accepted_conf_ge_0.80": st["haiku_accepted"], "opus_kept_conf_ge_0.85": st["opus_kept"],
           "a39_dropped_low_conf": st["a39_dropped"], "labelled_pool": st["haiku_accepted"] + st["opus_kept"]}
    for k, v in got.items():
        if (qc_labels or {}).get(k) != v:
            p.append(f"QC A39_labels.{k} {(qc_labels or {}).get(k)} != re-derived {v}")
    aud = [r for r in pop if "opus_audit_label" in r]
    dis = [r for r in aud if r["label"] != r["opus_audit_label"]]
    dom = Counter(r["domain"] for r in aud)
    ddis = Counter(r["domain"] for r in dis)
    worst = max((ddis[d] / dom[d] for d in dom), default=0.0)
    rep["audit"] = {"read": len(aud), "disagreements": len(dis), "worst_domain_rate": round(worst, 4)}
    if worst > AUDIT_MAX_DISAGREE:
        p.append(f"5% Opus audit: a domain disagrees {worst:.3f} > {AUDIT_MAX_DISAGREE}")
    if (qc_audit or {}).get("audit_items_read") != len(aud) or (qc_audit or {}).get("disagreements") != len(dis):
        p.append(f"QC A39_5pct_opus_audit ({(qc_audit or {}).get('audit_items_read')} read, {(qc_audit or {}).get('disagreements')} disagreements) "
                 f"!= re-derived ({len(aud)}, {len(dis)})")
    return rep, p


def mixdev_problems(dev, cand_ids, pop, mixdev_ids_json, man_dev) -> tuple[dict, list]:
    p = []
    dev_ids = [r["id"] for r in dev]
    rep = {"rows": len(dev), "domains": len(Counter(pop[i]["domain"] for i in dev_ids if i in pop))}
    if len(dev) != MIXDEV_ROWS or len(set(dev_ids)) != len(dev_ids):
        p.append(f"mixdev has {len(dev)} rows ({len(set(dev_ids))} distinct), want {MIXDEV_ROWS}")
    if set(dev_ids) & cand_ids:
        p.append(f"{len(set(dev_ids) & cand_ids)} mixdev ids are among the candidates")
    flagged = {i for i, r in pop.items() if r.get("mixdev")}
    if set(dev_ids) != flagged:
        p.append("mixdev ids != the population's mixdev flags")
    listed = {i for v in (mixdev_ids_json.get("ids") or {}).values() for i in v} if isinstance(mixdev_ids_json.get("ids"), dict) else set(mixdev_ids_json.get("ids") or [])
    if set(dev_ids) != listed:
        p.append("mixdev ids != mixdev_ids.json")
    per = Counter(pop[i]["domain"] for i in dev_ids if i in pop)
    if any(v != MIXDEV_PER_DOMAIN for v in per.values()) or sum(per.values()) != len(dev_ids):
        p.append(f"mixdev is not {MIXDEV_PER_DOMAIN} per domain: {dict(per)}")
    if any((r.get("meta") or {}).get("sampler") != "S5" or (r.get("meta") or {}).get("dev_only") is not True for r in dev):
        p.append("a mixdev row is not an S5 / dev_only row")
    if man_dev is not None and man_dev.get("rows") != len(dev):
        p.append("MANIFEST mixdev row count differs from the file")
    return rep, p


def twin_problems(rows, rels, trained_pids, dropped_patterns) -> tuple[dict, list]:
    p = []
    tw = [r for r in rows if (r.get("meta") or {}).get("twin_of")]
    by = {r["id"]: r for r in rows}
    pairs = [(by[r["meta"]["twin_of"]], r) for r in tw if r["meta"]["twin_of"] in by]
    gtw = K.g_tw(pairs)
    if len(pairs) != len(tw) or not gtw["pass"]:
        p.append(f"G-TW: {len(pairs)}/{len(tw)} twins with a base in the rows, {gtw['violations']} violations")
    pats = {(r["meta"].get("negtwin") or {}).get("pattern") for r in tw}
    if None in pats:
        p.append("a twin row has no meta.negtwin.pattern")
    off = pats - set(trained_pids) - {None}
    if off:
        p.append(f"{len(off)} twin patterns outside the frozen trained catalogue")
    gone = pats & set(dropped_patterns)
    if gone:
        p.append(f"{len(gone)} twin patterns are patterns the pooled audit dropped")
    if {x.get("b") for x in rels} != {r["id"] for r in tw} or len(rels) != len(tw) or any(x.get("a") not in by or x.get("b") not in by for x in rels):
        p.append("relations are not exactly the twin links inside the rows")
    elif any(by[x["b"]]["meta"]["twin_of"] != x["a"] for x in rels):
        p.append("a relation edge does not match the twin's base")
    return {"twins": len(tw), "g_tw": {k: gtw[k] for k in ("n_pairs", "violations", "pass")}}, p


def mixdev_overlap_problems(dev, rows) -> tuple[dict, list]:
    """The mixdev is never trained: no candidate shares its group id, call id or text (state) with a mixdev row."""
    p = []
    g_d, c_d, t_d = ({r.get(k) for r in dev} - {None} for k in ("group_id", "call_id", "state"))
    g_c, c_c, t_c = ({r.get(k) for r in rows} - {None} for k in ("group_id", "call_id", "state"))
    shared = {"group_id": len(g_d & g_c), "call_id": len(c_d & c_c), "text": len(t_d & t_c)}
    for k, n in shared.items():
        if n:
            p.append(f"{n} mixdev {k} values are also in the candidates")
    if any(not r.get("state") for r in dev) or any(not r.get("group_id") for r in dev):
        p.append("a mixdev row has no text or group id (the disjointness cannot be shown)")
    return {"shared_with_candidates": shared}, p


def keep_anchors(high_rows: list, frac: float = KEEP_HIGH, seed: int = ROUTE_SEED) -> set:
    """A42-D 5.3, re-implemented from its definition (gblock/tools/route_a42d.py keep_anchors): in every (card, label) stratum keep
    floor(0.35 n + u) rows, u ~ U[0,1) seeded by the stratum; rows are taken by lowest sha256 rank."""
    strata = defaultdict(list)
    for r in high_rows:
        strata[(r["card_id"], r["label"])].append(r["id"])
    kept = set()
    for key in sorted(strata):
        ids = sorted(strata[key], key=lambda c: hashlib.sha256(f"{seed}|anchor|{c}".encode()).hexdigest())
        rng = random.Random(f"{seed}|anchor|{key[0]}|{key[1]}")
        kept |= set(ids[:min(len(ids), int(math.floor(frac * len(ids) + rng.random())))])
    return kept


ROUTE_PAIRS = {"haiku_agree_high_anchor": "AGREE-HIGH", "haiku_agree_low": "AGREE-LOW", "opus_a39": "OPUS_KEPT", "opus_disagree": "DISAGREE"}


def routing_problems(classes, pop, routed, stats_funnel, qc_routing) -> tuple[dict, list]:
    """A42-D 5.2-5.4 re-derived from the C1-read class file. classes: route_a42d/classes.jsonl rows; pop: population.jsonl rows;
    routed: routed_block.jsonl rows; stats_funnel: routed_block_stats.json funnel; qc_routing: QC gates_run.A42D_5_1_5_2_routing."""
    p = []
    cb, pb, rb = {r["id"]: r for r in classes}, {r["id"]: r for r in pop}, {r["id"]: r for r in routed}
    if len(cb) != len(classes):
        p.append("classes.jsonl has duplicate ids")
    if set(cb) != set(pb):
        p.append(f"classes.jsonl ids != population ids ({len(set(cb) - set(pb))} extra, {len(set(pb) - set(cb))} missing)")
    drift = sum(1 for i, c in cb.items() if i in pb and any(c.get(k) != pb[i].get(k) for k in ("status", "mixdev", "label", "card_id", "domain", "qtype", "conf")))
    if drift:
        p.append(f"{drift} class rows differ from the population on status / mixdev / label / card / domain / qtype / conf")
    # (1) every class re-computed from the C1 read (5.2); the C1 read of an Opus-labelled or dropped row is report-only
    bad_cls = 0
    for c in classes:
        am_ok = c.get("c1_argmax") == c.get("label")
        pl = c.get("c1_p_label")
        if c.get("mixdev"):
            want = "MIXDEV"
        elif c.get("status") == "opus_kept":
            want = "OPUS_KEPT"
        elif c.get("status") == "a39_dropped":
            want = "A39_DROPPED"
        elif am_ok and isinstance(pl, (int, float)) and pl >= P_HIGH:
            want = "AGREE-HIGH"
        elif am_ok:
            want = "AGREE-LOW"
        else:
            want = "DISAGREE"
        bad_cls += c.get("class") != want
    if bad_cls:
        p.append(f"{bad_cls} rows carry a class other than the one their C1 read and status give (A42-D 5.2)")
    cnt = Counter(c.get("class") for c in classes)
    # (2) the 35% anchors (5.3), re-drawn
    high = [c for c in classes if c.get("class") == "AGREE-HIGH"]
    stored = {c["id"] for c in high if c.get("anchor_kept")}
    drawn = keep_anchors(high)
    if stored != drawn:
        p.append(f"AGREE-HIGH anchors differ from the seeded draw ({len(stored - drawn)} stored but not drawn, {len(drawn - stored)} drawn but not stored)")
    if any(c.get("anchor_kept") for c in classes if c.get("class") != "AGREE-HIGH"):
        p.append("a row outside AGREE-HIGH is marked as an anchor")
    rate = len(stored) / len(high) if high else 0.0
    if abs(rate - KEEP_HIGH) > ANCHOR_RATE_TOL:
        p.append(f"AGREE-HIGH anchors kept {len(stored)} of {len(high)} ({rate:.3f}), not 35% (A42-D 5.3)")
    # (3) the routed rows: class / source pairs, labels, confidences, no mixdev and no dropped row
    nroute = {src: 0 for src in ROUTE_PAIRS}
    differs, bad = 0, Counter()
    for r in routed:
        c = cb.get(r["id"])
        if c is None:
            bad["routed row not in classes.jsonl"] += 1
            continue
        want = ROUTE_PAIRS.get(r.get("source"))
        if want is None or c.get("class") != want or c.get("mixdev"):
            bad["routed row in a class its source does not allow (or a mixdev row)"] += 1
            continue
        nroute[r["source"]] += 1
        if r["source"] == "haiku_agree_high_anchor" and not c.get("anchor_kept"):
            bad["routed AGREE-HIGH row that is not an anchor"] += 1
        if r["source"] == "opus_disagree":
            differs += r["label"] != c["label"]
            if not isinstance(r.get("conf"), (int, float)) or r["conf"] < OPUS_MIN_CONF - 1e-9:
                bad["kept DISAGREE row under Opus confidence 0.85"] += 1
        elif r["label"] != c["label"] or r.get("conf") != c.get("conf"):
            bad["routed row relabelled or with another confidence than the classed row"] += 1
    p += [f"routing: {n} x {k}" for k, n in bad.items()]
    # (4) the funnel, re-counted from the class file
    f = stats_funnel or {}
    got = {"a39_dropped_stay_dropped": cnt["A39_DROPPED"], "agree_high_total": cnt["AGREE-HIGH"], "agree_high_anchor_kept": len(stored),
           "agree_low_kept": cnt["AGREE-LOW"], "disagree_total": cnt["DISAGREE"], "mixdev_held_out": cnt["MIXDEV"], "opus_a39_kept": cnt["OPUS_KEPT"]}
    for k, v in got.items():
        if f.get(k) != v:
            p.append(f"funnel.{k} {f.get(k)} != re-counted from classes.jsonl {v}")
    out_dis = f.get("disagree_kept_opus_label", 0) + sum((f.get("disagree_dropped_at_opus") or {}).values()) + f.get("disagree_unread_dropped", 0)
    if out_dis != cnt["DISAGREE"]:
        p.append(f"DISAGREE rows {cnt['DISAGREE']} != kept + dropped at Opus + unread in the funnel ({out_dis})")
    if f.get("disagree_kept_label_differs_from_haiku", 0) < differs:
        p.append("more routed DISAGREE rows carry an Opus label that differs from Haiku's than the funnel records")
    if (qc_routing or {}).get("c1_read_population") != len(classes) or (qc_routing or {}).get("mixdev_held_out") != cnt["MIXDEV"]:
        p.append("QC A42D_5_1_5_2_routing population / mixdev counts != classes.jsonl")
    return {"classes": dict(cnt), "population": len(classes), "anchors_kept": len(stored), "anchors_of": len(high), "anchor_rate": round(rate, 4),
            "routed_by_source": nroute, "routed_disagree_label_differs_from_haiku": differs}, p


def audit_disclosure(pop, counts) -> tuple[dict, list]:
    """The A39 5% Opus audit: sampled vs read. The 6% per-domain bar applies to the rows read (label_problems); the unanswered rest is recorded."""
    p = []
    samp = [r for r in pop if r.get("haiku_audit")]
    read = [r for r in samp if "opus_audit_label" in r]
    if any("opus_audit_label" in r and not r.get("haiku_audit") for r in pop):
        p.append("a row carries an Opus audit label but is not in the audit sample")
    if any(r.get("status") != "haiku_accepted" for r in samp):
        p.append("the audit sample holds a row that is not a Haiku-accepted row")      # (mixdev rows may be in it: the audit ran before the mixdev draw)
    if (counts or {}).get("audit_rows") != len(samp):
        p.append(f"counts.json audit_rows {(counts or {}).get('audit_rows')} != {len(samp)} sampled rows in the population")
    if (counts or {}).get("opus_audit_items_read") != len(read):
        p.append(f"counts.json opus_audit_items_read {(counts or {}).get('opus_audit_items_read')} != {len(read)} rows with an audit label")
    acc = sum(1 for r in pop if r.get("status") == "haiku_accepted")
    dom_s, dom_r = Counter(r["domain"] for r in samp), Counter(r["domain"] for r in read)
    return {"sampled": len(samp), "read": len(read), "never_answered": len(samp) - len(read), "sampled_rows_later_in_mixdev": sum(1 for r in samp if r.get("mixdev")),
            "haiku_accepted_rows": acc,
            "sampled_share": round(len(samp) / max(1, acc), 4), "read_share": round(len(read) / max(1, acc), 4),
            "per_domain_sampled_read": {d: [dom_s[d], dom_r[d]] for d in sorted(dom_s)},
            "disclosure": "the audit sampled 5% per domain; the rows not answered by Opus were not read, so the audit covers the read share; the 6% bar is applied to the rows read, unchanged"}, p


def program_problems(rows, trained, pairs, check=None, min_patterns: int = MIN_PATTERNS) -> tuple[dict, list]:
    """A42-D 7.3 / A43 f / A48 h on every live twin: negtwins.rtw.twin_checks(base core, twin core, pattern, pairs) must be empty
    (check_pair, bad_edit_site, the modal-scope and class checks, polarity A / B). The trained catalogue must hold >= 300 patterns."""
    check = check or RTW.twin_checks
    p = []
    by, byp = {r["id"]: r for r in rows}, {x.pid: x for x in trained}
    n = unparsed = missing = 0
    fails = Counter()
    for r in rows:
        if not (r.get("meta") or {}).get("twin_of"):
            continue
        b = by.get(r["meta"]["twin_of"])
        pat = byp.get(((r["meta"].get("negtwin") or {}).get("pattern")))
        cb, ct = (NC.split_instruction(b["instructions"]), NC.split_instruction(r["instructions"])) if b else (None, None)
        if b is None or pat is None:
            missing += 1
            continue
        if not cb or not ct:
            unparsed += 1
            continue
        n += 1
        bad = check(cb[1], ct[1], pat, pairs)
        if bad:
            fails[str(bad[0])[:48]] += 1
    nfail = sum(fails.values())
    if missing:
        p.append(f"{missing} twins have no base row or no pattern in the trained catalogue (program checks cannot run)")
    if unparsed:
        p.append(f"{unparsed} twin or base instructions do not split into preamble and core")
    if nfail:
        p.append(f"{nfail} of {n} twins fail the program checks (A42-D 7.3 / A48 h): {dict(fails.most_common(5))}")
    if len(trained) < min_patterns:
        p.append(f"the trained catalogue has {len(trained)} patterns < {min_patterns} (A42-D 7.3)")
    return {"twins_checked": n, "failures": nfail, "unparsed": unparsed, "catalogue_patterns": len(trained)}, p


PERMISSIVE = re.compile(r"\b(cc0|cc by|cc by-sa|public domain|pd|odc pddl|pddl|open government licence)\b", re.I)
NON_PERMISSIVE = re.compile(r"by-nc|by-nd|\bnc\b|non-?commercial|no derivatives|all rights reserved|proprietary|unknown", re.I)
VERDICT_ZERO = ("hit", "deny_taint", "no_new_rows", "pass_with_parent_no_new_rows", "ohs3_hit", "sealed_hit")


def source_problems(rows, verdicts, c1o, final_sources, summary, shas, min_domains: int = MIN_DOMAINS) -> tuple[dict, list]:
    """A39 (b) source-level gates. The deny-list verdicts and the C1-overlap check are cached upstream files: they are re-asserted here and
    bound by sha256 to the files they were run on (deny-list, query, program); the licences are checked on the rows themselves."""
    p = []
    doms = Counter(r.get("domain") or (r.get("meta") or {}).get("domain") for r in rows)
    if None in doms:
        p.append("a row has no domain")
    if len(doms) < min_domains:
        p.append(f"{len(doms)} domains < {min_domains} (A39 b)")
    d = set(doms) - {None}
    v = verdicts or {}
    if v.get("canonical") is not True or v.get("provisional"):
        p.append("deny-list verdicts are not canonical or list provisional entries")
    cn = v.get("counts") or {}
    for k in VERDICT_ZERO:
        if cn.get(k) != 0:
            p.append(f"deny-list counts.{k} is {cn.get(k)}, want 0")
    vd = v.get("verdicts") or {}
    if cn.get("datasets") != len(vd) or cn.get("pass") != len(vd):
        p.append("deny-list counts do not match its verdict entries")
    if not d <= set(vd):
        p.append(f"domains without a deny-list verdict: {sorted(d - set(vd))}")
    badv = [k for k, x in vd.items() if x.get("hit") or x.get("verdict") != "pass" or x.get("taint_hits") or x.get("matches") or x.get("parent_no_new_rows_pass")]
    if badv:
        p.append(f"deny-list verdict not a clean pass for {sorted(badv)}")
    for key, name in (("denylist_sha256", "denylist_built"), ("query_sha256", "denylist_query_final"), ("program_sha256", "denylist_program")):
        if shas.get(name) is None:
            p.append(f"{name} file missing (its sha256 cannot be bound)")
        elif v.get(key) != shas[name]:
            p.append(f"deny-list verdicts {key} differs from the {name} file on disk")
    co = c1o or {}
    if not d <= set(co):
        p.append(f"domains without a C1-overlap entry: {sorted(d - set(co))}")
    hit = {k: len(x) for k, x in co.items() if x or not isinstance(x, list)}
    if hit:
        p.append(f"C1-overlap lists are not empty: {hit}")
    fs = final_sources or {}
    if not d <= set(fs):
        p.append(f"domains without a final_sources entry: {sorted(d - set(fs))}")
    sm = summary or {}
    if sm.get("problems"):
        p.append("summary.json lists problems")
    if not d <= set(sm.get("per_domain") or {}):
        p.append("summary.json lacks a domain of the rows")
    lic = Counter()
    for r in rows:
        l = (r.get("meta") or {}).get("licence")
        txt = str(l or "").split(" (text)")[0]
        if not l:
            lic["missing"] += 1
        elif NON_PERMISSIVE.search(txt) or not PERMISSIVE.search(txt):
            lic["not permissive"] += 1
    if lic:
        p.append(f"row licences: {dict(lic)} (every row must record a permissive text licence, A39 b)")
    return {"domains": len(doms), "deny_list_datasets": cn.get("datasets"), "deny_list_clean_passes": len(vd) - len(badv),
            "c1_overlap_domains": len(co), "c1_overlap_hits": sum(len(x) for x in co.values() if isinstance(x, list))}, p


def card_band_report(rows) -> dict:
    """Live yes share of every yes/no card (base + twins), the A42-D 5.5 band check as a record (the bar itself is mix_c2.block_rules)."""
    by = defaultdict(list)
    for r in rows:
        if r.get("qtype") == "noul":
            by[(r.get("meta") or {}).get("card_id")].append(r["gold"])
    cards = {c: round(sum(g) / len(g), 3) for c, g in sorted(by.items(), key=lambda x: str(x[0])) if len(g) >= mix_c2.GB_CARD_MIN_ROWS}
    return {"band": list(mix_c2.GB_YES_BAND), "cards_checked": len(cards), "cards_not_checked": len(by) - len(cards),
            "min": min(cards.values(), default=None), "max": max(cards.values(), default=None), "yes_share_per_card": cards}


def refresh_problems(qc: dict, n_twins: int, g_tw: dict) -> list:
    """A record that was already finalized must carry the refreshed negtwin_gates (live twins, g_tw)."""
    if not (qc.get("finalize") or {}).get("tool"):
        return []
    ng = qc.get("negtwin_gates") or {}
    p = []
    if ng.get("twins") != n_twins or (ng.get("g_tw") or {}).get("n_pairs") != g_tw.get("n_pairs") or (ng.get("g_tw") or {}).get("pass") is not True:
        p.append(f"finalized QC negtwin_gates ({ng.get('twins')} twins) != the live recompute ({n_twins} twins)")
    if "negtwin_gates_superseded" not in qc:
        p.append("finalized QC record has no negtwin_gates_superseded")
    return p


def a60_problems(parts: dict, rec: dict, hold_rows, hold_rels, hold_sha) -> tuple[dict, list]:
    """parts: {block: rows} for GB, MD, RTW as on disk. Recompute the pooled spec 3.18 shares and compare with the record."""
    p = []
    allrows = [dict(r, _block=b) for b, rr in parts.items() for r in rr]
    rep, probs = mix_c2.a60_shares(allrows)
    p += probs
    if rep["by_kind"] != ((rec.get("pooled_after") or {}).get("by_kind")):
        p.append(f"recomputed pooled complement counts {rep['by_kind']} != the A60 record {(rec.get('pooled_after') or {}).get('by_kind')}")
    if rec.get("block_rule_problems") or (rec.get("pooled_after") or {}).get("problems"):
        p.append("A60 record carries problems")
    h = rec.get("hold") or {}
    gb_ids = {r["id"] for r in parts["GB"]}
    if h.get("rows_sha256") != hold_sha[0]:
        p.append("hold rows file differs from its recorded sha")
    if h.get("relations_sha256") != hold_sha[1]:
        p.append("hold relations file differs from its recorded sha")
    if h.get("rows") != len(hold_rows) or h.get("relations") != len(hold_rels):
        p.append(f"hold has {len(hold_rows)} rows / {len(hold_rels)} relations, record says {h.get('rows')} / {h.get('relations')}")
    if any(r.get("role") != "complement" or not (r.get("meta") or {}).get("twin_of") for r in hold_rows):
        p.append("a held row is not a complement twin")
    if {r["id"] for r in hold_rows} & gb_ids:
        p.append("a held row is also a candidate")
    if (rec.get("block") or {}).get("rows_before") != len(parts["GB"]) + len(hold_rows):
        p.append(f"rows kept {len(parts['GB'])} + held {len(hold_rows)} != A60 rows_before {(rec.get('block') or {}).get('rows_before')}")
    if (rec.get("block") or {}).get("rows_after") != len(parts["GB"]):
        p.append("A60 rows_after != the candidate file")
    if rec.get("equiv_twins_untouched") is not True:
        p.append("A60 record: equiv_twins_untouched is not true")
    return {"complement_twins": rep["complement_twins"], "shares": rep["shares"], "by_kind": rep["by_kind"], "by_block": rep.get("by_block")}, p


def audit_problems(qc: dict, report: dict, n_rows: int, n_twins: int, pooled_rep: dict) -> list:
    p = []
    na = qc.get("negtwin_audit") or {}
    if na.get("final_twins") != n_twins:
        p.append(f"QC negtwin_audit.final_twins {na.get('final_twins')} != {n_twins} twins in the file")
    if (report.get("final_twins") or {}).get("GB") != n_twins:
        p.append(f"POOLED_AUDIT_REPORT final_twins.GB {(report.get('final_twins') or {}).get('GB')} != {n_twins}")
    if (report.get("final_rows") or {}).get("GB") != n_rows:
        p.append(f"POOLED_AUDIT_REPORT final_rows.GB {(report.get('final_rows') or {}).get('GB')} != {n_rows}")
    if report.get("dry_run") is not False:
        p.append("POOLED_AUDIT_REPORT is a dry run")
    if (report.get("pooled_spec_3_18_shares") or {}).get("by_kind") != pooled_rep["by_kind"]:
        p.append("POOLED_AUDIT_REPORT pooled shares != the recomputed pooled shares")
    for k in ("sampled", "opus_confirmed_errors", "batch_id"):
        if na.get(k) != report.get(k):
            p.append(f"QC negtwin_audit.{k} != POOLED_AUDIT_REPORT.{k}")
    if (qc.get("negtwin_gates") or {}).get("g_tw", {}).get("pass") is not True:
        p.append("QC negtwin_gates.g_tw is not pass")
    return p


# ------------------------------------------------------------------------------------------------ the verdict

@contextlib.contextmanager
def _patched(paths: Paths):
    """check_family / family_inputs read c2io.C2_PARTS and sel.SHARDS; point them at the tool's paths for the call."""
    old = (c2io.C2_PARTS, sel.SHARDS)
    c2io.C2_PARTS, sel.SHARDS = paths.parts, paths.shards
    try:
        yield
    finally:
        c2io.C2_PARTS, sel.SHARDS = old


def input_files(P: Paths) -> dict:
    """Every non-candidate file whose content the verdict relies on (name -> path). Their sha256 go into the record and are re-checked at write."""
    f = {n: P.route / n for n in ("classes.jsonl", "population.jsonl", "routed_block.jsonl", "routed_block_stats.json", "mixdev_ids.json", "counts.json")}
    f.update({"accepted_haiku.jsonl": P.label / "accepted_haiku.jsonl", "opus_finalize_A39.json": P.label / "opus_finalize_A39.json"})
    f.update({n: P.checks / n for n in ("denylist_verdicts_final.json", "c1_overlap.json", "final_sources.json", "summary.json",
                                         "denylist_built.json", "denylist_query_final.json")})
    f["denylist.py"] = P.denylist_program
    f["POOLED_AUDIT_REPORT.json"] = P.stage3 / "POOLED_AUDIT_REPORT.json"
    f["TRAINED_CATALOGUE.json"] = FZ.TRAINED_FILE
    f["c3_hold_a60.jsonl"] = P.parts / "GB" / "out" / "c3_hold_a60.jsonl"
    f["c3_hold_a60.relations.jsonl"] = P.parts / "GB" / "out" / "c3_hold_a60.relations.jsonl"
    return f


def sha_if(p: Path):
    return sha(p) if Path(p).is_file() else None


def verdict(paths: Paths | None = None, now: datetime.datetime | None = None, crowd: bool = True) -> tuple[dict, list]:
    P = paths or Paths()
    qc = jf(P.qc)
    p: list = []

    def ld(fn, path, default):
        """Read one input; a missing or unparsable file is a problem (never a crash, never a silent empty)."""
        try:
            return fn(path)
        except (OSError, ValueError) as e:
            p.append(f"input {Path(path).name}: cannot be read ({type(e).__name__})")
            return default

    rows, rels, man = jl(P.cand), jl(P.rel), jf(P.man)
    dev = jl(P.mixdev)
    inputs = {n: sha_if(f) for n, f in input_files(P).items()}
    # files
    p += [f"manifest: {x}" for x in c2io.manifest_problems("GB", man, {c2io.CAND: (sha(P.cand), len(rows)), c2io.REL: (sha(P.rel), len(rels))})]
    md = (man.get("mixdev") or {}).get("mixdev_S5.jsonl") or {}
    if md.get("sha256") != sha(P.mixdev):
        p.append("manifest: mixdev_S5.jsonl sha256 differs from the MANIFEST's")
    for name, f in (("routed_block.jsonl", P.route / "routed_block.jsonl"), ("mixdev_ids.json", P.route / "mixdev_ids.json")):
        if (man.get("inputs") or {}).get(name) != sha_if(f):
            p.append(f"manifest: input {name} differs from the MANIFEST's sha256")
    p += [f"qc: {x}" for x in mix_c2.mx.qc_binding(qc, {P.cand.name: P.cand, P.rel.name: P.rel})]
    # schema / candidates
    p += [f"candidates: {x}" for x in c2io.candidate_problems("GB", rows)]
    bad = Counter(x[:60] for r in rows for x in R.validate_row(r, training=True) if x not in SCHEMA_EXCEPT)
    if bad:
        p.append(f"schema: validate_row problems {dict(bad)}")
    # block rules
    rep, bp = mix_c2.block_rules("GB", rows, loaded=True)
    p += bp
    # labels / routing / audit
    base = [r for r in rows if not (r.get("meta") or {}).get("twin_of")]
    pop = ld(jl, P.route / "population.jsonl", [])
    popd = {r["id"]: r for r in pop}
    routed = ld(jl, P.route / "routed_block.jsonl", [])
    mj = ld(jf, P.route / "mixdev_ids.json", {})
    accepted = ld(jl, P.label / "accepted_haiku.jsonl", [])
    fin = ld(jf, P.label / "opus_finalize_A39.json", {})
    gr = qc.get("gates_run") or {}
    lrep, lp = label_problems(base, routed, pop, len(accepted), len(fin.get("opus_kept") or []), {r["id"] for r in dev},
                              gr.get("A39_labels"), gr.get("A39_5pct_opus_audit"))
    p += [f"labels: {x}" for x in lp]
    stats = ld(jf, P.route / "routed_block_stats.json", {})
    if (gr.get("A42D_5_1_5_2_routing") or {}).get("funnel") != stats.get("funnel"):
        p.append("labels: QC routing funnel != routed_block_stats.json funnel")
    if stats.get("problems"):
        p.append("labels: routed_block_stats.json lists problems")
    classes = ld(jl, P.route / "classes.jsonl", [])
    rrep, rp = routing_problems(classes, pop, routed, stats.get("funnel"), gr.get("A42D_5_1_5_2_routing"))
    p += [f"routing: {x}" for x in rp]
    arep_, ap_ = audit_disclosure(pop, ld(jf, P.route / "counts.json", {}))
    p += [f"audit-sample: {x}" for x in ap_]
    mrep, mp = mixdev_problems(dev, {r["id"] for r in rows}, popd, mj, md)
    p += [f"mixdev: {x}" for x in mp]
    orep, op = mixdev_overlap_problems(dev, rows)
    p += [f"mixdev: {x}" for x in op]
    # twins: G-TW, catalogue, relations; then the per-twin program checks
    audit = ld(jf, P.stage3 / "POOLED_AUDIT_REPORT.json", {})
    trained_list, pairs = FZ.load_trained()
    trep, tp = twin_problems(rows, rels, {x.pid for x in trained_list}, audit.get("patterns_dropped") or [])
    p += [f"twins: {x}" for x in tp]
    prep, pp = program_problems(rows, trained_list, pairs)
    p += [f"programs: {x}" for x in pp]
    p += [f"twins: {x}" for x in refresh_problems(qc, trep["twins"], trep["g_tw"])]
    # A39 (b) source-level gates (cached upstream, sha-bound)
    shas = {"denylist_built": inputs["denylist_built.json"], "denylist_query_final": inputs["denylist_query_final.json"], "denylist_program": inputs["denylist.py"]}
    srep, sp = source_problems(rows, ld(jf, P.checks / "denylist_verdicts_final.json", {}), ld(jf, P.checks / "c1_overlap.json", {}),
                               ld(jf, P.checks / "final_sources.json", {}), ld(jf, P.checks / "summary.json", {}), shas)
    p += [f"source: {x}" for x in sp]
    # A60 pooled shares over GB + MD + RTW on disk (a missing block file is a problem, never an empty block)
    parts = {"GB": rows}
    for b in ("MD", "RTW"):
        f = P.parts / b / "out" / c2io.CAND
        if f.is_file():
            parts[b] = jl(f)
        else:
            parts[b] = []
            p.append(f"a60: {b} candidates file is missing (the pooled shares cannot be re-derived)")
    hold, holdr = P.parts / "GB" / "out" / "c3_hold_a60.jsonl", P.parts / "GB" / "out" / "c3_hold_a60.relations.jsonl"
    arep, apb = a60_problems(parts, qc.get("a60") or {}, ld(jl, hold, []), ld(jl, holdr, []), (inputs["c3_hold_a60.jsonl"], inputs["c3_hold_a60.relations.jsonl"]))
    p += [f"a60: {x}" for x in apb]
    p += [f"audit: {x}" for x in audit_problems(qc, audit, len(rows), trep["twins"], arep)]
    # crowd label coverage (verify_crowd_labels logic, family GB)
    crep = None
    if not crowd:
        p.append("crowd: label coverage check skipped (a verdict without it can never pass)")
    else:
        try:
            with _patched(P):
                crep = vcl.check_family(c2io.C2InputLog(), "GB")
        except SystemExit as e:               # family_inputs / load_c1 refuse by SystemExit (MANIFEST sha, a shard not done, the view)
            p.append(f"crowd: check refused: {e}")
    if crep is not None:
        p += [f"crowd: {x}" for x in crep["problems"]]
        if crep["labels_for_candidates"] != len(rows) or crep["candidates_without_label"] or crep["candidates_with_other_than_one_label"]:
            p.append(f"crowd: labels for {crep['labels_for_candidates']} of {len(rows)} candidates")
        if crep.get("view_problem"):
            p.append(f"crowd: {crep['view_problem']}")
        if crep.get("rows_with_bad_probability_set"):
            p.append(f"crowd: {crep['rows_with_bad_probability_set']} bad probability sets")
    if qc.get("problems"):
        p.append("QC record lists problems")
    if qc.get("family") != "GB":
        p.append(f"QC record names family {qc.get('family')!r}")
    facts = {"rows": len(rows), "base_rows": len(base), "twins": trep["twins"], "relations": len(rels), "g_tw": trep["g_tw"], "program_checks": prep,
             "block_rules": rep, "caps_ok": not bp, "card_band": card_band_report(rows), "labels": lrep, "routing": rrep, "audit_sample": arep_,
             "mixdev": mrep | orep, "source_gates": srep, "a60_pooled": {k: arep[k] for k in ("complement_twins", "shares", "by_kind")},
             "crowd": ("skipped" if not crowd else "refused" if crep is None else {k: crep[k] for k in ("candidate_rows", "rows_read", "labels", "labels_for_candidates", "surplus_labels_for_rows_no_longer_candidates",
                                           "candidates_without_label", "candidates_with_other_than_one_label", "candidates_changed_since_read", "pg_bins")
                      if k in crep}),
             "candidates_sha256": sha(P.cand), "relations_sha256": sha(P.rel), "manifest_sha256": sha(P.man), "mixdev_sha256": sha(P.mixdev),
             "qc_sha256_before": sha(P.qc), "inputs_sha256": inputs, "tool_sha256": sha(Path(__file__)), "gates_pending_after": PENDING}
    # the record as the mixer will read it, then mix admission
    new = would_be(qc, facts, now)
    files = {P.cand.name: P.cand, P.rel.name: P.rel}
    p += [f"admission: {x}" for x in mix_c2.admission("GB", new, mix_c2.mx.qc_binding(new, files))]
    return {**facts, "problems": p, "would_pass": not p}, p


def would_be(qc: dict, v: dict, now=None) -> dict:
    """The QC record --write would store (a copy; the input is not changed). v: the verdict facts."""
    now = now or datetime.datetime.now(datetime.timezone.utc)
    t = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    new = json.loads(json.dumps(qc))
    fi = qc.get("fix_iterations")
    new["pass"], new["passed_utc"], new["fix_iterations"] = True, t, fi
    new["stage"] = ("final non-G13 gates passed (finalize_gb.py, A66); G13 incl. the OHS-AC path and the crowd selection still pending")
    new["note"] = ("pass=true records gates re-derived by finalize_gb.py (Ruling A66) from the files on disk at unchanged bars: files and shas, schema, block "
                   "rules, labels and the 5% audit, the A42-D 5.2-5.4 routing (classes re-computed, anchors re-drawn), mixdev disjointness, the per-twin "
                   "program checks, G-TW, the A60 pooled shares, the pooled twin audit and the crowd-label coverage. The A39 (b) deny-list and C1-overlap "
                   "verdicts are cached upstream files, re-asserted and bound by sha256 (finalize.inputs_sha256). negtwin_gates is refreshed from the live "
                   "twin rows; the packaged block is kept under negtwin_gates_superseded. gates_run holds the packaging-time record: its counts are "
                   "re-derived and compared here, never edited. None is waived and no bar changed. G13 and the crowd selection are still required for mix admission.")
    new["fix_iterations_basis"] = "carried unchanged from the packaged QC record; finalize_gb.py does not change the count"
    new["gates_pending"] = list(PENDING)
    new["files"] = {c2io.CAND: {"sha256": v["candidates_sha256"], "rows": v["rows"]}, c2io.REL: {"sha256": v["relations_sha256"], "rows": v["relations"]}}
    # negtwin_gates: refreshed from the live recompute; the packaged block (W6 numbers) is kept as history, once
    old = qc.get("negtwin_gates") or {}
    if (qc.get("finalize") or {}).get("tool") and "negtwin_gates_superseded" in qc:
        sup = qc["negtwin_gates_superseded"]
    else:
        sup = dict(old, superseded_by="negtwin_gates (recomputed by finalize_gb.py, A66)",
                   superseded_note=("the packaged tw1 block of 16 Oct (224 twins, yes-share rebalance of the 234 -> 224 step) predates the pooled audit (224 -> 197) "
                                    "and the A60 selection (197 -> 101); gates_run.A42D_5_5_rebalance_and_caps.twin_rebalance_w6 describes the same superseded state"))
    a60b = (qc.get("a60") or {}).get("block") or {}
    new["negtwin_gates_superseded"] = sup
    new["negtwin_gates"] = {"tool": "zed_orch/gb_final/finalize_gb.py (recomputed from candidates_c2.jsonl)", "twins": v["twins"], "g_tw": v["g_tw"],
                            "program_checks": v["program_checks"], "caps_ok": v["caps_ok"], "yes_share_band_live": v["card_band"],
                            "twin_count_history": {"tw1_packaged": sup.get("twins"), "after_pooled_audit": a60b.get("twins_before"), "after_a60_selection": a60b.get("twins_after")},
                            "utc": t}
    new["finalize"] = {"tool": "zed_orch/gb_final/finalize_gb.py", "tool_sha256": v["tool_sha256"], "ruling": "A66", "utc": t,
                       "verdict": {k: v[k] for k in ("rows", "base_rows", "twins", "relations", "g_tw", "program_checks", "block_rules", "labels", "routing",
                                                     "audit_sample", "mixdev", "source_gates", "a60_pooled", "candidates_sha256", "relations_sha256", "mixdev_sha256")},
                       "inputs_sha256": v["inputs_sha256"],
                       "accepted_upstream_inputs": ["gblock/checks/denylist_verdicts_final.json (A39 b deny-list verdicts, run 13 Oct, cached, sha-bound)",
                                                    "gblock/checks/c1_overlap.json (A39 b C1-overlap check, cached, sha-bound)",
                                                    "gblock/route_a42d/classes.jsonl (the C1 read of the 18,773 rows; classes and anchors re-derived here)"]}
    return new


def write(P: Paths, v: dict, now: datetime.datetime | None = None) -> Path:
    """Re-check every sha the verdict stands on, back up the old record, then write the new one (temp file + rename).
    Only P.qc is written (plus the backup copy)."""
    stale = [k for k, f in (("qc_sha256_before", P.qc), ("candidates_sha256", P.cand), ("relations_sha256", P.rel), ("manifest_sha256", P.man),
                            ("mixdev_sha256", P.mixdev)) if sha(f) != v[k]]
    stale += [n for n, f in input_files(P).items() if sha_if(f) != v["inputs_sha256"].get(n)]
    if v["tool_sha256"] != sha(Path(__file__)):
        stale.append("tool")
    if stale:
        raise RuntimeError(f"a file changed since the verdict was computed: {stale}; run the dry run again")
    qc = jf(P.qc)
    new = would_be(qc, v, now)
    stamp = (now or datetime.datetime.now(datetime.timezone.utc)).strftime("%Y%m%dT%H%M%SZ")
    bdir = P.backup / stamp
    bdir.mkdir(parents=True, exist_ok=False)
    shutil.copy2(P.qc, bdir / "QC_REPORT.json")
    if sha(bdir / "QC_REPORT.json") != v["qc_sha256_before"]:
        raise RuntimeError("backup differs from the record")
    text = json.dumps(new, indent=1) + "\n"
    tmp = P.qc.with_name(P.qc.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, P.qc)
    if sha(P.qc) != sha_b(text.encode("utf-8")) or jf(P.qc) != new:
        raise RuntimeError("the written record differs from the intended record")
    return bdir


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args(argv)
    P = Paths()
    v, p = verdict(P)
    print(json.dumps(v, indent=1))
    if not a.write:
        return 0 if not p else 1
    if p:
        print("REFUSED: problems above")
        return 2
    if jf(P.qc).get("pass") is True and (jf(P.qc).get("finalize") or {}).get("tool"):
        print("REFUSED: the record is already finalized (pass=true with a finalize record); not rewritten")
        return 3
    bdir = write(P, v)
    print("written", P.qc, "backup", bdir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
