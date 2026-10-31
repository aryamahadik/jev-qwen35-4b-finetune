"""v14 golden, family fact_tables: raw rows for "feverous" (FEVEROUS, Aly et al., NeurIPS 2021 Datasets): does the
Wikipedia evidence (table cells, infobox rows, sentences, list items) support / refute the claim?

Source : official FEVER site https://fever.ai/dataset/feverous.html -> feverous_train_challenges.jsonl (TRAIN only;
         dev and the unlabelled test are never downloaded), sha256 pinned. Evidence text comes from the official
         December-2020 page dump feverous-wiki-pages.zip, read by HTTP range requests (feverous_fetch.py): a seeded
         sample of 96 of its 544 members is streamed and only pages cited by train evidence are kept
         (cache/feverous/pages_subset.jsonl.gz; per-member CRC-32 and inflated sha256 in cache/feverous/members.json).
         Claims whose evidence pages all fall in that sample are usable (~9.6k of 71k).
Licence: https://fever.ai/download/feverous/license.html: annotations under the licence of the Wikipedia pages or,
         where unavailable, CC BY-SA 3.0 (i.e. CC BY-SA). Not derived from FEVER 1.0: new claims written by
         annotators from highlighted 2020 Wikipedia sentences/tables, new verdicts and evidence.
Texts  : claims written by trained annotators; verdicts (SUPPORTS / REFUTES / NOT ENOUGH INFO) and evidence sets
         annotated by humans (a second annotator verified). No model-written text or labels.
Rows   : state = the claim's first evidence set rendered from the page dump (per page: title; each cited table with
         its caption, header rows and every row holding an evidence cell, spans expanded; cited sentences, list items
         and section names in page order) + the claim. Two yes/no questions (one per claim):
           "Does the evidence support the claim?"   yes = SUPPORTS; no = REFUTES or NOT ENOUGH INFO
           "Does the evidence refute the claim?"    yes = REFUTES;  no = SUPPORTS or NOT ENOUGH INFO
         Same rendering for every label (only the cited evidence is shown, never extra rows), so NEI claims stay
         unverifiable. Each question is balanced 50/50; at most 8,000 rows.
Filters: evidence must render (every cited element found); <= 25 table rows, state <= 6,000 chars; <= 3 claims per
         page; claim and state dedup; tables on TabFact (OHS-2 held-out source) pages dropped, claims sharing an
         8-gram with a TabFact statement dropped; 13-word-run decontamination against our local non-held-out files
         and the VitaminC test source split (OHS-1).
Deterministic, CPU only (seed 20261101).   ../../../.venv/bin/python build_feverous.py [--manifest]
"""
import gzip
import json
import random
import re
import sys
from collections import Counter, defaultdict

import ft_common as C

KEY = "feverous"
TRAIN_URL = "https://fever.ai/download/feverous/feverous_train_challenges.jsonl"
TRAIN_SHA = "0c29ccba41e27c5b988ca5132085e8d67c7921f265707bea170bfbde12bceee7"
LICENCE_URL = "https://fever.ai/download/feverous/license.html"
LICENCE_SHA = "eaddbd6e2854b45e6925bac9171fb6a2438492dc0efd4fda80144e836ae1ad05"
LICENCE = ("CC BY-SA 3.0 / Wikipedia page licence terms (https://fever.ai/download/feverous/license.html: 'made available "
           "under the license terms described on the applicable Wikipedia article pages, or ... CC BY-SA 3.0')")
CACHE = C.CACHE / "feverous"
MAX_PER_PAGE = 3
MAX_ROWS_TABLE = 25
MAX_STATE = 6000
MAX_ROWS = 8000
N_REFUTE_Q_REFUTES = 1300  # rows of the "refute?" question with gold yes

Q_SUP = "Does the evidence support the claim?"
Q_REF = "Does the evidence refute the claim?"
DEFS = {
    "support": {
        "yes": "The evidence (table cells, sentences and list items, with their page and headers) shows every part of "
               "the claim is true, directly or by simple reasoning such as counting, comparing or adding values.",
        "no": "The evidence does not establish the claim: it contradicts at least one part of it, or leaves some part "
              "unconfirmed (not enough information counts as no).",
    },
    "refute": {
        "yes": "The evidence (table cells, sentences and list items, with their page and headers) shows at least one "
               "part of the claim is false, directly or by simple reasoning such as counting, comparing or adding.",
        "no": "The evidence does not show the claim is false: it either supports the claim or does not settle it "
              "(not enough information counts as no).",
    },
}
ID_RE = re.compile(r"^(.*?)_(sentence|cell|header_cell|table_caption|item|section|title)(?:_(.*))?$")
LINK = re.compile(r"\[\[([^\]|]*)\|([^\]]*)\]\]|\[\[([^\]]*)\]\]")
CHALLENGE_EDGE = {"Numerical Reasoning": "numeric", "Multi-hop Reasoning": "multi_hop",
                  "Combining Tables and Text": "table", "Entity Disambiguation": "ambiguous"}


