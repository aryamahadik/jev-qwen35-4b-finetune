#!/usr/bin/env python3
"""G-block label cascade, step 1: route Haiku answers (PREREG_FINAL A39 d). CPU only; no network.

Nothing here sets, edits or chooses a label: a Haiku answer is either taken as given (validated, confident) or the
item is sent to Opus. The Opus step 2 (keep only Opus confidence >= 0.85) and the audit verdict (> 6% disagreement
re-reads the domain) run on the Opus answers later.

Inputs (read-only):
  candidates/candidates.jsonl, label/key.json ({qid: candidate id}), label/chunks/chunk_XXXX.json and
  label/MANIFEST.json (chunk and key sha256s: refuses chunks changed after the build);
  label/haiku/*.json Haiku answers, the TEACH-0 answer format [{qid, answer, confidence}] (also accepted:
  {"answers": [...]} or {qid: {answer, confidence}}). An answer file named like a chunk (chunk_0007.json) may only
  answer that chunk's qids.
Steps:
  (1) validate: a yes/no answer is "yes" / "no" (case and outer spaces ignored); a choice answer is exactly one of the
      item's options (outer spaces ignored); confidence is a number in [0, 1]. Unknown qids, answers outside their own
      chunk and conflicting duplicates are problems and are not used.
  (2) accept the Haiku label when valid and confidence >= 0.80;
  (3) route everything else (low confidence, invalid, unanswered) plus a seeded 5% audit sample of the accepted rows
      (ceil(5%) per domain, since the audit verdict is per domain) into Opus chunks: the same TEACH-0 item format,
      new opaque qids (disjoint from Haiku's), a seeded order that mixes routed and audit items (a reader cannot tell
      them apart), 50 per chunk;
  (4) write label/accepted_haiku.jsonl ({id, label, confidence, qid, audit}), label/opus_queue/chunks/,
      label/opus_queue/key.json ({qid: candidate id}), label/opus_queue/roles.json ({candidate id: {role, reason}};
      orchestrator only, like the keys), label/opus_queue/MANIFEST.json and label/ROUTE.md (counts per domain / card).

Superseded ids (A39 fix5, FIX5.md): candidates/superseded_fix5.json lists candidate ids whose card was re-rendered as
a '*_b2' replacement. They stay in candidates.jsonl / label/key.json / label/chunks/ (so every input hash stays valid)
but are dropped HERE, before any accept / route / audit decision: they never reach accepted_haiku.jsonl or the Opus
queue. The replacements are routed only with --fix5 (label/fix5/: candidates/fix5_candidates.jsonl, key.json, chunks and
MANIFEST.json are verified; their Haiku answers are read from label/fix5/haiku or --fix5-haiku DIR).

  ../../../.venv/bin/python tools/route.py [--dry-run] [--allow-missing-chunks] [--force] [--fix5]
    --allow-missing-chunks  route the items of chunks with no Haiku answer at all to Opus too (default: refuse, since
                            that means the Haiku pass is not finished)
    --force                 replace an existing opus_queue whose key would change
    --fix5                  add the '*_b2' replacements of the superseded ids (needs superseded_fix5.json)
Writes go through c2_kit.paths (A38 guard, never-open guard, lean/ only).
"""
from __future__ import annotations

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
import build_candidates as B  # noqa: E402  (paths, seed, the chunk item format and qid scheme)
from build_candidates import kp  # noqa: E402

SUPERSEDED = B.CAND_DIR / "superseded_fix5.json"      # A39 fix5: candidate ids replaced by '*_b2' re-renders
FIX5_DIR = B.LABEL / "fix5"
FIX5_CAND = B.CAND_DIR / "fix5_candidates.jsonl"
ACCEPT_CONF = 0.80     # A39 d step 1
AUDIT_SHARE = 0.05     # A39 d audit
OPUS_SECRET = hashlib.sha256(f"gblock|opus|blind_read|{B.SEED}".encode()).hexdigest().encode()


# ------------------------------------------------------------------------------------------------------- loading

