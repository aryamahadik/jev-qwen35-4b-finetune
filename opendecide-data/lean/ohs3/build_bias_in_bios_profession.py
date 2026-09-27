"""OHS-3 part: bias_in_bios_profession (choice, 20 options, track U).

Source: Bias in Bios (De-Arteaga et al. 2019, MIT), the Ravfogel et al. 2020 version on the Hugging Face Hub,
LabHC/bias_in_bios, split test, pinned revision 052f01de644dba841176e0449528b41f27d94a61.
Question: which profession does the biography describe? Options: the 20 most frequent professions in test.

Determinism: the first run downloads the test parquet at the pinned revision, checks its sha256, reads ONLY the
columns hard_text and profession (the gender column is never loaded), and saves a reduced snapshot
(row_index, hard_text, profession) as gzipped JSONL under ohs3/cache/bias_in_bios_profession/. The downloaded
parquet is deleted. Every later run reads only that snapshot, so rows are identical. Sampling seed: 20261026.

Redaction: every whole-word occurrence (case-insensitive, singular or plural) of any of the 20 option names is
replaced by "[PROFESSION]" in every state, so the gold name cannot leak and the redaction itself is not a cue.
No other edits (leading/trailing whitespace stripped only).

No model predictions, results or LLM APIs are used.
"""
import gzip
import hashlib
import json
import os
import random
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import requests

LEAN = Path(__file__).resolve().parents[1]
CACHE = LEAN / "ohs3" / "cache" / "bias_in_bios_profession"
SNAP = CACHE / "test_hard_text_profession.jsonl.gz"
FETCH_META = CACHE / "fetch_meta.json"
OUT = LEAN / "data" / "ohs3_parts" / "bias_in_bios_profession.jsonl"
SUMMARY = LEAN / "data" / "ohs3_parts" / "bias_in_bios_profession_summary.json"

TASK = "bias_in_bios_profession"
SEED = 20261026
TIE_SEED = 3  # selection_criteria.md section 5: ties at the 20-label cap broken by random.Random(3)
N_ITEMS = 142
N_LABELS = 20
DATASET = "LabHC/bias_in_bios"
REVISION = "052f01de644dba841176e0449528b41f27d94a61"
SPLIT = "test"
PARQUET = "data/test-00000-of-00001-5598c840ce8de1ee.parquet"
PARQUET_SHA256 = "ee98d9b19e1e209ff91b34a2d46606e13330ca28eca0d0a5b1220f3a77ab0763"
URL = f"https://huggingface.co/datasets/{DATASET}/resolve/{REVISION}/{PARQUET}"
CARD_URL = f"https://huggingface.co/datasets/{DATASET}/blob/{REVISION}/README.md"
LICENCE = ("MIT (dataset card of LabHC/bias_in_bios at the pinned revision; original release "
           "https://github.com/microsoft/biosbias, MIT)")
ATTRIBUTION = ("Bias in Bios: De-Arteaga et al. 2019 (FAT* '19, doi:10.1145/3287560.3287572); version of "
               "Ravfogel et al. 2020 (ACL), distributed as LabHC/bias_in_bios on the Hugging Face Hub.")

# Official numeric label -> profession name, from the dataset card (README.md) at the pinned revision.
CARD_NAMES = {
    0: "accountant", 1: "architect", 2: "attorney", 3: "chiropractor", 4: "comedian", 5: "composer", 6: "dentist",
    7: "dietitian", 8: "dj", 9: "filmmaker", 10: "interior_designer", 11: "journalist", 12: "model", 13: "nurse",
    14: "painter", 15: "paralegal", 16: "pastor", 17: "personal_trainer", 18: "photographer", 19: "physician",
    20: "poet", 21: "professor", 22: "psychologist", 23: "rapper", 24: "software_engineer", 25: "surgeon",
    26: "teacher", 27: "yoga_teacher",
}
DISPLAY_OVERRIDE = {"dj": "DJ"}

