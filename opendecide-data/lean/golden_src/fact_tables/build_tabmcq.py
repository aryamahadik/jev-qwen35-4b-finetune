"""v14 golden, family fact_tables: raw rows for "tabmcq" (TabMCQ v1.0, Jauhar, Turney & Hovy 2016): is a proposed
answer to a science question correct according to a table of curated science facts (Aristo Tablestore)?

Source : AI2 public bucket https://ai2-public-datasets.s3.us-west-2.amazonaws.com/tablestore-questions/TabMCQ_v_1.0.zip
         (sha256 pinned; listed on the AWS Open Data Registry entry "allenai-tablestore-questions", ManagedBy AI2).
         MCQs.tsv + Tables/{regents,monarch}/*.tsv. The package has no splits (counts as train). Tables/auto (semi-
         automatically built tables) are not used.
Licence: CC BY-SA 4.0, README.txt inside the package ("This package is distributed under the Creative Commons
         Attribution-ShareAlike 4.0 International License"); the registry entry also states CC BY-SA 4.0.
Texts  : manually curated fact tables (REGENTS and MONARCH tables, built by hand); questions, four choices and the
         correct choice written by crowd workers from one table row (human).
Rows   : state = table (header + rows) + question + proposed answer. Proposed = the correct choice (gold "yes") or
         one crowd-written wrong choice (gold "no"). ~20% ask "... is the proposed answer wrong?" (gold flips).
Precision filters (drop, never edit):
  * the correct choice must occur in the table cell the MCQ points to (RELEVANT ROW/COL) -- drops ~10% of MCQs,
    including wrong keys such as "winter solstice in the Southern hemisphere: March";
  * a wrong choice is used only if it occurs in the answer column of a DIFFERENT row (so the table itself ties it to
    other facts), not in the answer row, and that row differs from the answer row in a column the question was
    written from (QUESTION-ALIGNMENT, filler columns ignored), so it fails the question's condition; that row is
    always shown;
  * choices like "both A and B", "all/none of the above" are never used (drop the MCQ if it is the key);
  * one MCQ per (table, row), at most 45 per table (limits table memorisation); duplicate states dropped;
    13-word-run decontamination against local non-held-out files.
Tables longer than 25 rows are shown as header + answer row + the wrong choice's row (or a random row for yes rows)
+ random rows, 15 rows in all, gaps marked "| ... |".
Deterministic, CPU only (seed 20261101).   ../../../.venv/bin/python build_tabmcq.py [--manifest]
"""
import csv
import io
import random
import re
import sys
import zipfile
from collections import Counter, defaultdict

import ft_common as C

KEY = "tabmcq"
URL = "https://ai2-public-datasets.s3.us-west-2.amazonaws.com/tablestore-questions/TabMCQ_v_1.0.zip"
SHA = "9571ff2e5766721215db8046774b6f14431c6693f64825f5ef84f994455a345a"
LICENCE = ("CC BY-SA 4.0 (README.txt inside TabMCQ_v_1.0.zip, section LICENCE; AWS Open Data Registry entry "
           "allenai-tablestore-questions, ManagedBy Allen Institute for AI: 'CC BY-SA')")
CACHE = C.CACHE / "tabmcq"
MAX_PER_TABLE = 45
NEG_SHARE = 0.2
BIG = 25
SHOW = 15

Q_CORRECT = "According to the table of facts, is the proposed answer to the question correct?"
Q_WRONG = "According to the table of facts, is the proposed answer to the question wrong?"
DEFS = {
    "correct": {
        "yes": "The table's row for the fact the question asks about gives exactly the proposed answer (same entity, "
               "value or property), so it answers the question correctly.",
        "no": "The table shows the proposed answer belongs to a different row or fact than the one the question asks "
              "about, so it does not answer the question.",
    },
    "wrong": {
        "yes": "It is wrong: the table shows the proposed answer belongs to a different row or fact than the one the "
               "question asks about.",
        "no": "It is not wrong: the table's row for the fact the question asks about gives exactly the proposed answer.",
    },
}
META_CHOICE = re.compile(r"\b(both|all of the above|none of the above|neither|all of these|none of these)\b|"
                         r"^\s*[a-d]\s*(and|&)\s*[a-d]\s*$", re.I)