def load_inputs():
    cands = {r["id"]: r for r in B.read_jsonl(B.CAND)}
    key = json.loads(kp.check_path(B.KEY).read_text(encoding="utf-8"))
    man = json.loads(kp.check_path(B.LABEL / "MANIFEST.json").read_text(encoding="utf-8"))
    probs = []
    if B.sha256_file(B.KEY) != man["key_sha256"]:
        probs.append("label/key.json differs from MANIFEST.json")
    if B.sha256_file(B.CAND) != man["candidates_sha256"]:
        probs.append("candidates.jsonl differs from MANIFEST.json")
    chunk_of, items = {}, {}
    names = sorted(p.stem for p in B.CHUNKS.glob("chunk_*.json"))
    if names != sorted(man["chunks"]):
        probs.append("chunk files differ from MANIFEST.json")
    for n in names:
        p = B.CHUNKS / f"{n}.json"
        if B.sha256_file(p) != man["chunks"].get(n, {}).get("sha256"):
            probs.append(f"{n}: sha256 differs from MANIFEST.json")
        for it in json.loads(kp.check_path(p).read_text(encoding="utf-8")):
            chunk_of[it["qid"]] = n
            items[it["qid"]] = it
    if set(chunk_of) != set(key) or set(key.values()) != set(cands):
        probs.append("key, chunks and candidates do not cover the same items")
    if probs:
        raise SystemExit("route: inputs are not the built label set: " + "; ".join(probs))
    return cands, key, chunk_of, items


def load_superseded(cands: dict) -> frozenset:
    """Superseded candidate ids (A39 fix5), or an empty set when there is no superseded_fix5.json. Refuses a file that
    does not match the built candidates."""
    if not SUPERSEDED.exists():
        return frozenset()
    d = json.loads(kp.check_path(SUPERSEDED).read_text(encoding="utf-8"))
    ids = d["superseded_ids"]
    probs = []
    if len(ids) != len(set(ids)) or d.get("n_superseded") != len(ids):
        probs.append("superseded ids are not unique or n_superseded differs")
    if [i for i in ids if i not in cands]:
        probs.append("superseded ids that are not candidates")
    if d["inputs"]["candidates_sha256"] != B.sha256_file(B.CAND):
        probs.append("candidates.jsonl differs from the one the superseded list was made for")
    if probs:
        raise SystemExit("route: superseded_fix5.json is not usable: " + "; ".join(probs))
    return frozenset(ids)


def load_fix5(superseded: frozenset) -> tuple:
    """(cands, key, chunk_of) of the fix5 replacements, verified against label/fix5/MANIFEST.json. Chunk names are
    'fix5/chunk_XXXX' so they never clash with the base chunk names."""
    if not superseded:
        raise SystemExit("route: --fix5 needs candidates/superseded_fix5.json")
    man = json.loads(kp.check_path(FIX5_DIR / "MANIFEST.json").read_text(encoding="utf-8"))
    sup = json.loads(kp.check_path(SUPERSEDED).read_text(encoding="utf-8"))
    cands = {r["id"]: r for r in B.read_jsonl(FIX5_CAND)}
    key = json.loads(kp.check_path(FIX5_DIR / "key.json").read_text(encoding="utf-8"))
    probs = []
    for what, p, want in (("fix5 candidates", FIX5_CAND, man["candidates_sha256"]),
                          ("fix5 key", FIX5_DIR / "key.json", man["key_sha256"]),
                          ("superseded_fix5.json", SUPERSEDED, man["superseded_sha256"])):
        if B.sha256_file(p) != want:
            probs.append(f"{what} differs from label/fix5/MANIFEST.json")
    chunk_of = {}
    names = sorted(p.stem for p in (FIX5_DIR / "chunks").glob("chunk_*.json"))
    if names != sorted(man["chunks"]):
        probs.append("fix5 chunk files differ from label/fix5/MANIFEST.json")
    for n in names:
        p = FIX5_DIR / "chunks" / f"{n}.json"
        if B.sha256_file(p) != man["chunks"].get(n, {}).get("sha256"):
            probs.append(f"fix5 {n}: sha256 differs from label/fix5/MANIFEST.json")
        for it in json.loads(kp.check_path(p).read_text(encoding="utf-8")):
            chunk_of[it["qid"]] = f"fix5/{n}"
    if set(chunk_of) != set(key) or set(key.values()) != set(cands):
        probs.append("fix5 key, chunks and candidates do not cover the same items")
    if {c[:-len(sup["replacement_suffix"])] for c in cands} != set(superseded):
        probs.append("fix5 replacements are not exactly the superseded ids")
    if probs:
        raise SystemExit("route: fix5 inputs are not the built fix5 set: " + "; ".join(probs))
    return cands, key, chunk_of