# Author-written, frozen 2026-09-26: one short neutral definition per label (paraphrasing O*NET-style titles).
# Written for every profession on the card, before sampling; only the 20 used as options appear on the card.
DEFS = {
    "accountant": "Prepares, examines and analyzes financial records, and advises on accounts, taxes and audits.",
    "architect": "Plans and designs buildings and other structures.",
    "attorney": "A licensed lawyer who advises and represents clients in legal matters.",
    "chiropractor": "Treats problems of the spine, joints and muscles, mainly by manual adjustment.",
    "comedian": "Performs humorous material, such as stand-up comedy, for an audience.",
    "composer": "Writes original music for performance or recording.",
    "dentist": "Diagnoses and treats problems of the teeth, gums and mouth.",
    "dietitian": "Plans and advises on food and nutrition to promote health or manage disease.",
    "dj": "Selects and plays recorded music for an audience, at events, clubs or on radio.",
    "filmmaker": "Makes films, for example by directing, producing or shooting them.",
    "interior_designer": "Plans and designs the interior spaces of buildings.",
    "journalist": "Researches, writes or presents news and stories for print, broadcast or online media.",
    "model": "Poses for photographers or artists, or shows clothing and products in fashion shows or advertising.",
    "nurse": "Provides and coordinates patient care and health education as a nursing professional.",
    "painter": "An artist who creates works with paint.",
    "paralegal": "Assists lawyers with legal research, documents and case preparation.",
    "pastor": "A member of the clergy who leads a Christian congregation.",
    "personal_trainer": "Leads and instructs individuals in physical exercise and fitness.",
    "photographer": "Takes photographs, professionally or as an artist.",
    "physician": "A medical doctor who diagnoses and treats illness and injury.",
    "poet": "Writes poetry.",
    "professor": "Teaches and does research at a college or university.",
    "psychologist": "Studies the mind and behavior, and assesses or treats mental, emotional or behavioral problems.",
    "rapper": "Writes and performs rap or hip-hop music.",
    "software_engineer": "Designs, develops and tests computer software.",
    "surgeon": "A medical doctor who treats disease or injury by operating.",
    "teacher": "Instructs students in one or more subjects, usually in a school.",
    "yoga_teacher": "Leads and instructs yoga classes.",
}
INSTRUCTIONS = "What is this person's profession?"
MASK = "[PROFESSION]"

sha = lambda s: hashlib.sha256(s.encode()).hexdigest()


def display(name):
    return DISPLAY_OVERRIDE.get(name, name.replace("_", " ").capitalize())


def fetch_snapshot():
    import pyarrow.parquet as pq

    CACHE.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    tmp = CACHE / "_download.parquet"
    with requests.get(URL, stream=True, timeout=300) as r:
        r.raise_for_status()
        h = hashlib.sha256()
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
                h.update(chunk)
    got = h.hexdigest()
    if got != PARQUET_SHA256:
        tmp.unlink()
        raise SystemExit(f"parquet sha256 mismatch: {got}")
    # Read only the two allowed columns; the gender column is never loaded.
    t = pq.read_table(tmp, columns=["hard_text", "profession"]).to_pydict()
    tmp.unlink()
    lines = "".join(json.dumps({"row_index": i, "hard_text": x, "profession": p}, ensure_ascii=False) + "\n"
                    for i, (x, p) in enumerate(zip(t["hard_text"], t["profession"])))
    SNAP.write_bytes(gzip.compress(lines.encode(), mtime=0))
    meta = {"dataset": DATASET, "revision": REVISION, "split": SPLIT, "file": PARQUET, "url": URL,
            "parquet_sha256": got, "columns_read": ["hard_text", "profession"], "n_rows": len(t["profession"]),
            "snapshot_file": SNAP.name, "snapshot_sha256": hashlib.sha256(SNAP.read_bytes()).hexdigest(),
            "fetched_at_utc": started}
    FETCH_META.write_text(json.dumps(meta, indent=1))


def load_snapshot():
    if not FETCH_META.exists() or not SNAP.exists():
        fetch_snapshot()
    meta = json.loads(FETCH_META.read_text())
    raw = SNAP.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == meta["snapshot_sha256"], "cached snapshot changed"
    recs = [json.loads(l) for l in gzip.decompress(raw).decode().split("\n") if l]
    assert len(recs) == meta["n_rows"]
    assert all(set(r) == {"row_index", "hard_text", "profession"} for r in recs)
    return meta, recs


def norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def build_redactor(names):
    # Longest names first so multi-word names are matched before any single word inside them.
    alts = []
    for n in sorted(names, key=lambda x: (-len(x), x)):
        words = n.replace("_", " ").split()
        stem = r"\s+".join(re.escape(w) for w in words)
        alts.append(stem + r"(?:e?s)?")
    return re.compile(r"(?<!\w)(?:" + "|".join(alts) + r")(?!\w)", re.I)


