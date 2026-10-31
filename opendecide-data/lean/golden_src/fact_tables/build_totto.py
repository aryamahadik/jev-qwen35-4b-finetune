"""v14 golden, family fact_tables: raw rows for "totto_claims" (ToTTo, Parikh et al., EMNLP 2020) recast as claim
verification against a Wikipedia table: is the sentence supported by the table?

Source : https://storage.googleapis.com/totto-public/totto_data.zip, member totto_data/totto_train_data.jsonl ONLY
         (read by HTTP range requests in totto_fetch.py; dev/test bytes never downloaded; CRC-32 checked, inflated
         sha256 73be72ca... recorded in cache/totto/member.json). Deterministic 1-in-5 sample by md5(example_id).
Licence: CC BY-SA 3.0, stated in the official README (github.com/google-research-datasets/ToTTo @ 7b0ad536,
         "The ToTTo dataset is released under the Creative Commons Share-Alike 3.0 license").
Texts  : Wikipedia tables; each sentence is a Wikipedia sentence that annotators edited (deleted unsupported parts,
         decontextualised) until it is fully supported by the highlighted cells and page/section titles (human).
Rows   : state = page title, section title, table + claim.
           yes ("supported"): the human final sentence, verbatim.
           no  ("contradicted", label by construction): the same human sentence with ONE highlighted cell value that
               appears verbatim once in it replaced by the value of the same column in another, non-highlighted row
               (same kind: number/year/text). Safety rules: the sentence must also name at least one other
               highlighted cell of the same row verbatim (anchor), the new value must not already be in the sentence,
               and no table row may contain both an anchor value and the new value (so the edited claim matches no
               row); a text value embedded in a longer capitalised name is never edited. The donor row is always
               shown, so "value not in table" is never a giveaway. Reviewer fixes (strict review): a text donor
               that contains or is contained in the original value ("Labour" -> "Labour hold") is never used, and
               footnote/note rows (one repeated value) are never donors.
         Positives are drawn only from examples that also admit such an edit (same distribution for both labels).
         ~20% ask "Is the claim contradicted by the table?" (gold flips; edge=negation).
Filters: one example per (page, section) table; tables on TabFact pages dropped (OHS-2 held-out source), claims
         sharing an 8-gram with a TabFact statement dropped; 13-word-run decontamination vs local non-held-out files
         and the VitaminC test source split; state <= 5,000 chars (large tables shown as header + highlighted rows +
         donor row + 2 random rows, gaps marked "| ... |").
Deterministic, CPU only (seed 20261101).   ../../../.venv/bin/python build_totto.py [--manifest]
"""
import gzip
import json
import random
import re
import sys
from collections import Counter

import ft_common as C

KEY = "totto_claims"
LICENCE = ("CC BY-SA 3.0 (README of github.com/google-research-datasets/ToTTo @ 7b0ad5368ed523f75dc872249ce200f99d2d4b15: "
           "'The ToTTo dataset is released under the Creative Commons Share-Alike 3.0 license')")
CACHE = C.CACHE / "totto"
MAX_ROWS = 6000
NEG_SHARE = 0.2
MAX_STATE = 5000
FULL_TABLE_ROWS = 20

Q_SUP = "Is the claim supported by the table?"
Q_CON = "Is the claim contradicted by the table?"
DEFS = {
    "supported": {
        "yes": "Every fact in the claim matches the table and its page and section titles: each value is paired with "
               "the right row and column (right entity, year, number, place or name).",
        "no": "The table contradicts the claim: at least one stated value belongs to a different row than the one the "
              "claim ties it to (for example another year's number or another entry's name).",
    },
    "contradicted": {
        "yes": "The table contradicts the claim: at least one stated value belongs to a different row than the one the "
               "claim ties it to (for example another year's number or another entry's name).",
        "no": "The claim is supported: every fact matches the table and its page and section titles, with each value "
              "paired with the right row and column.",
    },
}
YEAR = re.compile(r"^(1[5-9]\d\d|20[0-2]\d)$")
NUMERIC = re.compile(r"^[-−+]?[\d,]*\.?\d+%?$")