def load_haiku(hdir: Path) -> dict:
    """{file stem: parsed JSON} for every *.json answer file (sorted)."""
    out = {}
    if hdir.is_dir():
        for p in sorted(hdir.glob("*.json")):
            out[p.stem] = json.loads(kp.check_path(p).read_text(encoding="utf-8"))
    return out


def answer_pairs(raw) -> tuple:
    """[(qid, answer object)], problems, from one answer file's parsed JSON."""
    probs = []
    if isinstance(raw, dict) and isinstance(raw.get("answers"), list):
        raw = raw["answers"]
    if isinstance(raw, list):
        pairs = []
        for a in raw:
            if isinstance(a, dict) and isinstance(a.get("qid"), str):
                pairs.append((a["qid"], a))
            else:
                probs.append("an answer without a qid")
        return pairs, probs
    if isinstance(raw, dict):
        return [(q, a if isinstance(a, dict) else {"answer": a}) for q, a in raw.items()], probs
    return [], ["answers are a list or an object"]


# ------------------------------------------------------------------------------------------------------- routing

def validate(row: dict, a: dict) -> tuple:
    """(label, confidence, None) or (None, None, why)."""
    ans, c = a.get("answer"), a.get("confidence")
    if not isinstance(ans, str):
        return None, None, "answer is not a string"
    if isinstance(c, bool):
        return None, None, "confidence is not a number"
    try:
        c = float(c)
    except (TypeError, ValueError):
        return None, None, "confidence is not a number"
    if not math.isfinite(c) or not 0.0 <= c <= 1.0:
        return None, None, "confidence outside [0, 1]"
    if row["qtype"] == "noul":
        s = ans.strip().lower()
        return (s, c, None) if s in ("yes", "no") else (None, None, "yes/no answer is not yes or no")
    s = ans.strip()
    return (s, c, None) if s in row["options"] else (None, None, "answer is not one of the options")


def route(cands: dict, key: dict, chunk_of: dict, raw_files: dict, allow_missing_chunks: bool = False,
          superseded: frozenset = frozenset()) -> dict:
    """Pure routing. Returns {accepted: {cid: (label, conf, qid)}, routed: {cid: reason}, audit: [cid], problems,
    per-row status}. Superseded ids (A39 fix5) get status "superseded" and take no part in accept / route / audit /
    the missing-chunk check."""
    probs, got = [], defaultdict(list)
    chunk_names = set(chunk_of.values())
    for stem, raw in raw_files.items():
        pairs, pp = answer_pairs(raw)
        probs += [f"{stem}: {p}" for p in pp]
        for qid, a in pairs:
            if qid not in key:
                probs.append(f"{stem}: unknown qid {qid}")
            elif stem in chunk_names and chunk_of[qid] != stem:
                probs.append(f"{stem}: qid {qid} belongs to {chunk_of[qid]} (not used)")
            else:
                got[qid].append((stem, a))
    answered_chunks = {chunk_of[q] for q in got}
    live_chunks = {chunk_of[q] for q in key if key[q] not in superseded}   # a chunk of only superseded ids needs no answer
    missing_chunks = sorted(live_chunks - answered_chunks)
    if missing_chunks and not allow_missing_chunks:
        raise SystemExit(f"route: {len(missing_chunks)} of {len(chunk_names)} chunks have no Haiku answer "
                         f"(e.g. {missing_chunks[:3]}); finish the Haiku pass or pass --allow-missing-chunks")
    accepted, routed, status = {}, {}, {}
    for qid in sorted(key):
        cid = key[qid]
        if cid in superseded:
            status[cid] = ("superseded", None, None)
            continue
        row = cands[cid]
        ans = got.get(qid, [])
        if not ans:
            routed[cid], status[cid] = "missing", ("missing", None, None)
            continue
        uniq = {json.dumps({"answer": a.get("answer"), "confidence": a.get("confidence")}, sort_keys=True)
                for _, a in ans}
        if len(uniq) > 1:
            probs.append(f"qid {qid}: {len(ans)} different answers (conflict; routed)")
            routed[cid], status[cid] = "invalid: conflicting duplicate answers", ("invalid", None, None)
            continue
        if len(ans) > 1:
            probs.append(f"qid {qid}: answered {len(ans)} times identically (one used)")
        label, conf, why = validate(row, ans[0][1])
        if label is None:
            routed[cid], status[cid] = f"invalid: {why}", ("invalid", None, None)
        elif conf >= ACCEPT_CONF:
            accepted[cid], status[cid] = (label, conf, qid), ("accepted", label, conf)
        else:
            routed[cid], status[cid] = "low_confidence", ("low_confidence", label, conf)
    by_dom = defaultdict(list)
    for cid in sorted(accepted):
        by_dom[cands[cid]["domain"]].append(cid)
    audit = []
    for d in sorted(by_dom):
        acc = by_dom[d]
        n = math.ceil(AUDIT_SHARE * len(acc))
        audit += random.Random(f"{B.SEED}|gblock|audit|{d}").sample(acc, n)
    return {"accepted": accepted, "routed": routed, "audit": sorted(audit), "problems": probs, "status": status,
            "missing_chunks": missing_chunks}


