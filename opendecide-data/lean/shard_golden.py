"""Split the golden rows that 4B-E labels into shards for the resumable teacher-labelling job (FINETUNE_PLAN.md 3.2
step 4), plus the shard/label file helpers that od_gcp.py label, build_2b_kd.py and flag_labels.py share.

Rows to label = golden_train minus:
  - attacked twins (the 'b' side of every inv relation; their teacher is copied from the clean partner later);
  - rows with teacher_src = blend50 (old in-sample teachers);
  - rows whose sha1(state, instructions, options) is in a file of 4B-E's lineage (in-sample for the teacher);
  - gold_probs rows (the trainer uses gold_probs and ignores any teacher);
  - the 3 csqa rows with duplicate options.

  python shard_golden.py --dry-run                       # counts only
  python shard_golden.py --out data/v14_label_shards     # shard_000.jsonl ... + shards.json (manifest, written last)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
LINEAGE = ("train_v07", "train_v08s2", "train_v09s3", "train_v10s4", "train_v11", "train_v11b", "train_v11c",
           "train_v13t", "train_prism_arms")  # 4B-E = v13t <- v11c <- v11b <- (0.3 v10 + 0.7 v11), plus the arm file
CSQA_DUP = ("r_84331130428f", "r_33cba1e12b8e", "r_8e993e070c07")  # duplicate options: cannot be keyed by option
MANIFEST = "shards.json"


def row_key(r) -> str:
    """Identity of a question for the in-sample check: sha1(state NUL instructions NUL json(options))."""
    s = (r.get("state") or "") + "\x00" + (r.get("instructions") or "") + "\x00" + json.dumps(r.get("options"))
    return hashlib.sha1(s.encode()).hexdigest()


def read_jsonl(path):
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def read_ids(path):
    with open(path) as f:
        return [json.loads(l)["id"] for l in f if l.strip()]


def write_atomic(path, lines):
    """Write lines to path.tmp, fsync, then os.replace: a crash never leaves a partial file under the final name."""
    path = Path(path)
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w") as f:
        for l in lines:
            f.write(l if l.endswith("\n") else l + "\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def write_json_atomic(path, obj):
    write_atomic(path, [json.dumps(obj, indent=2)])


def lineage_keys(data_dir=DATA, names=LINEAGE, warn=print):
    keys, seen = set(), {}
    for n in names:
        p = Path(data_dir) / f"{n}.jsonl"
        if not p.exists():
            warn(f"WARNING: lineage file {p} is missing; its rows are not excluded")
            seen[n] = None
            continue
        k = 0
        with open(p) as f:
            for l in f:
                if l.strip():
                    keys.add(row_key(json.loads(l)))
                    k += 1
        seen[n] = k
    return keys, seen


def exclusion_reason(r, inv_b, lineage, csqa=CSQA_DUP):
    """The first reason a golden row is not labelled, or None (checked in this order)."""
    m = r.get("meta") or {}
    if r["id"] in inv_b:
        return "attacked_twin"
    if m.get("teacher_src") == "blend50":
        return "blend50"
    if row_key(r) in lineage:
        return "in_lineage"
    if m.get("gold_probs"):
        return "gold_probs"
    if r["id"] in csqa:
        return "csqa_dup_options"
    return None


def select_rows(rows, rels, lineage):
    """(rows to label in file order, first-reason counts, per-reason totals where reasons overlap)."""
    inv_b = {x["b"] for x in rels if x["type"] == "inv"}
    keep, first, total = [], Counter(), Counter()
    for r in rows:
        why = exclusion_reason(r, inv_b, lineage)
        m = r.get("meta") or {}
        for k, hit in (("attacked_twin", r["id"] in inv_b), ("blend50", m.get("teacher_src") == "blend50"),
                       ("in_lineage", row_key(r) in lineage), ("gold_probs", bool(m.get("gold_probs"))),
                       ("csqa_dup_options", r["id"] in CSQA_DUP)):
            total[k] += hit
        if why:
            first[why] += 1
        else:
            keep.append(r)
    return keep, first, total


def split_even(n, shard_rows):
    """Shard sizes: ceil(n / shard_rows) shards, as equal as possible."""
    k = max(1, math.ceil(n / shard_rows))
    return [n // k + (i < n % k) for i in range(k)]


def shard_name(i):
    return f"shard_{i:03d}.jsonl"


def shard_files(shards_dir):
    """Shard paths in order, from the manifest (which must list existing files) or, without one, by glob."""
    d = Path(shards_dir)
    m = d / MANIFEST
    if m.exists():
        files = [d / s["file"] for s in json.loads(m.read_text())["shards"]]
        missing = [str(p) for p in files if not p.exists()]
        if missing:
            raise FileNotFoundError(f"{m} lists missing shards: {missing[:3]}")
        return files
    return sorted(d.glob("shard_[0-9][0-9][0-9].jsonl"))


def label_paths(out_dir, shard_path):
    stem = Path(shard_path).name[: -len(".jsonl")]
    return Path(out_dir) / f"{stem}.jsonl", Path(out_dir) / f"{stem}.meta.json"


def shard_done(shard_path, out_path, meta_path) -> bool:
    """A labelled shard counts as done only if its meta exists (written last) AND the label file has one line per input
    row with the same ids in the same order, AND the meta's row count agrees, AND the meta's shard_sha256 is the shard
    file's current hash (rows regenerated under the same ids, new state or gold, must be labelled again)."""
    out_path, meta_path = Path(out_path), Path(meta_path)
    if not (meta_path.exists() and out_path.exists()):
        return False
    try:
        meta = json.loads(meta_path.read_text())
        got = read_ids(out_path)
    except (json.JSONDecodeError, KeyError):
        return False
    want = read_ids(shard_path)
    return got == want and meta.get("rows") == len(want) and meta.get("shard_sha256") == _sha_file(shard_path)


