"""Counts-only overlap check of the clean think sets (clean_sets.py candidates) against held-out items. FOR THE
ORCHESTRATOR: it reads the reference files in this process only and never prints or stores their text.

A17: "Clean sets only: public TRAIN or validation splits that share no item with the Decision Index test items,
OHS-1/2/3, ejs-5, JevBench or the sealed suite. Overlap is checked counts-only before any read."
PLAN_knowledge_gap.md section 4 (decontamination): drop a candidate on an exact match after normalising the text, or a
shared 13-word sequence; n-grams found in more than --boiler (20) items of one reference are template text and are
ignored (the DI overlap tool's rule). The embedding-similarity >= 0.92 rule is NOT run here (no embedding model on
this CPU path); the output says so.

References (each name=path; a path is a .jsonl / .jsonl.gz / .parquet / .json file or a folder of them):
  --di      the Decision Index items as a file/folder OUTSIDE bench/external_quarantine (no default). PLAN_knowledge_gap
            section 4: compare against the public full test sets "so the existing quarantine never needs opening";
            any path inside bench/external_quarantine is refused.
  --ref     any other held-out set: public full test sets in a git-ignored quarantine-style folder (MMLU test, all GPQA,
            GSM8K test, CRUXEval, CLadder, ARC test, HellaSwag val, WinoGrande dev, MuSR, SATA-Bench), OHS-1/2/3,
            ejs-5, JevBench, the sealed exports.
Text of a reference item = every string leaf of the record (keys starting with "_" skipped). Text of a candidate =
its question (state) and options (the fixed instruction line is left out).
Words = lowercase [a-z0-9]+ runs (decontam.py rule). Exact match = a candidate's normalised question equals a
normalised string leaf (>= 6 words) of a reference item.

  python think/check_overlap_di.py [--candidates think/data/clean] [--di PATH] [--ref name=path ...] [--n 13]
Writes data/clean/overlap_drop_ids.json (our candidate ids to drop + counts + candidate sha256) and
data/clean/overlap_report.json (counts only). Prints counts only.
"""
from __future__ import annotations

import argparse
import gzip
import json
import re
import sys
from pathlib import Path

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

HERE = Path(__file__).resolve().parent
JEV = HERE.parents[2]
sys.path.insert(0, str(HERE))
from common import read_jsonl, sha256_file  # noqa: E402

QUARANTINE = (JEV / "bench/external_quarantine").resolve()


def _no_quarantine(path) -> Path:
    p = Path(path).resolve()
    if p == QUARANTINE or QUARANTINE in p.parents:
        raise SystemExit(f"refused: {path} is inside bench/external_quarantine (use the public full test sets)")
    return Path(path)
W = re.compile(r"[a-z0-9]+")
MASK = (1 << 64) - 1
EXACT_MIN_WORDS = 6


def words(t: str) -> list:
    return W.findall(str(t).lower())


def leaves(x, out):
    if isinstance(x, str):
        out.append(x)
    elif isinstance(x, dict):
        for k, v in x.items():
            if not str(k).startswith("_"):
                leaves(v, out)
    elif isinstance(x, (list, tuple)):
        for v in x:
            leaves(v, out)
    return out


class Hasher:
    def __init__(self, n):
        self.n = n
        self.pow = np.random.default_rng(12345).integers(1, 2 ** 63, size=n, dtype=np.uint64) | np.uint64(1)

    def grams(self, ws) -> np.ndarray:
        if len(ws) < self.n:
            return np.empty(0, dtype=np.uint64)
        ids = np.fromiter((hash(w) & MASK for w in ws), dtype=np.uint64, count=len(ws))
        with np.errstate(over="ignore"):
            return np.unique((sliding_window_view(ids, self.n) * self.pow).sum(axis=1, dtype=np.uint64))


def _files(path: Path) -> list:
    if path.is_dir():
        return sorted(p for p in path.rglob("*") if p.is_file() and (p.suffix in (".jsonl", ".parquet", ".json")
                                                                      or p.name.endswith(".jsonl.gz")))
    return [path]


def iter_items(path: Path):
    for f in _files(path):
        if f.suffix == ".parquet":
            import pyarrow.parquet as pq
            yield from pq.read_table(f).to_pylist()
        elif f.name.endswith(".jsonl.gz") or f.suffix == ".jsonl":
            op = gzip.open if f.name.endswith(".gz") else open
            with op(f, "rt", encoding="utf-8") as fh:
                for line in fh:
                    if line.strip():
                        yield json.loads(line)
        else:
            d = json.loads(f.read_text())
            yield from (d if isinstance(d, list) else next((v for v in d.values() if isinstance(v, list)), [d]))