# ------------------------------------------------------------------------------------------------------- report

def pct(a, b):
    return f"{100.0 * a / b:.1f}%" if b else "-"


def label_mix(rows_labels: list, qtype: str) -> str:
    if not rows_labels:
        return "-"
    c = Counter(rows_labels)
    if qtype == "noul":
        return f"yes {pct(c.get('yes', 0), len(rows_labels))}"
    top, n = c.most_common(1)[0]
    return f"top '{top}' {pct(n, len(rows_labels))} ({len(c)} labels)"


def report(cands, res, opus_key, haiku_files, opus_chunks, inputs_sha, n_superseded=0, fix5=False) -> str:
    """`cands` = the live candidates only (superseded ids are not in it)."""
    st, audit = res["status"], set(res["audit"])
    groups = {"domain": defaultdict(list), "card": defaultdict(list)}
    for cid, r in cands.items():
        groups["domain"][r["domain"]].append(cid)
        groups["card"][r["card_id"]].append(cid)
    opus_set = set(opus_key.values())

    def line(name, cids, extra=""):
        s = Counter(st[c][0] for c in cids)
        acc = [c for c in cids if st[c][0] == "accepted"]
        n_ans = len(cids) - s.get("missing", 0)
        return (f"| {name}{extra} | {len(cids)} | {n_ans} | {s.get('invalid', 0)} | {s.get('missing', 0)} | "
                f"{len(acc)} | {pct(len(acc), len(cids))} | {s.get('low_confidence', 0)} | "
                f"{sum(1 for c in acc if c in audit)} | {sum(1 for c in cids if c in opus_set)} | ")

    hdr = ("| {} | candidates | answered | invalid | missing | accepted (conf >= 0.80) | accept rate | "
           "low conf | audit | Opus queue | accepted label mix |")
    sep = "|---|---|---|---|---|---|---|---|---|---|---|"
    L = ["# G-block label routing, step 1 (PREREG_FINAL A39 d)", "",
         "Haiku 5.5 answered the gold-free chunks in `label/chunks/`. A valid answer with confidence >= 0.80 is "
         "accepted as given; everything else (confidence < 0.80, invalid, unanswered) goes to Opus 5.5, together with a "
         "seeded 5% audit sample of the accepted rows (ceil(5%) per domain, seed 20261013). Opus keeps a row only at "
         "confidence >= 0.85 (step 2, later); if Haiku and Opus disagree on more than 6% of a domain's audit rows, that "
         "domain's accepted rows are re-read by Opus. No label is edited by hand. Written by `tools/route.py`.", ""]
    n = len(cands)
    s = Counter(v[0] for v in st.values())
    L += ["## Totals", "",
          f"- Candidates: {n}; Haiku answer files: {len(haiku_files)}; chunks with no answer: "
          f"{len(res['missing_chunks'])}.",
          *([f"- Superseded (A39 fix5, FIX5.md): {n_superseded} ids are excluded from every count below; their "
             f"'*_b2' replacements are {'included (--fix5)' if fix5 else 'NOT routed in this run (no --fix5)'}."]
            if n_superseded else []),
          f"- Accepted (Haiku, conf >= 0.80): {s.get('accepted', 0)} ({pct(s.get('accepted', 0), n)}); "
          f"pilot reference: 53% (A39 d).",
          f"- Routed to Opus: {len(res['routed'])} = low confidence {s.get('low_confidence', 0)} + invalid "
          f"{s.get('invalid', 0)} + unanswered {s.get('missing', 0)}.",
          f"- Audit sample (accepted rows also read by Opus): {len(res['audit'])}.",
          f"- Opus queue: {len(opus_key)} items in {len(opus_chunks)} chunks (`label/opus_queue/chunks/`).",
          f"- Problems: {len(res['problems'])}.", ""]
    reasons = Counter(v for v in res["routed"].values())
    if reasons:
        L += ["Routing reasons: " + "; ".join(f"{k} {v}" for k, v in reasons.most_common()), ""]
    L += ["## Per domain", "", hdr.format("domain"), sep]
    for d in sorted(groups["domain"]):
        cids = groups["domain"][d]
        acc = [c for c in cids if st[c][0] == "accepted"]
        yn = [st[c][1] for c in acc if cands[c]["qtype"] == "noul"]
        L.append(line(d, cids) + (f"yes {pct(yn.count('yes'), len(yn))} of {len(yn)} yes/no |" if yn else "- |"))
    L += ["", "## Per card", "", hdr.format("card"), sep]
    for k in sorted(groups["card"]):
        cids = groups["card"][k]
        qt = cands[cids[0]]["qtype"]
        acc = [st[c][1] for c in cids if st[c][0] == "accepted"]
        L.append(line(k, cids, " (yes/no)" if qt == "noul" else " (choice)") + label_mix(acc, qt) + " |")
    if res["problems"]:
        L += ["", "## Problems (first 50)", ""] + [f"- {p}" for p in res["problems"][:50]]
    L += ["", "## Files", "",
          "- `label/accepted_haiku.jsonl`: {id, label, confidence, qid, audit} per accepted row (qid = the Haiku "
          "chunk qid).",
          "- `label/opus_queue/chunks/chunk_XXXX.json`: TEACH-0 items, new opaque qids; routed and audit items mixed.",
          "- `label/opus_queue/key.json` ({qid: candidate id}) and `label/opus_queue/roles.json` ({candidate id: "
          "{role, reason}}): orchestrator only, never sent to a reader.",
          "- Inputs (sha256): " + "; ".join(f"{k} {v[:16]}" for k, v in sorted(inputs_sha.items())), ""]
    return "\n".join(L)


