"""Build golden v14 rows for "infotabs_nli" (InfoTabs: NLI over Wikipedia infoboxes; Gupta et al., ACL 2020).

Source : HF table-benchmark/infotabs @ 5e26f025fbbf2055f6905cf553ad9c81048891ea, data/train parquet ONLY (dev and
         the alpha1/2/3 test sets are never loaded). Table ids / annotator ids / original E-C-N codes are taken from
         the official train TSV (github.com/infotabs/infotabs @ 34e7dc0900a0d861ad62be3d7371d8eb0aace4fe,
         data/maindata/infotabs_train.tsv) and every parquet row is checked against it (hypothesis + label).
Licence: Apache-2.0, LICENSE file at the root of github.com/infotabs/infotabs (same commit; GitHub licence API
         reports spdx Apache-2.0).
Texts  : Wikipedia infoboxes + hypotheses written by MTurk workers; labels are the writers' own E / C / N (human).
         Train has no annotator vote distributions -> soft = null.
Reuse  : the 600 rows already used by the v0.13 breadth set (data/v13_parts/raw/infotabs.jsonl) are excluded, so
         this set adds only new hypotheses.
Decontamination (drop, never edit):
  * TabFact (OHS-2 held-out source): table title == a TabFact caption, or the hypothesis shares a word 8-gram (or,
    if shorter than 8 words, the whole hypothesis) with any TabFact statement (r1 + r2 collected_data, all splits;
    github.com/wenhuchen/Table-Fact-Checking @ 2ab782ba42b5808076ac91fec846473aa5315a79).
  * Our local dev/eval files: any word 13-gram of the linearised infobox or of the hypothesis, or the whole
    hypothesis (>= 6 words).
Question types (each source row used once, one type only):
  * nli3   : 3-way Entailment / Contradiction / Neutral (same card as the v0.13 breadth set)          3,000 rows
  * true   : yes/no "is the hypothesis definitely true?"  (yes = E; no = C or N)                      2,250 rows
  * false  : yes/no "is the hypothesis definitely false?" (yes = C; no = E or N)                      2,250 rows
Selection: seed 20261131, at most 5 hypotheses per table, dedupe of normalised hypotheses, state 15-4,000 chars.
"""
import ast
import json
import random
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as C  # noqa: E402

KEY = "infotabs_nli"
SEED = 20261131
HF_REPO = "table-benchmark/infotabs"
HF_REV = "5e26f025fbbf2055f6905cf553ad9c81048891ea"
HF_FILE = "data/train-00000-of-00001.parquet"
GH_REV = "34e7dc0900a0d861ad62be3d7371d8eb0aace4fe"
TF_REV = "2ab782ba42b5808076ac91fec846473aa5315a79"
LICENCE = ("Apache-2.0 (LICENSE at root of github.com/infotabs/infotabs @ 34e7dc09; HF mirror "
           "table-benchmark/infotabs carries the same data, rows verified against the official TSV)")
CACHE = C.CACHE_ROOT / "infotabs"
BREADTH_ROWS = C.LEAN / "data" / "v13_parts" / "raw" / "infotabs.jsonl"
PER_TABLE = 5
CODE = {"E": "Entailment", "C": "Contradiction", "N": "Neutral"}

Q_NLI3 = ("Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most "
          "people know, how does the hypothesis relate to the table?")
Q_TRUE = ("Treating the infobox as up to date and using only it plus facts most people know, is the hypothesis "
          "definitely true?")
Q_FALSE = ("Treating the infobox as up to date and using only it plus facts most people know, is the hypothesis "
           "definitely false?")
DEFS = {
    "nli3": {
        "Entailment": "The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), "
                      "shows the hypothesis is definitely true.",
        "Contradiction": "The infobox, plus facts most people know and simple reasoning, shows the hypothesis is "
                         "definitely false, even when the conflict is indirect (for example via dates, counts or "
                         "roles).",
        "Neutral": "The hypothesis adds details the infobox does not cover, and facts most people know cannot settle "
                   "them, so it may or may not be true.",
    },
    "true": {
        "yes": "The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the "
               "hypothesis is definitely true.",
        "no": "The hypothesis is not established: either the infobox shows it is false, or it adds details the "
              "infobox does not cover, so it may or may not be true.",
    },
    "false": {
        "yes": "The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely "
               "false, even when the conflict is indirect (for example via dates, counts or roles).",
        "no": "The hypothesis is not shown to be false: either the infobox confirms it, or it concerns details the "
              "infobox does not cover, so it may or may not be true.",
    },
}
# per question type: {orig code: rows}
QUOTA = {
    "nli3": {"E": 1000, "C": 1000, "N": 1000},
    "true": {"E": 1125, "C": 562, "N": 563},
    "false": {"C": 1125, "E": 562, "N": 563},
}
GOLD = {
    "nli3": lambda c: CODE[c],
    "true": lambda c: "yes" if c == "E" else "no",
    "false": lambda c: "yes" if c == "C" else "no",
}
NEG = re.compile(r"\b(not|no|never|none|neither|nor|without|nobody|nothing)\b|n't\b", re.I)
QUANT = re.compile(r"\b(all|every|each|some|only|at least|at most|more than|less than|fewer than|exactly|most|"
                   r"several|many|both|any|multiple|majority|over|under)\b", re.I)
