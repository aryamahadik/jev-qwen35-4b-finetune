"""WikiSQL candidates (C_DATA_SPEC.md v4 3.2 #8: "execute the SQL"; program labels from SQL execution).

Train split only (data/train.jsonl, train.tables.jsonl, train.db from the repo's data.tar.bz2; dev/test members are
never extracted). Split 90/10 by Wikipedia page title (page_title, else the WikiSQL page id) for the mix-tuning dev.

Framings (labels: solver A = Python over train.tables.jsonl with exact Fractions; solver B = SQLite over the official
train.db with WikiSQL's DBEngine semantics; a candidate is kept only when both agree):
  ws_lookup_ch  choice: the crowd question (human text) + the table; gold = the executed no-aggregation SQL answer
                (exactly one matching row); options = other values of the same column (+ abstain on some rows).
  ws_agg_ch     choice: templated reading of the SQL (conditions + aggregate); gold = executed value; distractors
                are specific computation errors (wrong aggregate, condition ignored, one row dropped, ...).
  ws_count_yn   yes/no: number of rows meeting the SQL's condition(s) vs a threshold T.
  ws_agg_yn     yes/no: executed aggregate (or numeric lookup) vs a threshold T.
"""
from __future__ import annotations

import json
import re
import sqlite3
from fractions import Fraction

from p2_common import RAW, TMP, page_bucket, rng_for, stable_id, norm, log_progress
from render import CONTAINERS, fmt_num, holds, pick_ranked, pick_threshold, render_table, to_frac

AGG = ["", "MAX", "MIN", "COUNT", "SUM", "AVG"]
OPS = ["=", ">", "<"]
DATASET = "WikiSQL"
SOURCE = "c_pub_wikisql"

AGG_WORDS = re.compile(r"\b(how many|number of|total|average|mean|sum|most|least|highest|lowest|largest|smallest|"
                       r"maximum|minimum|max|min|fewest|greatest|biggest|first|last|earliest|latest|top|bottom|"
                       r"count|combined|all)\b", re.I)
STOP = set("the a an of in on at to for by with and or is was what which who whom whose when where how name tell me "
           "did does do are were be has have had its it this that from as".split())


def load():
    tabs = {}
    with open(RAW / "data" / "train.tables.jsonl") as f:
        for line in f:
            t = json.loads(line)
            tabs[t["id"]] = t
    qs = []
    with open(RAW / "data" / "train.jsonl") as f:
        for i, line in enumerate(f):
            q = json.loads(line)
            q["_idx"] = i
            qs.append(q)
    return tabs, qs


def page_of(t):
    return t.get("page_title") or ("wikisql-page-" + t["id"].split("-")[1])


# ------------------------------------------------------------------ solver A (python, exact)

def num(v):
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return to_frac(v)
    s = str(v).replace(",", "").strip()
    m = re.fullmatch(r"-?\d+(\.\d+)?", s)
    if not m:
        raise ValueError(v)
    return Fraction(s)


def match_rows(t, conds):
    out = []
    for i, r in enumerate(t["rows"]):
        ok = True
        for ci, op, v in conds:
            cell = r[ci]
            if t["types"][ci] == "real":
                try:
                    a, b = num(cell), num(v)
                except ValueError:
                    return None
                ok = (a == b) if op == 0 else (a > b) if op == 1 else (a < b)
            else:
                if op != 0:
                    return None  # lexicographic text comparison: never used
                ok = str(cell).strip().lower() == str(v).strip().lower()
            if not ok:
                break
        if ok:
            out.append(i)
    return out


def exec_a(t, sel, agg, conds):
    rows = match_rows(t, conds)
    if rows is None:
        return None
    vals = [t["rows"][i][sel] for i in rows]
    if agg == 0:
        return {"rows": rows, "values": vals}
    if agg == 3:
        return {"rows": rows, "value": Fraction(len(rows))}
    if t["types"][sel] != "real" or not rows:
        return None
    try:
        nv = [num(v) for v in vals]
    except ValueError:
        return None
    if agg == 1:
        return {"rows": rows, "value": max(nv)}
    if agg == 2:
        return {"rows": rows, "value": min(nv)}
    if agg == 4:
        return {"rows": rows, "value": sum(nv)}
    if agg == 5:
        return {"rows": rows, "value": sum(nv) / len(nv)}
    return None


