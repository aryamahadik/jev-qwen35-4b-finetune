"""Build raw rows for the v0.13 breadth set "infotabs" (InfoTabs, NLI over Wikipedia infoboxes).

Source: HF table-benchmark/infotabs @ 5e26f025fbbf2055f6905cf553ad9c81048891ea, data/train parquet ONLY
(dev and test alpha1/2/3 are never loaded). Raw snapshot kept in breadth_src/cache/infotabs/.
Table ids / annotator ids / original E-C-N codes come from the official train TSV
(github.com/infotabs/infotabs @ 34e7dc0900a0d861ad62be3d7371d8eb0aace4fe, data/maindata/infotabs_train.tsv).
Licence: Apache-2.0, LICENSE file at the root of github.com/infotabs/infotabs (same commit; GitHub licence API
reports spdx Apache-2.0). Texts: Wikipedia infoboxes + hypotheses written by MTurk workers; labels are the
writers' own E/C/N (human). No annotator distributions exist for train (validation votes only cover dev/test),
so soft = null.

Decontamination (drop, never edit):
  * TabFact (OHS-2 held-out source): table title == a TabFact caption, or the hypothesis shares a word 8-gram
    (or, if shorter than 8 words, the whole hypothesis) with any TabFact statement (r1+r2 collected_data, all splits).
  * Our own local files (data/*.jsonl except ohs*): any word 13-gram of the linearised infobox or of the
    hypothesis, or the whole hypothesis (>= 6 words), occurring in any string of any line.
Selection: seed 20261101, one row per table (1,590 train tables -> breadth), round-robin over labels, dedup of
normalised hypotheses, state length 15-4,000 chars, at most 600 rows.
"""
import ast
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

import pandas as pd

SEED = 20261101
MAX_ROWS = 600
KEY = "infotabs"
HF_REPO = "table-benchmark/infotabs"
HF_REV = "5e26f025fbbf2055f6905cf553ad9c81048891ea"
HF_FILE = "data/train-00000-of-00001.parquet"
GH_REV = "34e7dc0900a0d861ad62be3d7371d8eb0aace4fe"
LICENCE = ("Apache-2.0 (LICENSE at root of github.com/infotabs/infotabs @ 34e7dc09; "
           "HF mirror table-benchmark/infotabs carries the same data)")

LEAN = Path(__file__).resolve().parent.parent
CACHE = LEAN / "breadth_src" / "cache" / "infotabs"
OUT = LEAN / "data" / "v13_parts" / "raw" / f"{KEY}.jsonl"
DEFS = LEAN / "data" / "v13_parts" / "defs" / f"{KEY}.json"

LABELS = ["Entailment", "Contradiction", "Neutral"]
CODE = {"E": "Entailment", "C": "Contradiction", "N": "Neutral"}
INSTRUCTIONS = ("Treat the infobox as up to date (its dates and ages are current). Using only the infobox and "
                "facts most people know, how does the hypothesis relate to the table?")

WORD = re.compile(r"[a-z0-9]+")


def words(s):
    return WORD.findall(s.lower())


def ngrams(ws, n):
    return {" ".join(ws[i:i + n]) for i in range(len(ws) - n + 1)}


def fetch(url, dest):
    if not dest.exists():
        subprocess.run(["curl", "-sfL", "-o", str(dest), url], check=True)
    return dest


def load_train():
    pq = CACHE / "train-00000-of-00001.parquet"
    if not pq.exists():
        from huggingface_hub import hf_hub_download
        p = hf_hub_download(HF_REPO, HF_FILE, repo_type="dataset", revision=HF_REV)
        CACHE.mkdir(parents=True, exist_ok=True)
        shutil.copy(p, pq)
    sha = hashlib.sha256(pq.read_bytes()).hexdigest()
    df = pd.read_parquet(pq)
    tsv = fetch(f"https://raw.githubusercontent.com/infotabs/infotabs/{GH_REV}/data/maindata/infotabs_train.tsv",
                CACHE / "infotabs_train_github.tsv")
    gh = pd.read_csv(tsv, sep="\t", dtype=str, keep_default_na=False, quoting=3)
    assert len(gh) == len(df), (len(gh), len(df))
    rows = []
    mism = 0
    for i, r in enumerate(df.itertuples(index=False)):
        g = gh.iloc[int(r.original_dataset_id) - 1]
        if g.hypothesis.strip() != r.question.strip() or CODE[g.label] != r.answer:
            mism += 1
            continue
        rows.append({"oid": r.original_dataset_id, "table_raw": r.table, "title": r.table_title,
                     "hyp": r.question, "label": r.answer, "code": g.label, "table_id": g.table_id,
                     "annotator": g.annotater_id})
    print(f"train rows {len(df)}, aligned with GitHub TSV {len(rows)}, mismatched {mism}, parquet sha256 {sha[:16]}")
    return rows, sha


