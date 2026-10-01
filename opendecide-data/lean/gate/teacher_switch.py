"""PREREG_FINAL.md section 6: the teacher switch rule, conditions (c) and (d), computed exactly as written there.

The 2B's teacher switches from 4B-E to the new 4B only if ALL of (a)-(e) hold. This tool computes (c) and (d); it
reports (b) from the ship-look JSON when given one; (a) timing and (e) budget are the owner's call and are only listed.

(c) Dev-select margin: >= +1.0 pp over 4B-E on dev-select = the point difference in micro accuracy over ALL dev-select
    rows of the 9 gate splits (tb_mixtral included; ties and missing = wrong, gate_dev.score), against the FRESH 4B-E
    read of the scoring job (q35_4b_pxE_fresh), never the stored one.
(d) Memorisation check:
    - dev rows: the 3,209 rows of the 9 gate splits whose source is in golden_train: clinc150 881, banking77 559,
      pg_* 1,049, hard_* 208, tb_label_nli 113, hate 399 (hate matched with std_hate + gd_ghc_hate). The per-source
      list is DEV_SEEN_ROWS below; it is re-derived from the data with gate_dev.source_seen (the PREREG 3.2 name rule)
      against golden_train's source names on every run that can see golden_train, and any difference is reported (the
      PREREG list is used regardless).
    - training rows: golden_train rows drawn with seed 0, the same count per (dev) source. The pool of a dev source is
      every golden_train row whose source the name rule matches to it (TRAIN_POOL: hate -> gd_ghc_hate + std_hate as
      PREREG says; hard_affect -> hard_affect + hard_affect_c by the same rule; every other source -> its exact name),
      in file order. Draw: one random.Random(0), dev sources in sorted order, rnd.sample(range(len(pool)), n), indices
      sorted. The rows are copied byte for byte into data/memo4b_train_rows.jsonl (frozen: MEMO_SHA256).
    - pass if accuracy gap (train - dev) <= 2 pp AND gap in mean gold-option probability (train - dev) <= 0.03.
      Accuracy = gate_dev.score (ties wrong). Gold-option probability = p(gold option) as read: yes/no rows p("yes")
      when gold is 1 else p("no"); choice rows p(gold). Both are means over all 3,209 rows of each set, one model.

  python gate/teacher_switch.py build [--replay]                write data/memo4b_train_rows.jsonl (new file only) and
                                                                gate/memo4b_train_rows.json (sha256, counts, pools)
  python gate/teacher_switch.py check CAND REF [--memo-name N] [--ship-json look_ship1.json ...] [--json out.json]
        CAND: the candidate's pred name (its 9 standard dev reads from the gate job, and its read of the memo rows,
        preds_memo4b_train_rows/<N>.jsonl, N = CAND by default). REF: the fresh 4B-E read (q35_4b_pxE_fresh).

The memo read is `od_gcp.py predict --name CAND --splits memo4b_train_rows` with the gate's settings
(gate/teacher_switch_l4.sh). The verdict counts only when every read is a clean od_gcp predict read and the memo read
matches the candidate's dev reads on base, host, GPU, torch, CUDA, revision, chat template, layout and style.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

LEAN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LEAN))
import gate_dev as gd  # noqa: E402

ROOT = LEAN  # --root: another tree with the same data/ and preds_*/ layout (tests)
GOLDEN = "v14_parts/golden_train"
MEMO = "memo4b_train_rows"           # data/<MEMO>.jsonl; od_gcp predict --splits <MEMO> writes preds_<MEMO>/<name>.jsonl
MEMO_MANIFEST = "gate/memo4b_train_rows.json"
MEMO_SEED = 0
# The frozen training-row sample (written once by `build`; `check` refuses any other file)
MEMO_SHA256 = "8ec3029cc93f16a0c0416e4334882c67afc49a1acf40c520d2ba5860d4f24db3"
MEMO_ROWS = 3209

# pre-registered thresholds (PREREG_FINAL.md 6)
SELECT_MIN_PP = 1.0     # (c)
ACC_GAP_MAX_PP = 2.0    # (d) accuracy gap, train - dev, pp
PGOLD_GAP_MAX = 0.03    # (d) mean gold-option probability gap, train - dev
EPS = 1e-9

# PREREG 6 (d) as written: dev family -> rows, total 3,209
PREREG_FAMILIES = {"clinc150": 881, "banking77": 559, "pg_*": 1049, "hard_*": 208, "tb_label_nli": 113, "hate": 399}
# the same set per dev source (23 sources over the 9 gate splits; derived 1 Oct 2026 and checked on every run)
DEV_SEEN_ROWS = {
    "banking77": 559, "clinc150": 881, "hate": 399, "tb_label_nli": 113,
    "pg_conflict": 150, "pg_evidence": 150, "pg_multihop": 150, "pg_numeric": 150, "pg_policy": 150,
    "pg_routing": 150, "pg_temporal": 149,
    "hard_affect": 17, "hard_clinical": 21, "hard_contracts": 18, "hard_evidence_a": 17, "hard_evidence_b": 16,
    "hard_evidence_claims_a": 15, "hard_evidence_claims_b": 14, "hard_nli_a": 19, "hard_nli_b": 17,
    "hard_policy_a": 18, "hard_policy_b": 20, "hard_scales": 16}
# dev source -> the golden_train sources it is matched with (gate_dev.source_seen on golden_train's names)
TRAIN_POOL = {s: [s] for s in DEV_SEEN_ROWS}
TRAIN_POOL.update({"hate": ["gd_ghc_hate", "std_hate"], "hard_affect": ["hard_affect", "hard_affect_c"]})
# L4 time model of the 30 Sep parity read (gate/RUNBOOK_4B_GATE.md 2): 0.057 s per row + 0.10 s per 1K characters
SEC_PER_ROW, SEC_PER_KCHAR = 0.057, 0.10


def stop(msg):
    sys.exit(f"teacher_switch: {msg}")


def family(s):
    return "pg_*" if s.startswith("pg_") else "hard_*" if s.startswith("hard_") else s


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def golden_path():
    return ROOT / f"data/{GOLDEN}.jsonl"


# ------------------------------------------------------------------------------------------------ the dev rows (d)
def dev_counts(splits):
    """dev source -> {split: rows} over the 9 gate splits."""
    out = defaultdict(Counter)
    for sp in splits:
        for l in open(ROOT / f"data/{sp}.jsonl"):
            r = json.loads(l)
            out[r["source"]][sp] += 1
    return {s: dict(v) for s, v in out.items()}


def golden_sources():
    c = Counter()
    with open(golden_path()) as f:
        for l in f:
            c[json.loads(l)["source"]] += 1
    return c


def derive_dev_seen(splits, gsrc=None):
    """Re-derive the dev rows of (d) from the data: dev sources whose name gate_dev.source_seen matches to a
    golden_train source. Returns (derived {source: rows}, pools {source: [train sources]}, issues [text]). issues lists
    every difference from the PREREG text (PREREG_FAMILIES) and from DEV_SEEN_ROWS / TRAIN_POOL; empty = identical."""
    dev = dev_counts(splits)
    gsrc = gsrc if gsrc is not None else golden_sources()
    derived, pools = {}, {}
    for s in sorted(dev):
        m = gd.source_seen(s, set(gsrc))
        if m:
            derived[s], pools[s] = sum(dev[s].values()), sorted(m)
    issues = []
    fam = Counter()
    for s, n in derived.items():
        fam[family(s)] += n
    for f in sorted(set(fam) | set(PREREG_FAMILIES)):
        if fam.get(f, 0) != PREREG_FAMILIES.get(f, 0):
            issues.append(f"family {f}: derived {fam.get(f, 0)} rows, PREREG {PREREG_FAMILIES.get(f, 0)}")
    for s in sorted(set(derived) | set(DEV_SEEN_ROWS)):
        if derived.get(s) != DEV_SEEN_ROWS.get(s):
            issues.append(f"source {s}: derived {derived.get(s)} rows, frozen list {DEV_SEEN_ROWS.get(s)}")
        elif pools.get(s) != sorted(TRAIN_POOL[s]):
            issues.append(f"source {s}: name rule matches {pools.get(s)}, frozen pool {sorted(TRAIN_POOL[s])}")
    if sum(derived.values()) != sum(PREREG_FAMILIES.values()):
        issues.append(f"total: derived {sum(derived.values())} rows, PREREG {sum(PREREG_FAMILIES.values())}")
    return derived, pools, issues


def check_frozen_lists():
    """The hard-coded lists agree with the PREREG text (families and total)."""
    fam = Counter()
    for s, n in DEV_SEEN_ROWS.items():
        fam[family(s)] += n
    assert dict(fam) == PREREG_FAMILIES, (dict(fam), PREREG_FAMILIES)
    assert sum(DEV_SEEN_ROWS.values()) == MEMO_ROWS == 3209
    owners = Counter(k for v in TRAIN_POOL.values() for k in v)
    assert max(owners.values()) == 1, "a golden_train source sits in two pools"


# ------------------------------------------------------------------------------------------------ the training rows (d)
def draw(gsrc_lines):
    """gsrc_lines: dev source -> its pool (golden_train lines in file order). Returns (lines, info), deterministic."""
    rnd = random.Random(MEMO_SEED)
    out, info = [], {}
    for s in sorted(DEV_SEEN_ROWS):
        pool, n = gsrc_lines[s], DEV_SEEN_ROWS[s]
        if len(pool) < n:
            stop(f"{s}: pool has {len(pool)} golden_train rows, {n} needed")
        idx = sorted(rnd.sample(range(len(pool)), n))
        out += [pool[i] for i in idx]
        info[s] = {"rows": n, "pool_sources": TRAIN_POOL[s], "pool_rows": len(pool)}
    return out, info


def pools_from_golden():
    owner = {k: s for s, v in TRAIN_POOL.items() for k in v}
    pools = {s: [] for s in DEV_SEEN_ROWS}
    gsrc = Counter()
    with open(golden_path()) as f:
        for l in f:
            src = json.loads(l)["source"]
            gsrc[src] += 1
            if src in owner:
                pools[owner[src]].append(l.rstrip("\n") + "\n")
    return pools, gsrc


def sample_lines():
    """(lines, info, golden source counts): the seed-0 sample, recomputed from golden_train."""
    pools, gsrc = pools_from_golden()
    lines, info = draw(pools)
    return lines, info, gsrc


def est_minutes(rows):
    sec = sum(SEC_PER_ROW + SEC_PER_KCHAR * (len(r["state"]) + len(r.get("card") or "")) / 1000 for r in rows)
    return sec / 60


def replay_unseen(ids):
    """Info: which of these ids the main run never trained on (the leftover units of its single pass, replayed on CPU
    by replay_steps.py exactly as train_decoder draws batches; no model)."""
    import replay_steps as rs
    cfg = json.loads((LEAN / "runs/q35_4b_main.json").read_text())
    c = rs.stream_cfg(cfg)
    rows_all, _, _, units, _ = rs.load_data(c, ROOT / "data")
    uid = rs.unit_ids(units)
    seen, n = set(), 0
    for _, batch, _, _ in rs.stream(units, c):
        us = {uid[r["id"]] for r in batch}
        if us & seen:
            break
        seen |= us
        n += 1
    dropped = {r["id"] for k, u in enumerate(units) if k not in seen for r in u}
    return {"pass_batches": n, "config_steps": rs.n_steps(len(rows_all), c["batch"], cfg["epochs"]),
            "dropped_rows_in_pass": len(dropped), "sampled_rows_not_trained": sorted(set(ids) & dropped)}


def cmd_build(a):
    check_frozen_lists()
    splits = gd.SPLITS.split(",")
    lines, info, gsrc = sample_lines()
    derived, pools, issues = derive_dev_seen(splits, gsrc)
    print(f"dev rows (PREREG 6 d): {sum(DEV_SEEN_ROWS.values())} over {len(DEV_SEEN_ROWS)} sources; "
          + ", ".join(f"{f} {n}" for f, n in PREREG_FAMILIES.items()))
    if issues:
        print("DERIVATION DIFFERS FROM PREREG (the PREREG list is used):\n   " + "\n   ".join(issues))
    else:
        print(f"re-derived from the data (gate_dev.source_seen vs golden_train's {len(gsrc)} source names): identical "
              f"({sum(derived.values())} rows; hate -> {pools['hate']}; hard_affect -> {pools['hard_affect']})")
    data = "".join(lines).encode()
    sha = hashlib.sha256(data).hexdigest()
    rows = [json.loads(l) for l in lines]
    ids = [r["id"] for r in rows]
    if len(set(ids)) != len(ids):
        stop("duplicate ids in the sample")
    if MEMO_SHA256 != "__UNSET__" and sha != MEMO_SHA256:  # before any write: never leave a non-frozen sample behind
        stop(f"the draw gives sha256 {sha}, the frozen MEMO_SHA256 is {MEMO_SHA256}")
    out = ROOT / f"data/{MEMO}.jsonl"
    if out.exists():
        old = sha256_file(out)
        if old != sha:
            stop(f"{out} exists with sha256 {old}, the draw gives {sha}: never overwritten (new file only)")
        print(f"{out.relative_to(ROOT)} exists and is identical (sha256 {sha})")
    else:
        out.write_bytes(data)
        print(f"wrote {out.relative_to(ROOT)}: {len(rows)} rows, sha256 {sha}")
    qt = Counter(r["qtype"] for r in rows)
    dev_qt = Counter()
    for sp in splits:
        for l in open(ROOT / f"data/{sp}.jsonl"):
            r = json.loads(l)
            if r["source"] in DEV_SEEN_ROWS:
                dev_qt[r["qtype"]] += 1
    man = {"file": f"data/{MEMO}.jsonl", "sha256": sha, "rows": len(rows), "seed": MEMO_SEED,
           "rule": "PREREG_FINAL.md 6 (d): golden_train rows drawn with seed 0, the same count per dev source; pool = "
                   "golden_train rows whose source gate_dev.source_seen matches to the dev source, in file order; "
                   "random.Random(0), dev sources sorted, sample(range(len(pool)), n), indices sorted; lines copied "
                   "byte for byte",
           "golden_train": {"file": f"data/{GOLDEN}.jsonl", "sha256": sha256_file(golden_path()),
                            "rows": sum(gsrc.values())},
           "dev_rows": {"total": sum(DEV_SEEN_ROWS.values()), "families": PREREG_FAMILIES, "by_source": DEV_SEEN_ROWS,
                        "derivation_issues": issues},
           "by_dev_source": info, "qtype_train": dict(qt), "qtype_dev": dict(dev_qt),
           "est_l4_minutes": round(est_minutes(rows), 1)}
    mp = ROOT / MEMO_MANIFEST
    prev = json.loads(mp.read_text()) if mp.exists() else {}
    if a.replay:
        man["training_pass"] = replay_unseen(ids)
    elif prev.get("sha256") == sha and "training_pass" in prev:  # keep the earlier replay of this same sample
        man["training_pass"] = prev["training_pass"]
    if "training_pass" in man:
        tp = man["training_pass"]
        print(f"training pass replay: {tp['pass_batches']} batches (config {tp['config_steps']} steps), "
              f"{tp['dropped_rows_in_pass']} golden_train row(s) never trained; sampled rows among them: "
              f"{len(tp['sampled_rows_not_trained'])}")
    mp.write_text(json.dumps(man, indent=2) + "\n")
    print(f"wrote {MEMO_MANIFEST}; qtype train {dict(qt)} vs dev {dict(dev_qt)}; "
          f"estimated L4 read {man['est_l4_minutes']} min")
    return man


# ------------------------------------------------------------------------------------------------ check (c) and (d)
def p_gold(r, pr):
    if r["qtype"] == "noul":
        return float(pr.get("yes" if r["gold"] == 1 else "no", 0.0))
    return float(pr.get(r["gold"], 0.0))


def summarize(items):
    """items: [(row, probs)] -> {n, acc (%), pgold (mean)}."""
    n = len(items)
    if not n:
        return {"n": 0, "acc": math.nan, "pgold": math.nan}
    return {"n": n, "acc": 100 * sum(gd.score(r, p)[0] for r, p in items) / n,
            "pgold": sum(p_gold(r, p) for r, p in items) / n}


def breakdown(items, key):
    by = defaultdict(list)
    for r, p in items:
        by[key(r)].append((r, p))
    return {k: summarize(v) for k, v in sorted(by.items())}


def memo_rows():
    p = ROOT / f"data/{MEMO}.jsonl"
    if not p.exists():
        stop(f"{p} missing: run `python gate/teacher_switch.py build` first")
    sha = sha256_file(p)
    rows = [json.loads(l) for l in open(p)]
    return rows, sha


def read_check(m, want_perm=None):
    """gate_dev's per-read rules for a clean od_gcp predict read; returns (signature, [issues])."""
    g = gd.pipe_sig(m)
    bad = []
    if g["path"] != "predict":
        bad.append(f"path {g['path']} (not od_gcp predict)")
    if not g["has_load"]:
        bad.append("no load record")
    else:
        if not g["revision"]:
            bad.append("no pinned base revision")
        if not g["chat_template_sha"]:
            bad.append("no chat_template_sha")
        if g["forced"] is None or g["forced"]:
            bad.append(f"forced overrides {g['forced']}")
    nokey = [k for k in ("base", "host", "gpu", "torch", "cuda") if not g[k]]
    if nokey:
        bad.append(f"no {'/'.join(nokey)} recorded")
    if g["tta"]:
        bad.append(f"TTA on ({', '.join(g['tta'])})")
    if g["perm_seed"] != want_perm:
        bad.append(f"perm_seed {g['perm_seed']} (needs {want_perm})")
    return g, bad


