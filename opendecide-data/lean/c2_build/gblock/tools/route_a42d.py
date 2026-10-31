#!/usr/bin/env python3
"""G-block routing with the C1 read (PREREG_FINAL A42-D item 5, 5.1-5.7; A45). CPU only; no network; no model runs here.

C1 output is a routing signal only. It is never a label and never a target. Nothing in this file sets, edits or
chooses a label: a row keeps its Haiku label, its A39 Opus label, or (DISAGREE rows only) the label Opus gives it now.

Routing population (A42-D 5.1, "kept and dropped"; see RECONCILE_A45.md): the wave-1 G-block rows that carry a Haiku
or an Opus verdict:
  haiku_accepted  11,200  Haiku conf >= 0.80 (A39 d step 1)         -> classed AGREE-HIGH / AGREE-LOW / DISAGREE
  opus_kept        1,272  A39 Opus conf >= 0.85                      -> keep their status
  a39_dropped      6,301  A39 Opus read, conf < 0.85                 -> keep their status (C1 read is report-only)
  = 18,773 rows ("about 18.8K"). Wave 2 / W8 are NOT in it (program or by-construction gold, no Haiku label cascade).
The G-block mixdev (150 per domain, drawn from the 12,472 kept rows BEFORE routing, seeded) is held out: never trained,
never routed.

Sub-commands (run from anywhere; the paths are fixed):
  reconcile   write gblock/RECONCILE_A45.md and route_a42d/counts.json from the files
  population  write route_a42d/population.jsonl (+ mixdev_ids.json): the 18,773 rows with their status
  split       write the C1 read split file(s) under lean/data/ (+ sha256) and route_a42d/split_manifest.json
  classify    --preds PATH  C1 predictions (od_gcp.py predict output) -> classes, AGREE-HIGH anchors, DISAGREE Opus chunks
  finalize    --answers DIR  Opus answers on the DISAGREE chunks -> rebalance, caps -> route_a42d/routed_block.jsonl
Every subcommand takes --out DIR (default gblock/route_a42d). Writes go through c2_kit.paths (A38 guard, never-open,
lean/ only) unless GUARD is switched off (tests only).
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

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
import build_candidates as B  # noqa: E402  (paths, seed, TEACH-0 chunk item format, opaque qids)
import route as R  # noqa: E402  (validate(): the same answer check as the A39 cascade)
from build_candidates import kp  # noqa: E402

GB = B.GB
LEAN = B.LEAN
OUT = GB / "route_a42d"
DATA = LEAN / "data"
SEED = B.SEED                      # 20261013
GUARD = True                       # False only in tests (writes outside lean/)

HAIKU_CONF = 0.80                  # A39 d
OPUS_CONF = 0.85                   # A39 d step 2 and A42-D 5.4
P_HIGH = 0.90                      # A42-D 5.2
KEEP_HIGH = 0.35                   # A42-D 5.3
MAX_CHUNKS = 40                    # A42-D 5.4
MIN_CHUNKS = 20                    # planning range only (reported, never padded)
CHUNK = B.CHUNK                    # 50
YES_LO, YES_HI = 0.40, 0.60        # A42-D 5.5 (per yes/no card)
BLOCK_CAP = 15000                  # A39 e / A42-D 5.5 (twins included)
DOMAIN_CAP = 0.20                  # A39 e
MIXDEV_PER_DOMAIN = 150            # A39 e
SPLIT_NAME = "gblock_a42d_c1read"  # lean/data/<name>.jsonl ; predictions land in lean/preds_<name>/
C1_NAME = "q35_4b_main500k"
C1_BASE = "Qwen/Qwen3.5-4B"
C1_REV = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
DISAGREE_SECRET = hashlib.sha256(f"gblock|a42d|disagree|blind_read|{SEED}".encode()).hexdigest().encode()

LB = B.LABEL
CAND_DIR = B.CAND_DIR
W2 = GB / "wave2"


# ---------------------------------------------------------------------------------------------------- io helpers

def _write(path: Path, text: str) -> Path:
    if GUARD:
        return kp.write_text(path, text)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _write_json(path: Path, obj) -> Path:
    return _write(path, json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n")


def _write_jsonl(path: Path, rows) -> Path:
    return _write(path, "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows))


def _read_json(path: Path):
    return json.loads(kp.check_path(path).read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list:
    return [json.loads(l) for l in kp.check_path(path).read_text(encoding="utf-8").split("\n") if l.strip()]


def _sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _rank(salt: str, cid: str) -> str:
    return hashlib.sha256(f"{SEED}|{salt}|{cid}".encode()).hexdigest()


def _count_lines(path: Path) -> int:
    with open(kp.check_path(path), "rb") as f:
        return sum(1 for l in f if l.strip())


# ------------------------------------------------------------------------------------- 1. the routing population

def load_live() -> dict:
    """Active wave-1 candidates: candidates.jsonl minus superseded plus the '*_b2' replacements (FIX5.md)."""
    cands = {r["id"]: r for r in _read_jsonl(B.CAND)}
    sup = set(_read_json(CAND_DIR / "superseded_fix5.json")["superseded_ids"])
    live = {c: r for c, r in cands.items() if c not in sup}
    for r in _read_jsonl(CAND_DIR / "fix5_candidates.jsonl"):
        assert r["id"] not in live, r["id"]
        live[r["id"]] = r
    return live


def load_opus_reads(live: dict) -> dict:
    """{candidate id: {role, reason, label, conf, valid, why, chunk}} for every item with an Opus answer file entry,
    plus the list of queue items in answered chunks that have no usable answer. Reads label/opus/*.json."""
    qkey = _read_json(LB / "opus_queue" / "key.json")
    roles = _read_json(LB / "opus_queue" / "roles.json")
    reads, in_chunks = {}, {}
    for p in sorted((LB / "opus").glob("chunk_*.json")):
        chunk_items = _read_json(LB / "opus_queue" / "chunks" / p.name)
        for it in chunk_items:
            in_chunks[qkey[it["qid"]]] = p.stem
        raw = _read_json(p)
        for a in raw:
            cid = qkey.get(a["qid"])
            if cid is None or in_chunks.get(cid) != p.stem:
                raise SystemExit(f"opus answer {p.name}: qid {a['qid']} is not in its own chunk")
            if cid in reads:
                raise SystemExit(f"opus answer: duplicate qid {a['qid']}")
            label, conf, why = R.validate(live[cid], a)
            reads[cid] = {"label": label, "conf": conf, "valid": label is not None, "why": why, "chunk": p.stem}
    unanswered = sorted(c for c in in_chunks if c not in reads)
    return {"reads": reads, "in_answered_chunks": in_chunks, "unanswered": unanswered, "roles": roles}


def build_population() -> dict:
    """The routing population and every count of it, from the files. Returns {rows, counts, mixdev}."""
    live = load_live()
    acc = {r["id"]: r for r in _read_jsonl(LB / "accepted_haiku.jsonl")}
    assert set(acc) <= set(live), "accepted rows outside the live candidates"
    op = load_opus_reads(live)
    roles, reads = op["roles"], op["reads"]
    rows = {}
    for cid, a in acc.items():
        r = live[cid]
        rows[cid] = {"id": cid, "domain": r["domain"], "card_id": r["card_id"], "qtype": r["qtype"],
                     "status": "haiku_accepted", "label": a["label"], "conf": a["confidence"],
                     "haiku_audit": bool(a["audit"])}
        if cid in reads:   # the 5% audit read: report-only
            rows[cid]["opus_audit_label"], rows[cid]["opus_audit_conf"] = reads[cid]["label"], reads[cid]["conf"]
    routed_read = 0
    for cid, rd in reads.items():
        if roles[cid]["role"] != "route":
            continue
        routed_read += 1
        assert cid not in rows, cid
        r = live[cid]
        kept = rd["valid"] and rd["conf"] >= OPUS_CONF
        rows[cid] = {"id": cid, "domain": r["domain"], "card_id": r["card_id"], "qtype": r["qtype"],
                     "status": "opus_kept" if kept else "a39_dropped", "label": rd["label"], "conf": rd["conf"],
                     "haiku_audit": False}
        if not rd["valid"]:
            rows[cid]["opus_invalid"] = rd["why"]
    # cross-check against the A39 finalize file
    fin = _read_json(LB / "opus_finalize_A39.json")
    fin_ids = {k["id"] for k in fin["opus_kept"]}
    mine = {c for c, r in rows.items() if r["status"] == "opus_kept"}
    assert fin_ids == mine, f"opus_kept differs from opus_finalize_A39.json ({len(fin_ids)} vs {len(mine)})"
    # mixdev: 150 per domain from the kept pool (haiku_accepted + opus_kept), seeded, BEFORE any routing
    kept_by_dom = defaultdict(list)
    for c, r in rows.items():
        if r["status"] in ("haiku_accepted", "opus_kept"):
            kept_by_dom[r["domain"]].append(c)
    mixdev = {}
    for d in sorted(kept_by_dom):
        ids = sorted(kept_by_dom[d], key=lambda c: _rank("mixdev", c))[:MIXDEV_PER_DOMAIN]
        assert len(ids) == MIXDEV_PER_DOMAIN, (d, len(ids))
        mixdev[d] = sorted(ids)
    mset = {c for v in mixdev.values() for c in v}
    for c in rows:
        rows[c]["mixdev"] = c in mset
    live_ids = set(live)
    unread = sorted(live_ids - set(rows))
    unread_reason = Counter()
    chunk_of_q = {}
    qkey = _read_json(LB / "opus_queue" / "key.json")
    cid_chunk = {}
    for p in sorted((LB / "opus_queue" / "chunks").glob("chunk_*.json")):
        for it in _read_json(p):
            cid_chunk[qkey[it["qid"]]] = p.stem
    sel = set(_read_json(LB / "opus_queue" / "SELECTION_A41.json")["selected_chunks"])
    for c in unread:
        ch = cid_chunk.get(c)
        if ch is None:
            unread_reason["not in the Opus queue"] += 1
        elif c in op["unanswered"]:
            unread_reason["in an answered chunk, no answer"] += 1
        elif ch not in {p.stem for p in (LB / "opus").glob("chunk_*.json")}:
            unread_reason["chunk not answered (A41 selection / chunk 15)"] += 1
        else:
            unread_reason["other"] += 1
    cnt = Counter(r["status"] for r in rows.values())
    counts = {
        "live_candidates": len(live), "superseded": 2846,
        "haiku_accepted": cnt["haiku_accepted"], "opus_kept": cnt["opus_kept"], "a39_dropped": cnt["a39_dropped"],
        "population": len(rows), "opus_route_items_read": routed_read,
        "opus_answers_total": len(reads), "opus_audit_items_read": len(reads) - routed_read,
        "opus_answered_chunks": len({v["chunk"] for v in reads.values()}),
        "items_in_answered_chunks": len(op["in_answered_chunks"]),
        "items_in_answered_chunks_without_answer": len(op["unanswered"]),
        "routed_by_haiku_cascade": sum(1 for v in roles.values() if v["role"] == "route"),
        "routed_never_read": len(unread), "never_read_reason": dict(unread_reason),
        "queue_items": len(roles), "queue_chunks": len(list((LB / "opus_queue" / "chunks").glob("chunk_*.json"))),
        "selected_chunks_A41": len(sel),
        "mixdev": len(mset), "kept_pool": cnt["haiku_accepted"] + cnt["opus_kept"],
        "audit_rows": sum(1 for r in rows.values() if r["haiku_audit"]),
        "by_domain": dict(Counter(r["domain"] for r in rows.values())),
    }
    return {"rows": rows, "counts": counts, "mixdev": mixdev}


def cmd_population(a):
    pop = build_population()
    out = Path(a.out)
    rows = [pop["rows"][c] for c in sorted(pop["rows"])]
    _write_jsonl(out / "population.jsonl", rows)
    _write_json(out / "mixdev_ids.json", {"seed": SEED, "per_domain": MIXDEV_PER_DOMAIN,
                                          "rule": "per domain, the 150 kept rows (haiku_accepted + opus_kept) with the "
                                                  "lowest sha256(seed|mixdev|id); drawn before any C1 read",
                                          "ids": pop["mixdev"]})
    _write_json(out / "counts.json", pop["counts"])
    print(json.dumps({k: v for k, v in pop["counts"].items() if k != "by_domain"}, indent=1))


def load_population(out: Path) -> dict:
    return {r["id"]: r for r in _read_jsonl(Path(out) / "population.jsonl")}


# ------------------------------------------------------------------------------------- 2. C1 split-file converter

def to_split_row(c: dict) -> dict:
    """The od_gcp.py predict row (DATA/<split>.jsonl): id, state, instructions, qtype, options, card. No label, no gold."""
    return {"id": c["id"], "state": c["state"], "instructions": c["instructions"], "qtype": c["qtype"],
            "options": c["options"], "card": c["card"], "domain": c["domain"], "card_id": c["card_id"]}


def split_names(shards: int) -> list:
    return [SPLIT_NAME] if shards == 1 else [f"{SPLIT_NAME}_s{i}" for i in range(shards)]


def cmd_split(a):
    live = load_live()
    pop = load_population(Path(a.out))
    ids = sorted(pop)
    names = split_names(a.shards)
    ddir = Path(a.data_dir)
    man = {"what": "C1 read split files (A42-D 5.1): every row of the routing population, kept and dropped",
           "rows": len(ids), "splits": {}, "c1": C1_NAME, "base": C1_BASE, "preds_dir": f"preds_{SPLIT_NAME}"}
    for k, name in enumerate(names):
        part = [c for j, c in enumerate(ids) if j % a.shards == k]
        rows = [to_split_row(live[c]) for c in part]
        for r in rows:
            assert r["qtype"] in ("noul", "choice") and r["state"] and (r["qtype"] == "noul" or r["options"])
        path = ddir / f"{name}.jsonl"
        text = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
        _write(path, text)
        h = hashlib.sha256(text.encode()).hexdigest()
        _write(ddir / f"{name}.jsonl.sha256", f"{h}  {name}.jsonl\n")
        man["splits"][name] = {"rows": len(rows), "sha256": h, "noul": sum(r["qtype"] == "noul" for r in rows),
                               "choice": sum(r["qtype"] == "choice" for r in rows),
                               "choice_reads_with_tta": 2 * sum(r["qtype"] == "choice" for r in rows)}
        print(f"{path} {len(rows)} rows sha256 {h}")
    _write_json(Path(a.out) / "split_manifest.json", man)


# ------------------------------------------------------------------------------------- 3. classes (A42-D 5.2)

def argmax(probs: dict) -> str:
    return max(sorted(probs), key=lambda k: probs[k])      # ties -> first label in sorted order (never happens in practice)


def classify_rows(pop: dict, preds: dict) -> dict:
    """pop {id: row}; preds {id: probs}. Returns {id: {class, c1_label, c1_p_label, c1_argmax_p}}.
    Classes on haiku_accepted rows that are not mixdev: AGREE-HIGH / AGREE-LOW / DISAGREE. Every other row gets its
    status as its class (OPUS_KEPT, A39_DROPPED, MIXDEV) and is report-only for C1."""
    out = {}
    for cid, r in pop.items():
        p = preds[cid]
        am = argmax(p)
        d = {"c1_argmax": am, "c1_p_argmax": p[am], "c1_p_label": p.get(r["label"])}
        if r["mixdev"]:
            d["class"] = "MIXDEV"
        elif r["status"] == "opus_kept":
            d["class"] = "OPUS_KEPT"
        elif r["status"] == "a39_dropped":
            d["class"] = "A39_DROPPED"
        elif am == r["label"] and p[r["label"]] >= P_HIGH:
            d["class"] = "AGREE-HIGH"
        elif am == r["label"]:
            d["class"] = "AGREE-LOW"
        else:
            d["class"] = "DISAGREE"
        out[cid] = d
    return out


def load_preds(path: Path, pop: dict, live: dict, allow_missing=False) -> dict:
    preds, probs_ = {}, []
    for r in _read_jsonl(path):
        if r["id"] in preds:
            probs_.append(f"duplicate prediction for {r['id']}")
        preds[r["id"]] = r["probs"]
    missing = sorted(set(pop) - set(preds))
    extra = sorted(set(preds) - set(pop))
    if missing and not allow_missing:
        raise SystemExit(f"classify: {len(missing)} population rows have no C1 prediction (e.g. {missing[:2]})")
    if extra:
        probs_.append(f"{len(extra)} predictions for ids outside the population (ignored)")
    for cid, p in list(preds.items()):
        if cid not in pop:
            del preds[cid]
            continue
        want = ["yes", "no"] if pop[cid]["qtype"] == "noul" else list(live[cid]["options"])
        if sorted(p) != sorted(want) or abs(sum(p.values()) - 1) > 1e-3 or any(v < 0 for v in p.values()):
            probs_.append(f"{cid}: probs keys/sum invalid")
    if probs_ and not allow_missing:
        raise SystemExit("classify: " + "; ".join(probs_[:5]))
    return preds


def _bernoulli_round(x: float, rng: random.Random) -> int:
    return int(math.floor(x + rng.random()))


def keep_anchors(high_rows: list, frac=KEEP_HIGH) -> set:
    """A42-D 5.3: keep 35% of AGREE-HIGH, stratified by card x label (seeded). In each stratum the number kept is
    floor(0.35 n + u), u ~ U[0,1) seeded by the stratum (unbiased rounding); rows are taken by lowest sha256 rank."""
    strata = defaultdict(list)
    for r in high_rows:
        strata[(r["card_id"], r["label"])].append(r["id"])
    kept = set()
    for key in sorted(strata):
        ids = sorted(strata[key], key=lambda c: _rank("anchor", c))
        rng = random.Random(f"{SEED}|anchor|{key[0]}|{key[1]}")
        k = min(len(ids), _bernoulli_round(frac * len(ids), rng))
        kept |= set(ids[:k])
    return kept


def pick_disagree_reads(dis_rows: list, max_items=MAX_CHUNKS * CHUNK) -> tuple:
    """A42-D 5.4. All DISAGREE rows if they fit in <= 40 chunks of 50; otherwise a seeded subsample uniform by card:
    the same sampling fraction in every card (largest-remainder rounding, seeded), total exactly max_items.
    Returns (read ids, unread ids)."""
    ids_all = sorted(r["id"] for r in dis_rows)
    if len(ids_all) <= max_items:
        return ids_all, []
    by_card = defaultdict(list)
    for r in dis_rows:
        by_card[r["card_id"]].append(r["id"])
    f = max_items / len(ids_all)
    quota = {c: f * len(v) for c, v in by_card.items()}
    base = {c: int(math.floor(q)) for c, q in quota.items()}
    rest = max_items - sum(base.values())
    order = sorted(quota, key=lambda c: (-(quota[c] - base[c]), _rank("dis_tie", c)))
    for c in order[:rest]:
        base[c] += 1
    read = []
    for c in sorted(by_card):
        ids = sorted(by_card[c], key=lambda x: _rank("dis_read", x))
        read += ids[:base[c]]
    read_set = set(read)
    return sorted(read), sorted(c for c in ids_all if c not in read_set)


OPUS_PROMPT = """You are an annotator. Read ONLY the one chunk file named in your task and the Read tool for that file; write ONLY your
own answer file. Do not read, list or search any other file, and do not run commands.

The chunk is a JSON list of items. Each item has: qid, kind ("yes/no" or "choice"), text, question, options (choice
items only) and definitions (what each answer means). Decide each item from the text and the definitions alone.

For every item write {"qid": ..., "answer": ..., "confidence": ...}:
  - answer: for kind "yes/no" exactly "yes" or "no"; for kind "choice" exactly one of the item's options (same spelling).
  - confidence: a number from 0 to 1 for how sure you are that the answer is right. Use 0.85 or more only when the
    text and the definitions clearly settle it. Use a lower number when two answers are reasonable.
Answer every item. Save the answers as a JSON list in your answer file, in any order, and reply with one line.
"""


def cmd_classify(a):
    out = Path(a.out)
    live = load_live()
    pop = load_population(out)
    pp = Path(a.preds) if a.preds else LEAN / f"preds_{SPLIT_NAME}" / f"{C1_NAME}.jsonl"
    preds = load_preds(pp, pop, live, a.allow_missing)
    pop = {c: r for c, r in pop.items() if c in preds}
    cls = classify_rows(pop, preds)
    high = [pop[c] for c in sorted(cls) if cls[c]["class"] == "AGREE-HIGH"]
    low = [pop[c] for c in sorted(cls) if cls[c]["class"] == "AGREE-LOW"]
    dis = [pop[c] for c in sorted(cls) if cls[c]["class"] == "DISAGREE"]
    anchors = keep_anchors(high)
    read_ids, unread_ids = pick_disagree_reads(dis)
    n_chunks = math.ceil(len(read_ids) / CHUNK) if read_ids else 0
    avoid = set(_read_json(LB / "key.json")) | set(_read_json(LB / "opus_queue" / "key.json")) \
        | set(_read_json(LB / "fix5" / "key.json"))
    chunks, key = B.make_chunks([live[c] for c in read_ids], DISAGREE_SECRET, f"{SEED}|a42d|disagree|order",
                                avoid=avoid) if read_ids else ([], {})
    assert len(chunks) <= MAX_CHUNKS and all(len(items) <= CHUNK for _, items in chunks)
    files = {f"{n}.json": B.chunk_text(items) for n, items in chunks}
    cdir = out / "disagree" / "chunks"
    for name, text in files.items():
        _write(cdir / name, text)
    _write_json(out / "disagree" / "key.json", key)                      # orchestrator only, never sent to a reader
    _write(out / "disagree" / "PROMPT.txt", OPUS_PROMPT)
    man = {"what": "A42-D 5.4 DISAGREE chunks for Opus (gold-free TEACH-0 items; no Haiku or C1 label inside)",
           "seed": SEED, "n_items": len(key), "n_chunks": len(chunks), "disagree_rows": len(dis),
           "read": len(read_ids), "unread_dropped": len(unread_ids),
           "subsampled": bool(unread_ids), "in_20_40_chunk_range": MIN_CHUNKS <= len(chunks) <= MAX_CHUNKS,
           "key_sha256": hashlib.sha256((json.dumps(key, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode()).hexdigest(),
           "chunks": {n: {"n": len(items), "sha256": hashlib.sha256(files[f'{n}.json'].encode()).hexdigest()}
                      for n, items in chunks},
           "preds_sha256": _sha(pp), "population_sha256": _sha(out / "population.jsonl")}
    _write_json(out / "disagree" / "MANIFEST.json", man)
    rows = []
    for c in sorted(cls):
        r = dict(pop[c])
        r.update(cls[c])
        r["anchor_kept"] = c in anchors
        r["disagree_read"] = c in set(read_ids)
        rows.append(r)
    _write_jsonl(out / "classes.jsonl", rows)
    stats = class_stats(rows, anchors, read_ids, unread_ids, len(chunks))
    _write_json(out / "classes_stats.json", stats)
    print(json.dumps(stats["summary"], indent=1))


def class_stats(rows: list, anchors: set, read_ids: list, unread_ids: list, n_chunks: int) -> dict:
    cnt = Counter(r["class"] for r in rows)
    by_dom = defaultdict(Counter)
    by_card = defaultdict(Counter)
    for r in rows:
        by_dom[r["domain"]][r["class"]] += 1
        by_card[r["card_id"]][r["class"]] += 1
    agree = lambda cl: [r for r in rows if r["class"] in cl]
    hi = [r for r in rows if r["status"] == "haiku_accepted" and not r["mixdev"]]
    rep = {}
    for st in ("opus_kept", "a39_dropped"):
        sub = [r for r in rows if r["status"] == st and not r["mixdev"]]
        rep[st] = {"n": len(sub), "c1_argmax_equals_opus_label": sum(r["c1_argmax"] == r["label"] for r in sub)}
    return {"summary": {"classes": dict(cnt), "agree_high_kept": len(anchors), "disagree_read": len(read_ids),
                        "disagree_unread_dropped": len(unread_ids), "disagree_chunks": n_chunks,
                        "haiku_accepted_routed": len(hi),
                        "disagree_share_of_haiku_accepted": round(cnt["DISAGREE"] / max(1, len(hi)), 4)},
            "report_only_vs_opus_label": rep,
            "per_domain": {d: dict(c) for d, c in sorted(by_dom.items())},
            "per_card": {d: dict(c) for d, c in sorted(by_card.items())}}


# ------------------------------------------------------------------------------------- 4. rebalance and caps

def _thin(rows: list, frac: float, salt: str) -> list:
    """Seeded stratified (card x label) thinning to ~frac. Kept rows = lowest sha256 rank in each stratum."""
    strata = defaultdict(list)
    for r in rows:
        strata[(r["card_id"], r["label"])].append(r)
    out = []
    for key in sorted(strata):
        rs = sorted(strata[key], key=lambda r: _rank(salt, r["id"]))
        rng = random.Random(f"{SEED}|{salt}|{key[0]}|{key[1]}|{len(rs)}")
        k = min(len(rs), _bernoulli_round(frac * len(rs), rng))
        out += rs[:k]
    return out


def rebalance(rows: list) -> list:
    """A42-D 5.5: yes share 40-60% per yes/no card, by seeded down-sampling of the over-represented label within the
    card (lowest sha256 rank kept; factor 1.0, no preference by source). Never relabels. A card with only one label
    cannot be balanced and leaves the block. Choice cards have no yes share and are untouched."""
    by_card = defaultdict(list)
    for r in rows:
        by_card[r["card_id"]].append(r)
    out = []
    for cid in sorted(by_card):
        rs = by_card[cid]
        if rs[0]["qtype"] != "noul":
            out += rs
            continue
        yes = sorted([r for r in rs if r["label"] == "yes"], key=lambda r: _rank("rebalance", r["id"]))
        no = sorted([r for r in rs if r["label"] == "no"], key=lambda r: _rank("rebalance", r["id"]))
        y, n = len(yes), len(no)
        if y == 0 or n == 0:
            continue
        if 10 * y > 6 * (y + n):          # yes over-represented: yes <= 1.5 x no
            yes = yes[:(3 * n) // 2]
        elif 10 * y < 4 * (y + n):        # no over-represented: no <= 1.5 x yes
            no = no[:(3 * y) // 2]
        out += yes + no
    return out


def apply_caps(rows: list, twins: int = 0, block_cap=BLOCK_CAP, dom_cap=DOMAIN_CAP) -> list:
    """Rebalance, then the domain cap (<= 20% of the block, shares on the non-twin rows; twins are generated from the
    block's own yes/no rows and keep its domain mix) and the block cap (rows + twins <= 15,000), by seeded stratified
    thinning, repeated until all three hold. Only ever removes rows."""
    rows = rebalance(rows)
    for it in range(200):
        n = len(rows)
        dom = Counter(r["domain"] for r in rows)
        bad = [d for d in sorted(dom) if dom[d] > dom_cap * n + 1e-9]
        if bad:
            d = max(bad, key=lambda x: dom[x])
            others = n - dom[d]
            target = math.floor(others * dom_cap / (1 - dom_cap))
            keep_d = _thin([r for r in rows if r["domain"] == d], target / dom[d], f"domcap{it}")
            rows = [r for r in rows if r["domain"] != d] + keep_d
            rows = rebalance(rows)
            continue
        if n + twins > block_cap:
            rows = rebalance(_thin(rows, max(0, block_cap - twins) / n, f"blockcap{it}"))
            continue
        return sorted(rows, key=lambda r: r["id"])
    raise SystemExit("apply_caps: no fixpoint after 200 rounds")


def check_block(rows: list, twins: int = 0, block_cap=BLOCK_CAP, dom_cap=DOMAIN_CAP, mixdev: set = frozenset()) -> list:
    probs = []
    ids = [r["id"] for r in rows]
    if len(set(ids)) != len(ids):
        probs.append("repeated rows")
    if set(ids) & set(mixdev):
        probs.append("mixdev row in the block")
    if len(rows) + twins > block_cap:
        probs.append(f"block {len(rows)} + twins {twins} > {block_cap}")
    dom = Counter(r["domain"] for r in rows)
    for d, v in dom.items():
        if v > dom_cap * len(rows) + 1e-9:
            probs.append(f"domain {d} {v}/{len(rows)} above {dom_cap:.0%}")
    byc = defaultdict(Counter)
    for r in rows:
        if r["qtype"] == "noul":
            byc[r["card_id"]][r["label"]] += 1
    for c, k in byc.items():
        t = k["yes"] + k["no"]
        if not (4 * t <= 10 * k["yes"] <= 6 * t):
            probs.append(f"card {c} yes share {k['yes']}/{t} outside 40-60%")
    return probs


def assemble(pop: dict, cls_rows: dict, disagree_kept: dict) -> tuple:
    """Pre-rebalance kept rows. cls_rows {id: class}; disagree_kept {id: (opus label, conf)}.
    Returns (rows, funnel)."""
    rows, fun = [], Counter()
    for cid in sorted(pop):
        r, c = pop[cid], cls_rows[cid]
        base = {"id": cid, "domain": r["domain"], "card_id": r["card_id"], "qtype": r["qtype"]}
        if c == "MIXDEV":
            fun["mixdev_held_out"] += 1
        elif c == "OPUS_KEPT":
            rows.append({**base, "label": r["label"], "conf": r["conf"], "source": "opus_a39"})
            fun["opus_a39_kept"] += 1
        elif c == "A39_DROPPED":
            fun["a39_dropped_stay_dropped"] += 1
        elif c == "AGREE-LOW":
            rows.append({**base, "label": r["label"], "conf": r["conf"], "source": "haiku_agree_low"})
            fun["agree_low_kept"] += 1
        elif c == "AGREE-HIGH":
            fun["agree_high_total"] += 1
            if r.get("anchor_kept"):
                rows.append({**base, "label": r["label"], "conf": r["conf"], "source": "haiku_agree_high_anchor"})
                fun["agree_high_anchor_kept"] += 1
        elif c == "DISAGREE":
            fun["disagree_total"] += 1
            if cid in disagree_kept:
                lab, conf = disagree_kept[cid]
                rows.append({**base, "label": lab, "conf": conf, "source": "opus_disagree",
                             "haiku_label": r["label"]})
                fun["disagree_kept_opus_label"] += 1
                fun["disagree_kept_label_differs_from_haiku"] += int(lab != r["label"])
    return rows, fun


def cmd_finalize(a):
    out = Path(a.out)
    live = load_live()
    crow = {r["id"]: r for r in _read_jsonl(out / "classes.jsonl")}
    pop = {c: r for c, r in crow.items()}
    key = _read_json(out / "disagree" / "key.json")
    man = _read_json(out / "disagree" / "MANIFEST.json")
    adir = Path(a.answers)
    got, probs_ = {}, []
    for p in sorted(adir.glob("chunk_*.json")):
        if man["chunks"].get(p.stem) is None:
            probs_.append(f"{p.name}: not a DISAGREE chunk")
            continue
        qs = {it["qid"] for it in _read_json(out / "disagree" / "chunks" / p.name)}
        for x in _read_json(p):
            if x.get("qid") not in qs:
                probs_.append(f"{p.name}: qid {x.get('qid')} not in its own chunk")
            elif key[x["qid"]] in got:
                probs_.append(f"duplicate answer {x['qid']}")
            else:
                got[key[x["qid"]]] = x
    dk, why = {}, Counter()
    for cid, x in got.items():
        label, conf, w = R.validate(live[cid], x)
        if label is None:
            why["invalid"] += 1
        elif conf < OPUS_CONF:
            why["low_confidence"] += 1
        else:
            dk[cid] = (label, conf)
    why["unanswered"] = len(key) - len(got)
    rows, fun = assemble(pop, {c: r["class"] for c, r in crow.items()}, dk)
    fun["disagree_unread_dropped"] = man["unread_dropped"]
    fun["disagree_dropped_at_opus"] = dict(why)
    mix = {c for c, r in crow.items() if r["mixdev"]}
    block = apply_caps(rows, a.twins)
    bad = check_block(block, a.twins, mixdev=mix)
    if bad:
        raise SystemExit("finalize: block checks failed: " + "; ".join(bad))
    _write_jsonl(out / "routed_block.jsonl", block)
    res = block_report(rows, block, fun, a.twins, probs_)
    _write_json(out / "routed_block_stats.json", res)
    _write(out / "ROUTE_A42D.md", render_md(res))
    print(json.dumps(res["summary"], indent=1))


def block_report(pre: list, block: list, fun: Counter, twins: int, problems: list) -> dict:
    def yes_shares(rs):
        k = defaultdict(Counter)
        for r in rs:
            if r["qtype"] == "noul":
                k[r["card_id"]][r["label"]] += 1
        return {c: round(v["yes"] / (v["yes"] + v["no"]), 3) for c, v in sorted(k.items())}
    return {"summary": {"pre_rebalance_rows": len(pre), "block_rows": len(block), "twins_assumed": twins,
                        "block_plus_twins": len(block) + twins,
                        "by_source": dict(Counter(r["source"] for r in block)),
                        "by_domain": dict(sorted(Counter(r["domain"] for r in block).items())),
                        "max_domain_share": round(max(Counter(r["domain"] for r in block).values()) / len(block), 4)
                        if block else 0},
            "funnel": dict(fun), "problems": problems,
            "yes_share_before": yes_shares(pre), "yes_share_after": yes_shares(block),
            "removed_by_caps": len(pre) - len(block)}


def render_md(res: dict) -> str:
    s = res["summary"]
    L = ["# G-block routing result (PREREG_FINAL A42-D item 5)", "",
         "Generated by `tools/route_a42d.py finalize`. C1 output was a routing signal only; no label was edited.", "",
         "## Funnel", ""]
    L += [f"- {k}: {v}" for k, v in sorted(res["funnel"].items())]
    L += ["", f"- rows before rebalance and caps: {s['pre_rebalance_rows']}",
          f"- removed by the 40-60% yes-share rebalance, domain cap and block cap: {res['removed_by_caps']}",
          f"- **routed block: {s['block_rows']}** (+ {s['twins_assumed']} twins assumed = {s['block_plus_twins']} of 15,000)",
          f"- max domain share {s['max_domain_share']:.1%} (cap 20%)", "", "## By source", ""]
    L += [f"- {k}: {v}" for k, v in sorted(s["by_source"].items())]
    L += ["", "## By domain", ""] + [f"- {k}: {v}" for k, v in s["by_domain"].items()]
    L += ["", "## Yes share per yes/no card (before -> after)", ""]
    for c in sorted(res["yes_share_before"]):
        L.append(f"- {c}: {res['yes_share_before'][c]} -> {res['yes_share_after'].get(c, 'left the block')}")
    if res["problems"]:
        L += ["", "## Problems", ""] + [f"- {p}" for p in res["problems"]]
    return "\n".join(L) + "\n"


# ------------------------------------------------------------------------------------- 5. reconciliation report

def cmd_reconcile(a):
    pop = build_population()
    c = pop["counts"]
    w2 = W2
    w2s = _read_json(w2 / "route" / "route_stats.json")
    fin2 = _read_json(w2 / "opus_finalize_A40.json")
    finw8 = _read_json(w2 / "opus_finalize_w8.json")
    k2 = _count_lines(w2 / "kept_haiku.jsonl")
    f2 = _count_lines(w2 / "final_kept_A40.jsonl")
    kw8 = _count_lines(w2 / "kept_haiku_w8.jsonl")
    fw8 = _count_lines(w2 / "final_kept_w8.jsonl")
    cand2 = _count_lines(w2 / "candidates" / "candidates.jsonl")
    cw8 = _count_lines(w2 / "candidates" / "w8_candidates.jsonl")
    fin = _read_json(LB / "opus_finalize_A39.json")
    bd = c["by_domain"]
    nr = c["opus_route_items_read"]
    md = f"""# RECONCILE_A45: every G-block count, from the files

Written by `tools/route_a42d.py reconcile` (A45 task, 15 Oct 2026). Nothing was relabelled; no file in the build was
changed. All numbers below are recomputed from the files named in the table.

## Populations

| Population | File | Count |
|---|---|---:|
| Wave-1 rows in `candidates.jsonl` (includes the superseded ones) | `candidates/candidates.jsonl` | 20,003 |
| Superseded by fix5 (card re-rendered with the `no` line) | `candidates/superseded_fix5.json` | {c['superseded']:,} |
| fix5 `_b2` replacements | `candidates/fix5_candidates.jsonl` | 2,846 |
| **Live wave-1 candidates** (20,003 - 2,846 = 17,157 base, + 2,846 replacements) | candidates + fix5 | **{c['live_candidates']:,}** |
| Haiku-accepted (conf >= 0.80) | `label/accepted_haiku.jsonl` | {c['haiku_accepted']:,} |
| of which in the 5% Opus audit sample | same, `audit` = true | {c['audit_rows']:,} (493 of them read, 0 disagreements) |
| Routed to Opus by the Haiku cascade (low conf 8,733 + invalid 4 + missing 66) | `label/opus_queue/roles.json` role `route` | {c['routed_by_haiku_cascade']:,} |
| Opus queue (routed + audit), in {c['queue_chunks']} chunks | `label/opus_queue/{{key,roles}}.json` | {c['queue_items']:,} |
| Chunks the A41 selection ran (150 seeded + 14 slipped) | `SELECTION_A41.json` (150) + A41 note (14) | 164 |
| Chunks with an Opus answer file | `label/opus/` | {c['opus_answered_chunks']} |
| Items in those 163 chunks (nominal 163 x 50 = 8,150; the last queue chunk has 18) | `label/opus_queue/chunks/` | {c['items_in_answered_chunks']:,} |
| of which with no answer in the file | `label/opus/` | {c['items_in_answered_chunks_without_answer']} |
| Opus answers | `label/opus/` | {c['opus_answers_total']:,} |
| of which route items | | {nr:,} |
| of which audit items (Haiku-accepted rows) | | {c['opus_audit_items_read']} |
| **Opus-kept** (route items, valid, conf >= 0.85) | `opus_finalize_A39.json` `opus_kept` | **{len(fin['opus_kept']):,}** (recomputed: {c['opus_kept']:,}) |
| **A39-dropped** (route items read, conf < 0.85) | `opus_finalize_A39.json` `dropped.low_conf` | **{fin['dropped']['low_conf']:,}** (recomputed: {c['a39_dropped']:,}) |
| Routed rows never read by Opus (24 unselected chunks, chunk 15, the 52 unanswered) | derived | {c['routed_never_read']:,} |
| Labelled pool (Haiku 11,200 + Opus 1,272) | | {c['kept_pool']:,} |
| G-block mixdev (150 x 11 domains, drawn from the pool) | `route_a42d/mixdev_ids.json` | {c['mixdev']:,} |

Items in answered chunks without an answer: {c['items_in_answered_chunks_without_answer']} (48 route items, 4 audit items). The never-read rows by
reason: {json.dumps(c['never_read_reason'])}.

## The routing population A42-D 5.1 means: 18,773 rows ("about 18.8K")

The C1 read covers every wave-1 row that carries a Haiku or an Opus verdict, kept and dropped:

    haiku_accepted {c['haiku_accepted']:,} + opus_kept {c['opus_kept']:,} + a39_dropped {c['a39_dropped']:,} = {c['population']:,}

- **18.8K is not a file count.** No file holds it. It is 11,200 + 7,573 = {c['population']:,}: the Haiku-accepted rows
  plus the Opus-read route items (1,272 kept + 6,301 dropped). FINAL_PLAN item 6 and A42-D 5.1 round it to 18.8K.
  The state map's "8,150 items in 163 answered chunks" is the nominal 163 x 50. The chunks hold {c['items_in_answered_chunks']:,}
  items, {c['opus_answers_total']:,} were answered, and {nr:,} of those are route items. 7,573 = 1,272 + 6,301 is
  therefore consistent with the files; it is not a shortfall against 8,150.
- The 493 audit items are Haiku-accepted rows. They are in the 11,200, not in the 7,573.
- Rows never read by Opus ({c['routed_never_read']:,}) have no kept or dropped verdict. They are outside the
  population (they were never kept and are not in the 12,472). They are not read by C1 either; adding them would be a
  report-only extra and is not needed for any rule.
- The live candidates (20,003) are the whole wave-1 set. {c['population']:,} of them have a verdict.
- Per-domain counts of the population: {json.dumps(bd, sort_keys=True)}.

## Wave 2 and W8 are not in the routing population

| Population | File | Count |
|---|---|---:|
| Wave-2 candidates (W1-W7) | `wave2/candidates/candidates.jsonl` | {cand2:,} |
| Haiku-kept (Haiku = program/construction gold, conf >= 0.80) | `wave2/kept_haiku.jsonl` | {k2:,} |
| Opus-kept at the queue (agrees with gold, conf >= 0.85) | `wave2/opus_finalize_A40.json` `opus_kept` | {len(fin2['opus_kept']):,} |
| Opus queue dropped | same, `dropped` | {fin2['dropped']['opus_disagree_or_low']:,} + {fin2['dropped']['no_opus_answer']} no answer |
| Pool (9,073 + 431) | | {k2 + len(fin2['opus_kept']):,} |
| After the A40 (ii) seeded cap | `wave2/final_kept_A40.jsonl` | {f2:,} |
| W8 candidates / Haiku-kept / Opus-kept / capped | `w8_candidates.jsonl`, `kept_haiku_w8.jsonl`, `opus_finalize_w8.json`, `final_kept_w8.jsonl` | {cw8:,} / {kw8:,} / {finw8['queued_kept']} / {fw8:,} |

- **ROUTE.md vs opus_finalize_A40.json.** `wave2/ROUTE.md` was written 13 Oct 17:53 UTC, before the Opus reads. Its line
  "Opus reads have NOT been run" was true then and is stale now. `opus_finalize_A40.json` (18:04) is later and is the
  record the PREREG A40 result cites: 64 of 65 chunks read, 431 kept, 2,270 dropped. The two files do not conflict
  once dated. `ROUTE.md` was not edited.
- **Why they are outside.** Wave-2 and W8 labels are the program or by-construction gold (A40 c), not Haiku or Opus labels.
  A42-D 5.2 defines its classes on "Haiku-accepted rows (Haiku confidence >= 0.80 per A39 d)", FINAL_PLAN item 6's
  evidence is on the wave-1 cascade, and wave 2 has its own cap (A40 d: 8,000, 9,200 with W8). The 15,000 cap of
  A39 e / A42-D 5.5 is the wave-1 block's.
- HANDOFF's "G-block 12,472, wave 2 7,295, W8 1,200" is the labelled pools: 12,472 = 11,200 + 1,272.
- The A40 note says wave 2 is 8,495 after W8 (7,295 + 1,200). The sum of the three pools is 12,472 + 8,495 = 20,967.

## Consequence for A42-D item 5

- Classes (5.2) apply to the {c['haiku_accepted']:,} Haiku-accepted rows minus the mixdev rows drawn from them.
- The {c['opus_kept']:,} Opus-kept rows and {c['a39_dropped']:,} dropped rows keep their status; their C1 reads are report-only.
- The mixdev ({c['mixdev']:,} rows, 150 per domain) comes out of the 12,472 kept rows before any class is formed and is never trained.
- The "about 5K rows freed" of 5.7 is the 65% AGREE-HIGH leaving the block plus the rebalance.
"""
    _write(GB / "RECONCILE_A45.md", md)
    _write_json(Path(a.out) / "counts.json", c)
    print(md[:200])


def parser():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in (("reconcile", cmd_reconcile), ("population", cmd_population), ("split", cmd_split),
                     ("classify", cmd_classify), ("finalize", cmd_finalize)):
        p = sub.add_parser(name)
        p.add_argument("--out", default=str(OUT))
        p.set_defaults(fn=fn)
        if name == "split":
            p.add_argument("--shards", type=int, default=1)
            p.add_argument("--data-dir", default=str(DATA))
        if name == "classify":
            p.add_argument("--preds", default="")
            p.add_argument("--allow-missing", action="store_true")
        if name == "finalize":
            p.add_argument("--answers", required=True)
            p.add_argument("--twins", type=int, default=0, help="G-block complement twins counted in the 15,000 cap")
    return ap


if __name__ == "__main__":
    args = parser().parse_args()
    args.fn(args)
