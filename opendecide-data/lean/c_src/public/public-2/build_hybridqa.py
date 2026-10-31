"""HybridQA candidates (C_DATA_SPEC.md v4 3.2 #7). Train split only (released_data/train.traced.json); tables and
linked passages from WikiTables-WithLinks at a pinned commit (hq_fetch.py). Split 90/10 by page title.

Gold = the crowd answer (answer-text). Only questions whose answer occurs at exactly one traced node are used, and the
answer text must occur (normalized) in exactly one table row's evidence: its cells or the shown passages linked from it.
Framings:
  hq_cell_ch  choice, answer is a table cell: options = cells of the same column from other rows; every option's row
              shows its linked passages (trimmed the same way), so the passages cannot single out the gold row.
  hq_row_yn   yes/no: "is the answer found in the row for <key>?" (its cells or linked passages); asked row = gold
              row (yes) or another shown row (no).
Passages are trimmed by one rule for every shown row: first sentence + sentences sharing a content word with the
question (+ the answer sentence in the gold row), at most 60 words per passage, at most 2 passages per row.
"""
from __future__ import annotations

import json
import re

from p2_common import RAW, TMP, DedupIndex, detok, est_tokens, log_progress, norm, page_bucket, rng_for, stable_id
from render import render_table

SOURCE = "c_pub_hybridqa"
WT = RAW / "wtwl"
STOP = set("the a an of in on at to for by with and or is was were what which who whom whose when where how name "
           "did does do are be has have had its it this that from as than then there their his her he she they "
           "one also into after before about over under between during".split())
SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])")

W_CELL = {
    "hq_cell_w1": "Using the table and the linked passages, which entry answers the question?",
    "hq_cell_w2": "Which option is the answer to the question?",
    "hq_cell_w3": "Read the table together with its passages and pick the cell that answers the question.",
    "hq_cell_w4": "Based only on the evidence shown, select the correct answer.",
}
W_ROW = {
    "hq_row_w1": "Is the answer to the question found in the row for {key}?",
    "hq_row_w2": "Does the row for {key} (its cells or its linked passages) hold the answer to the question?",
    "hq_row_w3": "Is {key}'s row the one that supplies the answer to the question?",
    "hq_row_w4": "Would you find the answer to the question in the row for {key}, counting its linked passages?",
}
CARDS = {
    "hq_card_line_ch": {"style": "one_line", "qtype": "choice",
                        "text": "Answer only from the table and the passages linked from its cells (marked [P1], "
                                "[P2], ...); no outside knowledge."},
    "hq_card_rubric_ch": {"style": "rubric", "qtype": "choice",
                          "text": "Rules:\n- Use only the table and the linked passages shown; no outside knowledge.\n"
                                  "- A cell marked [Pn] links to passage [Pn] about that cell's entity.\n"
                                  "- Find the row the question describes (its cells and passages must fit every "
                                  "detail of the question), then give the requested entry of that row."},
    "hq_card_line_yn": {"style": "one_line", "qtype": "noul",
                        "text": "- yes: the named row's cells or its linked passages contain the answer to the "
                                "question.\n- no: the answer is not in that row; it comes from another row."},
    "hq_card_rubric_yn": {"style": "rubric", "qtype": "noul",
                          "text": "- yes: the answer to the question is stated in the named row: in one of its cells "
                                  "or in a passage linked from one of its cells (marked [Pn]).\n- no: the answer "
                                  "is not stated in that row.\nWork it out from the table and the passages shown "
                                  "only; exactly one row holds the answer."},
}


def page_of(table_id):
    return re.sub(r"_\d+$", "", table_id).replace("_", " ")


def content_words(q):
    return {w for w in norm(q).split() if w not in STOP and len(w) >= 3}