def label_view(meta_path) -> dict:
    """What a labelled shard was made with: its meta's settings (model, base revision, layout, view, TTA, merge) and
    style."""
    m = json.loads(Path(meta_path).read_text())
    return {"settings": m.get("settings"), "style": m.get("style")}


def one_view(views: dict, where) -> dict | None:
    """views = {shard name: label_view}. One label set comes from one model, base, layout and view: raises otherwise."""
    distinct = sorted({json.dumps(v, sort_keys=True) for v in views.values()})
    if len(distinct) > 1:
        raise RuntimeError(f"label shards in {where} were made with different settings: {distinct}")
    return next(iter(views.values()), None)


def load_labels(labels_dir, shards_dir=None, return_view=False):
    """{id: probs} from a label directory (every shard must be done when shards_dir is given) or a preds .jsonl. The
    shards of a directory must all have the same settings and style (one_view); return_view=True also returns them
    (None for a .jsonl)."""
    p = Path(labels_dir)
    if p.is_file():
        out = {x["id"]: x["probs"] for x in read_jsonl(p)}
        return (out, None) if return_view else out
    out, views = {}, {}
    if shards_dir is not None:
        bad = []
        for s in shard_files(shards_dir):
            lp, mp = label_paths(p, s)
            if not shard_done(s, lp, mp):
                bad.append(s.name)
                continue
            views[s.name] = label_view(mp)
            out.update({x["id"]: x["probs"] for x in read_jsonl(lp)})
        if bad:
            raise RuntimeError(f"{len(bad)} shard(s) not labelled (or incomplete) in {p}: {bad[:5]}")
    else:
        for lp in sorted(p.glob("shard_[0-9][0-9][0-9].jsonl")):
            mp = lp.with_name(lp.name[: -len(".jsonl")] + ".meta.json")
            if mp.exists():
                views[lp.name] = label_view(mp)
                out.update({x["id"]: x["probs"] for x in read_jsonl(lp)})
    view = one_view(views, p)
    return (out, view) if return_view else out


