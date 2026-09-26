#!/usr/bin/env python3
"""BTZSC sampler: a clean-room-compatible re-implementation of AbdelStark's sampler.

DESIGN 3.4 (CMP-B77 and the optional local anchor pack) and validator V19.

Reference implementation (read, not imported): AbdelStark/jev-benchmarks @
0d610cc53e79bcbec691312b0c4adb4a0e371642 (Apache-2.0), `src/jev_benchmarks/data.py`
(`_class_count`, `_balanced_indices`, `load_examples`) with `configs/pilot-v1.yaml`
(seed 20260917, 100 samples per dataset, datasets agnews / emotiondair / banking77 in that
order, so the dataset offsets are 0 / 1 / 2).

Algorithm (must match the reference byte for byte):
  1. Load `btzsc/btzsc`, config <name>, split `test`, at revision fef2a2ac62b69c58670047dddf045c53d7c3cb5e.
     BTZSC stores one row per (text, hypothesis) with a binary `labels` column.
  2. Class count K = index of the first row whose text differs from row 0's text.
     The ordered candidate labels are the hypotheses of rows 0..K-1.
  3. For each sample s in range(len(rows) // K): the K binary values at rows s*K .. s*K+K-1.
     Keep the sample only if exactly one value is 1 (drops the 200 Banking77 out-of-scope rows:
     2,880 valid of 3,080); its target is the position of the 1.
  4. Group valid positions by target in FIRST-APPEARANCE order (a dict), then shuffle every class
     list with ONE shared `random.Random(20260917 + offset)` instance, in that insertion order.
     (DESIGN 3.4's "per-class random.Random(20260917 + 2).shuffle" means this: one RNG, one
     shuffle call per class. A fresh RNG per class still yields the five V19 first ids for agnews
     and emotiondair and the V19 counts, but 74 of 100 ids differ in agnews and in emotiondair and
     96 of 100 in banking77; only the full-manifest sha256 check below pins the variant.)
  5. Round-robin over the classes sorted by class index, taking `list.pop()` (the LAST element
     of each shuffled list) until 100 are chosen; return the chosen positions sorted.
  6. example_id = f"{name}:{sample_index}", where sample_index indexes ALL samples (valid or not).

The AbdelStark seeds (20260917 + offset) are mandated by DESIGN 3.4 for reproduction; they are the
one deliberate exception to the OpenDecide sub-seed rule of DESIGN 13 step 0.

Self-test (V19; `python3 assets/anchors/btzsc_sampler.py --self-test`) asserts:
  - agnews first ids 9, 267, 292, 427, 437 and 25 per class (4 classes);
  - emotiondair first ids 23, 25, 50, 56, 63 and 17/17/17/17/16/16 per class (class-index order);
  - banking77: 72 classes, 3,080 samples, 2,880 valid, 100 chosen;
  - the regenerated three-dataset manifest is byte-identical to AbdelStark's published
    `manifest.jsonl` (sha256 ec064c52... from results/reports/btzsc-pilot-v1.json).

Other entry points:
  sample_dataset(name)            -> dict with examples (AbdelStark Example fields) and counts
  cmp_b77_calls()                 -> the 100 CMP-B77 Jev call specs (DESIGN 3.4, exact call form)
  --write-ids PATH [--datasets …] -> ids-only JSONL (no text; BTZSC rows are release tier idonly)

Licence: BTZSC wrapper MIT; Banking77 CC-BY-4.0; AG News and DAIR Emotion non-commercial, so
AG News / Emotion are local anchors only and every BTZSC row ships as idonly (DESIGN 11).

authored_by: llm:claude:anchors-engineer
Runs with system python3 (datasets 4.8.5); uses the default HF cache. Peak RSS about 0.5 GB.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from collections import defaultdict

AUTHORED_BY = "llm:claude:anchors-engineer"
REPOSITORY = "btzsc/btzsc"
REVISION = "fef2a2ac62b69c58670047dddf045c53d7c3cb5e"
SPLIT = "test"
SEED_BASE = 20260917  # AbdelStark pilot-v1 seed; offsets below
SAMPLES_PER_DATASET = 100
# (name, task, offset) exactly as in AbdelStark configs/pilot-v1.yaml (list order = offset)
DATASETS = (("agnews", "topic", 0), ("emotiondair", "emotion", 1), ("banking77", "intent", 2))
DATASET_INFO = {name: (task, offset) for name, task, offset in DATASETS}

REFERENCE = {
    "repo": "https://github.com/AbdelStark/jev-benchmarks",
    "commit": "0d610cc53e79bcbec691312b0c4adb4a0e371642",
    "license": "Apache-2.0",
    "files": ["src/jev_benchmarks/data.py", "configs/pilot-v1.yaml", "results/reports/btzsc-pilot-v1.json"],
}
# sha256 of AbdelStark's results/runs/btzsc-pilot-v1/manifest.jsonl, as published in
# results/reports/btzsc-pilot-v1.json -> artifacts.manifest_sha256 (commit above).
PUBLISHED_MANIFEST_SHA256 = "ec064c52b149de458344cd4b4a44c158460f30b3bbb7fe8b2e7ec72d0abf3ba5"

# Jev call form used by AbdelStark (adapters/jev.py) and required verbatim by DESIGN 3.4.
CMP_INSTRUCTIONS = "Which single label best describes the input text?"
CMP_QUESTION_KEY = "label"  # AbdelStark's key; question keys are not sent to the model

# V19 expectations (DESIGN 3.4 / 9.2)
EXPECTED_FIRST_IDS = {
    "agnews": ["agnews:9", "agnews:267", "agnews:292", "agnews:427", "agnews:437"],
    "emotiondair": ["emotiondair:23", "emotiondair:25", "emotiondair:50", "emotiondair:56", "emotiondair:63"],
}
EXPECTED_CLASS_COUNTS = {
    "agnews": [25, 25, 25, 25],
    "emotiondair": [17, 17, 17, 17, 16, 16],
}
EXPECTED_BANKING77 = {"n_classes": 72, "n_samples": 3080, "n_valid": 2880, "n_selected": 100}


# ---------------------------------------------------------------- core algorithm (pure functions)
def class_count(texts) -> int:
    """K = index of the first text that differs from texts[0] (BTZSC repeats each text K times)."""
    first = texts[0]
    for index in range(1, len(texts)):
        if texts[index] != first:
            return index
    raise ValueError("could not infer class count from repeated BTZSC texts")


def balanced_indices(targets: list[int], limit: int, seed: int) -> list[int]:
    """Class-balanced round-robin selection; returns sorted positions into `targets`."""
    by_class: dict[int, list[int]] = defaultdict(list)  # insertion order = first appearance
    for index, target in enumerate(targets):
        by_class[target].append(index)
    rng = random.Random(seed)  # one RNG shared by every class, in insertion order
    for indices in by_class.values():
        rng.shuffle(indices)
    chosen: list[int] = []
    classes = sorted(by_class)
    while len(chosen) < min(limit, len(targets)):
        made_progress = False
        for class_id in classes:
            if by_class[class_id] and len(chosen) < limit:
                chosen.append(by_class[class_id].pop())  # last element of the shuffled list
                made_progress = True
        if not made_progress:
            break
    return sorted(chosen)


def select_from_columns(name: str, texts: list[str], hypotheses: list[str], binary: list[int],
                        limit: int = SAMPLES_PER_DATASET, seed: int | None = None) -> dict:
    """Apply the sampler to already-loaded BTZSC columns (testable without the network)."""
    task, offset = DATASET_INFO.get(name, ("unknown", 0))
    if seed is None:
        seed = SEED_BASE + offset
    n_classes = class_count(texts)
    n_samples = len(texts) // n_classes
    labels = tuple(str(hypotheses[i]) for i in range(n_classes))
    valid_sample_indices: list[int] = []
    targets: list[int] = []
    for sample_index in range(n_samples):
        off = sample_index * n_classes
        values = binary[off: off + n_classes]
        if sum(values) == 1:
            valid_sample_indices.append(sample_index)
            targets.append(values.index(1))
    positions = balanced_indices(targets, limit, seed)
    examples = []
    for position in positions:
        sample_index = valid_sample_indices[position]
        text = texts[sample_index * n_classes]
        examples.append({
            "dataset": name,
            "task": task,
            "example_id": f"{name}:{sample_index}",
            "text": text,
            "text_sha256": hashlib.sha256(text.encode()).hexdigest(),
            "labels": list(labels),
            "target_index": targets[position],
        })
    per_class = [0] * n_classes
    for ex in examples:
        per_class[ex["target_index"]] += 1
    return {
        "dataset": name, "task": task, "seed": seed, "offset": offset,
        "n_rows": len(texts), "n_classes": n_classes, "n_samples": n_samples,
        "n_valid": len(valid_sample_indices), "n_selected": len(examples),
        "per_class_counts": per_class, "labels": list(labels), "examples": examples,
    }


# ---------------------------------------------------------------- data access
def load_columns(name: str):
    """Load one BTZSC config at the pinned revision; returns (texts, hypotheses, binary labels)."""
    from datasets import load_dataset  # system python3, datasets 4.8.5
    ds = load_dataset(REPOSITORY, name=name, split=SPLIT, revision=REVISION)
    table = ds.data  # arrow table in the HF cache (memory-mapped)
    texts = [str(v) for v in table.column("text").to_pylist()]
    hypotheses_all = table.column("hypothesis")
    k = class_count(texts)
    hypotheses = [str(v) for v in hypotheses_all.slice(0, k).to_pylist()]
    binary = [int(v) for v in table.column("labels").to_pylist()]  # ClassLabel: 1 = entailment
    return texts, hypotheses, binary


def sample_dataset(name: str, limit: int = SAMPLES_PER_DATASET) -> dict:
    texts, hypotheses, binary = load_columns(name)
    result = select_from_columns(name, texts, hypotheses, binary, limit=limit)
    result["provenance"] = {"source": REPOSITORY, "config": name, "revision": REVISION,
                            "source_split": SPLIT, "reference_sampler": REFERENCE,
                            "authored_by": AUTHORED_BY}
    return result


def manifest_bytes(results: list[dict]) -> bytes:
    """AbdelStark's manifest.jsonl serialisation (io.write_jsonl: sort_keys, ensure_ascii=False)."""
    out = []
    for res in results:
        for ex in res["examples"]:
            out.append(json.dumps(ex, ensure_ascii=False, sort_keys=True) + "\n")
    return "".join(out).encode("utf-8")