# ------------------------------------------------------------------------------------------------------- main

def main(argv):
    dry = "--dry-run" in argv
    allow = "--allow-missing-chunks" in argv
    force = "--force" in argv
    with_fix5 = "--fix5" in argv
    hdir = Path(argv[argv.index("--haiku") + 1]) if "--haiku" in argv else B.LABEL / "haiku"
    fdir = Path(argv[argv.index("--fix5-haiku") + 1]) if "--fix5-haiku" in argv else FIX5_DIR / "haiku"
    out = Path(argv[argv.index("--out") + 1]) if "--out" in argv else B.LABEL
    kp.require_a38()
    cands, key, chunk_of, _ = load_inputs()
    superseded = load_superseded(cands)
    raw = load_haiku(kp.check_path(hdir))
    raw_path = {stem: hdir / f"{stem}.json" for stem in raw}
    if with_fix5:
        fc, fk, fco = load_fix5(superseded)
        if set(fc) & set(cands) or set(fk) & set(key):
            raise SystemExit("route: fix5 ids or qids collide with the base set")
        cands, key, chunk_of = {**cands, **fc}, {**key, **fk}, {**chunk_of, **fco}
        for stem, parsed in load_haiku(kp.check_path(fdir)).items():
            raw[f"fix5/{stem}"] = parsed
            raw_path[f"fix5/{stem}"] = fdir / f"{stem}.json"
    res = route(cands, key, chunk_of, raw, allow_missing_chunks=allow, superseded=superseded)
    live = {c: r for c, r in cands.items() if c not in superseded}
    opus_ids = sorted(set(res["routed"]) | set(res["audit"]))
    chunks, okey = B.make_chunks([cands[c] for c in opus_ids], OPUS_SECRET, f"{B.SEED}|gblock|opus|order",
                                 avoid=set(key))
    files = {f"{n}.json": B.chunk_text(items) for n, items in chunks}
    roles = {c: ({"role": "audit", "reason": "5% audit of accepted Haiku rows"} if c in set(res["audit"]) else
                 {"role": "route", "reason": res["routed"][c]}) for c in opus_ids}
    okey_text = json.dumps(okey, indent=1) + "\n"
    acc_rows = [{"id": c, "label": l, "confidence": cf, "qid": q, "audit": c in set(res["audit"])}
                for c, (l, cf, q) in sorted(res["accepted"].items())]
    s = Counter(v[0] for v in res["status"].values())
    print(f"candidates {len(live)} live (+{len(superseded)} superseded, excluded{'; fix5 replacements included' if with_fix5 else ''}); answer files {len(raw)}; accepted {s.get('accepted', 0)}; low conf "
          f"{s.get('low_confidence', 0)}; invalid {s.get('invalid', 0)}; missing {s.get('missing', 0)}; audit "
          f"{len(res['audit'])}; Opus queue {len(okey)} in {len(chunks)} chunks; problems {len(res['problems'])}")
    if dry:
        return res
    qdir = out / "opus_queue"
    okey_path = qdir / "key.json"
    if okey_path.exists() and kp.check_path(okey_path).read_text(encoding="utf-8") != okey_text and not force:
        raise SystemExit("route: label/opus_queue/key.json would change; rerun with --force to replace the queue")
    assert not any(r["id"] in superseded for r in acc_rows) and not (set(okey.values()) & superseded), "superseded id leaked"
    kp.write_jsonl(out / "accepted_haiku.jsonl", acc_rows)
    cdir = qdir / "chunks"
    if cdir.is_dir():
        for old in cdir.glob("chunk_*.json"):
            if old.name not in files:
                old.unlink()
    for name, text in files.items():
        kp.write_text(cdir / name, text)
    kp.write_text(okey_path, okey_text)
    kp.write_json(qdir / "roles.json", roles)
    kp.write_json(qdir / "MANIFEST.json", {
        "what": "G-block Opus queue (PREREG_FINAL A39 d): routed Haiku items + 5% audit, TEACH-0 item format",
        "seed": B.SEED, "accept_conf": ACCEPT_CONF, "audit_share": AUDIT_SHARE, "n_items": len(okey),
        "n_chunks": len(chunks), "roles": dict(Counter(v["role"] for v in roles.values())),
        "reasons": dict(Counter(v["reason"] for v in roles.values())),
        "key_sha256": hashlib.sha256(okey_text.encode()).hexdigest(),
        "chunks": {n: {"n": len(items), "sha256": hashlib.sha256(files[f"{n}.json"].encode()).hexdigest()}
                   for n, items in chunks}})
    inputs_sha = {"candidates": B.sha256_file(B.CAND), "key": B.sha256_file(B.KEY)}
    per_file = [f"{st}:{B.sha256_file(raw_path[st])}" for st in sorted(raw)]
    inputs_sha["haiku answers (all files)"] = hashlib.sha256("\n".join(per_file).encode()).hexdigest()
    if superseded:
        inputs_sha["superseded_fix5"] = B.sha256_file(SUPERSEDED)
    if with_fix5:
        inputs_sha["fix5 candidates"] = B.sha256_file(FIX5_CAND)
        inputs_sha["fix5 key"] = B.sha256_file(FIX5_DIR / "key.json")
    kp.write_text(out / "ROUTE.md", report(live, res, okey, raw, chunks, inputs_sha, len(superseded), with_fix5))
    return res


if __name__ == "__main__":
    main(sys.argv[1:])