def pipeline(cand, ref, memo_name, splits):
    """Issues that keep the check from counting: the 9 dev reads of CAND and REF (gate_dev.pipeline_check: clean
    od_gcp predict reads, one value of base/host/GPU/torch/CUDA/revision/chat template), and the memo read: clean, and
    the same values as CAND's dev reads on those fields plus layout and style."""
    issues, sigs = gd.pipeline_check([cand, ref], gd.std_reads(splits, attacks=False))
    m = gd.read_meta(f"preds_{MEMO}", memo_name)
    if m is None:
        return issues + [f"{memo_name}: no preds_{MEMO}/{memo_name}.meta.json"], None
    g, bad = read_check(m)
    issues += [f"{memo_name} [{MEMO}]: {b}" for b in bad]
    for k in gd.PIPE_MATCH + ("layout", "style"):
        vals = {s[k] for s in sigs.get(cand, {}).values()}
        if len(vals) == 1 and g[k] != next(iter(vals)):
            issues.append(f"{memo_name} [{MEMO}]: {k} {g[k]!r} differs from {cand}'s dev reads ({next(iter(vals))!r})")
    if m.get("rows") not in (None, MEMO_ROWS):
        issues.append(f"{memo_name} [{MEMO}]: meta says {m.get('rows')} rows, not {MEMO_ROWS}")
    return issues, g


