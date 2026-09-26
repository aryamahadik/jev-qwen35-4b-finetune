#!/usr/bin/env python3
"""s02_normalise: run every registered source loader and write normalised records (DESIGN 13 step 2).

For each registered loader (build/loaders/) and each of its splits:
  * iterate the loader, validate every record against the contract (common.validate_record), reject duplicate
    source_ids, add meta.text_sha256 (sha256 of the post-hygiene text; used by rehydrate);
  * write data/interim/normalised/<source>__<split>.jsonl, sorted by source_id (natural order), canonical JSON;
  * record per-split statistics in data/reports/normalise_summary.json (merged with entries from earlier runs):
    counts, drops by reason, label distribution, soft-label coverage, text lengths, within-split exact duplicates
    (after 9.1 normalisation; informational, dedup is s03's job), PII masks applied and residual PII matches.
Any contract violation or loader exception fails the step (nothing is written for that split).

    python3 build/steps/s02_normalise.py                      # every registered loader
    python3 build/steps/s02_normalise.py --sources banking77  # just these (comma-separated)

authored_by: llm:claude:foundation-engineer-1
"""
from __future__ import annotations

import collections
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import common  # noqa: E402

STEP = "s02_normalise"
SUMMARY = common.REPORTS / "normalise_summary.json"
MAX_LABELS_LISTED = 250
MAX_ERROR_EXAMPLES = 20


def _pct(values: list[int], q: float) -> int:
    if not values:
        return 0
    s = sorted(values)
    return s[min(len(s) - 1, int(round(q * (len(s) - 1))))]


def _label_repr(label) -> str:
    if isinstance(label, list):
        return "|".join(label) if label else "<empty>"
    return "<none>" if label is None else str(label)


def normalise_split(loaders, source: str, split: str, registered: dict, log) -> tuple[dict, list[dict] | None]:
    spec = loaders.get(source)
    ctx, it = loaders.iter_records(source, split, log=log)
    recs: list[dict] = []
    errors: list[str] = []
    n_errors = 0
    seen: set[str] = set()
    for rec in it:
        errs = common.validate_record(rec, sources=registered)
        if isinstance(rec, dict):
            if rec.get("source") != source:
                errs.append(f"record source {rec.get('source')!r} != loader source {source!r}")
            if rec.get("split") != split:
                errs.append(f"record split {rec.get('split')!r} != requested split {split!r}")
            meta = rec.get("meta")
            if isinstance(meta, dict) and any(k in meta for k in common.RESERVED_META):
                errs.append(f"meta uses reserved keys {[k for k in common.RESERVED_META if k in meta]}")
            sid = rec.get("source_id")
            if isinstance(sid, str):
                if sid in seen:
                    errs.append(f"duplicate source_id {sid!r}")
                seen.add(sid)
        if errs:
            n_errors += 1
            if len(errors) < MAX_ERROR_EXAMPLES:
                errors.append(f"{rec.get('source_id') if isinstance(rec, dict) else '?'}: " + "; ".join(errs))
            continue
        rec["meta"]["text_sha256"] = common.text_sha256(rec["text"])
        recs.append(rec)

    try:
        revision = ctx.revision
    except Exception as exc:
        revision = f"<unresolved: {exc}>"
    entry = {"source": source, "split": split, "module": spec.module, "lock_key": spec.lock_key,
             "revision": revision, "info": dict(spec.info), "drops": dict(sorted(ctx.drops.items())),
             "notes": dict(sorted(ctx.notes.items())), "n_invalid_records": n_errors, "error_examples": errors}
    if n_errors or not recs:
        entry["status"] = "failed" if n_errors else "empty"
        return entry, None

    labels = collections.Counter(_label_repr(r["label"]) for r in recs)
    label_types = collections.Counter(type(r["label"]).__name__ if r["label"] is not None else "none" for r in recs)
    soft_types = collections.Counter(type(r["soft"]).__name__ for r in recs if r["soft"] is not None)
    chars = [len(r["text"]) for r in recs]
    words = [len(r["text"].split()) for r in recs]
    norm_seen: dict[str, int] = {}
    for r in recs:
        h = common.norm_hash(r["text"])
        norm_seen[h] = norm_seen.get(h, 0) + 1
    dup_rows = sum(c - 1 for c in norm_seen.values() if c > 1)
    meta_keys = collections.Counter(k for r in recs for k in r["meta"])
    entry.update({
        "status": "ok",
        "n_records": len(recs),
        "n_labels": len(labels),
        "label_types": dict(sorted(label_types.items())),
        "label_counts": dict(sorted(labels.items())) if len(labels) <= MAX_LABELS_LISTED
        else dict(sorted(labels.most_common(MAX_LABELS_LISTED))),
        "label_counts_truncated": len(labels) > MAX_LABELS_LISTED,
        "label_count_min_max": [min(labels.values()), max(labels.values())],
        "n_soft": sum(1 for r in recs if r["soft"] is not None),
        "soft_types": dict(sorted(soft_types.items())),
        "text_chars": {"min": min(chars), "median": int(statistics.median(chars)), "p95": _pct(chars, 0.95), "max": max(chars)},
        "text_words": {"min": min(words), "median": int(statistics.median(words)), "p95": _pct(words, 0.95), "max": max(words)},
        "n_under_min_tokens": sum(1 for w in words if w < int(common.cfg("caps", "min_text_tokens"))),
        "within_split_exact_dup": {"rows_beyond_first": dup_rows, "groups": sum(1 for c in norm_seen.values() if c > 1)},
        "pii_masked_records": sum(1 for r in recs if r["meta"].get("pii_masked")),
        "pii_masks_total": sum(int(r["meta"].get("pii_masked", 0)) for r in recs),
        "pii_residual_matches": sum(common.pii_residual(r["text"]) for r in recs),
        "meta_keys": dict(sorted(meta_keys.items())),
    })
    return entry, recs


