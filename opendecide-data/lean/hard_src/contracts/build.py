"""Build the v0.11 HARD 'contracts' items (teacher-authored; no external model, no external dataset).

Writes
  lean/data/v11_parts/hard/contracts.jsonl        rows with gold
  lean/data/v11_parts/hard/contracts.blind.jsonl  identical rows without "gold"
Deterministic (seed 20261001); re-runnable:
  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python lean/hard_src/contracts/build.py
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import DEFS, CHOICE_Q, YES_Q, NEG_Q, SEC_Q, article  # noqa: E402

SEED = 20261001
OUT = HERE.parents[1] / "data" / "v11_parts" / "hard"
BATCHES = ["items1", "items2", "items3", "items4"]
NONE_LABEL = DEFS["NONE"][0]
SEC_NONE_DEF = "none of the quoted provisions meets the definition above."


def load_items():
    items = []
    for b in BATCHES:
        mod = __import__(b)
        items.extend(mod.ITEMS)
    keys = [it["key"] for it in items]
    dup = [k for k, n in Counter(keys).items() if n > 1]
    assert not dup, f"duplicate keys {dup}"
    return items


def label(k):
    return DEFS[k][0]


def def_line(k):
    lab, d = DEFS[k]
    return f"- {lab}: {d}"


def words(s):
    return len(re.findall(r"\S+", s))


def call_id(instr, state, options, card):
    blob = json.dumps([instr, state, options, card], ensure_ascii=False)
    return "c_" + hashlib.sha1(blob.encode()).hexdigest()[:12]


class Phraser:
    """Deterministic, balanced assignment of question templates (seeded shuffled cycles)."""

    def __init__(self, name, pool):
        self.rng = random.Random(f"{SEED}:{name}")
        self.pool = list(pool)
        self.queue = []

    def next(self):
        if not self.queue:
            self.queue = self.pool[:]
            self.rng.shuffle(self.queue)
        return self.queue.pop()


# Distractor categories that none of the size-varied items' target clauses can meet (checked by hand).
SAFE_EXTRA = ["SEV", "EA", "AUD", "NS", "EXC"]


def vary_size(it, keys):
    """Vary the option count of standard 8-option items (6-12 options) deterministically.
    Only removes non-gold distractors, and only adds categories from SAFE_EXTRA."""
    rng = random.Random(f"{SEED}:size:{it['key']}")
    delta = rng.choice([-2, -1, 0, 0, 1, 2, 3, 4])
    keep = {it["gold"]} | ({it["twin"]["gold"]} if it.get("twin") else set())
    keys = list(keys)
    if delta < 0:
        droppable = [k for k in keys if k not in keep]
        for k in rng.sample(droppable, -delta):
            keys.remove(k)
    elif delta > 0:
        pool = [k for k in SAFE_EXTRA if k not in keys]
        keys += rng.sample(pool, min(delta, len(pool)))
    return keys


def apply_subs(state, subs, key):
    for old, new in subs:
        n = state.count(old)
        assert n == 1, f"{key}: substitution target found {n} times: {old[:60]!r}"
        state = state.replace(old, new)
    return state


def build():
    items = load_items()
    ph = {"cat": Phraser("cat", CHOICE_Q), "yn": Phraser("yn", YES_Q), "neg": Phraser("neg", NEG_Q),
          "sec": Phraser("sec", SEC_Q)}
    rows = []
    n = 0

    def emit(it, state, gold_row, instr, options, card, qtype, role, twin_of=None, diff=None):
        nonlocal n
        n += 1
        rid = f"r_hard_contracts_{n}"
        meta = {"domain": "contracts", "difficulty": diff or it["diff"]}
        if twin_of:
            meta = {"domain": "contracts", "twin_of": twin_of, "difficulty": diff or it["diff"]}
        rows.append({
            "id": rid,
            "group_id": f"g:hard_contracts:{it['key']}",
            "call_id": call_id(instr, state, options, card),
            "split": "train",
            "track": "HARD",
            "source": "hard_contracts",
            "state": state,
            "qtype": qtype,
            "instructions": instr,
            "options": options,
            "gold": gold_row,
            "role": role,
            "card": card,
            "meta": meta,
        })
        return rid

    for it in items:
        kind = it["kind"]
        tw = it.get("twin")
        if kind == "cat":
            keys = [k for k in it["opts"] if k != "NONE"]
            if not it["keep_order"] and len(it["opts"]) == 8:
                keys = vary_size(it, keys)
            if not it["keep_order"]:
                random.Random(f"{SEED}:opts:{it['key']}").shuffle(keys)
            if "NONE" in it["opts"]:
                keys.append("NONE")
            options = [label(k) for k in keys]
            card = "\n".join(def_line(k) for k in keys)
            instr = it["q"] or ph["cat"].next().format(t=it["t"])
            instr = instr[0].upper() + instr[1:]
            bid = emit(it, it["state"], label(it["gold"]), instr, options, card, "choice", "choice")
            if tw:
                assert tw["gold"] != it["gold"], it["key"]
                assert tw["gold"] in keys, (it["key"], tw["gold"])
                st = apply_subs(it["state"], tw["subs"], it["key"])
                ins = instr if not (tw["q"] or tw["t"]) else (tw["q"] or instr.replace(it["t"], tw["t"]))
                emit(it, st, label(tw["gold"]), ins, options, card, "choice", "choice", twin_of=bid)
        elif kind == "sec":
            options = list(it["sections"]) + [NONE_LABEL]
            card = def_line(it["cat"]) + "\n" + f"- {NONE_LABEL}: {SEC_NONE_DEF}"
            if it["extra"]:
                card = "\n".join([def_line(k) for k in it["extra"]]) + "\n" + card
            c = label(it["cat"])
            instr = it["q"] or ph["sec"].next().format(c=c, a=article(c))
            instr = instr[0].upper() + instr[1:]
            g = NONE_LABEL if it["gold"] == "NONE" else it["gold"]
            bid = emit(it, it["state"], g, instr, options, card, "choice", "choice")
            if tw:
                g2 = NONE_LABEL if tw["gold"] == "NONE" else tw["gold"]
                assert g2 != g and g2 in options, it["key"]
                st = apply_subs(it["state"], tw["subs"], it["key"])
                emit(it, st, g2, tw["q"] or instr, options, card, "choice", "choice", twin_of=bid)
        elif kind == "yn":
            c = label(it["cat"])
            card = "\n".join(def_line(k) for k in [it["cat"]] + it["extra"])
            role = "neg" if it["neg"] else "aff"
            tmpl = it["q"] or ph["neg" if it["neg"] else "yn"].next()
            instr = tmpl.format(t=it["t"], c=c, a=article(c))
            instr = instr[0].upper() + instr[1:]
            g = (1 - it["truth"]) if it["neg"] else it["truth"]
            bid = emit(it, it["state"], g, instr, None, card, "noul", role)
            if tw:
                assert tw["gold"] in (0, 1) and tw["gold"] != it["truth"], it["key"]
                st = apply_subs(it["state"], tw["subs"], it["key"])
                g2 = (1 - tw["gold"]) if it["neg"] else tw["gold"]
                emit(it, st, g2, tw["q"] or instr, None, card, "noul", role, twin_of=bid)
        else:
            raise ValueError(kind)
    return items, rows


REQ = ["id", "group_id", "call_id", "split", "track", "source", "state", "qtype", "instructions", "options", "gold",
       "role", "card", "meta"]


def validate(rows):
    errs = []
    ids, cids = set(), Counter()
    for r in rows:
        if list(r.keys()) != REQ:
            errs.append((r["id"], "keys"))
        if r["id"] in ids:
            errs.append((r["id"], "dup id"))
        ids.add(r["id"])
        cids[r["call_id"]] += 1
        if r["split"] != "train" or r["track"] != "HARD" or r["source"] != "hard_contracts":
            errs.append((r["id"], "split/track/source"))
        w = words(r["state"])
        if not 80 <= w <= 450:
            errs.append((r["id"], f"state words {w}"))
        if r["qtype"] == "choice":
            o = r["options"]
            if not (isinstance(o, list) and 3 <= len(o) <= 28 and len(set(o)) == len(o)):
                errs.append((r["id"], "options"))
            if any(": " in x for x in o):
                errs.append((r["id"], "': ' in option"))
            if r["gold"] not in o:
                errs.append((r["id"], "gold not in options"))
            if r["role"] != "choice":
                errs.append((r["id"], "role"))
        elif r["qtype"] == "noul":
            if r["options"] is not None or r["gold"] not in (0, 1) or r["role"] not in ("aff", "neg"):
                errs.append((r["id"], "noul fields"))
        else:
            errs.append((r["id"], "qtype"))
        if not r["card"] or not all(line.startswith("- ") and ": " in line for line in r["card"].split("\n")):
            errs.append((r["id"], "card format"))
        if r["qtype"] == "choice" and r["options"][-1] == NONE_LABEL and all(
                line[2:].split(": ", 1)[0] in r["options"] for line in r["card"].split("\n")) is False:
            pass
        m = r["meta"]
        if m.get("domain") != "contracts" or m.get("difficulty") not in (1, 2, 3):
            errs.append((r["id"], "meta"))
        if "twin_of" in m and m["twin_of"] not in ids:
            errs.append((r["id"], "twin_of unknown"))
    dup_c = [c for c, k in cids.items() if k > 1]
    if dup_c:
        errs.append(("-", f"duplicate call_ids {dup_c}"))
    # twins share group, differ in call_id and gold
    by_id = {r["id"]: r for r in rows}
    for r in rows:
        t = r["meta"].get("twin_of")
        if t:
            b = by_id[t]
            if b["group_id"] != r["group_id"] or b["call_id"] == r["call_id"] or b["gold"] == r["gold"]:
                errs.append((r["id"], "twin relation"))
    return errs


def summary(rows):
    base = [r for r in rows if "twin_of" not in r["meta"]]
    twins = [r for r in rows if "twin_of" in r["meta"]]
    choice = [r for r in rows if r["qtype"] == "choice"]
    noul = [r for r in rows if r["qtype"] == "noul"]
    gold_choice = Counter(r["gold"] for r in choice)
    return {
        "rows": len(rows),
        "base_items": len(base),
        "twins": len(twins),
        "twin_rate": round(len(twins) / len(base), 3),
        "base_by_qtype": dict(Counter(r["qtype"] for r in base)),
        "rows_by_qtype": dict(Counter(r["qtype"] for r in rows)),
        "twins_by_qtype": dict(Counter(r["qtype"] for r in twins)),
        "yes_no_gold": dict(Counter(r["gold"] for r in noul)),
        "yes_no_roles": dict(Counter(r["role"] for r in noul)),
        "choice_gold_top": gold_choice.most_common(12),
        "choice_gold_max_share": round(max(gold_choice.values()) / len(choice), 3),
        "option_count_hist_rows": dict(sorted(Counter(len(r["options"]) for r in choice).items())),
        "option_count_hist_base": dict(sorted(Counter(len(r["options"]) for r in base if r["options"]).items())),
        "difficulty_rows": dict(sorted(Counter(r["meta"]["difficulty"] for r in rows).items())),
        "distinct_phrasings": {
            "choice": len(set(re.sub(r"(Section|section|clause|Clause|the|rule|standard) .*", "", r["instructions"])
                              for r in choice)),
            "choice_templates_used": len(set(r["instructions"] for r in choice)),
            "noul_instructions": len(set(r["instructions"] for r in noul)),
        },
        "state_words": {"min": min(words(r["state"]) for r in rows), "max": max(words(r["state"]) for r in rows),
                        "mean": round(sum(words(r["state"]) for r in rows) / len(rows), 1)},
    }


def main():
    items, rows = build()
    errs = validate(rows)
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "contracts.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(OUT / "contracts.blind.jsonl", "w") as f:
        for r in rows:
            b = {k: v for k, v in r.items() if k != "gold"}
            f.write(json.dumps(b, ensure_ascii=False) + "\n")
    s = summary(rows)
    print(json.dumps(s, indent=1))
    if errs:
        print("ERRORS:")
        for e in errs:
            print(" ", e)
        sys.exit(1)
    print("OK: schema valid")


if __name__ == "__main__":
    main()
