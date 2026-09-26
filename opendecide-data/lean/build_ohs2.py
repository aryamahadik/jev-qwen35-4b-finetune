"""OHS-2: merge the held-out parts (ohs2/build_*.py -> data/ohs2_parts/*.jsonl), validate, decontaminate against
everything we trained, tuned or selected on, split groups into an open half (A, items may be inspected) and a sealed
half (S, aggregates only), then freeze: data/ohs2.jsonl, data/ohs2_calls.jsonl, data/ohs2_summary.json and
data/ohs2.sha256. Commit these BEFORE any model is run on them (see PREREG_OHS2.md).
  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python build_ohs2.py

Rules (mirrors build_ohs.py, without a consistency layer: OHS-2 holds only the datasets' own texts):
  * validate: required fields, split == "ohs2", gold in options (choice) or gold in {0,1} with options null (yes/no),
    unique ids, one state per call_id and one call_id per state, 20-6,000 character states, no class above 40% of a
    task (1/2 for yes/no tasks, which cannot go below 50/50), no normalised state shared by two groups.
  * decontaminate: drop every group whose state equals (after normalisation) or shares a 12-word run with any text in
    our training/dev/eval files: every data/**/*.jsonl (including data/v11_parts/**) except the held-out files
    (data/ohs*.jsonl, data/ohs_parts/, data/ohs2_parts/), plus ../data/**/*.jsonl. Every string field is scanned
    (state, text, instructions, card, options, meta, ...). A state shorter than 12 words is checked as one run.
    OHS-1 files are held out and are never opened here.
  * halves: group-level, A if int(sha256("ohs2:" + group_id)) is even, else S.
Deterministic, CPU only, no network, no model calls.
"""
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE / "data"
PARTS = D / "ohs2_parts"
EXTRA_DIRS = [HERE.parent / "data"]  # the pre-lean pipeline's data (opendecide-data/data)
GRAM = 12
MAX_OPTIONS = 255
MAX_SHARE = 0.40
LEN_RANGE = (20, 6000)
PART_SUMMARIES = {"arxiv_fresh": HERE / "ohs2/arxiv_fresh_cache/summary.json", "misc": HERE / "ohs2/misc_summary.json",
                  "science": PARTS / "science_summary.json"}
REQUIRED = ["id", "group_id", "call_id", "split", "track", "source", "state", "qtype", "instructions", "options", "gold",
            "role", "card", "meta"]

words = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).split()
sha = lambda s: hashlib.sha256(s.encode()).hexdigest()


def grams(w, n=GRAM):
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def is_heldout(p: Path, root: Path) -> bool:
    parts = [x.lower() for x in p.relative_to(root).parts]
    return parts[0].startswith("ohs") or any(x in ("ohs", "ohs_parts", "ohs2_parts", "bench") or x.startswith("ohs")
                                             for x in parts[:-1])


def touched_files():
    fs = [p for p in sorted(D.rglob("*.jsonl")) if not is_heldout(p, D)]
    for root in EXTRA_DIRS:
        if root.exists():
            fs += [p for p in sorted(root.rglob("*.jsonl")) if not is_heldout(p, root)]
    return fs


def strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from strings(v)


def task_of(r):
    return r["meta"].get("task") or r["source"]