# ------------------------------------------------------------------ solver B (sqlite, official DBEngine semantics)

class DB:
    def __init__(self):
        self.db = sqlite3.connect(str(RAW / "data" / "train.db"))
        self.schema = {}

    def types(self, tid):
        name = "table_" + tid.replace("-", "_")
        if name not in self.schema:
            sql = self.db.execute("SELECT sql FROM sqlite_master WHERE tbl_name = ?", (name,)).fetchone()[0]
            inner = re.findall(r"\((.*)\)", sql)[0]
            self.schema[name] = dict(tup.split() for tup in inner.split(", "))
        return name, self.schema[name]

    def execute(self, tid, sel, agg, conds):
        name, schema = self.types(tid)
        select = f"col{sel}"
        if agg:
            select = f"{AGG[agg]}({select})"
        where, params = [], {}
        for k, (ci, op, v) in enumerate(conds):
            if isinstance(v, str):
                v = v.lower()
            if schema[f"col{ci}"] == "real" and not isinstance(v, (int, float)):
                try:
                    v = float(str(v).replace(",", ""))
                except ValueError:
                    return None
            where.append(f"col{ci} {OPS[op]} :p{k}")
            params[f"p{k}"] = v
        q = f"SELECT {select} AS result FROM {name}" + (" WHERE " + " AND ".join(where) if where else "")
        return [r[0] for r in self.db.execute(q, params).fetchall()]


def agree(resA, resB, agg):
    if resA is None or resB is None:
        return False
    if agg == 0:
        a = sorted(norm(fmt_num(v)) if isinstance(v, (int, float)) else norm(v) for v in resA["values"])
        b = sorted(norm(fmt_num(v)) if isinstance(v, (int, float)) else norm(v) for v in resB)
        return a == b
    if len(resB) != 1 or resB[0] is None:
        return False
    try:
        return abs(float(resA["value"]) - float(resB[0])) < 1e-6 * max(1.0, abs(float(resB[0])))
    except (TypeError, ValueError):
        return False


# ------------------------------------------------------------------ rendering

OPP = {  # yes/no comparison phrases (count and value); semantics fixed in the card
    ">": ["more than", "greater than", "above"],
    ">=": ["at least", "no less than", "greater than or equal to"],
    "<": ["less than", "below", "under"],
    "<=": ["at most", "no more than", "not more than"],
}
COUNT_OPP = {">": ["more than"], ">=": ["at least", "no fewer than"], "<": ["fewer than"], "<=": ["at most", "no more than"]}


def holds(x: Fraction, op, T: Fraction):
    return {">": x > T, ">=": x >= T, "<": x < T, "<=": x <= T}[op]


def cond_text(t, conds):
    parts = []
    for ci, op, v in conds:
        h = t["header"][ci]
        if op == 0:
            # show the table's own spelling of the matched value when unique
            cells = {str(r[ci]) for r in t["rows"] if str(r[ci]).strip().lower() == str(v).strip().lower()}
            vv = cells.pop() if len(cells) == 1 else str(v)
            if t["types"][ci] == "real":
                parts.append(f"'{h}' equals {fmt_num(num(v))}")
            else:
                parts.append(f"'{h}' is \"{vv}\"")
        else:
            parts.append(f"'{h}' is {'greater than' if op == 1 else 'less than'} {fmt_num(num(v))}")
    return " and ".join(parts)


AGG_PHRASE = {1: "the largest value of '{h}'", 2: "the smallest value of '{h}'", 4: "the sum of '{h}'",
              5: "the average (mean) of '{h}'", 3: "the number of rows"}