def run(args, log):
    import loaders
    registered = loaders.sources()
    import_errors = dict(sorted(loaders.IMPORT_ERRORS.items()))
    for mod, tb in import_errors.items():
        log.error("loader module %s failed to import:\n%s", mod, tb)
    requested = [s.strip() for s in args.sources.split(",") if s.strip()] if args.sources else sorted(registered)
    unknown = [s for s in requested if s not in registered]
    if unknown:
        return {"ok": False, "error": f"no loader registered for {unknown}; registered: {sorted(registered)}"}
    split_filter = {s.strip() for s in args.splits.split(",")} if args.splits else None

    summary = common.read_json(SUMMARY) if SUMMARY.exists() else {}
    entries = dict(summary.get("entries", {}))
    outputs: list[str] = []
    failed: list[str] = []
    for source in requested:
        for split in registered[source]:
            if split_filter and split not in split_filter:
                continue
            name = f"{source}__{split}"
            log.info("normalise %s", name)
            try:
                entry, recs = normalise_split(loaders, source, split, registered, log)
            except Exception as exc:
                log.exception("loader %s failed on split %s", source, split)
                entry, recs = {"source": source, "split": split, "status": "failed",
                               "error": f"{type(exc).__name__}: {exc}"}, None
            if recs is None:
                failed.append(name)
                log.error("%s: %s %s", name, entry.get("status"), entry.get("error_examples") or entry.get("error", ""))
            else:
                out = common.write_jsonl(common.normalised_path(source, split), recs, sort_key=common.record_sort_key)
                entry["output"] = out
                outputs.append(out["path"])
                log.info("%s: %d records -> %s (drops %s, within-split dup rows %d, pii masks %d)", name, len(recs),
                         out["path"], entry["drops"], entry["within_split_exact_dup"]["rows_beyond_first"],
                         entry["pii_masks_total"])
            entries[name] = entry

    summary = {
        "summary_version": 1,
        "generated_by": "build/steps/s02_normalise.py",
        "record_contract": list(common.RECORD_FIELDS),
        "registered": {s: list(v) for s, v in registered.items()},
        "import_errors": {m: tb.strip().splitlines()[-1] for m, tb in import_errors.items()},
        "entries": dict(sorted(entries.items())),
        "failed": sorted(n for n, e in entries.items() if e.get("status") not in ("ok",)),
    }
    out = common.write_json(SUMMARY, summary)
    outputs.append(out["path"])
    if import_errors and not args.sources:
        return {"ok": False, "error": f"loader modules failed to import: {sorted(import_errors)}", "outputs": outputs}
    if failed:
        return {"ok": False, "error": f"failed: {failed}", "outputs": outputs}
    inputs = sorted(common.LOADERS_DIR.glob("*.py")) + ([common.LOCK_PATH] if common.LOCK_PATH.exists() else [])
    return {"outputs": outputs, "inputs": inputs, "partial": bool(args.sources or args.splits),
            "info": {"normalised": sorted(outputs[:-1]), "import_errors": sorted(import_errors)}}


if __name__ == "__main__":
    ap = common.step_argparser(__doc__.splitlines()[0])
    ap.add_argument("--sources", default=None, help="comma-separated loader names (default: all registered)")
    ap.add_argument("--splits", default=None, help="comma-separated split names to restrict to")
    sys.exit(common.step_main(STEP, __file__, run, parser=ap))