def validate(rows):
    errs = []
    ids = Counter(r["id"] for r in rows)
    errs += [f"duplicate id {i}" for i, c in ids.items() if c > 1]
    by_call, by_state, by_norm = defaultdict(set), defaultdict(set), defaultdict(set)
    for r in rows:
        miss = [k for k in REQUIRED if k not in r]
        if miss:
            errs.append(f"{r.get('id')}: missing {miss}")
            continue
        if r["split"] != "ohs2":
            errs.append(f"{r['id']}: split {r['split']!r}")
        if r["qtype"] == "choice":
            o = r["options"]
            if not (isinstance(o, list) and len(set(o)) == len(o) and 2 <= len(o) <= MAX_OPTIONS and r["gold"] in o):
                errs.append(f"{r['id']}: gold not in options / bad options")
            if r["role"] != "choice":
                errs.append(f"{r['id']}: choice row with role {r['role']!r}")
        elif r["qtype"] == "noul":
            if not (r["gold"] in (0, 1) and not isinstance(r["gold"], bool) and r["options"] is None):
                errs.append(f"{r['id']}: yes/no row needs gold 0/1 and options null")
            if r["role"] != "aff":
                errs.append(f"{r['id']}: yes/no row with role {r['role']!r}")
        else:
            errs.append(f"{r['id']}: qtype {r['qtype']!r}")
        if not (LEN_RANGE[0] <= len(r["state"]) <= LEN_RANGE[1]):
            errs.append(f"{r['id']}: state length {len(r['state'])}")
        if r["card"] is not None and not (isinstance(r["card"], str) and r["card"].strip()
                                          and all(l.startswith("- ") for l in r["card"].split("\n"))):
            errs.append(f"{r['id']}: card must be null or '- <option>: <definition>' lines")
        by_call[r["call_id"]].add(r["state"])
        by_state[r["state"]].add(r["call_id"])
        by_norm[" ".join(words(r["state"]))].add(r["group_id"])
    errs += [f"call_id {c} spans {len(s)} different states" for c, s in by_call.items() if len(s) > 1]
    errs += [f"one state has {len(c)} call_ids: {sorted(c)}" for s, c in by_state.items() if len(c) > 1]
    errs += [f"normalised state shared by groups {sorted(g)}" for g in by_norm.values() if len(g) > 1]
    # balance: no class above 40% of a task (a yes/no task can do no better than 50/50, so its cap is 1/2)
    by_task, n_cls = defaultdict(Counter), defaultdict(set)
    for r in rows:
        by_task[task_of(r)][str(r["gold"])] += 1
        n_cls[task_of(r)] |= set(r["options"] or ["1", "0"])
    for t, c in by_task.items():
        cap = max(MAX_SHARE, 1 / len(n_cls[t]))
        if max(c.values()) > cap * sum(c.values()):
            errs.append(f"task {t}: class share {max(c.values()) / sum(c.values()):.2f} > {cap:.2f}")
    return errs