TEMP = re.compile(r"\b(\d{4}|years?|century|decades?|months?|before|after|born|died|age|aged|old|older|younger|"
                  r"since|until|during|currently|still|former|later|earlier|first|last)\b", re.I)
NUM = re.compile(r"\d|\b(one|two|three|four|five|six|seven|eight|nine|ten|twice|double|half)\b", re.I)


def edge_of(h):
    if NEG.search(h):
        return "negation"
    if QUANT.search(h):
        return "quantifier"
    if TEMP.search(h):
        return "temporal"
    if NUM.search(h):
        return "numeric"
    return "table"


def load_train():
    pq = CACHE / "train-00000-of-00001.parquet"
    if not pq.exists():
        from huggingface_hub import hf_hub_download
        p = hf_hub_download(HF_REPO, HF_FILE, repo_type="dataset", revision=HF_REV)
        CACHE.mkdir(parents=True, exist_ok=True)
        shutil.copy(p, pq)
    sha = C.sha256_file(pq)
    df = pd.read_parquet(pq)
    tsv = C.fetch(f"https://raw.githubusercontent.com/infotabs/infotabs/{GH_REV}/data/maindata/infotabs_train.tsv",
                  CACHE / "infotabs_train_github.tsv")
    gh = pd.read_csv(tsv, sep="\t", dtype=str, keep_default_na=False, quoting=3)
    assert len(gh) == len(df), (len(gh), len(df))
    rows, mism = [], 0
    for r in df.itertuples(index=False):
        g = gh.iloc[int(r.original_dataset_id) - 1]
        if g.hypothesis.strip() != r.question.strip() or CODE[g.label] != r.answer:
            mism += 1
            continue
        rows.append({"oid": str(r.original_dataset_id), "table_raw": r.table, "title": r.table_title,
                     "hyp": r.question, "code": g.label, "table_id": g.table_id, "annotator": g.annotater_id})
    print(f"train rows {len(df)}, aligned {len(rows)}, mismatched {mism}, parquet sha256 {sha[:16]}")
    return rows, {"parquet": sha, "tsv": C.sha256_file(tsv)}


def linearise(table_raw):
    d = ast.literal_eval(table_raw)
    lines = []
    for k, vals in d.items():
        if not isinstance(vals, list):
            vals = [vals]
        vals = [C.clean(v) for v in vals if C.clean(v)]
        if not vals:
            continue
        key = "Title" if k == "title" else C.clean(k)
        lines.append(f"{key}: {', '.join(vals)}")
    return "\n".join(lines)


def tabfact_index():
    caps, grams, short = set(), set(), set()
    for f in ["r1_training_all.json", "r2_training_all.json"]:
        p = C.fetch(f"https://raw.githubusercontent.com/wenhuchen/Table-Fact-Checking/{TF_REV}/collected_data/{f}",
                    CACHE / "tabfact" / f)
        for _tid, (stmts, _labels, cap) in json.load(open(p)).items():
            caps.add(" ".join(C.words(cap)))
            for s in stmts:
                ws = C.words(s)
                grams |= C.ngrams(ws, 8)
                short.add(" ".join(ws))
    return caps, grams, short


