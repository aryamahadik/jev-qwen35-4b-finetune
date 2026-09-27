"""OHS-3 part: causal_news_corpus (natural yes/no, track U).

Source: Causal News Corpus V2 (Tan et al. 2022, CASE@EMNLP 2022; V2 for CASE 2023), official GitHub repo
tanfiona/CausalNewsCorpus, file data/V2/dev_subtask1.csv, pinned to commit PINNED_SHA (CC0 1.0).
NOT the Hugging Face conversion.

Question: is the sentence Causal? Gold 1 = label 1 (Causal), gold 0 = label 0 (Non-Causal); 72/72 from dev
(185/155 available, so no top-up from train is needed; the train top-up path is kept but unused).
State: the sentence text exactly as in the CSV (only leading/trailing whitespace stripped). The corpus is
pre-tokenised (" ," spacing); that spacing is the source's own form and is kept. Identical (normalised) sentences
are deduplicated.

Card: official definition from the CNC annotation manual (documentation/Event_Causality_Manual_for_CASE_2022_Public.pdf
in the same repo at the same commit), section 3.1.1 "General Definition", quoted near-verbatim (definitions verbatim; connective examples condensed; joined into one card line).

Determinism: the first run downloads the raw files at the pinned commit into ohs3/cache/causal_news_corpus/ and
checks their git blob hashes against the hashes GitHub listed for that commit. Later runs read only the cache.
Sampling seed: 20261026.

No model predictions, results or LLM APIs are used.
"""
import csv
import hashlib
import io
import json
import random
import re
import sys
import time
from collections import Counter
from pathlib import Path

import requests

LEAN = Path(__file__).resolve().parents[1]
CACHE = LEAN / "ohs3" / "cache" / "causal_news_corpus"
OUT = LEAN / "data" / "ohs3_parts" / "causal_news_corpus.jsonl"
SUMMARY = LEAN / "data" / "ohs3_parts" / "causal_news_corpus_summary.json"

TASK = "causal_news_corpus"
SEED = 20261026
N_PER_CLASS = 72
REPO = "tanfiona/CausalNewsCorpus"
PINNED_SHA = "4796c7e89d9b346f8e1280dac441dacde2be6b86"  # master HEAD, committed 2024-02-09T08:24:19Z
PINNED_SHA_DATE = "2024-02-09T08:24:19Z"
SNAPSHOT_FETCHED = "2026-09-26"
# path in repo -> expected git blob sha (from GitHub contents/trees API at PINNED_SHA)
FILES = {
    "data/V2/dev_subtask1.csv": "f9c95a0a24e95aea540101aeb4855e5ace6c2ed1",
    "data/V2/train_subtask1.csv": "096589064a3eba51f4ae00dd20568abf0ec9fcb7",
    "data/V2/README.md": "111670f00e4652c9e7c0ab06705c5dd8c3c2b12f",
    "documentation/Event_Causality_Manual_for_CASE_2022_Public.pdf": "2f57ec4d3b35321425076c86bff0e53a7c51ce6d",
    "LICENSE": "0e259d42c996742e9e3cba14c677129b2c1b6311",
}
RAW = "https://raw.githubusercontent.com/{repo}/{sha}/{path}"
BLOB_URL = "https://github.com/{repo}/blob/{sha}/{path}"
LICENCE = "CC0-1.0 (repository LICENSE: Creative Commons CC0 1.0 Universal)"
CITATION = ("Tan et al. (2022), The Causal News Corpus: Annotating Causal Relations in Event Sentences from News, LREC 2022 "
            "(documentation/2022.lrec-1.246.pdf in the repo); Tan et al. (2022), Event Causality Identification with Causal "
            "News Corpus - Shared Task 3, CASE@EMNLP 2022.")

ASKED_LABEL = "Causal"
MANUAL_PATH = "documentation/Event_Causality_Manual_for_CASE_2022_Public.pdf"
# Verbatim quotes from the manual, section 3.1.1 General Definition (PDTB-3 CONTINGENCY and its four Level-2 senses)
# plus the exclusion sentence and the Subtask 1 description from section 1.
ASKED_DEF = (
    "The sentence contains cause-effect meaning. The label follows the PDTB-3 definition for CONTINGENCY: "
    "\"one argument provides the reason, explanation or justification for the situation described by the other.\" "
    "It covers four senses: CAUSE: Arg1 and Arg2 are causally influenced but not in a conditional relation "
    "(example connectives \"because\", \"since\"); PURPOSE: One Arg describes the goal while the other Arg describes "
    "the action undertaken to achieve the goal (\"in order to\", \"so that\"); CONDITION: One Arg presents an "
    "unrealized situation, that when realized, would lead to the situation described by the other Arg (\"if\", "
    "\"as long as\"); NEGATIVE-CONDITION: One Arg presents an unrealized situation, that if it does not occur, would "
    "lead to the situation described by the other Arg (\"till\", \"unless\"). Senses that provide reasons for the "
    "speaker to utter a speech, or the hearer to have a belief, are not annotated as causal."
)
INSTRUCTIONS = "Is this sentence causal?"
CARD = f"- {ASKED_LABEL}: {ASKED_DEF}"

