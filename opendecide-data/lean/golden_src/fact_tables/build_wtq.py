"""v14 golden, family fact_tables: raw rows for "wtq" (WikiTableQuestions, Pasupat & Liang, ACL 2015) as yes/no
answer verification against a Wikipedia table.

Source : GitHub ppasupat/WikiTableQuestions release v1.0.2 (WikiTableQuestions-1.0.2-compact.zip, sha256 pinned), file
         data/training.tsv ONLY (pristine-unseen-tables = the test set and pristine-seen-tables are never read) and the
         training tables csv/*/*.tsv; page titles from page/<t>-page/<id>.json at repo commit 7d455a5a (only files of
         training tables are fetched). Question filter: SQUALL (github tzshi/squall @ ee6dda91, data/squall.json,
         CC BY-SA 4.0 in LICENSE-data): only WTQ training questions that SQUALL's expert annotators could write a
         deterministic SQL query for are used (drops "show me an example of ..." and other non-deterministic
         questions, whose other answers could also be right).
Licence: CC BY-SA 4.0 (WikiTableQuestions LICENSE file at the repo root = CC BY-SA 4.0 legal code; GitHub licence API
         spdx CC-BY-SA-4.0). Tables are Wikipedia content (CC BY-SA).
Texts  : Wikipedia tables; questions written by MTurk workers; answers kept only when >= 2 workers agreed (human).
Rows   : state = page title + table + question + proposed answer; proposed = the human answer (gold "yes" for
         "correct?") or a wrong answer built from it (gold "no"): another cell of the same column (not mentioned in the
         question), a count/number off by a small amount, one list item swapped or dropped, or the opposite yes/no.
         ~20% of rows ask the negated question "... is the proposed answer wrong?" (gold flips; edge=negation).
Filters: SQUALL membership; gold items must be table cells, numbers or yes/no; <= 4 questions per table; tables whose
         Wikipedia page is a TabFact page (OHS-2 held-out source) are dropped, as are questions sharing an 8-gram with
         a TabFact statement; 13-word-run decontamination of tables and questions against local non-held-out files
         and the VitaminC test source split; state <= 7,000 chars; yes/no balanced per answer category.
Deterministic, CPU only (seed 20261101).   ../../../.venv/bin/python build_wtq.py [--manifest]
"""
import csv
import json
import random
import re
import sys
import zipfile
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

import requests

import ft_common as C

KEY = "wtq"
COMMIT = "7d455a5a707b96341ef72aff9428749d443d8aa9"
ZIP_URL = "https://github.com/ppasupat/WikiTableQuestions/releases/download/v1.0.2/WikiTableQuestions-1.0.2-compact.zip"
ZIP_SHA = "7c9ca7cc1ccd75fe4be0255b44be63f7b566761005f4ee6ce67e51c129d8b085"
SQUALL_COMMIT = "ee6dda91eacafd5ee800eb3fdc5d3a6575dc47e7"
SQUALL_SHA = "ceb244393916dc035a2f71a784c634d6a5fd4595b63e05d3b2fa58883af4f5cd"
LICENCE = (f"CC BY-SA 4.0 (github.com/ppasupat/WikiTableQuestions/blob/{COMMIT}/LICENSE = CC BY-SA 4.0 legal code; "
           "GitHub licence API spdx CC-BY-SA-4.0); question filter from SQUALL data, CC BY-SA 4.0 "
           f"(github.com/tzshi/squall/blob/{SQUALL_COMMIT}/LICENSE-data)")
CACHE = C.CACHE / "wtq"
MAX_PER_TABLE = 4
NEG_SHARE = 0.2
MAX_STATE = 7000

Q_CORRECT = "Based only on the table, is the proposed answer to the question correct?"
Q_WRONG = "Based only on the table, is the proposed answer to the question wrong?"
DEFS = {
    "correct": {
        "yes": "The proposed answer is exactly what the table gives for this question: the right cell, count or value, "
               "and when the question asks for several items, all of them and nothing else.",
        "no": "The proposed answer is not what the table gives: a different cell or value (for example a neighbouring "
              "row's entry), a count or number that is off, the opposite yes/no, or a list that misses or adds an item.",
    },
    "wrong": {
        "yes": "It is wrong: the table gives a different answer, for example another cell or value, a different count or "
               "number, the opposite yes/no, or a list with an item missing or added.",
        "no": "It is not wrong: the proposed answer is exactly what the table gives for this question, the right cell, "
              "count or value, and for several items all of them and nothing else.",
    },
}
OPEN_Q = re.compile(r"\b(name|list|give|tell me) (a|an|one|any|some)\b|\ban example\b|\bone of\b|\bat least one\b|"
                    r"\b(which|what|who) (is|was) (a|an|one)\b|\bany (one|of)\b", re.I)