W_LOOKUP = {
    "ws_lookup_w1": "Using only the table, which value answers the question?",
    "ws_lookup_w2": "Pick the table entry that answers the question.",
    "ws_lookup_w3": "According to the table, which option is the answer to the question?",
    "ws_lookup_w4": "Read the table and choose the value the question asks for.",
    "ws_lookup_w5": "Based on the table alone, select the correct answer.",
}
W_AGGCH = {
    "ws_aggch_w1": "Which option is the value the task asks for?",
    "ws_aggch_w2": "Work out the requested figure from the table and pick it.",
    "ws_aggch_w3": "Select the number that the described calculation gives on this table.",
    "ws_aggch_w4": "Choose the correct result of the calculation in the task.",
}
W_COUNT = {
    "ws_count_w1": "Is the number of rows that meet the condition {op} {T}?",
    "ws_count_w2": "Do {op} {T} rows of the table meet the condition?",
    "ws_count_w3": "Counting only the rows that satisfy the condition, is the count {op} {T}?",
    "ws_count_w4": "Does the table contain {op} {T} rows matching the condition?",
}
W_AGGYN = {
    "ws_aggyn_w1": "Is this quantity {op} {T}?",
    "ws_aggyn_w2": "Computed from the table, is the quantity {op} {T}?",
    "ws_aggyn_w3": "Does the quantity come out {op} {T}?",
    "ws_aggyn_w4": "Judging only by the table, is the stated quantity {op} {T}?",
}

CARDS = {
    "ws_card_line_ch": {"style": "one_line", "qtype": "choice",
                        "text": "Answer from the table only. A text condition matches a cell with the same text "
                                "(letter case ignored); numbers compare by value."},
    "ws_card_rubric_ch": {"style": "rubric", "qtype": "choice",
                          "text": "Rules:\n- Use only the table shown; no outside knowledge.\n"
                                  "- 'X is \"v\"' matches the rows whose X cell has exactly the text v (letter case "
                                  "ignored).\n- 'greater than' and 'less than' exclude the value itself.\n"
                                  "- The number of rows counts matching rows. The average is the sum divided by the "
                                  "number of matching rows, not rounded.\n- If an option says none of the listed "
                                  "values is right, pick it only when no other option is correct."},
    "ws_card_line_yn": {"style": "one_line", "qtype": "noul",
                        "text": "- yes: the comparison in the question holds exactly for the figure computed from "
                                "the table.\n- no: it does not hold."},
    "ws_card_rubric_yn": {"style": "rubric", "qtype": "noul",
                          "text": "- yes: the figure computed from the table makes the stated comparison true.\n"
                                  "- no: the figure makes the comparison false.\n"
                                  "How to compute: use only the table; 'X is \"v\"' matches cells with exactly the "
                                  "text v (letter case ignored); a count is the number of matching rows; the average "
                                  "is the sum divided by the number of matching rows, not rounded. 'more than', "
                                  "'greater than', 'above', 'less than', 'fewer than', 'below' and 'under' exclude the "
                                  "threshold itself; 'at least', 'no less than', 'no fewer than', 'greater than or "
                                  "equal to', 'at most', 'no more than' and 'not more than' include it."},
}


def pick_card(rng, qtype):
    u = rng.random()
    if u < 0.15:
        return None
    if u < 0.55:
        return f"ws_card_line_{'ch' if qtype == 'choice' else 'yn'}"
    return f"ws_card_rubric_{'ch' if qtype == 'choice' else 'yn'}"


def header_overlap(q, h):
    qw = {w.rstrip("s") for w in norm(q).split()}
    hw = [w.rstrip("s") for w in norm(h).split() if w not in STOP and len(w) >= 3]
    return any(w in qw for w in hw)


def table_state(t, rows, container, rng):
    return render_table(t["header"], [t["rows"][i] for i in rows], container, title=t.get("page_title"),
                        caption=t.get("caption") or t.get("section_title"))


def option_bucket(rng, avail):
    u = rng.random()
    k = 2 + rng.randint(1, 2) if u < 0.5 else rng.randint(5, 9) if u < 0.85 else rng.randint(10, 19)
    return max(2, min(k, avail + 1))


def threshold(rng, x: Fraction, want_yes: bool, integer: bool):
    if integer:
        step = Fraction(rng.choice([1, 1, 2, 3]))
    else:
        step = Fraction(round(max(1.0, abs(float(x)) * rng.choice([5, 10, 20]) / 100), 1)).limit_denominator(10)
    r = pick_threshold(rng, x, want_yes, step, boundary_ok=(x.denominator == 1))
    if not r:
        return None
    op, T, _ = r
    if not integer:
        T = Fraction(round(float(T), 1)).limit_denominator(10)
    if holds(x, op, T) != want_yes or (integer and T < 0):
        return None
    return op, T