def main():
    meta, recs = load_snapshot()
    counts = Counter(r["profession"] for r in recs)

    # 20 most frequent professions in test; ties broken by a seeded shuffle (Random(3)) before a stable sort.
    ids = sorted(counts)
    random.Random(TIE_SEED).shuffle(ids)
    ranked = sorted(ids, key=lambda k: -counts[k])
    keep = ranked[:N_LABELS]
    boundary_tie = counts[ranked[N_LABELS - 1]] == counts[ranked[N_LABELS]]
    keep_names = [CARD_NAMES[k] for k in keep]
    rx = build_redactor(keep_names)

    # Dedup: drop every record whose normalised text occurs more than once in the split (any label).
    ncount = Counter(norm(r["hard_text"]) for r in recs)
    drops = Counter()
    pool = {k: [] for k in keep}
    for r in recs:
        p = r["profession"]
        if p not in pool:
            drops["profession_not_in_top20"] += 1; continue
        text = (r["hard_text"] or "").strip()
        if ncount[norm(r["hard_text"] or "")] > 1:
            drops["duplicate_text"] += 1; continue
        log = [m.group(0) for m in rx.finditer(text)]
        state = rx.sub(MASK, text)
        if not (20 <= len(state) <= 6000):
            drops["state_length"] += 1; continue
        pool[p].append({"idx": r["row_index"], "pid": p, "state": state, "redactions": log})

    # Stratified: floor(142/20)=7 per label; the 2 remaining items go to labels in seeded order.
    rng = random.Random(SEED)
    base, rem = divmod(N_ITEMS, N_LABELS)
    order = sorted(keep)
    rng.shuffle(order)
    quota = {k: base + (1 if i < rem else 0) for i, k in enumerate(order)}
    chosen = []
    for k in sorted(keep):
        items = sorted(pool[k], key=lambda x: x["idx"])
        rng.shuffle(items)
        if len(items) < quota[k]:
            raise SystemExit(f"not enough items for {CARD_NAMES[k]}: {len(items)}")
        chosen += items[:quota[k]]
    rng.shuffle(chosen)

    opt_names = [display(CARD_NAMES[k]) for k in sorted(keep)]
    rows = []
    for it in chosen:
        name = CARD_NAMES[it["pid"]]
        opts = list(opt_names)
        rng.shuffle(opts)
        card = "\n".join(f"- {o}: {DEFS[next(n for n in keep_names if display(n) == o)]}" for o in opts)
        key = f"{SPLIT}:{it['idx']}"
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
            "options": opts,
            "gold": display(name),
            "role": "choice",
            "card": card,
            "meta": {
                "task": TASK,
                "dataset": DATASET,
                "revision": REVISION,
                "split": SPLIT,
                "file": PARQUET,
                "row_index": it["idx"],
                "profession_id": it["pid"],
                "original_label": name,
                "url": f"https://huggingface.co/datasets/{DATASET}/viewer/default/{SPLIT}?row={it['idx']}",
                "licence": LICENCE,
                "attribution": ATTRIBUTION,
                "redactions": it["redactions"],
            },
        })

    # checks
    assert len(rows) == N_ITEMS
    assert len({r["id"] for r in rows}) == len({r["group_id"] for r in rows}) == len({r["call_id"] for r in rows}) == len(rows)
    assert len({norm(r["state"]) for r in rows}) == len(rows)
    g = Counter(r["gold"] for r in rows)
    assert len(g) == N_LABELS and max(g.values()) <= 0.4 * len(rows)
    for r in rows:
        assert 20 <= len(r["state"]) <= 6000
        assert r["gold"] in r["options"] and len(r["options"]) == N_LABELS
        assert not rx.search(r["state"]), r["id"]
        assert "gender" not in json.dumps(r["meta"])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)
    OUT.write_text(text)

    lens = sorted(len(r["state"]) for r in rows)
    red_rows = [r for r in rows if r["meta"]["redactions"]]
    red_by_gold = Counter(r["gold"] for r in red_rows)
    red_words = Counter(w.lower() for r in rows for w in r["meta"]["redactions"])
    summary = {
        "task": TASK,
        "rows": len(rows),
        "qtype": "choice",
        "track": "U",
        "n_options": N_LABELS,
        "options": opt_names,
        "class_balance": dict(sorted(g.items())),
        "max_class_share": round(max(g.values()) / len(rows), 4),
        "instructions": INSTRUCTIONS,
        "card_definitions": {display(n): DEFS[n] for n in sorted(keep_names)},
        "label_names_source": f"official: profession names and numeric ids from the dataset card ({CARD_URL}); underscores shown as spaces, first letter capitalised, 'dj' shown as 'DJ'",
        "label_definitions_source": "author-written: one short neutral definition per label, written once on 2026-09-26 and frozen (O*NET-style paraphrase); no official definitions exist",
        "author_written_definitions": {display(n): DEFS[n] for n in sorted(keep_names)},
        "source": f"Hugging Face Hub dataset {DATASET}, split {SPLIT}, file {PARQUET}",
        "provenance": {
            "dataset": DATASET, "revision": REVISION, "revision_last_modified": "2023-09-10T15:41:38Z",
            "split": SPLIT, "file_url": URL, "parquet_sha256": meta["parquet_sha256"],
            "columns_read": meta["columns_read"], "fetched_at_utc": meta["fetched_at_utc"],
            "cache": str(SNAP.relative_to(LEAN)), "cache_sha256": meta["snapshot_sha256"],
            "record_ids": "meta.row_index = 0-based row index in the test parquet",
        },
        "licence": LICENCE,
        "attribution": ATTRIBUTION,
        "date_range": "not applicable: classic dataset (Common Crawl biographies collected for De-Arteaga et al. 2019; HF revision 2023-09-10); track U",
        "label_cap": {
            "rule": f"20 most frequent professions in the test split; ties broken by random.Random({TIE_SEED}) shuffle then stable sort by count",
            "tie_at_boundary": boundary_tie,
            "kept_counts_in_test": {CARD_NAMES[k]: counts[k] for k in keep},
            "dropped_labels_counts_in_test": {CARD_NAMES[k]: counts[k] for k in ranked[N_LABELS:]},
        },
        "pool": {"rows_in_split": len(recs), "eligible_per_label": {CARD_NAMES[k]: len(pool[k]) for k in keep},
                 "dropped": dict(drops)},
        "sampling": (f"per label: sort eligible by row_index, random.Random({SEED}) shuffle, take quota "
                     f"({base} each; +1 for the first {rem} labels of a seeded shuffle of profession ids: "
                     f"{[CARD_NAMES[k] for k in order[:rem]]}); rows then shuffled; options shuffled per row with the same RNG"),
        "state_format": "hard_text from the source (bio with the first sentence, which states the title, already removed by the dataset), whitespace-stripped, option names masked",
        "state_length": {"min": lens[0], "median": lens[len(lens) // 2], "max": lens[-1]},
        "redaction": {
            "replacement": MASK,
            "rule": "every whole-word, case-insensitive occurrence of any of the 20 option names (multi-word names allow any whitespace; optional plural 's'/'es'), in every row regardless of gold",
            "pattern": rx.pattern,
            "rows_with_redaction": len(red_rows),
            "rows_with_redaction_by_gold": dict(sorted(red_by_gold.items())),
            "matches_by_word": dict(red_words.most_common()),
            "per_row_log": "meta.redactions",
        },
        "gender_column": "never loaded (parquet read with columns=['hard_text','profession']) and not stored in rows, meta or cache",
        "row_indices": sorted(r["meta"]["row_index"] for r in rows),
        "output_sha256": sha(text),
        "uncertain": [
            "Definitions are author-written (no official definitions exist for the Bias in Bios labels).",
            "Labels come from the title in the removed first sentence of each web bio (automatic extraction by the dataset creators), so some labels may be noisy, and several pairs overlap (physician/surgeon, professor/teacher, filmmaker/photographer, poet/journalist).",
            "Redaction masks all 20 option names in every row (not only the gold name), so redaction is not a cue; related words (e.g. 'nursing', 'surgery', 'photography', 'dental', 'modeling') are left as content, so many items stay decidable from the bio. 'model(s)' is also masked where it has a non-profession sense (e.g. 'business model').",
            "Bias in Bios texts are public web biographies from Common Crawl; the MIT licence is as stated on the dataset card and the microsoft/biosbias repository.",
            "The HF mirror (LabHC) is the Ravfogel et al. 2020 version maintained by the Laboratoire Hubert Curien, not the original authors' scraper output; the spec pins this revision.",
        ],
    }
    SUMMARY.write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(json.dumps({k: v for k, v in summary.items() if k not in ("row_indices",)}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