def main():
    rows, sha = load_train()
    used = set()
    if BREADTH_ROWS.exists():
        for line in open(BREADTH_ROWS):
            used.add(json.loads(line)["rid"].rsplit("_", 1)[1])
    n0 = len(rows)
    rows = [r for r in rows if r["oid"] not in used]
    print(f"excluded v0.13 breadth rows: {n0 - len(rows)}")

    for r in rows:
        r["table_txt"] = linearise(r["table_raw"])
        r["state"] = f"Infobox:\n{r['table_txt']}\n\nHypothesis: {C.clean(r['hyp'])}"
        r["hw"] = C.words(r["hyp"])
        r["hn"] = " ".join(r["hw"])

    caps, tf8, tfshort = tabfact_index()
    n1 = len(rows)

    def tf_bad(r):
        if " ".join(C.words(r["title"])) in caps:
            return True
        if len(r["hw"]) < 8:
            return r["hn"] in tfshort
        return bool(C.ngrams(r["hw"], 8) & tf8)
    rows = [r for r in rows if not tf_bad(r)]
    print(f"TabFact decontam dropped {n1 - len(rows)} rows")

    tables = {}
    for r in rows:
        tables.setdefault(r["table_id"], r["table_txt"])
    tgrams = {tid: C.ngrams(C.words(t), 13) for tid, t in tables.items()}
    hpats = {}
    for r in rows:
        ps = C.ngrams(r["hw"], 13)
        if len(r["hw"]) >= 6:
            ps.add(r["hn"])
        hpats[r["oid"]] = ps
    hits = C.local_hits(set().union(*tgrams.values(), *hpats.values()))
    bad_tables = {tid for tid, g in tgrams.items() if g & hits}
    n2 = len(rows)
    rows = [r for r in rows if r["table_id"] not in bad_tables and not (hpats[r["oid"]] & hits)]
    print(f"local decontam dropped {n2 - len(rows)} rows ({len(bad_tables)} tables)")
    rows = [r for r in rows if 15 <= len(r["state"]) <= 4000 and r["code"] in CODE]

    rng = random.Random(SEED)
    rows.sort(key=lambda r: int(r["oid"]))
    rng.shuffle(rows)
    # dedupe hypotheses globally
    seen, uniq = set(), []
    for r in rows:
        if r["hn"] in seen:
            continue
        seen.add(r["hn"])
        uniq.append(r)
    rows = uniq

    # pools per (qtype, code); a row may enter only once overall; per-table cap across all types
    need = {(q, c): n for q, qq in QUOTA.items() for c, n in qq.items()}
    by_code = defaultdict(list)
    for r in rows:
        by_code[r["code"]].append(r)
    ptr = Counter()
    per_table = Counter()
    got = Counter()
    picked = []
    order = list(need)
    active = list(order)
    while active:
        for qc in list(active):
            q, c = qc
            pool = by_code[c]
            placed = False
            while ptr[c] < len(pool):
                r = pool[ptr[c]]
                ptr[c] += 1
                if per_table[r["table_id"]] >= PER_TABLE:
                    continue
                per_table[r["table_id"]] += 1
                picked.append((q, r))
                got[qc] += 1
                placed = True
                break
            if not placed or got[qc] >= need[qc]:
                active.remove(qc)
    print("picked per (qtype, code):", dict(got))

    out = []
    qtext = {"nli3": Q_NLI3, "true": Q_TRUE, "false": Q_FALSE}
    for q, r in picked:
        opts = list(DEFS[q])
        out.append({
            "key": KEY,
            "rid": f"infotabs_train_{r['oid']}",
            "state": r["state"],
            "instructions": qtext[q],
            "options": opts if q == "nli3" else ["yes", "no"],
            "gold": GOLD[q](r["code"]),
            "soft": None,
            "meta": {"dataset": HF_REPO, "config": "default", "revision": HF_REV, "licence": LICENCE,
                     "split": "train", "orig_label": r["code"], "family": C.FAMILY, "edge": edge_of(r["hyp"]),
                     "defs": q, "table_id": r["table_id"], "annotator": r["annotator"], "source_sha256": sha},
        })
    rng.shuffle(out)
    C.validate_rows(KEY, out, DEFS)
    C.write_rows(KEY, out)
    for q, d in DEFS.items():
        C.write_defs(KEY, d, qid=q)
    share = C.report(KEY, out)
    print("distinct tables:", len({r["meta"]["table_id"] for r in out}))
    e = Counter(r["meta"]["edge"] for r in out)
    C.append_manifest({
        "key": KEY, "family": C.FAMILY, "dataset": "InfoTabs (train; table-benchmark/infotabs + official TSV)",
        "licence": LICENCE, "rows": len(out),
        "qtype": "mixed: 3-way NLI (nli3) + yes/no 'definitely true?' (true) + yes/no 'definitely false?' (false)",
        "yesno_share": round(share, 4) if share is not None else None, "edge_tags": sorted(k for k in e if k),
        "notes": "Human hypotheses over Wikipedia infoboxes (table reasoning: dates, ages, counts, roles). Excludes "
                 "the 600 rows in v0.13 breadth; TabFact + local dev/eval decontaminated; <=5 hypotheses per table; "
                 "defs per question type in defs/infotabs_nli__{nli3,true,false}.json.",
    })
    if "--show" in sys.argv:
        C.show_samples(out, 6)


if __name__ == "__main__":
    main()