def build(targets, dev_target, out_path):
    tabs, qs = load()
    db = DB()
    rng0 = rng_for("ws_order")
    order = list(range(len(qs)))
    rng0.shuffle(order)
    used_tables = set()
    cands = []
    framing_of = ["ws_lookup_ch", "ws_agg_ch", "ws_count_yn", "ws_agg_yn"]
    stats = {"seen": 0, "disagree": 0, "kept": 0}
    want = {f: int(targets[f] * 1.6) + 20 for f in framing_of}
    dev_want = {f: dev_target[f] * 2 + 5 for f in framing_of}
    have = {("train", f): 0 for f in framing_of}
    have.update({("dev", f): 0 for f in framing_of})
    for qi in order:
        q = qs[qi]
        t = tabs[q["table_id"]]
        if q["table_id"] in used_tables:
            continue
        page = page_of(t)
        part = "dev" if page_bucket(page) == 0 else "train"
        if len(t["rows"]) < 3 or len(t["rows"]) > 40 or len(t["header"]) > 10:
            continue
        sql = q["sql"]
        sel, agg, conds = sql["sel"], sql["agg"], sql["conds"]
        if any(op != 0 and t["types"][ci] != "real" for ci, op, v in conds):
            continue
        stats["seen"] += 1
        rng = rng_for("ws", q["_idx"])
        # which framing can this record serve? (rotate so every framing gets candidates)
        options = []
        if agg == 0 and conds and all(op == 0 for _, op, _ in conds) and not AGG_WORDS.search(q["question"]) \
                and all(str(v).lower() in q["question"].lower() for _, _, v in conds) \
                and header_overlap(q["question"], t["header"][sel]):
            options.append("ws_lookup_ch")
        if conds:
            options.append("ws_count_yn")
            if t["types"][sel] == "real" and agg in (0, 1, 2, 4, 5):
                options += ["ws_agg_ch", "ws_agg_yn"]
            if agg == 3:
                options += ["ws_agg_ch"]
        options = [f for f in options if have[(part, f)] < (want[f] if part == "train" else dev_want[f])]
        if not options:
            continue
        # prefer the framing furthest from its target
        options.sort(key=lambda f: have[(part, f)] / max(1, (want[f] if part == "train" else dev_want[f])))
        row = None
        for fr in options:
            row = make_row(fr, q, t, db, rng, stats)
            if row:
                break
        if not row:
            continue
        row["_x"]["part"] = part
        row["_x"]["page"] = page
        have[(part, row["_x"]["framing"])] += 1
        used_tables.add(q["table_id"])
        cands.append(row)
        if all(have[("train", f)] >= want[f] for f in framing_of) and all(have[("dev", f)] >= dev_want[f] for f in framing_of):
            break
    stats["kept"] = len(cands)
    stats["have"] = {f"{p}:{f}": n for (p, f), n in have.items()}
    with open(out_path, "w") as f:
        for r in cands:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    log_progress(f"WikiSQL candidates: {json.dumps(stats)}")
    return stats


def base_row(q, t, fr, qtype, state, instr, options, gold, card_id, wid, container, extra):
    return {
        "id": stable_id("pub_ws_", fr, q["_idx"]),
        "group_id": "g:pub:wikisql:" + t["id"],
        "call_id": stable_id("c_pub_ws_", fr, q["_idx"]),
        "source": SOURCE,
        "state": state,
        "qtype": qtype,
        "instructions": instr,
        "options": options,
        "gold": gold,
        "role": "aff" if qtype == "noul" else "choice",
        "card": CARDS[card_id]["text"] if card_id else None,
        "meta": {},
        "_x": dict(framing=fr, card_id=card_id, wording_id=wid, container=container,
                   record_id=f"train.jsonl:{q['_idx']}", table_id=t["id"], **extra),
    }