def ship_b(paths, cand, ref):
    """(b) from the ship-look JSON(s) of gate_dev --mode ship: the look of CAND vs REF, SHIP and FINAL."""
    for p in paths or []:
        r = json.loads(Path(p).read_text())
        if r.get("mode") == "ship" and r.get("cand") == cand and r.get("ref") == ref:
            return {"look": str(p), "verdict": r.get("verdict"), "final": r.get("final"),
                    "pass": bool(r.get("verdict") == "SHIP" and r.get("final") is True)}
    return None


def select_margin(rows):
    """(c): gate_dev complete rows (cand slot = CAND, ref slot = fresh REF) -> the dev-select point difference."""
    sel = [x for x in rows if x["half"] == "select"]
    kc, kr = sum(x["ok_c"] for x in sel), sum(x["ok_r"] for x in sel)
    c = {"n": len(sel), "cand": 100 * kc / len(sel), "ref": 100 * kr / len(sel), "diff": 100 * (kc - kr) / len(sel),
         "min": SELECT_MIN_PP}
    c["pass"] = bool(c["diff"] >= SELECT_MIN_PP - EPS)
    c["info_confirm"] = gd.point([x for x in rows if x["half"] == "confirm"])
    c["info_all"] = gd.point(rows)
    return c


def matched_gap(dev_items, tr_items):
    """Info only (never decisive): the gaps with the training side re-weighted to the dev side's (source, qtype) mix.
    The PREREG draw matches counts per source only, and the dev rewrites (dev_negwords, dev_claims) make the dev side
    mostly yes/no while the training side is mostly choice."""
    cell = lambda r: (r["source"], r["qtype"])
    dv, tv = defaultdict(list), defaultdict(list)
    for r, p in dev_items:
        dv[cell(r)].append((r, p))
    for r, p in tr_items:
        tv[cell(r)].append((r, p))
    w = acc = pg = 0.0
    for k, items in dv.items():
        if k in tv:
            x, y = summarize(items), summarize(tv[k])
            w += x["n"]
            acc += x["n"] * (y["acc"] - x["acc"])
            pg += x["n"] * (y["pgold"] - x["pgold"])
    return {"dev_rows_covered": int(w), "acc_gap_pp": acc / w if w else math.nan, "pgold_gap": pg / w if w else math.nan}