sha256 = lambda b: hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


def git_blob_sha(b):
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def fetch(path):
    url = RAW.format(repo=REPO, sha=PINNED_SHA, path=path)
    for attempt in range(5):
        try:
            r = requests.get(url, timeout=120)
            r.raise_for_status()
            return r.content
        except Exception as e:  # noqa: BLE001
            print(f"retry {attempt} {path}: {e}", file=sys.stderr)
            time.sleep(3 * (attempt + 1))
    raise SystemExit(f"download failed: {url}")


def load_snapshot():
    CACHE.mkdir(parents=True, exist_ok=True)
    info = {}
    for path, blob in FILES.items():
        f = CACHE / Path(path).name
        if not f.exists():
            f.write_bytes(fetch(path))
        b = f.read_bytes()
        gb = git_blob_sha(b)
        if blob is not None and gb != blob:
            raise SystemExit(f"git blob mismatch for {path}: {gb} != {blob}")
        info[path] = {"cache_file": str(f.relative_to(LEAN)), "git_blob_sha": gb, "sha256": sha256(b), "bytes": len(b),
                      "raw_url": RAW.format(repo=REPO, sha=PINNED_SHA, path=path)}
    return info


def read_csv(name):
    text = (CACHE / name).read_bytes().decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s.lower())).strip()