def make_row(fr, q, t, db, rng, stats):
    sel, agg, conds = q["sql"]["sel"], q["sql"]["agg"], q["sql"]["conds"]
    container = rng.choice(CONTAINERS)
    all_rows = list(range(len(t["rows"])))
    if fr == "ws_lookup_ch":
        a = exec_a(t, sel, 0, conds)
        b = db.execute(t["id"], sel, 0, conds)
        if not agree(a, b, 0):
            stats["disagree"] += 1
            return None
        if len(a["rows"]) != 1:
            return None
        gold = a["values"][0]
        gtxt = fmt_num(gold) if isinstance(gold, (int, float)) else str(gold).strip()
        if not norm(gtxt) or norm(gtxt) in norm(q["question"]):
            return None
        pool, seen = [], {norm(gtxt)}
        for r in t["rows"]:
            v = r[sel]
            vt = fmt_num(v) if isinstance(v, (int, float)) else str(v).strip()
            if norm(vt) and norm(vt) not in seen:
                seen.add(norm(vt))
                pool.append(vt)
        if len(pool) < 2:
            return None
        k = option_bucket(rng, len(pool))
        abstain = rng.random() < 0.2
        abstain_gold = abstain and rng.random() < 0.4
        rng.shuffle(pool)
        opts = pool[:k - 1] + ([] if abstain_gold else [gtxt])
        if abstain:
            if abstain_gold:
                opts = pool[:k]
            opts.append("None of the listed values")
        lead = [o for o in opts if o != "None of the listed values"]
        rng.shuffle(lead)
        opts = lead + (["None of the listed values"] if abstain else [])
        goldo = "None of the listed values" if abstain_gold else gtxt
        wid = rng.choice(sorted(W_LOOKUP))
        state = table_state(t, all_rows, container, rng) + f"\n\nQuestion: {q['question'].strip()}"
        return base_row(q, t, fr, "choice", state, W_LOOKUP[wid], opts, goldo, pick_card(rng, "choice"), wid,
                        container, {"abstain_shown": abstain, "gold_is_abstain": abstain_gold, "k": len(opts),
                                    "record_text": state})
    if fr in ("ws_agg_ch", "ws_agg_yn"):
        use_agg = agg if agg in (1, 2, 3, 4, 5) else None
        if use_agg is None:
            # numeric lookup from a no-aggregation query: single matching row
            a = exec_a(t, sel, 0, conds)
            b = db.execute(t["id"], sel, 0, conds)
            if not agree(a, b, 0) or len(a["rows"]) != 1 or t["types"][sel] != "real":
                return None
            try:
                x = num(a["values"][0])
            except ValueError:
                return None
            qty = f"the value of '{t['header'][sel]}' in the row where {cond_text(t, conds)}"
            matched = a["rows"]
        else:
            a = exec_a(t, sel, use_agg, conds)
            b = db.execute(t["id"], sel, use_agg, conds)
            if not agree(a, b, use_agg) or not a["rows"]:
                stats["disagree"] += (a is not None and b is not None)
                return None
            if len(a["rows"]) < 2:
                # relax to a single condition that matches >= 2 rows (re-executed by both solvers)
                best = None
                for c in conds:
                    a2 = exec_a(t, sel, use_agg, [c])
                    b2 = db.execute(t["id"], sel, use_agg, [c])
                    if agree(a2, b2, use_agg) and len(a2["rows"]) >= 2 and (best is None or len(a2["rows"]) > len(best[1]["rows"])):
                        best = ([c], a2)
                if not best:
                    return None
                conds, a = best
            x = a["value"]
            if use_agg == 3:
                qty = f"the number of rows where {cond_text(t, conds)}"
            else:
                qty = AGG_PHRASE[use_agg].format(h=t["header"][sel]) + f" over the rows where {cond_text(t, conds)}"
            matched = a["rows"]
        integer = x.denominator == 1 and (use_agg in (None, 3) or all(
            num(t["rows"][i][sel]).denominator == 1 for i in matched))
        if fr == "ws_agg_yn":
            want_yes = rng.random() < 0.5
            th = threshold(rng, x, want_yes, integer)
            if not th:
                return None
            op, T = th
            opw = rng.choice(OPP[op])
            wid = rng.choice(sorted(W_AGGYN))
            state = table_state(t, all_rows, container, rng) + f"\n\nQuantity: {qty}."
            gold = int(holds(x, op, T))
            return base_row(q, t, fr, "noul", state, W_AGGYN[wid].format(op=opw, T=fmt_num(T)), None, gold,
                            pick_card(rng, "noul"), wid, container,
                            {"op": op, "T": fmt_num(T), "x": fmt_num(x), "boundary": T == x, "record_text": state})
        # choice: functional distractors
        vals = []
        try:
            mv = [num(t["rows"][i][sel]) for i in matched] if t["types"][sel] == "real" else []
            allv = [num(r[sel]) for r in t["rows"]] if t["types"][sel] == "real" else []
        except ValueError:
            return None
        if use_agg == 3:
            # symmetric off-by-k errors plus "condition ignored" counts; gold is never systematically the smallest
            n_all = Fraction(len(t["rows"]))
            vals = [x - 2, x - 1, x + 1, x + 2, n_all]
            for c in conds:
                a2 = exec_a(t, sel, 3, [c])
                if a2:
                    vals.append(a2["value"])
            vals = [v for v in vals if v >= 1]
            rng.shuffle(vals)
        elif mv:
            cand = {
                1: [min(mv), max(allv), sum(mv), sorted(mv)[-2] if len(mv) > 1 else None],
                2: [max(mv), min(allv), sum(mv), sorted(mv)[1] if len(mv) > 1 else None],
                4: [sum(allv), max(mv), sum(mv) - min(mv), sum(mv) / len(mv)],
                5: [sum(mv), sum(allv) / len(allv), max(mv), min(mv)],
                None: [],
            }[use_agg]
            vals = [v for v in cand if v is not None]
            if use_agg is None:
                others = [num(r[sel]) for i, r in enumerate(t["rows"]) if i not in matched]
                rng.shuffle(others)
                vals = others[:6]
        seen, opts = {fmt_num(x)}, []
        for v in vals:
            s = fmt_num(v)
            if s in seen or (v < 0 <= x):
                continue
            seen.add(s)
            opts.append(s)
        if len(opts) < 2:
            return None
        k = min(len(opts), rng.randint(2, 4))
        picked = pick_ranked(rng, opts, x, k)
        if not picked:
            return None
        abstain = rng.random() < 0.2
        abstain_gold = abstain and rng.random() < 0.4
        lead = picked + ([] if abstain_gold else [fmt_num(x)])
        rng.shuffle(lead)
        final = lead + (["None of these"] if abstain else [])
        goldo = "None of these" if abstain_gold else fmt_num(x)
        wid = rng.choice(sorted(W_AGGCH))
        state = table_state(t, all_rows, container, rng) + f"\n\nTask: find {qty}."
        return base_row(q, t, fr, "choice", state, W_AGGCH[wid], final, goldo, pick_card(rng, "choice"), wid,
                        container, {"abstain_shown": abstain, "gold_is_abstain": abstain_gold, "k": len(final),
                                    "x": fmt_num(x), "record_text": state})
    if fr == "ws_count_yn":
        # count rows meeting the SQL's conditions; prefer the (sub)condition with the most rows
        best = None
        for cs in [conds] + ([[c] for c in conds] if len(conds) > 1 else []):
            a = exec_a(t, sel, 3, cs)
            b = db.execute(t["id"], sel, 3, cs)
            if agree(a, b, 3) and a["value"] >= 1 and (best is None or a["value"] > best[1]):
                best = (cs, a["value"])
        if not best:
            stats["disagree"] += 1
            return None
        cs, x = best
        want_yes = rng.random() < 0.5
        th = threshold(rng, x, want_yes, True)
        if not th:
            return None
        op, T = th
        if T < 1 and op in ("<", "<="):
            return None
        opw = rng.choice(COUNT_OPP[op])
        wid = rng.choice(sorted(W_COUNT))
        state = table_state(t, all_rows, container, rng) + f"\n\nCondition: {cond_text(t, cs)}."
        gold = int(holds(x, op, T))
        return base_row(q, t, fr, "noul", state, W_COUNT[wid].format(op=opw, T=fmt_num(T)), None, gold,
                        pick_card(rng, "noul"), wid, container,
                        {"op": op, "T": fmt_num(T), "x": fmt_num(x), "boundary": T == x, "record_text": state})
    return None


if __name__ == "__main__":
    import sys
    tg = {"ws_lookup_ch": 350, "ws_agg_ch": 225, "ws_count_yn": 275, "ws_agg_yn": 300}
    dv = {"ws_lookup_ch": 20, "ws_agg_ch": 15, "ws_count_yn": 20, "ws_agg_yn": 20}
    print(build(tg, dv, TMP / "cand_wikisql.jsonl"))