def write_shards(keep, out_dir, shard_rows, source_info, overwrite=False):
    """Shard files first (each atomic), the manifest last. Refuses to change an existing shard set unless overwrite:
    a labelling job may be reading it."""
    out_dir = Path(out_dir)
    sizes = split_even(len(keep), shard_rows)
    rows_sha = _rows_sha(keep)
    m = out_dir / MANIFEST
    if m.exists() and not overwrite:
        old = json.loads(m.read_text())
        if old.get("rows") == len(keep) and [s["rows"] for s in old["shards"]] == sizes and \
                old.get("ids_sha256") == _ids_sha(r["id"] for r in keep) and old.get("rows_sha256") == rows_sha:
            print(f"{m} already holds this shard set; nothing written")
            return old
        raise SystemExit(f"{m} holds a different shard set; pass --overwrite to replace it (never while labelling)")
    out_dir.mkdir(parents=True, exist_ok=True)
    shards, k = [], 0
    for i, n in enumerate(sizes):
        part = keep[k:k + n]
        k += n
        p = out_dir / shard_name(i)
        write_atomic(p, [json.dumps(r) for r in part])
        shards.append({"file": p.name, "rows": n, "first_id": part[0]["id"], "last_id": part[-1]["id"],
                       "sha256": _sha_file(p)})
    man = {"rows": len(keep), "shard_rows": shard_rows, "shards": shards, "ids_sha256": _ids_sha(r["id"] for r in keep),
           "rows_sha256": rows_sha, **source_info}
    write_json_atomic(m, man)
    print(f"wrote {len(shards)} shards ({len(keep)} rows) to {out_dir}")
    return man


def _ids_sha(ids):
    return hashlib.sha256("\n".join(ids).encode()).hexdigest()


def _rows_sha(rows):
    """sha256 of the rows exactly as the shard files hold them (one JSON line each): same ids with new text differ."""
    h = hashlib.sha256()
    for r in rows:
        h.update((json.dumps(r) + "\n").encode())
    return h.hexdigest()


def _sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--golden", default="v14_parts/golden_train.jsonl", help="relative to data/")
    ap.add_argument("--relations", default="v14_parts/golden_relations.jsonl", help="relative to data/")
    ap.add_argument("--data-dir", default=str(DATA))
    ap.add_argument("--out", default="data/v14_label_shards", help="relative to this directory")
    ap.add_argument("--shard-rows", type=int, default=22000, help="target rows per shard (plan: about 20-25K)")
    ap.add_argument("--dry-run", action="store_true", help="print the counts, write nothing")
    ap.add_argument("--overwrite", action="store_true")
    a = ap.parse_args(argv)
    dd = Path(a.data_dir)
    rows = read_jsonl(dd / a.golden)
    rels = read_jsonl(dd / a.relations)
    lineage, seen = lineage_keys(dd, warn=lambda s: print(s, file=sys.stderr))
    keep, first, total = select_rows(rows, rels, lineage)
    qt = Counter(r["qtype"] for r in keep)
    chars = sum(len(r.get("state") or "") for r in keep) / max(1, len(keep))
    info = {"golden": a.golden, "golden_rows": len(rows), "excluded_first_reason": dict(first),
            "excluded_any_reason": dict(total), "excluded": len(rows) - len(keep), "lineage_rows": seen}
    print(json.dumps({**info, "to_label": len(keep), "noul_share": round(qt["noul"] / max(1, len(keep)), 4),
                      "mean_state_chars": round(chars), "shards": split_even(len(keep), a.shard_rows)}, indent=1))
    if a.dry_run:
        return keep, info
    out = Path(a.out) if Path(a.out).is_absolute() else HERE / a.out
    write_shards(keep, out, a.shard_rows, info, a.overwrite)  # prints what it wrote, or that nothing changed
    return keep, info


if __name__ == "__main__":
    main()