def decontaminate(rows):
    """Returns ({group_id: reason}, scan stats). Index the (small) OHS-2 side, stream our (large) side."""
    full, gram_owner, short = defaultdict(set), defaultdict(set), defaultdict(set)
    short_len_by_first = defaultdict(set)
    for r in rows:
        w = words(r["state"])
        full[" ".join(w)].add(r["group_id"])
        for g in grams(w):
            gram_owner[g].add(r["group_id"])
        if 0 < len(w) < GRAM:  # too short for a 12-word run: the whole state is the run
            short[" ".join(w)].add(r["group_id"])
            short_len_by_first[w[0]].add(len(w))
    hit, seen, nfiles, examples = {}, set(), 0, {}
    for p in touched_files():
        nfiles += 1
        with open(p, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    x = json.loads(line)
                except Exception:  # noqa: BLE001
                    continue
                for t in strings(x):
                    if len(t) < 20:
                        continue
                    h = hash(t)
                    if h in seen:
                        continue
                    seen.add(h)
                    w = words(t)
                    nt = " ".join(w)
                    src = str(p.relative_to(HERE.parent))
                    for g in full.get(nt, ()):
                        hit.setdefault(g, "exact text"); examples.setdefault(g, src)
                    for i in range(len(w) - GRAM + 1):
                        for g in gram_owner.get(" ".join(w[i:i + GRAM]), ()):
                            hit.setdefault(g, "shared 12-word run"); examples.setdefault(g, src)
                    if short:
                        for i, w0 in enumerate(w):
                            for L in short_len_by_first.get(w0, ()):
                                for g in short.get(" ".join(w[i:i + L]), ()):
                                    hit.setdefault(g, "short state contained"); examples.setdefault(g, src)
    return hit, {"files_scanned": nfiles, "unique_texts_scanned": len(seen), "hit_files": examples}


def cross_group_runs(rows):
    """Diagnostic: pairs of different groups inside OHS-2 that share a 12-word run (should be none)."""
    owner = defaultdict(set)
    for r in rows:
        for g in grams(words(r["state"])):
            owner[g].add(r["group_id"])
    pairs = Counter()
    for gs in owner.values():
        if len(gs) > 1:
            for a in gs:
                for b in gs:
                    if a < b:
                        pairs[(a, b)] += 1
    return pairs


def main():
    rows, part_files = [], {}
    for f in sorted(PARTS.glob("*.jsonl")):
        text = f.read_text(encoding="utf-8")
        part_files[f.name] = sha(text)
        for l in text.splitlines():
            if l.strip():
                r = json.loads(l)
                r["meta"].setdefault("part", f.stem)
                rows.append(r)
    n_in = len(rows)
    errs = validate(rows)
    if errs:
        print("VALIDATION FAILED:\n  " + "\n  ".join(errs[:50]))
        sys.exit(1)
    pairs = cross_group_runs(rows)
    if pairs:  # checked by hand at freeze time: shared table headers (tabfact) and shared topic + argument openings
        print(f"info: {len(pairs)} pairs of different groups share a 12-word run inside OHS-2 (listed in the summary)")

    hit, scan = decontaminate(rows)
    dropped = [{"group_id": g, "reason": hit[g], "first_file": scan["hit_files"][g],
                "rows": sorted(r["id"] for r in rows if r["group_id"] == g)} for g in sorted(hit)]
    rows = [r for r in rows if r["group_id"] not in hit]
    for d in dropped:
        print("dropped for overlap:", d)

    # open / sealed halves by group hash
    for r in rows:
        r["meta"]["half"] = "A" if int(sha("ohs2:" + r["group_id"]), 16) % 2 == 0 else "S"
    calls = {}
    for r in rows:
        calls.setdefault(r["call_id"], {"call_id": r["call_id"], "state": r["state"], "row_ids": []})["row_ids"].append(r["id"])

    files = {"ohs2.jsonl": rows, "ohs2_calls.jsonl": list(calls.values())}
    digest, hashes = [], {}
    for name, items in files.items():
        text = "".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in items)
        (D / name).write_text(text, encoding="utf-8")
        hashes[name] = sha(text)
        digest.append(f"{hashes[name]}  {name}")
    (D / "ohs2.sha256").write_text("\n".join(digest) + "\n")

    # summary
    part_summ = {}
    for k, p in PART_SUMMARIES.items():
        if p.exists():
            part_summ[k] = json.loads(p.read_text())
    tasks = {}
    by_task = defaultdict(list)
    for r in rows:
        by_task[task_of(r)].append(r)
    for t in sorted(by_task):
        rs = by_task[t]
        bal = Counter(str(r["gold"]) for r in rs)
        r0 = rs[0]
        ps = part_summ.get(r0["meta"]["part"], {}).get("tasks", {}).get(t, {})
        tasks[t] = {
            "part": r0["meta"]["part"], "source": r0["source"], "track": r0["track"], "qtype": r0["qtype"],
            "n": len(rs), "groups": len({r["group_id"] for r in rs}),
            "n_options": sorted({len(r["options"]) for r in rs if r["options"]}) or [2],
            "balance": dict(sorted(bal.items())), "max_class_share": round(max(bal.values()) / len(rs), 3),
            "licence": r0["meta"].get("licence"),
            "orig_split": r0["meta"].get("orig_split") or r0["meta"].get("source_split") or ps.get("orig_split") or ps.get("split"),
            "rows_with_card": sum(bool(r["card"]) for r in rs),
            "halves_rows": dict(sorted(Counter(r["meta"]["half"] for r in rs).items())),
        }
    groups = {r["group_id"]: r["meta"]["half"] for r in rows}
    summ = {
        "benchmark": "OHS-2", "split": "ohs2", "rows_in": n_in, "rows": len(rows), "calls": len(calls),
        "groups": len(groups), "tasks": len(tasks), "dropped_for_overlap": dropped,
        "by_part": dict(Counter(r["meta"]["part"] for r in rows)),
        "by_source": dict(Counter(r["source"] for r in rows)), "by_track": dict(Counter(r["track"] for r in rows)),
        "by_qtype": dict(Counter(r["qtype"] for r in rows)),
        "halves": {"rows": dict(sorted(Counter(r["meta"]["half"] for r in rows).items())),
                   "groups": dict(sorted(Counter(groups.values()).items()))},
        "max_options": max(len(r["options"] or [0, 1]) for r in rows),
        "state_chars": {"min": min(len(r["state"]) for r in rows), "max": max(len(r["state"]) for r in rows)},
        "yes_no_rows": sum(r["qtype"] == "noul" for r in rows),
        "decontamination": {"files_scanned": scan["files_scanned"], "unique_texts_scanned": scan["unique_texts_scanned"],
                            "rule": "normalised exact state or shared 12-word run (whole state if under 12 words) with any "
                                    "string in data/**/*.jsonl minus held-out files, and ../data/**/*.jsonl",
                            "cross_group_12gram_pairs_inside_ohs2": [[a, b, n] for (a, b), n in sorted(pairs.items())],
                            "cross_group_note": "same-task boilerplate only (tabfact table headers; argq topic line plus "
                                                "argument opening); distinct items, so groups are kept separate"},
        "per_task": tasks, "part_files_sha256": part_files, "sha256": hashes,
    }
    (D / "ohs2_summary.json").write_text(json.dumps(summ, indent=1, ensure_ascii=False))
    brief = {k: summ[k] for k in ("rows", "calls", "groups", "tasks", "by_part", "by_source", "by_track", "by_qtype", "halves",
                                  "max_options", "decontamination")}
    brief["dropped_for_overlap"] = len(dropped)
    brief["decontamination"] = {k: v for k, v in brief["decontamination"].items() if not k.startswith("cross_group")}
    print(json.dumps(brief, indent=1))


if __name__ == "__main__":
    main()
