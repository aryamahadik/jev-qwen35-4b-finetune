"""Build v0.11 HARD items, domain evidence_b (invented statutes/regulations applied to facts).

All item text was written by Claude (the teacher) in items_*.py; no external model or dataset is used.
Deterministic: seed 20261001 only fixes the output row order.
Run:  ../../../.venv/bin/python build.py   (from this folder)
Writes data/v11_parts/hard/evidence_b.jsonl and evidence_b.blind.jsonl (gold removed).
"""
import collections
import datetime as dt
import hashlib
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import items_a, items_b, items_c, items_d, items_e  # noqa: E402

SEED = 20261001
SRC = "hard_evidence_b"
DOMAIN = "evidence_b"
OUT_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "data", "v11_parts", "hard"))
OUT = os.path.join(OUT_DIR, "evidence_b.jsonl")
OUT_BLIND = os.path.join(OUT_DIR, "evidence_b.blind.jsonl")

KEYS = ["id", "group_id", "call_id", "split", "track", "source", "state", "qtype", "instructions",
        "options", "gold", "role", "card", "meta"]


def words(s):
    return len(re.findall(r"\S+", s))


def build_card(item):
    if item["card"] is not None:
        card = item["card"].strip("\n")
        if item["opts"]:  # emit card lines in the options' order
            lines = card.split("\n")
            pick = [[l for l in lines if l.startswith(f"- {o}: ")] for o in item["opts"]]
            if all(len(p) == 1 for p in pick) and len(lines) == len(pick):
                card = "\n".join(p[0] for p in pick)
        return card
    assert item["opts"] and item["tpl"], item["key"]
    lines = []
    for o in item["opts"]:
        d = item["extra"].get(o) or item["tpl"].format(o)
        lines.append(f"- {o}: {d}")
    return "\n".join(lines)


def call_id(instr, state, options, card):
    h = hashlib.sha1(json.dumps([instr, state, options, card], ensure_ascii=False).encode()).hexdigest()
    return "c_" + h[:12]


def check_dates():
    """Weekday claims stated inside items must be true calendar facts."""
    wd = lambda y, m, d: dt.date(y, m, d).strftime("%A")  # noqa: E731
    facts = [((2026, 10, 9), "Friday"), ((2026, 10, 12), "Monday"), ((2026, 10, 14), "Wednesday"),
             ((2026, 6, 1), "Monday"), ((2026, 6, 6), "Saturday"), ((2026, 6, 8), "Monday"), ((2026, 6, 9), "Tuesday"),
             ((2026, 7, 2), "Thursday"), ((2026, 7, 9), "Thursday"), ((2026, 7, 8), "Wednesday"),
             ((2026, 7, 19), "Sunday"), ((2026, 7, 18), "Saturday"), ((2026, 7, 20), "Monday"),
             ((2026, 3, 2), "Monday"), ((2026, 3, 4), "Wednesday"), ((2026, 3, 6), "Friday"),
             ((2026, 9, 4), "Friday"), ((2026, 8, 31), "Monday"), ((2026, 9, 7), "Monday")]
    for (y, m, d), name in facts:
        assert wd(y, m, d) == name, (y, m, d, name, wd(y, m, d))
    # day-count facts used by golds
    D = dt.date
    assert (D(2026, 5, 20) - D(2026, 3, 3)).days == 78 and (D(2026, 6, 12) - D(2026, 3, 3)).days == 101  # A2
    assert (D(2025, 6, 15) - D(2025, 1, 5)).days == 161 and (D(2025, 8, 15) - D(2025, 1, 5)).days == 222  # A16
    assert D(2026, 4, 3) + dt.timedelta(21) == D(2026, 4, 24)  # B1
    assert (D(2026, 5, 15) - D(2026, 3, 1)).days == 75  # B7
    assert (D(2026, 6, 1) - D(2026, 5, 10)).days == 22 and (D(2026, 6, 1) - D(2026, 4, 20)).days == 42  # B13
    assert D(2026, 9, 1) + dt.timedelta(30) == D(2026, 10, 1)  # B22
    assert D(2026, 6, 5) + dt.timedelta(60) == D(2026, 8, 4)  # C15
    assert D(2026, 5, 4) + dt.timedelta(14) == D(2026, 5, 18) and D(2026, 5, 9) + dt.timedelta(14) == D(2026, 5, 23)  # C12
    assert D(2026, 4, 10) + dt.timedelta(60) == D(2026, 6, 9)  # E8
    assert D(2026, 6, 1) + dt.timedelta(45) == D(2026, 7, 16) and D(2026, 7, 16) + dt.timedelta(20) == D(2026, 8, 5)  # E20
    assert D(2026, 3, 10) + dt.timedelta(90) == D(2026, 6, 8)  # E24
    assert (D(2027, 1, 1) - D(2026, 12, 5)).days == 27 and (D(2027, 1, 1) - D(2026, 12, 28)).days == 4  # C4
    assert (D(2026, 7, 21) - D(2026, 6, 6)).days == 45  # C22