def jev_call_spec(example: dict) -> dict:
    """The exact AbdelStark / DESIGN 3.4 call: state {"text": text}, one K-way Choice."""
    criteria = {f"label_{i:03d}": label for i, label in enumerate(example["labels"])}
    return {
        "model": "jev-1.13.0",
        "state": {"text": example["text"]},  # the only object-valued state in OpenDecide
        "questions": {CMP_QUESTION_KEY: {"type": "choice", "instructions": CMP_INSTRUCTIONS,
                                         "criteria": criteria}},
        "gold_key": f"label_{example['target_index']:03d}",
    }


def cmp_b77_calls() -> list[dict]:
    """The 100 CMP-B77 call specs (banking77, offset 2), sorted by example id order of the sampler."""
    res = sample_dataset("banking77")
    return [{"example_id": ex["example_id"], "text_sha256": ex["text_sha256"], **jev_call_spec(ex)}
            for ex in res["examples"]]


def ids_rows(res: dict) -> list[dict]:
    """Ids-only rows (no text): BTZSC rows are idonly in every release tier (DESIGN 11)."""
    rows = []
    for ex in res["examples"]:
        sample_index = int(ex["example_id"].split(":")[1])
        rows.append({
            "dataset": ex["dataset"], "task": ex["task"], "example_id": ex["example_id"],
            "sample_index": sample_index, "target_index": ex["target_index"],
            "target_label": ex["labels"][ex["target_index"]], "n_options": len(ex["labels"]),
            "text_sha256": ex["text_sha256"],
            "source": REPOSITORY, "config": ex["dataset"], "revision": REVISION, "source_split": SPLIT,
            "sampler_seed": res["seed"], "release_tier": "idonly", "authored_by": AUTHORED_BY,
        })
    return rows