def kind(v):
    v = v.strip()
    if YEAR.match(v):
        return "year"
    if NUMERIC.match(v):
        return "number"
    if re.search(r"\d", v):
        return "mixed"
    return "text"


def grid_of(table):
    """Expand spans; returns grid [[(text, is_header)]] and map (row, cell index) -> grid column."""
    grid, occ, pos = [], {}, {}
    for r, row in enumerate(table):
        cur, c = [], 0
        for k, cell in enumerate(row):
            while (r, c) in occ:
                cur.append(occ.pop((r, c)))
                c += 1
            rs, cs = max(1, int(cell.get("row_span", 1))), max(1, int(cell.get("column_span", 1)))
            v = (C.clean_cell(cell.get("value", ""), 300), bool(cell.get("is_header")))
            pos[(r, k)] = c
            for j in range(cs):
                cur.append(v)
                for rr in range(1, rs):
                    occ[(r + rr, c + j)] = v
            c += cs
        while (r, c) in occ:
            cur.append(occ.pop((r, c)))
            c += 1
        grid.append(cur)
    w = max(len(r) for r in grid)
    return [r + [("", False)] * (w - len(r)) for r in grid], pos


def occurs_once(val, sent):
    pat = re.compile(r"(?<![\w])" + re.escape(val) + r"(?![\w])")
    return len(pat.findall(sent)) == 1, pat


PARTICLES = {"de", "la", "le", "of", "von", "van", "du", "del", "di", "da", "des", "der", "den", "the", "y", "e", "and"}


def embedded_in_name(pat, sent):
    """True when the matched text value sits inside a longer capitalised name in the sentence."""
    m = pat.search(sent)
    before = sent[:m.start()].rstrip().split()
    after = sent[m.end():].lstrip().split()
    if before:
        b = before[-1]
        if b.lower() in PARTICLES - {"the", "and"} or (b[:1].isupper() and not b.endswith(("'s", "\u2019s", ",", ":"))
                                                          and len(before) > 1):
            return True
    if after:
        a = after[0]
        if a[:1].isupper() and not sent[m.end():m.end() + 1] in ",;:)\"":
            return True
    return False


def negatives(ex, grid, pos, sent):
    """All safe single-value edits of the sentence: list of (new_sentence, donor_row, target_kind)."""
    hl = [(r, pos.get((r, k))) for r, k in ex["highlighted_cells"] if (r, k) in pos]
    hl_set = set(hl)
    hl_vals = {C.norm(grid[r][c][0]) for r, c in hl if c is not None and r < len(grid)}
    s_norm = f" {C.norm(sent)} "
    out = []
    for r, c in hl:
        if c is None or r >= len(grid):
            continue
        v, is_h = grid[r][c]
        if is_h or len(v) < 2 and not v.isdigit():
            continue
        once, pat = occurs_once(v, sent)
        if not once:
            continue
        if kind(v) == "text" and embedded_in_name(pat, sent):
            continue  # e.g. "Paris" inside "Cercle de la Voile de Paris": editing it would not contradict the table
        anchors = [grid[r][cc][0] for rr, cc in hl if rr == r and cc is not None and cc != c
                   and not grid[r][cc][1] and len(grid[r][cc][0]) >= 2 and C.norm(grid[r][cc][0]) != C.norm(v)
                   and occurs_once(grid[r][cc][0], sent)[0]]
        if not anchors:
            continue
        an = [C.norm(a) for a in anchors]
        kv = kind(v)
        for dr in range(len(grid)):
            if dr == r or any(rr == dr for rr, _ in hl_set) or all(h for _, h in grid[dr]):
                continue
            if len({C.norm(t) for t, _ in grid[dr] if C.norm(t)}) <= 1:
                continue  # footnote / spanned note row ("— denotes releases that did not chart"), not a data row
            w, wh = grid[dr][c]
            wn = C.norm(w)
            if wh or not wn or wn == C.norm(v) or wn in hl_vals or f" {wn} " in s_norm or kind(w) != kv:
                continue
            vn = C.norm(v)
            if kv in ("text", "mixed") and (f" {vn} " in f" {wn} " or f" {wn} " in f" {vn} "):
                continue  # "Labour" -> "Labour hold", "Simpsons" -> "Simpsons: Lisa's Pony": not a contradiction
            if kv in ("number", "year"):
                x, y = C.parse_num(w), C.parse_num(v)
                if x is None or y is None or not C.clearly_different(x, y, C.decimals_of(v), rel=0.0):
                    continue
            # no table row may hold both an anchor value and the new value
            clash = False
            for row in grid:
                vals = {C.norm(t) for t, _ in row}
                if wn in vals and any(a in vals for a in an):
                    clash = True
                    break
            if clash:
                continue
            new = pat.sub(w.replace("\\", "\\\\"), sent, count=1)
            if new != sent:
                out.append((new, dr, kv))
    return out


