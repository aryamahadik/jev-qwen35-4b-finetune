"""OHS-3 part: fewrel_relation (20-way choice, track U).

Source: FewRel 1.0 (Han et al. 2018, EMNLP), official github.com/thunlp/FewRel, raw files data/train_wiki.json,
data/val_wiki.json and data/pid2name.json at a pinned commit (MIT licence). Not the HF tasksource copy.

Relation choice: all 80 relations (64 train_wiki + 16 val_wiki, 700 instances each) as P-ids, plain Python sorted()
(string order), random.Random(3).shuffle, first 20.
Label = Wikidata property name from pid2name.json; card definition = its Wikidata description from pid2name.json
(official, verbatim).
State: detokenised FewRel sentence with every head mention marked [[H: ...]] and every tail mention [[T: ...]].
Question: relation of head (Wikidata subject) to tail (Wikidata object).
Sampling (seed 20261026): 142 items, 7 per relation plus 1 extra for 2 seeded relations; within a relation, eligible
instances in file order are shuffled and the first n taken. Sentences that occur more than once anywhere in
train_wiki+val_wiki (after detokenisation, case/space-normalised) are dropped entirely.

Determinism: the first run downloads the pinned-commit raw files into ohs3/cache/fewrel_relation/ and records their
sha256; later runs read only the cache and verify the hashes.

No model predictions, results or LLM APIs are used.
"""
import hashlib
import json
import random
import re
import requests
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

LEAN = Path(__file__).resolve().parents[1]
CACHE = LEAN / "ohs3" / "cache" / "fewrel_relation"
OUT = LEAN / "data" / "ohs3_parts" / "fewrel_relation.jsonl"
SUMMARY = LEAN / "data" / "ohs3_parts" / "fewrel_relation_summary.json"

TASK = "fewrel_relation"
SEED = 20261026
REL_SEED = 3
N_REL = 20
N_ITEMS = 142
REPO = "thunlp/FewRel"
COMMIT = "278a2315d2138810a379cd8d5718914dc56e2582"  # master HEAD, committed 2022-05-04T14:41:14Z
COMMIT_DATE = "2022-05-04T14:41:14Z"
FILES = {"train_wiki.json": "data/train_wiki.json", "val_wiki.json": "data/val_wiki.json",
         "pid2name.json": "data/pid2name.json", "LICENSE": "LICENSE"}
RAW = "https://raw.githubusercontent.com/{repo}/{sha}/{path}"
LICENCE = "MIT (Copyright (c) 2018 THUNLP), github.com/thunlp/FewRel/blob/{}/LICENSE".format(COMMIT)
CITATION = ("Han, Zhu, Yu, Wang, Yao, Liu, Sun (2018). FewRel: A Large-Scale Supervised Few-Shot Relation "
            "Classification Dataset with State-of-the-Art Evaluation. EMNLP 2018.")
INSTRUCTIONS = "What is the relation of the head entity [[H: ...]] to the tail entity [[T: ...]] in this sentence?"

sha = lambda s: hashlib.sha256(s.encode()).hexdigest()
sha_b = lambda b: hashlib.sha256(b).hexdigest()


def fetch_snapshot():
    CACHE.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    info = {}
    for name, path in FILES.items():
        url = RAW.format(repo=REPO, sha=COMMIT, path=path)
        resp = requests.get(url, timeout=300); resp.raise_for_status(); raw = resp.content
        (CACHE / name).write_bytes(raw)
        info[name] = {"url": url, "bytes": len(raw), "sha256": sha_b(raw)}
    meta = {"repo": REPO, "commit": COMMIT, "commit_date": COMMIT_DATE, "files": info, "fetched_at_utc": started}
    (CACHE / "fetch_meta.json").write_text(json.dumps(meta, indent=1))


def load_snapshot():
    if not (CACHE / "fetch_meta.json").exists():
        fetch_snapshot()
    meta = json.loads((CACHE / "fetch_meta.json").read_text())
    assert meta["commit"] == COMMIT
    data = {}
    for name, fi in meta["files"].items():
        raw = (CACHE / name).read_bytes()
        assert sha_b(raw) == fi["sha256"], f"cache hash mismatch: {name}"
        data[name] = raw
    return meta, data


# ---------- detokenisation (spacing only; tokens themselves are never changed) ----------
NO_SPACE_BEFORE = {",", ".", ":", ";", "!", "?", ")", "]", "%", "'s", "’s", "n't", "...", "..", "”"}
NO_SPACE_AFTER = {"(", "[", "$", "£", "#", "“", "(;"}
JOIN_BOTH = {"-", "/"}


def detok(toks):
    toks = [t for t in toks if t.strip()]  # whitespace-only tokens (\n, \xa0) carry no text
    nq = sum(t == '"' for t in toks)
    balanced = nq % 2 == 0
    out, glue_next, open_q = "", True, False
    for t in toks:
        glue = glue_next
        glue_next = False
        if t in NO_SPACE_BEFORE or t in JOIN_BOTH:
            glue = True
        if t in NO_SPACE_AFTER or t in JOIN_BOTH:
            glue_next = True
        if t == '"' and balanced:
            if open_q:
                glue = True
            else:
                glue_next = True
            open_q = not open_q
        out += t if (glue or not out) else " " + t
    return out.strip()