ABBR = re.compile(r"(?:\b[A-Z]|\b(?:Mr|Mrs|Ms|Dr|St|Jr|Sr|No|Nos|Vol|vs|Inc|Co|Corp|Ltd|Mt|Ft|Gen|Col|Lt|Sgt|Capt|Rev|"
                  r"Prof|Sen|Rep|Gov|Pres|Bros|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|approx|ca|etc|e\.g|"
                  r"i\.e|U\.S|U\.K|D\.C|a\.m|p\.m))\.$")


def split_sents(text):
    parts = [p for p in SENT.split(text) if p.strip()]
    out = []
    for p in parts:
        if out and ABBR.search(out[-1]):
            out[-1] = out[-1] + " " + p.strip()
        else:
            out.append(p.strip())
    return out


def trim(passage, qwords, must=None, limit=60):
    sents = split_sents(detok(passage))
    if not sents:
        return ""
    keep = [0]
    for i, s in enumerate(sents[1:], 1):
        sw = set(norm(s).split())
        if (must and norm(must) and f" {norm(must)} " in f" {norm(s)} ") or (qwords & sw):
            keep.append(i)
    out, n = [], 0
    must_i = None
    if must:
        for i in keep:
            if f" {norm(must)} " in f" {norm(sents[i])} ":
                must_i = i
                break
    for i in keep:
        w = len(sents[i].split())
        if n + w > limit and i != must_i:
            continue
        out.append(sents[i])
        n += w
    return " ".join(out)


def load_table(tid):
    t = json.load(open(WT / "tables_tok" / f"{tid}.json"))
    req = json.load(open(WT / "request_tok" / f"{tid}.json"))
    return t, req


def key_column(t):
    n = len(t["data"])
    for c in range(len(t["header"])):
        vals = [norm(detok(r[c][0])) for r in t["data"]]
        if all(vals) and len(set(vals)) == n:
            return c
    return None


def build(targets, dev_target, out_path):
    pick = json.load(open(TMP / "hq_pick.json"))
    data = json.load(open(RAW / "hybridqa_train.traced.json"))
    by_table = {}
    for q in data:
        by_table.setdefault(q["table_id"], []).append(q)
    idx = DedupIndex()
    want = {f: int(targets[f] * 1.6) + 20 for f in targets}
    dev_want = {f: dev_target[f] * 2 + 5 for f in targets}
    have = {(p, f): 0 for p in ("train", "dev") for f in targets}
    stats = {"tables": 0, "no_q": 0, "dedup_drop": 0, "too_long": 0, "ambiguous": 0, "kept": 0}
    cands = []
    from hq_fetch import BAD_Q
    for part, tids in (("train", pick["train_tables"] + pick.get("train_tables_more", [])), ("dev", pick["dev_tables"])):
        for tid in tids:
            stats["tables"] += 1
            try:
                t, req = load_table(tid)
            except (FileNotFoundError, json.JSONDecodeError):
                continue
            rng = rng_for("hq", tid)
            qs = [q for q in by_table.get(tid, []) if len(q.get("answer-node") or []) == 1
                  and not BAD_Q.search(q["question"])]
            rng.shuffle(qs)
            row = None
            for q in qs:
                frs = [f for f in targets if have[(part, f)] < (want[f] if part == "train" else dev_want[f])]
                if not frs:
                    break
                node = q["answer-node"][0]
                if node[3] != "table" and "hq_cell_ch" in frs and len(frs) > 1:
                    frs = [f for f in frs if f != "hq_cell_ch"]
                frs.sort(key=lambda f: have[(part, f)] / (want[f] if part == "train" else dev_want[f]))
                for fr in frs:
                    row = make_row(fr, q, t, req, rng, idx, stats)
                    if row:
                        break
                if row:
                    break
            if not row:
                stats["no_q"] += 1
                continue
            row["_x"].update(part=part, page=page_of(tid))
            have[(part, row["_x"]["framing"])] += 1
            cands.append(row)
    stats["kept"] = len(cands)
    stats["have"] = {f"{p}:{f}": n for (p, f), n in have.items()}
    with open(out_path, "w") as f:
        for r in cands:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    log_progress(f"HybridQA candidates: {json.dumps(stats)}")
    return stats