def clean(v):
    return re.sub(r"\s+", " ", str(v)).strip()


def linearise(table_raw):
    d = ast.literal_eval(table_raw)
    lines = []
    for k, vals in d.items():
        if not isinstance(vals, list):
            vals = [vals]
        vals = [clean(v) for v in vals if clean(v)]
        if not vals:
            continue
        key = "Title" if k == "title" else clean(k)
        lines.append(f"{key}: {', '.join(vals)}")
    return "\n".join(lines)


def tabfact_index():
    tf = CACHE / "tabfact"
    tf.mkdir(parents=True, exist_ok=True)
    caps, grams, short = set(), set(), set()
    for f in ["r1_training_all.json", "r2_training_all.json"]:
        p = fetch(f"https://raw.githubusercontent.com/wenhuchen/Table-Fact-Checking/master/collected_data/{f}",
                  tf / f)
        for _tid, (stmts, _labels, cap) in json.load(open(p)).items():
            caps.add(" ".join(words(cap)))
            for s in stmts:
                ws = words(s)
                grams |= ngrams(ws, 8)
                short.add(" ".join(ws))
    return caps, grams, short


def iter_strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from iter_strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from iter_strings(v)


def local_hits(patterns):
    """Return the subset of normalised patterns (space-bounded) that occur in our local non-OHS data files."""
    files = sorted(p for p in (LEAN / "data").glob("*.jsonl") if not p.name.startswith("ohs"))
    tmpdir = Path(tempfile.mkdtemp(prefix="infotabs_decon_"))
    norm, pat = tmpdir / "norm.txt", tmpdir / "pat.txt"
    try:
        with open(norm, "w") as out:
            for f in files:
                with open(f, errors="replace") as fh:
                    for line in fh:
                        try:
                            o = json.loads(line)
                        except Exception:
                            o = line
                        for s in iter_strings(o):
                            ws = words(s)
                            if len(ws) >= 6:
                                out.write(" " + " ".join(ws) + " \n")
        pat.write_text("".join(f" {p} \n" for p in sorted(patterns)))
        tool = shutil.which("rg") or "grep"  # ripgrep (Aho-Corasick) is far faster than BSD grep for big -f lists
        res = subprocess.run([tool, "-F", "-o", "-N", "--no-filename", "-f", str(pat), str(norm)]
                             if tool.endswith("rg") else [tool, "-F", "-o", "-h", "-f", str(pat), str(norm)],
                             capture_output=True, text=True)
        assert res.returncode in (0, 1), res.stderr
        hits = {h.strip() for h in res.stdout.splitlines() if h.strip()}
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    print(f"local decontam: scanned {len(files)} files, {len(patterns)} patterns, {len(hits)} hit patterns")
    return hits