def dewiki(s):
    s = LINK.sub(lambda m: m.group(2) if m.group(2) is not None else m.group(3).replace("_", " "), str(s))
    s = s.replace("'''", "").replace("''", "")
    return re.sub(r"\s+", " ", s).strip()


def split_id(eid):
    m = ID_RE.match(eid)
    return (m.group(1), m.group(2), m.group(3)) if m else (None, None, None)


def table_grid(tab):
    """Expand row/column spans. Returns (grid of (text, is_header)), {cell_id: row index})."""
    grid, occupied, where = [], {}, {}
    for r, row in enumerate(tab["table"]):
        cur = []
        c = 0
        for cell in row:
            while (r, c) in occupied:
                cur.append(occupied.pop((r, c)))
                c += 1
            rs = max(1, int(cell.get("row_span", 1) or 1))
            cs = max(1, int(cell.get("column_span", 1) or 1))
            v = (dewiki(cell.get("value", "")), bool(cell.get("is_header")))
            where[cell["id"]] = r
            for k in range(cs):
                cur.append(v)
                for rr in range(1, rs):
                    occupied[(r + rr, c + k)] = v
            c += cs
        while (r, c) in occupied:
            cur.append(occupied.pop((r, c)))
            c += 1
        grid.append(cur)
    return grid, where