STOP = {"the", "a", "an", "of", "in", "on", "at", "to", "for", "by", "what", "which", "who", "how", "many", "much", "is",
        "was", "were", "are", "did", "does", "do", "and", "or", "with", "that", "this", "from", "as", "number", "total"}


def unesc(x):
    return x.replace("\\n", " ").replace("\\p", "|").replace("\\\\", "\\")


def load_table(z, ctx):
    name = "WikiTableQuestions/" + ctx.replace(".csv", ".tsv")
    rows = []
    for line in z.read(name).decode("utf-8").split("\n"):
        if line == "":
            continue
        rows.append([C.clean_cell(unesc(x), 10_000) for x in line.split("\t")])
    w = max(len(r) for r in rows)
    return [r + [""] * (w - len(r)) for r in rows]


def fetch_pages(ctxs):
    """page/<t>-page/<id>.json (title, url) for the given training tables; cached in cache/wtq/page/."""
    out = {}
    todo = []
    for ctx in ctxs:
        t, i = re.match(r"csv/(\d+)-csv/(\d+)\.csv", ctx).groups()
        p = CACHE / "page" / f"{t}-page" / f"{i}.json"
        if p.exists():
            out[ctx] = json.loads(p.read_text())
        else:
            todo.append((ctx, t, i, p))

    def get(item):
        ctx, t, i, p = item
        url = f"https://raw.githubusercontent.com/ppasupat/WikiTableQuestions/{COMMIT}/page/{t}-page/{i}.json"
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(r.text)
        return ctx, json.loads(r.text)

    with ThreadPoolExecutor(max_workers=8) as ex:
        for ctx, d in ex.map(get, todo):
            out[ctx] = d
    return out


HOW_MANY = re.compile(r"\bhow many\b|\bnumber of\b|\bhow much\b", re.I)
OR_Q = re.compile(r"(?:^|[,:]\s*|\b(?:between|either)\s+)([^,:?]+?)\s+or\s+([^,?]+?)\s*\??$", re.I)


def or_alternative(q, gold_txt, cellmap, body):
    """For "..., A or B?" questions: None if not such a question; else the other option (table spelling when it is
    a cell) when the gold is one of the two options, or "" (no safe distractor) when it is not."""
    m = OR_Q.search(q.strip())
    if not m:
        return None
    a, b = C.norm(m.group(1)), C.norm(m.group(2))
    a = re.sub(r"^(the|a|an)\s+", "", a)
    b = re.sub(r"^(the|a|an)\s+", "", b)
    g = C.norm(gold_txt)
    g2 = re.sub(r"^(the|a|an)\s+", "", g)
    if not a or not b or a == b:
        return None
    if g2 in (a, b) or g in (a, b):
        other = b if g2 == a or g == a else a
        for row in body:
            for v in row:
                if C.norm(v) == other:
                    return v
        return ""  # the other option is not a cell: its spelling would differ from the gold's (a giveaway)
    return ""


def light(s):
    return re.sub(r"\s+", " ", s.strip().lower())


def num_of(s):
    return C.parse_num(s) if re.fullmatch(r"-?[\d,]+(\.\d+)?", s.strip()) else None