def make_row(fr, q, t, req, rng, idx, stats):
    node = q["answer-node"][0]
    ans = (q.get("answer-text") or "").strip()
    na = norm(ans)
    if not na:
        return None
    r_gold, c_gold = node[1]
    data = t["data"]
    header = [detok(h[0]) for h in t["header"]]
    nrow, ncol = len(data), len(header)
    if not (3 <= nrow <= 25) or ncol > 8 or r_gold >= nrow:
        return None
    cells = [[detok(c[0]) for c in r] for r in data]
    qwords = content_words(q["question"])
    # question-level ambiguity guard: a linked entity of the gold row that also appears in another row (as a link or
    # as the same cell text) gives the question a second candidate row
    gold_links = {lk for c in data[r_gold] for lk in c[1]}
    gold_link_text = {norm(cells[r_gold][j]) for j, c in enumerate(data[r_gold]) if c[1]}
    for i, r in enumerate(data):
        if i == r_gold:
            continue
        if any(lk in gold_links for c in r for lk in c[1]) or any(norm(x) in gold_link_text for x in cells[i]):
            stats["ambiguous"] += 1
            return None

    def shares(i, skip_col=None):
        a = {norm(x) for j, x in enumerate(cells[i]) if j != skip_col and norm(x)}
        b = {norm(x) for j, x in enumerate(cells[r_gold]) if j != skip_col and norm(x)}
        return bool(a & b)
    # uniqueness of the answer among table cells
    cell_hits = [i for i, r in enumerate(cells) if any(f" {na} " in f" {norm(c)} " for c in r)]
    if fr == "hq_cell_ch":
        if node[3] != "table" or norm(cells[r_gold][c_gold]) != na:
            return None
        col_vals = {}
        for i, r in enumerate(cells):
            v = norm(r[c_gold])
            if v and v != na and v not in col_vals.values() and i != r_gold and not shares(i, skip_col=c_gold):
                col_vals[i] = v
        if len(col_vals) < 2:
            return None
        k = min(len(col_vals) + 1, rng.choice([3, 3, 4, 4, 5]))
        others = sorted(col_vals)
        rng.shuffle(others)
        shown = [r_gold] + others[:k - 1]
    else:
        kc = key_column(t)
        if kc is None:
            return None
        linked_rows = [i for i, r in enumerate(data) if i != r_gold and any(c[1] for c in r) and not shares(i)]
        if len(linked_rows) < 2:
            return None
        rng.shuffle(linked_rows)
        shown = [r_gold] + linked_rows[:rng.choice([2, 3])]
    # passages for every shown row (same trimming rule), at most 2 per row; answer link first in the gold row
    pid, plist, tags = 0, [], {}
    for i in sorted(shown):  # table order, so a passage number never marks the gold row
        links = []
        for j, c in enumerate(data[i]):
            for lk in c[1]:
                if lk in req and lk not in links:
                    links.append((j, lk))
        # same rule for every shown row: the passages that share the most content words with the question first
        rng.shuffle(links)
        links.sort(key=lambda x: -len(qwords & set(norm(detok(req[x[1]])).split())))
        if i == r_gold and node[3] == "passage":
            links.sort(key=lambda x: x[1] != node[2])
        for j, lk in links[:2]:
            must = ans if (i == r_gold and lk == node[2]) else None
            txt = trim(req[lk], qwords, must=must)
            if not txt:
                continue
            if i != r_gold and f" {na} " in f" {norm(txt)} ":
                stats["ambiguous"] += 1
                return None
            pid += 1
            tags[(i, j)] = tags.get((i, j), []) + [f"P{pid}"]
            plist.append((f"P{pid}", detok(data[i][j][0]), txt, i))
    # the answer must be in the gold row's evidence and nowhere else
    gold_ev = " ".join([" ".join(cells[r_gold])] + [p[2] for p in plist if p[3] == r_gold])
    if f" {na} " not in f" {norm(gold_ev)} ":
        stats["ambiguous"] += 1
        return None
    if any(i != r_gold for i in cell_hits):
        stats["ambiguous"] += 1
        return None
    # the shown evidence must carry the question's details: >= 60% of its content words appear in the gold row's
    # cells and shown passages, the headers or the page title (otherwise a needed bridge passage was cut)
    support = set(norm(gold_ev + " " + " ".join(header) + " " + detok(t.get("title") or "") + " "
                       + detok(t.get("section_title") or "")).split())
    if qwords and len(qwords & support) / len(qwords) < 0.6:
        stats["thin_evidence"] = stats.get("thin_evidence", 0) + 1
        return None
    # dedup vs golden_train (unit hashes) and the named C1 sources (10-grams)
    ev_text = "\n".join([" | ".join(r) for r in cells] + [p[2] for p in plist])
    if idx.unit_hits(ev_text) or idx.gram_hits(ev_text):
        stats["dedup_drop"] += 1
        return None
    shown_cells = [[c + ("".join(f" [{x}]" for x in tags.get((i, j), []))) for j, c in enumerate(r)]
                   for i, r in enumerate(cells)]
    container = rng.choice(["markdown", "csv", "html", "key_value", "pipe_plain"])
    table_txt = render_table(header, shown_cells, container, title=detok(t.get("title") or ""),
                             caption=detok(t.get("section_title") or "") or None)
    ptxt = "\n".join(f"[{p[0]}] {p[1]}: {p[2]}" for p in plist)
    state = f"{table_txt}\n\nLinked passages:\n{ptxt}\n\nQuestion: {q['question'].strip()}"
    if est_tokens(state) > 1800:
        stats["too_long"] += 1
        return None
    u = rng.random()
    sfx = "ch" if fr == "hq_cell_ch" else "yn"
    cid = None if u < 0.15 else (f"hq_card_line_{sfx}" if u < 0.55 else f"hq_card_rubric_{sfx}")
    if fr == "hq_cell_ch":
        opts = [cells[i][c_gold] for i in shown]
        rng.shuffle(opts)
        gold = cells[r_gold][c_gold]
        wid = rng.choice(sorted(W_CELL))
        instr = W_CELL[wid]
        qtype = "choice"
        extra = {"k": len(opts)}
    else:
        kc = key_column(t)
        want_yes = rng.random() < 0.5
        asked = r_gold if want_yes else rng.choice(shown[1:])
        key = f"{header[kc]} \"{cells[asked][kc]}\""
        wid = rng.choice(sorted(W_ROW))
        instr = W_ROW[wid].format(key=key)
        opts, gold, qtype = None, int(asked == r_gold), "noul"
        extra = {"asked_row": asked, "gold_row": r_gold}
    return {
        "id": stable_id("pub_hq_", fr, q["question_id"]),
        "group_id": "g:pub:hybridqa:" + q["table_id"],
        "call_id": stable_id("c_pub_hq_", fr, q["question_id"]),
        "source": SOURCE,
        "state": state,
        "qtype": qtype,
        "instructions": instr,
        "options": opts,
        "gold": gold,
        "role": "aff" if qtype == "noul" else "choice",
        "card": CARDS[cid]["text"] if cid else None,
        "meta": {},
        "_x": dict(framing=fr, card_id=cid, wording_id=wid, container=container,
                   record_id=f"train.traced.json:{q['question_id']}", table_id=q["table_id"],
                   answer_type=node[3], n_passages=len(plist), record_text=ev_text, **extra),
    }


if __name__ == "__main__":
    print(build({"hq_cell_ch": 550, "hq_row_yn": 450}, {"hq_cell_ch": 18, "hq_row_yn": 17}, TMP / "cand_hybridqa.jsonl"))