def main():
    files = load_snapshot()
    dev = read_csv("dev_subtask1.csv")
    train = read_csv("train_subtask1.csv")
    train_norm = {norm(r["text"]) for r in train}

    drops = Counter()
    pool = {1: [], 0: []}
    seen = set()
    for pos, r in enumerate(dev):
        text = r["text"].strip()
        lab = int(r["label"])
        n = norm(text)
        if n in seen:
            drops["duplicate_text"] += 1; continue
        seen.add(n)
        if not (20 <= len(text) <= 6000):
            drops["state_length"] += 1; continue
        pool[lab].append({"file": "data/V2/dev_subtask1.csv", "index": r["index"], "row": pos, "label": lab,
                          "state": text, "also_in_train": n in train_norm})
    for k in pool:
        pool[k].sort(key=lambda x: x["index"])

    rng = random.Random(SEED)
    picked, topup = {}, {}
    for k in (1, 0):
        items = list(pool[k])
        rng.shuffle(items)
        if len(items) < N_PER_CLASS:
            # top-up from train (not needed with the pinned files: dev has 185/155)
            extra = [{"file": "data/V2/train_subtask1.csv", "index": r["index"], "row": i, "label": int(r["label"]),
                      "state": r["text"].strip(), "also_in_train": True}
                     for i, r in enumerate(train) if int(r["label"]) == k and norm(r["text"]) not in seen
                     and 20 <= len(r["text"].strip()) <= 6000]
            extra.sort(key=lambda x: x["index"])
            rng.shuffle(extra)
            topup[k] = N_PER_CLASS - len(items)
            items += extra[:topup[k]]
        picked[k] = items[:N_PER_CLASS]
    chosen = picked[1] + picked[0]
    rng.shuffle(chosen)

    rows = []
    for it in chosen:
        key = f"{it['file']}:{it['index']}"
        rows.append({
            "id": "r_" + sha256(f"ohs3:{TASK}:row:{key}")[:12],
            "group_id": f"g:ohs3:{TASK}:{it['index']}",
            "call_id": "c_" + sha256(f"ohs3:{TASK}:call:{key}")[:12],
            "split": "ohs3",
            "track": "U",
            "source": TASK,
            "state": it["state"],
            "qtype": "noul",
            "instructions": INSTRUCTIONS,
            "options": None,
            "gold": it["label"],
            "role": "aff",
            "card": CARD,
            "meta": {
                "task": TASK,
                "dataset": "Causal News Corpus V2 (Subtask 1)",
                "repo": f"https://github.com/{REPO}",
                "file": it["file"],
                "commit_sha": PINNED_SHA,
                "commit_date": PINNED_SHA_DATE,
                "file_git_blob_sha": files[it["file"]]["git_blob_sha"],
                "index": it["index"],
                "csv_row": it["row"],
                "original_label": it["label"],
                "original_label_name": "Causal" if it["label"] == 1 else "Non-Causal",
                "asked_label": ASKED_LABEL,
                "url": BLOB_URL.format(repo=REPO, sha=PINNED_SHA, path=it["file"]),
                "snapshot_fetched": SNAPSHOT_FETCHED,
                "licence": LICENCE,
                "identical_sentence_in_train_subtask1": it["also_in_train"],
            },
        })

    # checks
    assert len(rows) == 2 * N_PER_CLASS
    assert len({r["id"] for r in rows}) == len({r["group_id"] for r in rows}) == len({r["call_id"] for r in rows}) == len(rows)
    assert len({norm(r["state"]) for r in rows}) == len(rows)
    g = Counter(r["gold"] for r in rows)
    assert g[1] == g[0] == N_PER_CLASS
    for r in rows:
        assert 20 <= len(r["state"]) <= 6000

    OUT.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)
    OUT.write_text(text)

    lens = sorted(len(r["state"]) for r in rows)
    summary = {
        "task": TASK,
        "rows": len(rows),
        "qtype": "noul",
        "track": "U",
        "class_balance": {"gold_1_Causal": g[1], "gold_0_Non-Causal": g[0]},
        "asked_label": ASKED_LABEL,
        "instructions": INSTRUCTIONS,
        "card": CARD,
        "label_definitions_source": (f"official: CNC annotation manual 'Event Causality in Socio-Political News - Annotation "
                                     f"Manual' ({BLOB_URL.format(repo=REPO, sha=PINNED_SHA, path=MANUAL_PATH)}), "
                                     "section 3.1.1 General Definition (PDTB-3 CONTINGENCY and its CAUSE / PURPOSE / "
                                     "CONDITION / NEGATIVE-CONDITION senses) and the +SPEECH-ACT/+BELIEF exclusion; quoted "
                                     "near-verbatim (the CONTINGENCY definition and the four sense definitions are verbatim; "
                                     "the 'Example connectives are X and Y' sentences are condensed into parentheses and the "
                                     "exclusion sentence is lightly shortened), with a short lead-in sentence paraphrasing the Subtask 1 description "
                                     "('identifies if a given event sentence contains any cause-effect meaning')."),
        "author_written_definitions": [],
        "source": "Causal News Corpus V2, official GitHub repo (not the HF conversion)",
        "citation": CITATION,
        "provenance": {"repo": f"https://github.com/{REPO}", "commit_sha": PINNED_SHA, "commit_date": PINNED_SHA_DATE,
                       "snapshot_fetched": SNAPSHOT_FETCHED, "files": files},
        "licence": LICENCE,
        "text_date_range": ("unknown per item; sentences come from English socio-political news (China and South Africa "
                            "sources) reused from the CASE 2021 Subtask 4 corpus; corpus published 2022 (V1) / V2 files "
                            "last changed 2023-05-10"),
        "pool": {"dev_rows": len(dev), "dev_label_counts": dict(Counter(int(r["label"]) for r in dev)),
                 "eligible_Causal": len(pool[1]), "eligible_Non-Causal": len(pool[0]), "dropped": dict(drops),
                 "train_topup_used": topup},
        "sampling": (f"per class: dev rows sorted by index, random.Random({SEED}).shuffle, take first {N_PER_CLASS}; "
                     "rows then shuffled with the same RNG"),
        "state_format": "sentence text verbatim from the CSV 'text' column (leading/trailing whitespace stripped only)",
        "state_length": {"min": lens[0], "median": lens[len(lens) // 2], "max": lens[-1]},
        "rows_whose_sentence_also_appears_in_train_subtask1": sum(r["meta"]["identical_sentence_in_train_subtask1"] for r in rows),
        "indices": sorted(r["meta"]["index"] for r in rows),
        "output_sha256": sha256(text),
        "uncertain": [
            "Track U: CNC dev is public since 2022 (V1) / 2023 (V2) and CNC train/dev are widely used for training, so "
            "contamination is possible; dev gold labels are public.",
            "All index values in dev_subtask1.csv start with 'train_' (inherited from the CASE 2021 source corpus ids); "
            "this is the source's own naming, and the file used is dev_subtask1.csv at the pinned commit.",
            "Text is pre-tokenised news sentences (spaces before punctuation) and a few contain page boilerplate such as "
            "'PUBLISHED : <date>'; kept verbatim because the label applies to the whole annotated text.",
            "The card's first sentence is a close paraphrase of the manual's Subtask 1 description; the sense definitions are verbatim, connective examples and the +SPEECH-ACT/+BELIEF exclusion are lightly condensed.",
        ],
    }
    SUMMARY.write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(json.dumps({k: v for k, v in summary.items() if k not in ("indices", "card")}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