def main():
    zp = C.fetch(ZIP_URL, CACHE / "WikiTableQuestions-1.0.2-compact.zip", ZIP_SHA)
    sq = C.fetch(f"https://raw.githubusercontent.com/tzshi/squall/{SQUALL_COMMIT}/data/squall.json",
                 CACHE / "squall_squall.json", SQUALL_SHA)
    squall_ids = {s["nt"] for s in json.load(open(sq))}
    z = zipfile.ZipFile(zp)
    rng = random.Random(C.SEED)
    drop = Counter()
    exs = list(csv.DictReader(z.read("WikiTableQuestions/data/training.tsv").decode("utf-8").splitlines(),
                              delimiter="\t", quoting=csv.QUOTE_NONE))  # TRAIN ONLY
    print(f"training examples {len(exs)}; in SQUALL {sum(e['id'] in squall_ids for e in exs)}")
    pages = fetch_pages(sorted({e["context"] for e in exs}))
    tfi = C.tabfact_index()

    tables, cands = {}, []
    for e in exs:
        if e["id"] not in squall_ids:
            drop["not in SQUALL (non-deterministic / not SQL-expressible)"] += 1
            continue
        ctx = e["context"]
        if ctx not in tables:
            tables[ctx] = load_table(z, ctx)
        t = tables[ctx]
        pg = pages[ctx]
        if C.tabfact_hit(tfi, title=pg["title"]):
            drop["TabFact page"] += 1
            continue
        q = C.clean_cell(unesc(e["utterance"]), 10_000)
        if C.tabfact_hit(tfi, text=q):
            drop["TabFact statement overlap"] += 1
            continue
        items = [C.clean_cell(unesc(x), 10_000) for x in e["targetValue"].split("|")]
        body = t[1:]
        cellmap = defaultdict(list)
        for r, row in enumerate(body):
            for c, v in enumerate(row):
                if v:
                    cellmap[C.norm(v)].append((r, c))
        nitems = [C.norm(x) for x in items]
        qn = f" {C.norm(q)} "
        dis = []
        if len(items) > 1:
            if not all(n in cellmap for n in nitems):
                drop["gold not in table"] += 1
                continue
            cat = "list"
            cols = {cellmap[n][0][1] for n in nitems}
            if len(cols) == 1:
                col = cols.pop()
                pool = sorted({v for row in body for v in [row[col]] if v and C.norm(v) not in nitems
                               and not any(C.norm(v) in n or n in C.norm(v) for n in nitems)
                               and f" {C.norm(v)} " not in qn})
                for i in range(len(items)):
                    for v in pool:
                        dis.append(("; ".join(items[:i] + [v] + items[i + 1:]), "item_swap"))
            for i in range(len(items)):
                dis.append(("; ".join(items[:i] + items[i + 1:]), "item_dropped"))
            gold_txt = "; ".join(items)
        else:
            g, gn = items[0], nitems[0]
            gold_txt = g
            if gn in ("yes", "no"):
                cat = "yes/no"
                dis.append(("no" if gn == "yes" else "yes", "yesno_flip"))
            elif gn in cellmap and not (HOW_MANY.search(q) and num_of(g) is not None):
                cat = "cell"
                gnum = num_of(g)
                cols = sorted({c for _, c in cellmap[gn]})
                if len(cols) > 1:  # prefer the column whose header the question names (e.g. "silver" medals)
                    qw = set(C.words(q)) - STOP
                    score = {c: len(set(C.words(t[0][c])) & qw) for c in cols}
                    best = max(score.values())
                    if best > 0:
                        cols = [c for c in cols if score[c] == best]
                for col in cols:
                    for row in body:
                        v = row[col]
                        vn = C.norm(v)
                        if not vn or vn == gn or vn in gn or gn in vn or f" {vn} " in qn:
                            continue
                        if gnum is not None:
                            x = num_of(v)
                            if x is None or not C.clearly_different(x, gnum, C.decimals_of(g), rel=0.0):
                                continue
                            if gnum != 0 and not (0.2 <= abs(x) / abs(gnum) <= 5) and abs(x - gnum) > 5:
                                continue  # keep numeric distractors of a similar size
                        elif num_of(v) is not None:
                            continue
                        dis.append((v, "other_cell_same_column"))
            elif num_of(g) is not None:
                cat = "number"
                x = num_of(g)
                dec = C.decimals_of(g)
                if dec == 0 and 1500 <= x <= 2100 and "," not in g:
                    for d in (-2, -1, 1, 2):
                        dis.append((str(int(x + d)), "year_off_by_%+d" % d))
                elif dec == 0 and abs(x) < 50:
                    deltas = [1, 2, -1, -2] if x >= 3 else [1, 2]
                    for d in deltas:
                        dis.append((C.fmt_num(x + d, 0, commas="," in g), "count_off_by_%+d" % d))
                else:
                    for f in (0.8, 0.9, 1.1, 1.25):
                        y = x * f
                        if C.clearly_different(y, x, dec):
                            dis.append((C.fmt_num(y, dec, commas="," in g), "number_scaled"))
            else:
                drop["gold not a cell/number/yes-no"] += 1
                continue
        alt = or_alternative(q, gold_txt, cellmap, body)
        if alt is not None:
            dis = [(alt, "other_option_in_question")] if alt else []
        if OPEN_Q.search(q):
            dis = []
        dis = [d for d in dis if light(d[0]) != light(gold_txt) and d[0].strip()]
        cands.append({"rid": e["id"], "ctx": ctx, "title": pg["title"], "question": q, "items": items,
                      "gold_txt": gold_txt, "dis": sorted(set(dis)), "cat": cat})

    # decontamination: tables (by context) + questions
    docs = {}
    for ctx in {cd["ctx"] for cd in cands}:
        docs["t:" + ctx] = C.render_table(tables[ctx])
    for cd in cands:
        docs["q:" + cd["rid"]] = cd["question"]
    hit = C.local_decontam(docs, heldout=True)
    n0 = len(cands)
    cands = [cd for cd in cands if "t:" + cd["ctx"] not in hit and "q:" + cd["rid"] not in hit]
    drop["13-gram overlap"] = n0 - len(cands)

    by_t = defaultdict(list)
    for cd in cands:
        by_t[cd["ctx"]].append(cd)
    pool = []
    for ctx in sorted(by_t):
        lst = sorted(by_t[ctx], key=lambda c: c["rid"])
        rng.shuffle(lst)
        lst.sort(key=lambda c: not c["dis"])
        seen, chosen = set(), []
        for cd in lst:
            n = C.norm(cd["question"])
            if n in seen:
                continue
            seen.add(n)
            chosen.append(cd)
            if len(chosen) >= MAX_PER_TABLE:
                break
        drop["over per-table cap / dup question"] += len(lst) - len(chosen)
        pool += chosen

    by_cat = defaultdict(list)
    for cd in pool:
        by_cat[cd["cat"]].append(cd)
    rows = []
    for cat in sorted(by_cat):
        lst = by_cat[cat]
        rng.shuffle(lst)
        can_no = [cd for cd in lst if cd["dis"]]
        k = min(len(can_no), len(lst) // 2)
        no_ids = {cd["rid"] for cd in can_no[:k]}
        yes = [cd for cd in lst if cd["rid"] not in no_ids][:k]
        drop["category balance"] += len(lst) - 2 * k
        for cd in can_no[:k]:
            kinds = sorted({d[1] for d in cd["dis"]})
            kind = rng.choice(kinds)
            rows.append((cd, rng.choice(sorted(d[0] for d in cd["dis"] if d[1] == kind)), False, kind))
        for cd in yes:
            rows.append((cd, cd["gold_txt"], True, "human_gold"))

    rows.sort(key=lambda x: x[0]["rid"])
    rng.shuffle(rows)
    n_neg = int(round(NEG_SHARE * len(rows)))
    out, seen = [], set()
    for i, (cd, ans_txt, is_gold, kind) in enumerate(rows):
        negq = i < n_neg
        state = (f"Wikipedia page: {cd['title']}\nTable (first row is the header):\n"
                 f"{C.render_table(tables[cd['ctx']])}\n\nQuestion: {cd['question']}\nProposed answer: {ans_txt}")
        if len(state) > MAX_STATE:
            drop["state too long"] += 1
            continue
        ns = C.norm(state)
        if ns in seen:
            drop["duplicate state"] += 1
            continue
        seen.add(ns)
        gold = ("yes" if not is_gold else "no") if negq else ("yes" if is_gold else "no")
        edges = []
        if negq:
            edges.append("negation")
        if kind == "item_dropped" or cd["cat"] == "list":
            edges.append("quantifier")
        if cd["cat"] == "number" or re.search(r"\b(how many|how much|total|difference|more than|less than|average)\b",
                                             cd["question"], re.I):
            edges.append("numeric")
        if re.search(r"\b(before|after|previous|next|first|last|earliest|latest|until|since|year)\b",
                     cd["question"], re.I):
            edges.append("temporal")
        if len(state) > 3500:
            edges.append("long_context")
        edges.append("table")
        prio = ["negation", "quantifier", "numeric", "temporal", "long_context", "table"]
        edge = next((e for e in prio if e in edges), None)
        out.append({
            "key": KEY, "rid": cd["rid"], "state": state, "instructions": Q_WRONG if negq else Q_CORRECT,
            "options": ["yes", "no"], "gold": gold, "soft": None,
            "meta": {"dataset": "ppasupat/WikiTableQuestions (github release v1.0.2)", "config": "data/training.tsv",
                     "revision": f"release v1.0.2 zip sha256:{ZIP_SHA}; pages git:{COMMIT}; squall git:{SQUALL_COMMIT}",
                     "licence": LICENCE, "split": "train", "orig_label": {"targetValue": cd["items"]},
                     "family": C.FAMILY, "edge": edge, "edge_all": edges, "defs": "wrong" if negq else "correct",
                     "proposed_is_gold": is_gold, "distractor": kind, "answer_category": cd["cat"],
                     "context_id": cd["ctx"]},
        })

    summ = C.check_rows(KEY, out)
    print("drops:", dict(drop))
    print("distractor kinds:", dict(Counter(r["meta"]["distractor"] for r in out)))
    print("categories:", dict(Counter((r["meta"]["answer_category"], r["meta"]["proposed_is_gold"]) for r in out)))
    C.write_outputs(KEY, out, DEFS)
    if "--manifest" in sys.argv:
        C.append_manifest({
            "key": KEY, "family": C.FAMILY, "dataset": "ppasupat/WikiTableQuestions (training.tsv)", "licence": LICENCE,
            "rows": summ["rows"], "qtype": "yesno", "yesno_share": round(summ["yesno_share"], 4),
            "edge_tags": summ["edge_tags"],
            "notes": ("Answer verification on Wikipedia tables. Yes rows = crowd answer agreed by >=2 workers; no rows = "
                      "another same-column cell, count/number off, list item swapped/dropped, flipped yes/no. Only "
                      "SQUALL-annotated (deterministic) questions; TabFact pages dropped; <=4 questions/table; 20% "
                      "negated question; 13-gram decontam incl. VitaminC test source."),
        })


if __name__ == "__main__":
    main()