def render_evidence(ev, pages):
    """Render one evidence set; None if any cited element is missing."""
    order, per_page = [], defaultdict(lambda: {"cells": defaultdict(set), "hdr": defaultdict(set), "sent": set(),
                                               "items": set(), "caps": set(), "sections": set()})
    ids = list(ev["content"]) + [x for v in ev["context"].values() for x in v]
    for eid in ids:
        p, kind, rest = split_id(eid)
        if p is None or p not in pages:
            return None
        if p not in order:
            order.append(p)
        d = per_page[p]
        if kind in ("cell", "header_cell"):
            t = rest.split("_")[0]
            (d["cells"] if kind == "cell" else d["hdr"])[t].add(eid[len(p) + 1:])
        elif kind == "sentence":
            d["sent"].add(int(rest))
        elif kind == "item":
            d["items"].add(rest)
        elif kind == "table_caption":
            d["caps"].add(rest)
        elif kind == "section":
            d["sections"].add(int(rest))
    blocks, n_cells, n_sent = [], 0, 0
    for p in order:
        pg, d = pages[p], per_page[p]
        lines = [f"Wikipedia page: {dewiki(pg['title'])}"]
        secs = [dewiki(pg.get(f"section_{i}", {}).get("value", "")) for i in sorted(d["sections"])]
        secs = [s for s in secs if s]
        if secs:
            lines.append("Section: " + " > ".join(secs))
        for t in sorted(set(d["cells"]) | set(d["hdr"]) | set(d["caps"]), key=int):
            tab = pg.get(f"table_{t}")
            if tab is None:
                return None
            grid, where = table_grid(tab)
            rows = set()
            for cid in d["cells"].get(t, set()) | d["hdr"].get(t, set()):
                if cid not in where:
                    return None
                rows.add(where[cid])
            n_cells += len(d["cells"].get(t, set()))
            hdr_rows = {r for r, row in enumerate(grid) if row and all(h for _, h in row)}
            # header rows directly above the first cited row (column headers), at most 2
            first = min(rows) if rows else 0
            above = sorted(r for r in hdr_rows if r < first)[-2:]
            show = sorted(set(above) | rows)
            if len(show) > MAX_ROWS_TABLE:
                return None
            cap = dewiki(tab.get("caption", "")) if tab.get("caption") else ""
            lines.append("Table" + (f" (caption: {cap})" if cap else "") + ":")
            last = -1
            for r in show:
                if last >= 0 and r != last + 1:
                    lines.append("| ... |")
                lines.append("| " + " | ".join(C.clean_cell(v, 200) for v, _ in grid[r]) + " |")
                last = r
        for i in sorted(d["sent"]):
            s = pg.get(f"sentence_{i}")
            if s is None:
                return None
            lines.append(f"Sentence: {dewiki(s)}")
            n_sent += 1
        for it in sorted(d["items"], key=lambda x: [int(y) for y in x.split("_")]):
            lst = pg.get(f"list_{it.split('_')[0]}")
            val = None
            if lst:
                for x in lst.get("list", []):
                    if x.get("id") == f"item_{it}":
                        val = dewiki(x.get("value", ""))
            if val is None:
                return None
            lines.append(f"List item: {val}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks), order, n_cells, n_sent


def main():
    train = C.fetch(TRAIN_URL, CACHE / "feverous_train_challenges.jsonl", TRAIN_SHA)
    C.fetch(LICENCE_URL, CACHE / "license.html", LICENCE_SHA)
    pages = {}
    with gzip.open(CACHE / "pages_subset.jsonl.gz", "rt", encoding="utf-8") as f:
        for line in f:
            o = json.loads(line)
            pages[o["title"]] = o
    members = json.load(open(CACHE / "members.json"))
    print(f"pages available: {len(pages)} from {len(members['members'])} dump members")
    tfi = C.tabfact_index()
    rng = random.Random(C.SEED)
    drop = Counter()
    cands, seen_claim = [], set()
    with open(train, encoding="utf-8") as f:
        next(f)
        for line in f:
            d = json.loads(line)
            claim = C.clean_cell(d["claim"], 10_000)
            if not claim or d["label"] not in ("SUPPORTS", "REFUTES", "NOT ENOUGH INFO"):
                drop["bad record"] += 1
                continue
            rendered = None
            for ev in d["evidence"]:
                rendered = render_evidence(ev, pages)
                if rendered is not None:
                    break
            if rendered is None:
                drop["evidence pages not in sample / not renderable"] += 1
                continue
            text, order, n_cells, n_sent = rendered
            state = f"Evidence:\n{text}\n\nClaim: {claim}"
            if len(state) > MAX_STATE:
                drop["state too long"] += 1
                continue
            if n_cells and any(C.tabfact_hit(tfi, title=p) for p in order):
                drop["TabFact page with table evidence"] += 1
                continue
            if C.tabfact_hit(tfi, text=claim):
                drop["TabFact statement overlap"] += 1
                continue
            nc = C.norm(claim)
            if nc in seen_claim:
                drop["duplicate claim"] += 1
                continue
            seen_claim.add(nc)
            cands.append({"rid": str(d["id"]), "claim": claim, "label": d["label"], "state": state,
                          "evidence_text": text, "page": order[0], "challenge": d.get("challenge"),
                          "n_cells": n_cells, "n_sent": n_sent, "n_pages": len(order)})
    print(f"candidates after rendering: {len(cands)}  {dict(Counter(c['label'] for c in cands))}")

    docs = {}
    for cd in cands:
        docs["e:" + cd["rid"]] = cd["evidence_text"]
        docs["c:" + cd["rid"]] = cd["claim"]
    hit = C.local_decontam(docs, heldout=True)
    n0 = len(cands)
    cands = [cd for cd in cands if "e:" + cd["rid"] not in hit and "c:" + cd["rid"] not in hit]
    drop["13-gram overlap"] = n0 - len(cands)

    by_page = defaultdict(list)
    for cd in cands:
        by_page[cd["page"]].append(cd)
    pool, seen_state = [], set()
    for p in sorted(by_page):
        lst = sorted(by_page[p], key=lambda c: int(c["rid"]))
        rng.shuffle(lst)
        lst.sort(key=lambda c: {"NOT ENOUGH INFO": 0, "REFUTES": 1, "SUPPORTS": 2}[c["label"]])  # rarer labels first
        chosen = []
        for cd in lst:
            ns = C.norm(cd["state"])
            if ns in seen_state:
                continue
            seen_state.add(ns)
            chosen.append(cd)
            if len(chosen) >= MAX_PER_PAGE:
                break
        drop["over per-page cap / dup state"] += len(lst) - len(chosen)
        pool += chosen

    S = [c for c in pool if c["label"] == "SUPPORTS"]
    R = [c for c in pool if c["label"] == "REFUTES"]
    N = [c for c in pool if c["label"] == "NOT ENOUGH INFO"]
    for lst in (S, R, N):
        lst.sort(key=lambda c: int(c["rid"]))
        rng.shuffle(lst)
    n2 = int(round(0.4 * len(N)))
    N2, N1 = N[:n2], N[n2:]
    r2 = min(N_REFUTE_Q_REFUTES, len(R) // 3)
    R2, R1 = R[:r2], R[r2:]
    s2 = max(0, r2 - len(N2))
    S2, S1 = S[:s2], S[s2:]
    # support? question: yes = S1, no = R1 + N1 (balanced)
    k = min(len(S1), len(R1) + len(N1), (MAX_ROWS - len(S2) - len(R2) - len(N2)) // 2)
    R1 = R1[:max(0, k - len(N1))]
    S1 = S1[:len(R1) + len(N1)]
    drop["label balance"] += len(pool) - (len(S1) + len(R1) + len(N1) + len(S2) + len(R2) + len(N2))
    sel = [(c, "support") for c in S1 + R1 + N1] + [(c, "refute") for c in S2 + R2 + N2]
    sel.sort(key=lambda x: int(x[0]["rid"]))
    rng.shuffle(sel)
    out = []
    for cd, qn in sel:
        lab = cd["label"]
        gold = ("yes" if lab == "SUPPORTS" else "no") if qn == "support" else ("yes" if lab == "REFUTES" else "no")
        edges = []
        if lab == "NOT ENOUGH INFO":
            edges.append("missing_info")
        if re.search(r"\b(not|no|never|none|neither|nor|without|non)\b|n't\b", cd["claim"], re.I):
            edges.append("negation")
        if cd["challenge"] in CHALLENGE_EDGE:
            edges.append(CHALLENGE_EDGE[cd["challenge"]])
        if cd["n_pages"] > 1 and "multi_hop" not in edges:
            edges.append("multi_hop")
        if re.search(r"\b(all|every|each|only|at least|at most|exactly|more than|less than|fewer than|over|under)\b",
                     cd["claim"], re.I):
            edges.append("quantifier")
        if re.search(r"\b(before|after|until|since|during|earlier|later|first|last)\b|\b1[5-9]\d\d\b|\b20[0-2]\d\b",
                     cd["claim"]):
            edges.append("temporal")
        if cd["n_cells"]:
            edges.append("table")
        prio = ["missing_info", "negation", "multi_hop", "numeric", "quantifier", "ambiguous", "temporal", "table"]
        edge = next((e for e in prio if e in edges), None)
        out.append({
            "key": KEY, "rid": cd["rid"], "state": cd["state"], "instructions": Q_SUP if qn == "support" else Q_REF,
            "options": ["yes", "no"], "gold": gold, "soft": None,
            "meta": {"dataset": "FEVEROUS (fever.ai), feverous_train_challenges.jsonl",
                     "config": "train; evidence from feverous-wiki-pages.zip (Dec 2020 dump), first renderable set",
                     "revision": f"train sha256:{TRAIN_SHA}; dump members in cache/feverous/members.json",
                     "licence": LICENCE, "split": "train", "orig_label": lab, "family": C.FAMILY, "edge": edge,
                     "edge_all": sorted(set(edges)), "defs": qn, "challenge": cd["challenge"],
                     "context_id": cd["page"], "evidence_cells": cd["n_cells"], "evidence_sentences": cd["n_sent"]},
        })

    summ = C.check_rows(KEY, out)
    print("drops:", dict(drop))
    print("labels x question:", dict(Counter((r["meta"]["defs"], r["meta"]["orig_label"]) for r in out)))
    print("challenge:", dict(Counter(r["meta"]["challenge"] for r in out)))
    print("with table evidence:", sum(r["meta"]["evidence_cells"] > 0 for r in out))
    C.write_outputs(KEY, out, DEFS)
    if "--manifest" in sys.argv:
        C.append_manifest({
            "key": KEY, "family": C.FAMILY, "dataset": "FEVEROUS train (fever.ai)", "licence": LICENCE,
            "rows": summ["rows"], "qtype": "yesno", "yesno_share": round(summ["yesno_share"], 4),
            "edge_tags": summ["edge_tags"],
            "notes": ("Claim vs Wikipedia evidence mixing table cells/infobox rows and sentences. Two questions: "
                      "'support?' (NEI and REFUTES = no) and 'refute?' (NEI and SUPPORTS = no), each 50/50. Evidence "
                      "rendered from the official Dec-2020 page dump (96/544 members streamed). <=3 claims/page; "
                      "TabFact pages dropped; 13-gram decontam incl. VitaminC test source."),
        })


if __name__ == "__main__":
    main()