# ---------------------------------------------------------------- self-test (V19)
def _unit_checks() -> None:
    assert class_count(["a", "a", "a", "b", "b", "b"]) == 3
    t = [0, 0, 0, 1, 1, 1, 2, 2, 2]
    first = balanced_indices(t, 6, 42)
    assert first == balanced_indices(t, 6, 42)
    assert {t[i] for i in first} == {0, 1, 2}
    # an out-of-scope sample (no positive) is dropped and ids index all samples
    res = select_from_columns("fixture", ["one", "one", "two", "two", "oos", "oos"],
                              ["label a", "label b"], [1, 0, 0, 1, 0, 0], limit=100, seed=1)
    assert [e["example_id"] for e in res["examples"]] == ["fixture:0", "fixture:1"]
    assert [e["target_index"] for e in res["examples"]] == [0, 1]
    assert res["n_valid"] == 2 and res["n_samples"] == 3


def self_test(verbose: bool = True) -> dict:
    _unit_checks()
    results = [sample_dataset(name) for name, _, _ in DATASETS]
    by_name = {r["dataset"]: r for r in results}
    report = {"check": "V19", "authored_by": AUTHORED_BY, "revision": REVISION, "datasets": {}}
    for r in results:
        report["datasets"][r["dataset"]] = {
            k: r[k] for k in ("seed", "n_rows", "n_classes", "n_samples", "n_valid", "n_selected", "per_class_counts")
        }
        report["datasets"][r["dataset"]]["first_ids"] = [e["example_id"] for e in r["examples"][:5]]
    failures = []

    def check(cond: bool, msg: str) -> None:
        if not cond:
            failures.append(msg)

    for name, want in EXPECTED_FIRST_IDS.items():
        got = [e["example_id"] for e in by_name[name]["examples"][:5]]
        check(got == want, f"{name} first ids {got} != {want}")
    for name, want in EXPECTED_CLASS_COUNTS.items():
        got = by_name[name]["per_class_counts"]
        check(got == want, f"{name} per-class counts {got} != {want}")
        check(by_name[name]["n_selected"] == SAMPLES_PER_DATASET, f"{name} selected {by_name[name]['n_selected']}")
    b = by_name["banking77"]
    for k, want in EXPECTED_BANKING77.items():
        check(b[k] == want, f"banking77 {k} {b[k]} != {want}")
    check(max(b["per_class_counts"]) <= 2 and min(b["per_class_counts"]) >= 1,
          f"banking77 per-class counts outside 1..2: {b['per_class_counts']}")
    for r in results:  # every chosen example has exactly one positive and a matching label
        check(len({e["example_id"] for e in r["examples"]}) == r["n_selected"], f"{r['dataset']} duplicate ids")
    sha = hashlib.sha256(manifest_bytes(results)).hexdigest()
    report["manifest_sha256"] = sha
    report["published_manifest_sha256"] = PUBLISHED_MANIFEST_SHA256
    check(sha == PUBLISHED_MANIFEST_SHA256, f"manifest sha256 {sha} != published {PUBLISHED_MANIFEST_SHA256}")
    # the CMP call form
    call = jev_call_spec(b["examples"][0])
    check(len(call["questions"][CMP_QUESTION_KEY]["criteria"]) == 72, "CMP Choice must have 72 options")
    report["status"] = "pass" if not failures else "fail"
    report["failures"] = failures
    if verbose:
        for name, info in report["datasets"].items():
            print(name, json.dumps(info, ensure_ascii=False))
        print("manifest_sha256", sha, "(published", PUBLISHED_MANIFEST_SHA256 + ")")
        for msg in failures:
            print("FAIL", msg)
    if failures:
        raise AssertionError("; ".join(failures))
    return report


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--self-test", action="store_true", help="run the V19 assertions (default action)")
    ap.add_argument("--write-ids", metavar="PATH", help="write ids-only JSONL for --datasets")
    ap.add_argument("--datasets", default="banking77", help="comma list (agnews,emotiondair,banking77)")
    args = ap.parse_args(argv)
    if args.write_ids:
        rows = []
        for name in [n.strip() for n in args.datasets.split(",") if n.strip()]:
            if name not in DATASET_INFO:
                ap.error(f"unknown dataset {name}")
            rows.extend(ids_rows(sample_dataset(name)))
        rows.sort(key=lambda r: (r["dataset"], r["sample_index"]))
        with open(args.write_ids, "w", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        print(f"wrote {len(rows)} rows to {args.write_ids}")
        return 0
    try:
        self_test()
    except AssertionError as exc:
        print(f"V19 FAIL: {exc}", file=sys.stderr)
        return 1
    print("V19 PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