def main():
    zp = C.fetch(URL, CACHE / "TabMCQ_v_1.0.zip", SHA)
    z = zipfile.ZipFile(zp)
    tables = {}

    def table(name):
        if name not in tables:
            sub, num = name.split("-", 1)
            raw = z.read(f"Tables/{sub}/{num}.tsv").decode("utf-8", errors="replace")
            rows = [[C.clean_cell(c, 300) for c in l.split("\t")] for l in raw.split("\n") if l.strip()]
            w = max(len(r) for r in rows)
            tables[name] = [r + [""] * (w - len(r)) for r in rows]
        return tables[name]

    mcqs = list(csv.DictReader(io.StringIO(z.read("MCQs.tsv").decode("utf-8", errors="replace")), delimiter="\t"))
    rng = random.Random(C.SEED)
    drop = Counter()
    cands = []
    for i, r in enumerate(mcqs):
        tname = r["RELEVANT TABLE"].strip()
        if not tname.startswith(("regents-", "monarch-")):
            drop["auto table"] += 1
            continue
        try:
            t = table(tname)
            ri, ci = int(r["RELEVANT ROW"]), int(r["RELEVANT COL"])
            key = int(r["CORRECT CHOICE"])
        except Exception:  # noqa: BLE001
            drop["bad record"] += 1
            continue
        choices = [C.clean_cell(r[f"CHOICE {k}"], 300) for k in range(1, 5)]
        if not (1 <= key <= 4) or not (0 < ri < len(t)) or ci >= len(t[ri]):
            drop["bad record"] += 1
            continue
        correct = choices[key - 1]
        cell = t[ri][ci]
        nc = C.norm(correct)
        if not nc or META_CHOICE.search(correct) or f" {nc} " not in f" {C.norm(cell)} ":
            drop["key not in the answer cell / meta choice"] += 1
            continue
        if len({C.norm(c) for c in choices}) < 4:
            drop["duplicate choices"] += 1
            continue
        # columns the question was written from (QUESTION-ALIGNMENT), minus the answer column and filler columns
        # (same text in every row, e.g. "is composed of")
        try:
            align = {int(x) for x in re.findall(r"\d+", r["QUESTION-ALIGNMENT"])}
        except Exception:  # noqa: BLE001
            align = set()
        cond = [c for c in sorted(align) if c != ci and c < len(t[ri])
                and len({C.norm(row[c]) for row in t[1:] if c < len(row)}) > 1]
        wrong = []
        for k, ch in enumerate(choices):
            n = C.norm(ch)
            if k == key - 1 or not n or META_CHOICE.search(ch):
                continue
            if f" {n} " in f" {C.norm(' '.join(t[ri]))} ":
                continue  # appears in the answer row itself
            rows_with = [rr for rr in range(1, len(t)) if rr != ri and ci < len(t[rr])
                         and f" {n} " in f" {C.norm(t[rr][ci])} "]
            # the wrong choice's row must fail the question's condition: differ from the answer row in some
            # condition column (else it would answer the question too, e.g. two minerals both "found in rocks")
            rows_with = [rr for rr in rows_with
                         if cond and any(C.norm(t[rr][c]) != C.norm(t[ri][c]) for c in cond if c < len(t[rr]))]
            if rows_with:
                wrong.append((ch, rows_with[0]))
        q = C.clean_cell(r["QUESTION"], 1000)
        cands.append({"rid": f"tabmcq-{i + 1}", "table": tname, "row": ri, "col": ci, "q": q, "correct": correct,
                      "wrong": wrong})

    docs = {}
    for cd in cands:
        docs["q:" + cd["rid"]] = cd["q"]
    for name in {cd["table"] for cd in cands}:
        docs["t:" + name] = C.render_table(table(name))
    hit = C.local_decontam(docs)
    n0 = len(cands)
    cands = [cd for cd in cands if "q:" + cd["rid"] not in hit and "t:" + cd["table"] not in hit]
    drop["13-gram overlap"] = n0 - len(cands)

    by_row, seen_q = defaultdict(list), set()
    for cd in cands:
        by_row[(cd["table"], cd["row"])].append(cd)
    per_table = defaultdict(list)
    for k in sorted(by_row):
        lst = sorted(by_row[k], key=lambda c: c["rid"])
        rng.shuffle(lst)
        lst.sort(key=lambda c: not c["wrong"])
        for cd in lst:
            nq = C.norm(cd["q"])
            if nq in seen_q:
                continue
            seen_q.add(nq)
            per_table[cd["table"]].append(cd)
            break
    pool = []
    for name in sorted(per_table):
        lst = per_table[name]
        rng.shuffle(lst)
        pool += lst[:MAX_PER_TABLE]
        drop["over per-table cap"] += max(0, len(lst) - MAX_PER_TABLE)
    rng.shuffle(pool)
    can_no = [cd for cd in pool if cd["wrong"]]
    k = min(len(can_no), len(pool) // 2)
    no_ids = {cd["rid"] for cd in can_no[:k]}
    yes = [cd for cd in pool if cd["rid"] not in no_ids][:k]
    drop["label balance"] += len(pool) - 2 * k
    sel = [(cd, False) for cd in can_no[:k]] + [(cd, True) for cd in yes]
    sel.sort(key=lambda x: x[0]["rid"])
    rng.shuffle(sel)
    n_neg = int(round(NEG_SHARE * len(sel)))
    out, seen = [], set()
    for i, (cd, is_correct) in enumerate(sel):
        t = table(cd["table"])
        if is_correct:
            ans, other = cd["correct"], None
        else:
            ans, other = rng.choice(sorted(cd["wrong"]))
        n = len(t)
        if n <= BIG:
            show = list(range(n))
        else:
            fixed = {0, cd["row"]} | ({other} if other is not None else set())
            rest = [r for r in range(1, n) if r not in fixed]
            show = sorted(fixed | set(rng.sample(rest, SHOW - len(fixed))))
        lines, last = [], -1
        for r in show:
            if last >= 0 and r != last + 1:
                lines.append("| ... |")
            lines.append("| " + " | ".join(t[r]) + " |")
            last = r
        if last != n - 1:
            lines.append("| ... |")
        negq = i < n_neg
        state = (f"Science facts table (first row is the header):\n" + "\n".join(lines) +
                 f"\n\nQuestion: {cd['q']}\nProposed answer: {ans}")
        ns = C.norm(state)
        if ns in seen:
            drop["duplicate state"] += 1
            continue
        seen.add(ns)
        gold = ("yes" if not is_correct else "no") if negq else ("yes" if is_correct else "no")
        edges = []
        if negq:
            edges.append("negation")
        if re.search(r"\b(not|no|never|none|except|least)\b|n't\b", cd["q"], re.I):
            edges.append("negation")
        if re.search(r"\b(more|less|most|least|greater|smaller|larger|heavier|lighter|faster|slower|average)\b",
                     cd["q"], re.I):
            edges.append("quantifier")
        if re.search(r"\d", cd["q"] + " " + ans):
            edges.append("numeric")
        if len(state) > 3500:
            edges.append("long_context")
        edges.append("table")
        prio = ["negation", "quantifier", "numeric", "long_context", "table"]
        edge = next((e for e in prio if e in edges), None)
        out.append({
            "key": KEY, "rid": cd["rid"], "state": state, "instructions": Q_WRONG if negq else Q_CORRECT,
            "options": ["yes", "no"], "gold": gold, "soft": None,
            "meta": {"dataset": "AI2 TabMCQ v1.0 (ai2-public-datasets/tablestore-questions)", "config": "MCQs.tsv",
                     "revision": f"TabMCQ_v_1.0.zip sha256:{SHA}", "licence": LICENCE, "split": "train",
                     "orig_label": {"correct_choice": cd["correct"], "table": cd["table"], "row": cd["row"],
                                    "col": cd["col"]},
                     "family": C.FAMILY, "edge": edge, "edge_all": sorted(set(edges)),
                     "defs": "wrong" if negq else "correct", "proposed_is_gold": is_correct,
                     "context_id": cd["table"]},
        })

    summ = C.check_rows(KEY, out)
    print("drops:", dict(drop))
    print("tables:", len({r["meta"]["context_id"] for r in out}))
    C.write_outputs(KEY, out, DEFS)
    if "--manifest" in sys.argv:
        C.append_manifest({
            "key": KEY, "family": C.FAMILY, "dataset": "AI2 TabMCQ v1.0 (Aristo Tablestore MCQs)", "licence": LICENCE,
            "rows": summ["rows"], "qtype": "yesno", "yesno_share": round(summ["yesno_share"], 4),
            "edge_tags": summ["edge_tags"],
            "notes": ("Science-facts tables (manual REGENTS/MONARCH tables) + crowd MCQs recast as answer verification. "
                      "Key must sit in the pointed answer cell; wrong choices only when the table ties them to another "
                      "row (shown). One MCQ per table row, <=45 per table; 20% negated question; 13-gram decontam."),
        })


if __name__ == "__main__":
    main()