def memo_gaps(dev_items, tr_items):
    """(d): [(row, probs)] of the dev rows and of the training rows, both read by the candidate -> the two gaps."""
    dev_s, tr_s = summarize(dev_items), summarize(tr_items)
    d = {"dev": dev_s, "train": tr_s, "acc_gap_pp": tr_s["acc"] - dev_s["acc"],
         "pgold_gap": tr_s["pgold"] - dev_s["pgold"], "acc_gap_max_pp": ACC_GAP_MAX_PP, "pgold_gap_max": PGOLD_GAP_MAX}
    d["acc_pass"] = bool(d["acc_gap_pp"] <= ACC_GAP_MAX_PP + EPS)
    d["pgold_pass"] = bool(d["pgold_gap"] <= PGOLD_GAP_MAX + EPS)
    d["pass"] = d["acc_pass"] and d["pgold_pass"]
    fam = lambda r: family(r["source"])
    d["info_by_family"] = {"dev": breakdown(dev_items, fam), "train": breakdown(tr_items, fam)}
    d["info_by_qtype"] = {"dev": breakdown(dev_items, lambda r: r["qtype"]),
                          "train": breakdown(tr_items, lambda r: r["qtype"])}
    d["info_qtype_matched"] = matched_gap(dev_items, tr_items)
    return d


