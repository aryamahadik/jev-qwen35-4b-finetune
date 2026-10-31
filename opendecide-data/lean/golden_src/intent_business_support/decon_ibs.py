"""13-gram decontamination for the intent_business_support v14 parts (CPU only, no model calls).

For every row written by this family's builders, look for a 13-word run (after lower-casing and stripping punctuation)
or an exact state shared with (a) our existing train/dev/eval files lean/data/*.jsonl (ohs* files are never opened) and
(b) the JevBench public files. Hits are written to decon_hits.json; every builder drops those rids when it writes
(see _ibs_common.write_rows), and this script also removes them from the current raw files in place.
Generic dialogue boilerplate n-grams that occur in many of our own rows (e.g. "is there anything else i can help you
with today") are not counted as evidence: an n-gram only counts if it occurs in <= 3 of this family's rows.
"""
import collections
import glob
import json
import re
from pathlib import Path

import _ibs_common as C

KEYS = ["dstc9_track1", "multiwoz21_sysacts", "taskmaster1", "taskmaster2", "taskmaster3", "nhtsa_complaints"]
N = 13
JB = C.LEAN.parents[1] / "bench" / "jevbench" / "datasets" / "public"
OUT = C.HERE / "decon_hits.json"


def words(t):
    return re.findall(r"[a-z0-9]+", t.lower())


def main():
    rows = {}
    for k in KEYS:
        p = C.RAW / f"{k}.jsonl"
        if p.exists():
            for line in open(p):
                r = json.loads(line)
                rows[(k, r["rid"])] = r
    grams = collections.defaultdict(set)
    exact = {}
    for key, r in rows.items():
        w = words(r["state"])
        exact[" ".join(w)] = key
        for i in range(len(w) - N + 1):
            grams[" ".join(w[i:i + N])].add(key)
    grams = {g: ks for g, ks in grams.items() if len(ks) <= 3}  # drop family-internal boilerplate
    files = [f for f in sorted(glob.glob(str(C.LEAN / "data" / "*.jsonl"))) if not Path(f).name.startswith("ohs")]
    files += sorted(glob.glob(str(JB / "*.jsonl")))
    hits = collections.defaultdict(set)
    for f in files:
        with open(f, encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                st = r.get("state") if isinstance(r, dict) else None
                if isinstance(st, str):
                    ek = " ".join(words(st))
                    if ek in exact:
                        hits[exact[ek]].add(Path(f).name + ":exact")
                w = words(line.replace("\\n", " "))
                for i in range(len(w) - N + 1):
                    g = " ".join(w[i:i + N])
                    if g in grams:
                        for key in grams[g]:
                            hits[key].add(Path(f).name)
    out = sorted([k, rid, sorted(v)] for (k, rid), v in hits.items())
    prev = json.load(open(OUT)) if OUT.exists() else []
    merged = {(k, rid): src for k, rid, src in prev}
    for k, rid, src in out:
        merged[(k, rid)] = sorted(set(merged.get((k, rid), [])) | set(src))
    with open(OUT, "w") as f:
        json.dump(sorted([k, rid, src] for (k, rid), src in merged.items()), f, indent=0)
    print(f"checked {len(files)} files; rows={len(rows)}; hits={len(out)}")
    for k, rid, src in out[:30]:
        print("  ", k, rid, src[:4])
    by_key = collections.Counter(k for k, _, _ in out)
    print("hits per key:", dict(by_key))
    # remove hits from the current raw files
    drop = {(k, rid) for k, rid in merged}
    for k in KEYS:
        p = C.RAW / f"{k}.jsonl"
        if not p.exists():
            continue
        kept = [line for line in open(p) if (k, json.loads(line)["rid"]) not in drop]
        with open(p, "w") as f:
            f.writelines(kept)


if __name__ == "__main__":
    main()