def main():
    check_dates()
    items = items_a.ITEMS + items_b.ITEMS + items_c.ITEMS + items_d.ITEMS + items_e.ITEMS
    keys = [x["key"] for x in items]
    assert len(keys) == len(set(keys)) == 130, (len(keys), len(set(keys)))

    rows, errors = [], []
    base_rows, twin_rows = [], []
    for n, x in enumerate(items, 1):
        card = build_card(x)
        opts = x["opts"]
        qt = x["qtype"]
        rid = f"r_hard_evidence_b_{n}"
        gid = f"g:{SRC}:{n}"
        # --- validation ---
        if qt == "choice":
            if not (3 <= len(opts) <= 28): errors.append((x["key"], "n_opts", len(opts)))
            if len(set(opts)) != len(opts): errors.append((x["key"], "dup opts"))
            if x["gold"] not in opts: errors.append((x["key"], "gold not in opts"))
            lines = card.split("\n")
            if len(lines) != len(opts) or not all(l.startswith(f"- {o}: ") and len(l) > len(o) + 6
                                                  for l, o in zip(lines, opts)):
                errors.append((x["key"], "card/options mismatch"))
        else:
            if opts is not None or x["gold"] not in (0, 1): errors.append((x["key"], "noul fields"))
            if not all(l.startswith("- ") and ": " in l for l in card.split("\n")):
                errors.append((x["key"], "noul card format"))
        wc = words(x["state"])
        if not (80 <= wc <= 450): errors.append((x["key"], "words", wc))
        if x["diff"] not in (1, 2, 3): errors.append((x["key"], "diff"))

        def mk(r_id, state, gold, twin_of=None):
            meta = {"domain": DOMAIN, "difficulty": x["diff"]}
            if twin_of: meta["twin_of"] = twin_of
            row = {"id": r_id, "group_id": gid, "call_id": call_id(x["q"], state, opts, card), "split": "train",
                   "track": "HARD", "source": SRC, "state": state, "qtype": qt, "instructions": x["q"],
                   "options": list(opts) if opts else None, "gold": gold,
                   "role": "choice" if qt == "choice" else "aff", "card": card, "meta": meta}
            return {k: row[k] for k in KEYS}

        b = mk(rid, x["state"], x["gold"])
        base_rows.append(b)
        if x["twin"]:
            st = x["state"]
            for old, new in x["twin"]:
                if st.count(old) != 1: errors.append((x["key"], "twin edit not unique", old[:40]))
                st = st.replace(old, new)
            tg = x["twin_gold"]
            if tg == x["gold"]: errors.append((x["key"], "twin gold unchanged"))
            if qt == "choice" and tg not in opts: errors.append((x["key"], "twin gold not in opts"))
            if qt == "noul" and tg not in (0, 1): errors.append((x["key"], "twin gold"))
            twin_rows.append((x, st, tg, rid))
            wc2 = words(st)
            if not (80 <= wc2 <= 450): errors.append((x["key"], "twin words", wc2))

    for i, (x, st, tg, base_id) in enumerate(twin_rows, 1):
        n = 130 + i
        card = build_card(x)
        opts = x["opts"]
        meta = {"domain": DOMAIN, "difficulty": x["diff"], "twin_of": base_id}
        gid = base_id.replace("r_hard_evidence_b_", f"g:{SRC}:")
        row = {"id": f"r_hard_evidence_b_{n}", "group_id": gid, "call_id": call_id(x["q"], st, opts, card),
               "split": "train", "track": "HARD", "source": SRC, "state": st, "qtype": x["qtype"],
               "instructions": x["q"], "options": list(opts) if opts else None, "gold": tg,
               "role": "choice" if x["qtype"] == "choice" else "aff", "card": card, "meta": meta}
        twin_rows[i - 1] = {k: row[k] for k in KEYS}

    rows = base_rows + twin_rows
    if len({r["call_id"] for r in rows}) != len(rows): errors.append(("*", "call_id collision"))
    if len({r["id"] for r in rows}) != len(rows): errors.append(("*", "id collision"))
    if errors:
        for e in errors: print("ERROR", e)
        sys.exit(1)

    # --- balance / leakage diagnostics ---
    def stats(rs):
        s = {}
        yn = [r for r in rs if r["qtype"] == "noul"]
        ch = [r for r in rs if r["qtype"] == "choice"]
        s["n"] = len(rs); s["noul"] = len(yn); s["choice"] = len(ch)
        s["noul_yes"] = sum(r["gold"] for r in yn); s["noul_no"] = len(yn) - s["noul_yes"]
        gc = collections.Counter(r["gold"] for r in ch)
        s["choice_top_gold"] = gc.most_common(3)
        s["choice_max_gold_share"] = round(gc.most_common(1)[0][1] / len(ch), 3)
        s["gold_position_hist"] = dict(sorted(collections.Counter(r["options"].index(r["gold"]) for r in ch).items()))
        s["n_options_hist"] = dict(sorted(collections.Counter(len(r["options"]) for r in ch).items()))
        s["words_min_max_mean"] = (min(words(r["state"]) for r in rs), max(words(r["state"]) for r in rs),
                                   round(sum(words(r["state"]) for r in rs) / len(rs), 1))
        return s

    lead = lambda q: " ".join(q.split()[:1])  # noqa: E731
    phr = {qt: len({lead(r["instructions"]) for r in base_rows if r["qtype"] == qt}) for qt in ("noul", "choice")}
    leaks = [r["id"] for r in rows if r["qtype"] == "choice" and r["gold"].lower() in r["instructions"].lower()]
    summary = {"base": stats(base_rows), "twins": len(twin_rows), "all": stats(rows),
               "twin_qtypes": dict(collections.Counter(r["qtype"] for r in twin_rows)),
               "distinct_question_openers": phr, "distinct_instructions": len({r["instructions"] for r in base_rows}),
               "gold_in_question": leaks,
               "difficulty": dict(sorted(collections.Counter(r["meta"]["difficulty"] for r in base_rows).items()))}

    rng = random.Random(SEED)
    out = list(rows)
    rng.shuffle(out)
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "w") as f:
        for r in out: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(OUT_BLIND, "w") as f:
        for r in out: f.write(json.dumps({k: v for k, v in r.items() if k != "gold"}, ensure_ascii=False) + "\n")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