def dev_items_of(rows):
    """The candidate's reads of the 3,209 dev rows of (d) (both halves), from gate_dev complete rows."""
    items, per_src = [], Counter()
    for x in rows:
        if x["source"] in DEV_SEEN_ROWS:
            items.append(({"qtype": x["qtype"], "gold": x["gold"], "options": x["options"], "source": x["source"]},
                          x["p_c"]))
            per_src[x["source"]] += 1
    if dict(per_src) != DEV_SEEN_ROWS:
        stop(f"dev rows per source {dict(per_src)} != the PREREG list {DEV_SEEN_ROWS}")
    return items


def train_items_of(memo_name):
    """The candidate's reads of the frozen training rows; stops unless the file is the frozen one and every row has a
    prediction."""
    mrows, msha = memo_rows()
    if msha != MEMO_SHA256:
        stop(f"data/{MEMO}.jsonl sha256 {msha} is not the frozen MEMO_SHA256 {MEMO_SHA256}")
    preds = gd.load(MEMO, memo_name)
    if preds is None:
        stop(f"preds_{MEMO}/{memo_name}.jsonl missing (gate/teacher_switch_l4.sh: vm-memo, then pull)")
    miss = [r["id"] for r in mrows if r["id"] not in preds]
    if miss:
        stop(f"preds_{MEMO}/{memo_name}.jsonl lacks {len(miss)} of {len(mrows)} rows (e.g. {miss[:3]}): the check "
             "must be complete")
    owner = {k: s for s, v in TRAIN_POOL.items() for k in v}
    return [({**r, "source": owner[r["source"]]}, preds[r["id"]]) for r in mrows], msha