def render(ex):
    """Return (plain sentence, marked sentence, head surface, tail surface)."""
    toks = list(ex["tokens"])
    span_of = {}
    for tag, key in (("H", "h"), ("T", "t")):
        for k, span in enumerate(ex[key][2]):
            for i in span:
                assert i not in span_of, "head/tail overlap"
                span_of[i] = (tag, k)
    marked, surf, i = [], {}, 0
    while i < len(toks):
        if i in span_of:
            tag, k = span_of[i]
            j = i
            while j < len(toks) and span_of.get(j) == (tag, k):
                j += 1
            ph = f"ZZPH{tag}{k}{i}ZZ"
            surf[ph] = f"[[{tag}: {detok(toks[i:j])}]]"
            marked.append(ph)
            i = j
        else:
            marked.append(toks[i])
            i += 1
    s = detok(marked)
    for ph, rep in surf.items():
        s = s.replace(ph, rep)
    hs = detok([toks[i] for i in ex["h"][2][0]])
    ts = detok([toks[i] for i in ex["t"][2][0]])
    return detok(toks), s, hs, ts


def norm(s):
    return re.sub(r"\s+", " ", s.lower()).strip()


def main():
    meta, data = load_snapshot()
    pid2name = json.loads(data["pid2name.json"])
    files = {"train_wiki.json": json.loads(data["train_wiki.json"]), "val_wiki.json": json.loads(data["val_wiki.json"])}
    where = {}
    for fn, d in files.items():
        for pid in d:
            assert pid not in where
            where[pid] = fn
    all_pids = sorted(where)
    assert len(all_pids) == 80 and all(len(files[where[p]][p]) == 700 for p in all_pids)

    # 1) pick 20 relations
    order = list(all_pids)
    random.Random(REL_SEED).shuffle(order)
    rels = order[:N_REL]
    names = {p: pid2name[p][0] for p in rels}
    defs = {p: pid2name[p][1] for p in rels}
    assert len(set(names.values())) == N_REL
    assert all(d and d != "No description defined" for d in defs.values())

    # 2) global duplicate-sentence count over every instance of all 80 relations
    sent_count = Counter()
    for fn, d in files.items():
        for pid, exs in d.items():
            for ex in exs:
                sent_count[norm(detok(ex["tokens"]))] += 1

    # 3) eligible pool per relation
    drops = Counter()
    pool = {}
    for p in rels:
        fn = where[p]
        items = []
        for idx, ex in enumerate(files[fn][p]):
            plain, marked, hs, ts = render(ex)
            if sent_count[norm(plain)] > 1:
                drops["duplicate_sentence"] += 1; continue
            if not (20 <= len(marked) <= 6000):
                drops["state_length"] += 1; continue
            assert marked.count("[[H: ") == len(ex["h"][2]) and marked.count("[[T: ") == len(ex["t"][2])
            items.append({"pid": p, "file": fn, "index": idx, "state": marked, "plain": plain,
                          "h": ex["h"], "t": ex["t"], "h_surface": hs, "t_surface": ts})
        pool[p] = items

    # 4) stratified sample
    rng = random.Random(SEED)
    base, extra = divmod(N_ITEMS, N_REL)
    plus_one = set(rng.sample(sorted(rels), extra))
    chosen = []
    for p in sorted(rels):
        n = base + (p in plus_one)
        items = list(pool[p])
        rng.shuffle(items)
        assert len(items) >= n, p
        chosen += items[:n]
    rng.shuffle(chosen)

    rows = []
    opt_sorted = sorted(rels, key=lambda p: names[p])
    for it in chosen:
        key = f"{it['file']}:{it['pid']}:{it['index']}"
        opts = list(opt_sorted)
        rng.shuffle(opts)
        options = [names[p] for p in opts]
        card = "\n".join(f"- {names[p]}: {defs[p]}" for p in opts)
        h, t = it["h"], it["t"]
        rows.append({
            "id": "r_" + sha(f"ohs3:{TASK}:row:{key}")[:12],
            "group_id": f"g:ohs3:{TASK}:{key}",
            "call_id": "c_" + sha(f"ohs3:{TASK}:call:{key}")[:12],
            "split": "ohs3",
            "track": "U",
            "source": TASK,
            "state": it["state"],
            "qtype": "choice",
            "instructions": INSTRUCTIONS,
            "options": options,
            "gold": names[it["pid"]],
            "role": "choice",
            "card": card,
            "meta": {
                "task": TASK,
                "dataset": "FewRel 1.0 (thunlp/FewRel GitHub)",
                "repo": f"https://github.com/{REPO}",
                "commit": COMMIT,
                "commit_date": COMMIT_DATE,
                "file": f"data/{it['file']}",
                "url": RAW.format(repo=REPO, sha=COMMIT, path=f"data/{it['file']}"),
                "pid": it["pid"],
                "index": it["index"],
                "record_id": key,
                "original_label": it["pid"],
                "label_name": names[it["pid"]],
                "head": {"name": h[0], "wikidata_id": h[1], "token_spans": h[2], "surface": it["h_surface"]},
                "tail": {"name": t[0], "wikidata_id": t[1], "token_spans": t[2], "surface": it["t_surface"]},
                "snapshot_utc": meta["fetched_at_utc"],
                "licence": LICENCE,
                "citation": CITATION,
            },
        })

    # checks
    assert len(rows) == N_ITEMS
    assert len({r["id"] for r in rows}) == len({r["group_id"] for r in rows}) == len({r["call_id"] for r in rows}) == len(rows)
    assert len({norm(r["state"]) for r in rows}) == len(rows)
    g = Counter(r["gold"] for r in rows)
    assert max(g.values()) / len(rows) <= 0.40 and set(g.values()) <= {base, base + 1}
    for r in rows:
        assert 20 <= len(r["state"]) <= 6000 and r["gold"] in r["options"] and len(r["options"]) == N_REL
        assert "ZZPH" not in r["state"]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)
    OUT.write_text(text)

    lens = sorted(len(r["state"]) for r in rows)
    summary = {
        "task": TASK,
        "rows": len(rows),
        "qtype": "choice",
        "track": "U",
        "n_options": N_REL,
        "class_balance": {f"{names[p]} ({p})": g[names[p]] for p in sorted(rels, key=lambda p: names[p])},
        "max_class_share": round(max(g.values()) / len(rows), 4),
        "instructions": INSTRUCTIONS,
        "labels": {p: {"name": names[p], "definition": defs[p], "file": where[p]} for p in sorted(rels)},
        "label_definitions_source": "official: Wikidata property label + description as shipped in FewRel data/pid2name.json (verbatim)",
        "author_written_definitions": [],
        "source": "FewRel 1.0 (Han et al. 2018), official GitHub raw files; HF tasksource copy not used",
        "citation": CITATION,
        "provenance": {"repo": f"https://github.com/{REPO}", "commit": COMMIT, "commit_date": COMMIT_DATE,
                       "files": meta["files"], "fetched_at_utc": meta["fetched_at_utc"],
                       "cache_dir": str(CACHE.relative_to(LEAN))},
        "licence": LICENCE,
        "date_range": "text from English Wikipedia as collected for FewRel (dataset released 2018; repo commit 2022-05-04); no per-item dates",
        "relation_selection": f"sorted() over the 80 P-id strings, random.Random({REL_SEED}).shuffle, first {N_REL}",
        "sampling": (f"random.Random({SEED}): sample {extra} relations (sorted P-ids) to get {base + 1} items, rest get {base}; "
                     f"per relation (sorted P-id order) shuffle eligible instances (file order) and take first n; then shuffle rows; "
                     f"options per row: names sorted alphabetically then shuffled with the same RNG; card lines follow option order"),
        "plus_one_relations": sorted(plus_one),
        "pool": {"eligible_per_relation": {p: len(pool[p]) for p in sorted(rels)}, "dropped": dict(drops),
                 "dedupe": "a sentence (detokenised, lowercased, whitespace-normalised) occurring >1 time anywhere in train_wiki+val_wiki is dropped (all copies)"},
        "state_format": ("FewRel tokens joined with rule-based spacing (no space before , . : ; ! ? ) ] % 's n't; none after ( [ $ # ; "
                         "'-' and '/' joined to both neighbours; balanced double quotes attached inward; whitespace-only tokens dropped). "
                         "Every head mention wrapped as [[H: ...]] and every tail mention as [[T: ...]] using the sentence's own tokens."),
        "state_length": {"min": lens[0], "median": lens[len(lens) // 2], "max": lens[-1]},
        "record_ids": sorted(r["meta"]["record_id"] for r in rows),
        "output_sha256": sha(text),
        "uncertain": [
            "Track U: FewRel is public since 2018 and widely used in training corpora (and on HF via tasksource), so contamination is likely.",
            "Detokenisation is heuristic: spaced hyphens ('four - level') are joined to 'four-level'; en/em dashes and single quotes keep spaces. Only spacing changes, never tokens.",
            "FewRel labels come from distant supervision against Wikidata and were human-filtered; a few sentences may express the relation only weakly, and some relation pairs are close (e.g. director vs screenwriter, part of vs owned by, operator vs owned by, spouse/sibling/mother).",
            "Some official descriptions reference other Wikidata property ids (e.g. 'Inverse property of \"occupant\" (P466)'); kept verbatim.",
            "Relations were sorted as P-id strings (plain sorted()), not numerically, before the Random(3) shuffle.",
        ],
    }
    SUMMARY.write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(json.dumps({k: v for k, v in summary.items() if k != "record_ids"}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