def main():
    rows, sha = load_train()
    for r in rows:
        r["table_txt"] = linearise(r["table_raw"])
        r["state"] = f"Premise:\n{r['table_txt']}\nHypothesis: {clean(r['hyp'])}"
        r["hw"] = words(r["hyp"])
        r["hn"] = " ".join(r["hw"])

    # --- TabFact decontam
    caps, tf8, tfshort = tabfact_index()
    n0 = len(rows)
    def tf_bad(r):
        if " ".join(words(r["title"])) in caps:
            return True
        if len(r["hw"]) < 8:
            return r["hn"] in tfshort
        return bool(ngrams(r["hw"], 8) & tf8)
    rows = [r for r in rows if not tf_bad(r)]
    print(f"TabFact decontam dropped {n0 - len(rows)} rows")

    # --- local 13-gram decontam (tables + hypotheses)
    tables = {}
    for r in rows:
        tables.setdefault(r["table_id"], r["table_txt"])
    tgrams = {tid: ngrams(words(t), 13) for tid, t in tables.items()}
    hpats = {}
    for r in rows:
        ps = ngrams(r["hw"], 13)
        if len(r["hw"]) >= 6:
            ps.add(r["hn"])
        hpats[r["oid"]] = ps
    allp = set().union(*tgrams.values(), *hpats.values())
    hits = local_hits(allp)
    bad_tables = {tid for tid, g in tgrams.items() if g & hits}
    n1 = len(rows)
    rows = [r for r in rows if r["table_id"] not in bad_tables and not (hpats[r["oid"]] & hits)]
    print(f"local decontam dropped {n1 - len(rows)} rows ({len(bad_tables)} tables)")

    # --- filters, selection
    rows = [r for r in rows if 15 <= len(r["state"]) <= 4000 and r["label"] in LABELS]
    rng = random.Random(SEED)
    rows.sort(key=lambda r: int(r["oid"]))
    rng.shuffle(rows)
    pools = {lab: [r for r in rows if r["label"] == lab] for lab in LABELS}
    used_tables, seen_h, out = set(), set(), []
    ptr = {lab: 0 for lab in LABELS}
    active = list(LABELS)
    while len(out) < MAX_ROWS and active:
        for lab in list(active):
            if len(out) >= MAX_ROWS:
                break
            pool = pools[lab]
            while ptr[lab] < len(pool):
                r = pool[ptr[lab]]
                ptr[lab] += 1
                if r["table_id"] in used_tables or r["hn"] in seen_h:
                    continue
                used_tables.add(r["table_id"])
                seen_h.add(r["hn"])
                out.append(r)
                break
            else:
                active.remove(lab)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as f:
        for r in out:
            f.write(json.dumps({
                "key": KEY,
                "rid": f"infotabs_train_{r['oid']}",
                "state": r["state"],
                "instructions": INSTRUCTIONS,
                "options": LABELS,
                "gold": r["label"],
                "soft": None,
                "meta": {"dataset": HF_REPO, "config": "default", "revision": HF_REV, "licence": LICENCE,
                         "split": "train", "orig_label": r["code"], "table_id": r["table_id"],
                         "source_parquet_sha256": sha},
            }, ensure_ascii=False) + "\n")

    # Faithful to the InfoTabs MTurk guideline (annotation-template1.html): "Using only the table and what you
    # believe most people know about the world" write a statement that is definitely true / may or may not be
    # true / definitely false; statements should need some inference, not restate the table.
    defs = {
        "Entailment": "The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), "
                      "shows the hypothesis is definitely true.",
        "Contradiction": "The infobox, plus facts most people know and simple reasoning, shows the hypothesis is "
                         "definitely false, even when the conflict is indirect (for example via dates, counts or roles).",
        "Neutral": "The hypothesis adds details the infobox does not cover, and facts most people know cannot "
                   "settle them, so it may or may not be true.",
    }
    for k, v in defs.items():
        assert 8 <= len(v.split()) <= 35, k
    DEFS.parent.mkdir(parents=True, exist_ok=True)
    DEFS.write_text(json.dumps(defs, indent=1, ensure_ascii=False) + "\n")

    # --- report
    c = Counter(r["label"] for r in out)
    L = sorted(len(r["state"]) for r in out)
    print(f"wrote {len(out)} rows -> {OUT}")
    print("labels:", dict(c), "max share %.1f%%" % (100 * max(c.values()) / len(out)))
    print("soft-label coverage: 0/%d (InfoTabs train has no annotator votes)" % len(out))
    print(f"state chars: min {L[0]} median {L[len(L)//2]} mean {sum(L)/len(L):.0f} max {L[-1]}")
    print(f"distinct tables {len(used_tables)}")


if __name__ == "__main__":
    sys.exit(main())