def cmd_check(a):
    check_frozen_lists()
    splits = gd.SPLITS.split(",")
    gd._MODE = "teacher_switch"
    memo_name = a.memo_name or a.cand
    not_final = []
    # the dev-row definition: re-derived when golden_train is here
    if golden_path().exists() and not a.no_rederive:
        _, _, issues = derive_dev_seen(splits)
        if issues:
            not_final.append("dev rows: derivation differs from PREREG (PREREG list used): " + "; ".join(issues))
    else:
        not_final.append(f"dev rows not re-derived (data/{GOLDEN}.jsonl {'skipped' if a.no_rederive else 'missing'})")
    # REF must be the fresh 4B-E read of the scoring job, vouched for by a passing refparity look (PREREG 4)
    if a.ref in (gd.STORED_REF["4b"], "q35_4b_pxE"):
        not_final.append(f"REF {a.ref} is a stored 4B-E read, not the fresh one of the scoring job (q35_4b_pxE_fresh)")
    else:
        why = gd.refparity_status(a.ref, "4b")
        if why:
            not_final.append(why)
    rows = gd.complete_rows(splits, a.cand, a.ref)  # stops when any row of the 9 splits lacks a prediction
    c = select_margin(rows)
    tr_items, msha = train_items_of(memo_name)
    d = memo_gaps(dev_items_of(rows), tr_items)
    issues, _ = pipeline(a.cand, a.ref, memo_name, splits)
    not_final += issues
    b = ship_b(a.ship_json, a.cand, a.ref)
    if a.ship_json and b is None:  # e.g. a shipped C3 checked against job 1's fresh read: its look used _fresh2
        not_final.append(f"(b): none of the --ship-json looks is {a.cand} vs {a.ref}: REF must be the fresh 4B-E read "
                         "of CAND's ship look (q35_4b_pxE_fresh2 for C3)")
    res = {"mode": "teacher_switch", "cand": a.cand, "ref": a.ref, "memo_name": memo_name, "memo_sha256": msha,
           "c": c, "d": d, "b": b, "final": not not_final, "not_final": not_final,
           "a_timing": "owner: the new 4B is finished before the 2B starts", "e_budget": "owner: ~33 L4-hours per view"}
    res["cd_pass"] = c["pass"] and d["pass"]
    if b is not None:
        res["bcd_pass"] = res["cd_pass"] and b["pass"]
    print_check(res)
    if a.json:
        Path(a.json).write_text(json.dumps(gd._clean(res), indent=2) + "\n")
    return res