def render(grid, show_rows):
    lines, last = [], -1
    for r in show_rows:
        if last >= 0 and r != last + 1:
            lines.append("| ... |")
        lines.append("| " + " | ".join(t for t, _ in grid[r]) + " |")
        last = r
    if last != len(grid) - 1:
        lines.append("| ... |")
    return "\n".join(lines)


def main():
    meta = json.load(open(CACHE / "member.json"))
    assert meta["sha256_inflated"] == "73be72ca31267b2f2688ec401a45ef1540580773ab39a128cf612f45141d3d9b"
    tfi = C.tabfact_index()
    rng = random.Random(C.SEED)
    drop = Counter()
    cands, seen_tab = [], set()
    exs = [json.loads(l) for l in gzip.open(CACHE / "train_sample.jsonl.gz", "rt", encoding="utf-8")]
    exs.sort(key=lambda e: e["example_id"])
    rng.shuffle(exs)
    for ex in exs:
        title, sec = C.clean_cell(ex["table_page_title"], 300), C.clean_cell(ex["table_section_title"], 300)
        tkey = (C.norm(title), C.norm(sec))
        if tkey in seen_tab:
            drop["table already used"] += 1
            continue
        if C.tabfact_hit(tfi, title=title, url=ex.get("table_webpage_url")):
            drop["TabFact page"] += 1
            continue
        sent = C.clean_cell(ex["sentence_annotations"][0]["final_sentence"], 2000)
        if not (5 <= len(sent.split()) <= 60):
            drop["sentence length"] += 1
            continue
        if C.tabfact_hit(tfi, text=sent):
            drop["TabFact statement overlap"] += 1
            continue
        try:
            grid, pos = grid_of(ex["table"])
        except Exception:  # noqa: BLE001
            drop["table parse"] += 1
            continue
        negs = negatives(ex, grid, pos, sent)
        if not negs:
            drop["no safe edit (not eligible)"] += 1
            continue
        seen_tab.add(tkey)
        cands.append({"rid": str(ex["example_id"]), "title": title, "sec": sec, "sent": sent, "grid": grid,
                      "hl_rows": sorted({r for r, _ in ex["highlighted_cells"]}), "negs": negs})
        if len(cands) >= int(MAX_ROWS * 1.25):
            break

    docs = {}
    for cd in cands:
        docs["t:" + cd["rid"]] = render(cd["grid"], range(len(cd["grid"])))
        docs["s:" + cd["rid"]] = cd["sent"]
    hit = C.local_decontam(docs, heldout=True)
    n0 = len(cands)
    cands = [cd for cd in cands if "t:" + cd["rid"] not in hit and "s:" + cd["rid"] not in hit]
    drop["13-gram overlap"] = n0 - len(cands)

    out, seen = [], set()
    half = min(len(cands), MAX_ROWS) // 2
    for i, cd in enumerate(cands[:2 * half]):
        is_neg = i % 2 == 1
        grid = cd["grid"]
        if is_neg:
            new, donor, kv = rng.choice(sorted(cd["negs"]))
            claim = new
        else:
            claim, donor, kv = cd["sent"], None, None
        n = len(grid)
        header = [r for r in range(min(3, n)) if all(h for _, h in grid[r])]
        if n <= FULL_TABLE_ROWS:
            show = list(range(n))
        else:
            others = [r for r in range(n) if r not in cd["hl_rows"] and r not in header and r != donor]
            extra = sorted(rng.sample(others, min(len(others), 3 if donor is None else 2)))
            show = sorted(set(header) | set(cd["hl_rows"]) | set(extra) | ({donor} if donor is not None else set()))
        table_txt = render(grid, show)
        head = f"Wikipedia page: {cd['title']}" + (f"\nSection: {cd['sec']}" if cd["sec"] else "")
        state = f"{head}\nTable:\n{table_txt}\n\nClaim: {claim}"
        if len(state) > MAX_STATE:
            drop["state too long"] += 1
            continue
        ns = C.norm(state)
        if ns in seen:
            drop["duplicate state"] += 1
            continue
        seen.add(ns)
        out.append({"cd": cd, "state": state, "neg": is_neg, "kind": kv, "claim": claim})
    out.sort(key=lambda x: x["cd"]["rid"])
    rng.shuffle(out)
    n_neg = int(round(NEG_SHARE * len(out)))
    rows = []
    for i, x in enumerate(out):
        negq = i < n_neg
        sup = not x["neg"]
        gold = ("no" if sup else "yes") if negq else ("yes" if sup else "no")
        edges = []
        if negq:
            edges.append("negation")
        if re.search(r"\b(not|no|never|none|neither|nor|without)\b|n't\b", x["claim"], re.I):
            edges.append("negation")
        if re.search(r"\b(all|every|each|only|at least|at most|exactly|more than|less than|fewer than)\b",
                     x["claim"], re.I):
            edges.append("quantifier")
        if x["kind"] == "number":
            edges.append("numeric")
        if x["kind"] == "year" or re.search(r"\b(1[5-9]\d\d|20[0-2]\d)\b", x["claim"]):
            edges.append("temporal")
        if len(x["cd"]["hl_rows"]) > 1:
            edges.append("multi_hop")
        edges.append("table")
        prio = ["negation", "quantifier", "numeric", "temporal", "multi_hop", "table"]
        edge = next((e for e in prio if e in edges), None)
        rows.append({
            "key": KEY, "rid": x["cd"]["rid"], "state": x["state"], "instructions": Q_CON if negq else Q_SUP,
            "options": ["yes", "no"], "gold": gold, "soft": None,
            "meta": {"dataset": "google-research-datasets/ToTTo (totto_data.zip, train member)",
                     "config": "totto_train_data.jsonl, final_sentence; 1-in-5 md5(example_id) sample",
                     "revision": f"zip Last-Modified 2021-08-25, md5 bjQY6SdF32vX/jpTUBHfLg==; member sha256:"
                                 f"{meta['sha256_inflated']}",
                     "licence": LICENCE, "split": "train",
                     "orig_label": {"final_sentence": x["cd"]["sent"]}, "family": C.FAMILY, "edge": edge,
                     "edge_all": sorted(set(edges)), "defs": "contradicted" if negq else "supported",
                     "claim_is_human_sentence": not x["neg"], "edited_value_kind": x["kind"],
                     "context_id": f"{x['cd']['title']} | {x['cd']['sec']}"},
        })

    summ = C.check_rows(KEY, rows)
    print("drops:", dict(drop))
    print("edited kinds:", dict(Counter(r["meta"]["edited_value_kind"] for r in rows)))
    C.write_outputs(KEY, rows, DEFS)
    if "--manifest" in sys.argv:
        C.append_manifest({
            "key": KEY, "family": C.FAMILY, "dataset": "ToTTo train (google-research-datasets)", "licence": LICENCE,
            "rows": summ["rows"], "qtype": "yesno", "yesno_share": round(summ["yesno_share"], 4),
            "edge_tags": summ["edge_tags"],
            "notes": ("Claim verification on Wikipedia tables. Supported = annotator-revised ToTTo sentence; "
                      "contradicted = same sentence with one highlighted cell value swapped for another row's value "
                      "of the same column (anchor kept, no row holds anchor+new value, donor row shown). One example "
                      "per table; TabFact pages dropped; 20% 'contradicted?' question; 13-gram decontam incl. VitaminC."),
        })


if __name__ == "__main__":
    main()
