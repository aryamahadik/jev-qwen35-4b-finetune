"""13-gram decontamination for the routing_dialogue v14 parts (CPU only, no model calls).

For every row written by this family's builders, look for a 13-word run (lower-cased, punctuation stripped) or an exact
state shared with (a) our existing train/dev/eval files lean/data/*.jsonl (ohs* files are never opened), (b) the
JevBench public files, (c) the v0.13 breadth raw parts (data/v13_parts/raw, e.g. the STAR user turns) and (d) every other
v14 raw part not written by this family. Hits go to decon_hits.json; builders drop those rids when they write
(_rd_common.write_rows) and this script also removes them from the current raw files in place.
Family-internal boilerplate n-grams (template assistant replies such as "is there anything else that I can do for you")
are not evidence: an n-gram only counts if it occurs in <= 3 of this family's rows.
"""
import collections
import glob
import json
import re
from pathlib import Path

import _rd_common as C

KEYS = ["smcalflow_action", "star_next_action", "sd311_routing", "wiki_help_routing"]
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
    grams = {g: ks for g, ks in grams.items() if len(ks) <= 3}
    files = [f for f in sorted(glob.glob(str(C.LEAN / "data" / "*.jsonl"))) if not Path(f).name.startswith("ohs")]
    files += sorted(glob.glob(str(JB / "*.jsonl")))
    files += sorted(glob.glob(str(C.LEAN / "data" / "v13_parts" / "raw" / "*.jsonl")))
    files += [f for f in sorted(glob.glob(str(C.RAW / "*.jsonl"))) if Path(f).stem not in KEYS]
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
    for k, rid, src in out[:40]:
        print("  ", k, rid, src[:4])
    print("hits per key:", dict(collections.Counter(k for k, _, _ in out)))
    drop = set(merged)
    for k in KEYS:
        p = C.RAW / f"{k}.jsonl"
        if not p.exists():
            continue
        kept = [l for l in open(p) if (k, json.loads(l)["rid"]) not in drop]
        with open(p, "w") as f:
            f.writelines(kept)
        print(f"  {k}: {len(kept)} rows after decon")


if __name__ == "__main__":
    main()