def norm(t: str) -> str:
    return " ".join(words(t))


class Ref:
    """Hashed n-grams (boilerplate removed) and exact-match keys of one reference. Holds no text after build."""

    def __init__(self, name, path, H: Hasher, boiler: int):
        self.name, self.path = name, Path(path)
        per, exact, n = [], set(), 0
        for it in iter_items(self.path):
            n += 1
            ls = leaves(it, [])
            per.append(H.grams(words("\n".join(ls))))
            for s in ls:
                k = norm(s)
                if len(k.split()) >= EXACT_MIN_WORDS:
                    exact.add(hash(k))
        allg = np.concatenate(per) if per else np.empty(0, dtype=np.uint64)
        uniq, cnt = np.unique(allg, return_counts=True)
        self.S = uniq[cnt <= boiler]
        self.exact = exact
        self.info = {"name": name, "path": str(self.path), "files": len(_files(self.path)), "items": n,
                     "grams": int(len(uniq)), "boilerplate_grams_dropped": int((cnt > boiler).sum()),
                     "exact_keys": len(exact)}

    def hit(self, g: np.ndarray, exact_key: int) -> tuple:
        ng = False
        if len(g) and len(self.S):
            i = np.searchsorted(self.S, g)
            i[i >= len(self.S)] = 0
            ng = bool((self.S[i] == g).any())
        return ng, exact_key in self.exact


def candidate_sets(cdir: Path) -> dict:
    return {p.name[: -len(".candidates.jsonl")]: p for p in sorted(cdir.glob("*.candidates.jsonl"))}


def run(cdir: Path, refs: list, n=13, boiler=20, out_dir=None) -> dict:
    """refs: [(name, path)]. Returns the drop file content (our ids + counts); writes both output files."""
    H = Hasher(n)
    built = [Ref(name, path, H, boiler) for name, path in refs]
    sets = candidate_sets(cdir)
    drop, counts, cand_sha = {}, {}, {}
    for s, p in sets.items():
        cand_sha[s] = sha256_file(p)
        c = {r.name: {"ngram": 0, "exact": 0} for r in built}
        ids, total = [], 0
        for row in read_jsonl(p):
            total += 1
            q = row.get("state") or ""
            g = H.grams(words(q + "\n" + "\n".join(row.get("options") or [])))
            k = hash(norm(q))
            bad = False
            for r in built:
                ng, ex = r.hit(g, k)
                c[r.name]["ngram"] += int(ng)
                c[r.name]["exact"] += int(ex)
                bad |= ng or ex
            if bad:
                ids.append(row["id"])
        drop[s] = ids
        counts[s] = {"candidates": total, "dropped": len(ids), "per_ref": c}
    res = {"ngram": n, "boilerplate_threshold_items": boiler, "exact_min_words": EXACT_MIN_WORDS,
           "embedding_check": "not run (no embedding model on this CPU path; plan rule sim >= 0.92)",
           "refs": [r.info for r in built], "candidates": cand_sha, "counts": counts, "drop_ids": drop}
    out_dir = Path(out_dir or cdir)
    (out_dir / "overlap_drop_ids.json").write_text(json.dumps(res, indent=1) + "\n")
    rep = {k: v for k, v in res.items() if k != "drop_ids"}
    (out_dir / "overlap_report.json").write_text(json.dumps(rep, indent=2) + "\n")
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--candidates", default=str(HERE / "data" / "clean"))
    ap.add_argument("--di", default=None, help="DI items file/folder outside the quarantine (optional)")
    ap.add_argument("--ref", action="append", default=[], help="name=path of another held-out set")
    ap.add_argument("--n", type=int, default=13)
    ap.add_argument("--boiler", type=int, default=20)
    a = ap.parse_args(argv)
    refs = []
    if a.di:
        if not Path(a.di).exists():
            raise SystemExit("--di: path missing")
        refs.append(("decision_index", _no_quarantine(a.di)))
    for spec in a.ref:
        name, path = spec.split("=", 1)
        if not Path(path).exists():
            raise SystemExit(f"--ref {name}: path missing")
        refs.append((name, _no_quarantine(path)))
    if not refs:
        raise SystemExit("no references given")
    res = run(Path(a.candidates), refs, a.n, a.boiler)
    print(json.dumps({"refs": [{k: r[k] for k in ("name", "items", "boilerplate_grams_dropped")} for r in res["refs"]],
                      "counts": {s: {k: v[k] for k in ("candidates", "dropped")} for s, v in res["counts"].items()}},
                     indent=1))


if __name__ == "__main__":
    main()