def pf(ok):
    return "PASS" if ok else "FAIL"


def print_check(r):
    c, d = r["c"], r["d"]
    print(f"TEACHER SWITCH (PREREG_FINAL.md 6): {r['cand']} vs fresh 4B-E {r['ref']}")
    if r["b"] is None:
        print("(b) ship rule: not given here (pass --ship-json with the ship look of this candidate vs this REF)")
    else:
        b = r["b"]
        print(f"(b) ship rule: {pf(b['pass'])}  verdict {b['verdict']}, final {b['final']} ({b['look']})")
    print(f"(c) dev-select margin: {pf(c['pass'])}  {c['cand']:.2f} vs {c['ref']:.2f} on {c['n']} dev-select rows: "
          f"{c['diff']:+.2f} pp (needs >= +{c['min']:.1f})")
    ic, ia = c["info_confirm"], c["info_all"]
    print(f"    info: dev-confirm {ic['diff']:+.2f} pp ({ic['n']} rows); all 9 splits {ia['diff']:+.2f} pp ({ia['n']} rows)")
    print(f"(d) memorisation: {pf(d['pass'])}")
    print(f"    dev rows   {d['dev']['n']}: accuracy {d['dev']['acc']:.2f}%, mean p(gold) {d['dev']['pgold']:.4f}")
    print(f"    train rows {d['train']['n']}: accuracy {d['train']['acc']:.2f}%, mean p(gold) {d['train']['pgold']:.4f}")
    print(f"    accuracy gap (train - dev) {d['acc_gap_pp']:+.2f} pp (<= {d['acc_gap_max_pp']:.1f}): {pf(d['acc_pass'])}")
    print(f"    p(gold) gap (train - dev) {d['pgold_gap']:+.4f} (<= {d['pgold_gap_max']:.2f}): {pf(d['pgold_pass'])}")
    print("    info by family (dev | train: accuracy %, mean p(gold)):")
    for f in sorted(d["info_by_family"]["dev"]):
        x, y = d["info_by_family"]["dev"][f], d["info_by_family"]["train"].get(f, {"acc": math.nan, "pgold": math.nan, "n": 0})
        print(f"      {f:13s} {x['n']:4d}: {x['acc']:6.2f} {x['pgold']:.3f} | {y['n']:4d}: {y['acc']:6.2f} {y['pgold']:.3f}")
    for q in sorted(d["info_by_qtype"]["dev"]):
        x, y = d["info_by_qtype"]["dev"][q], d["info_by_qtype"]["train"].get(q, {"acc": math.nan, "pgold": math.nan, "n": 0})
        print(f"      qtype {q:7s} {x['n']:4d}: {x['acc']:6.2f} {x['pgold']:.3f} | {y['n']:4d}: {y['acc']:6.2f} {y['pgold']:.3f}")
    qm = d["info_qtype_matched"]
    print(f"    info (never decisive), training side re-weighted to the dev (source, qtype) mix over "
          f"{qm['dev_rows_covered']} dev rows: accuracy gap {qm['acc_gap_pp']:+.2f} pp, p(gold) gap {qm['pgold_gap']:+.4f}")
    print("(a) timing, (e) budget: the owner's call (not computed)")
    if not r["final"]:
        print("NOT FINAL (decides nothing):\n   " + "\n   ".join(r["not_final"]))
    tail = f"(c) {pf(c['pass'])}, (d) {pf(d['pass'])}"
    if r["b"] is not None:
        tail = f"(b) {pf(r['b']['pass'])}, " + tail
    print(f"RESULT: {tail}{'' if r['final'] else ' [NOT FINAL]'}")


def main(argv=None):
    global ROOT
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="write the seed-0 training-row sample (new file only)")
    b.add_argument("--replay", action="store_true", help="also replay the main run's batch order (CPU) and report "
                                                          "sampled rows it never trained on")
    k = sub.add_parser("check", help="conditions (c) and (d)")
    k.add_argument("cand")
    k.add_argument("ref")
    k.add_argument("--memo-name", default=None, help="pred name in preds_memo4b_train_rows/ (default: CAND)")
    k.add_argument("--ship-json", nargs="*", default=None, help="gate_dev --mode ship JSON(s); the one of CAND vs REF "
                                                                 "gives (b)")
    k.add_argument("--json", default=None)
    k.add_argument("--no-rederive", action="store_true", help="skip the golden_train re-derivation (NOT FINAL)")
    for p in (b, k):
        p.add_argument("--root", default=None, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    if a.root:
        ROOT = Path(a.root).resolve()
        gd.ROOT = ROOT
    return cmd_build(a) if a.cmd == "build" else cmd_check(a)


if __name__ == "__main__":
    main()
