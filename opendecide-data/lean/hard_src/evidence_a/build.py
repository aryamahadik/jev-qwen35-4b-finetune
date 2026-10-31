"""Build HARD evidence_a items (v0.11). Deterministic; seed 20261001. CPU only, no external calls.

Writes:
  data/v11_parts/hard/evidence_a.jsonl        (with gold)
  data/v11_parts/hard/evidence_a.blind.jsonl  (identical rows, "gold" removed)
Run: .venv/bin/python lean/hard_src/evidence_a/build.py
"""
import hashlib
import json
import os
import random
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
LEAN = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT_DIR = os.path.join(LEAN, "data", "v11_parts", "hard")

from rules import (JNAME, RULES, LABEL, DEFS_EXC, EXC_OPTS, PURPOSE_OPTS, DEFS_PURPOSE, BRA_OPTS, DEFS_BRA,
                   BRM_OPTS, DEFS_BRM, DEFS_RULING, T_DEFS, T_OPTS)
import items1, items2, items3, items4, items5, items6, items7

SEED = 20261001
DOMAIN = "evidence_a"
SOURCE = "hard_evidence_a"
TERMINAL = {"none of these", "every requirement is satisfied", "no period is deficient",
            "every listed witness is competent", "none of the stages", "no stage is deficient",
            "all of them are hearsay"}
INTROS = ["Applicable provisions ({name}):", "Extract from the {name}:", "Relevant law ({name}):",
          "The following provisions of the {name} govern:", "{name} (extract):"]


def call_id(state, instructions, options, card):
    h = hashlib.sha1(json.dumps([state, instructions, options, card], ensure_ascii=False).encode()).hexdigest()
    return "c_" + h[:12]


def wc(s):
    return len(re.findall(r"\S+", s))


def resolve_options(it, rng):
    o = it.get("opts")
    if it.get("gold") in (0, 1) and o is None:
        return None, None
    if o == "EXC":
        opts, defs = list(EXC_OPTS[it["j"]]), DEFS_EXC[it["j"]]
    elif o == "PURPOSE":
        opts, defs = list(PURPOSE_OPTS), DEFS_PURPOSE
    elif o == "BRA":
        opts, defs = list(BRA_OPTS), DEFS_BRA
    elif o == "BRM":
        opts, defs = list(BRM_OPTS), DEFS_BRM
    elif o == "TMENU":
        size = it["tsize"]
        excl = set(it.get("texclude", []))
        chosen = []
        for x in [it["gold"]] + it.get("tmust", []):
            if x != "none of these" and x not in chosen:
                chosen.append(x)
        pool = [x for x in T_OPTS if x not in chosen and x != "none of these" and x not in excl]
        rng.shuffle(pool)
        chosen += pool[: size - 1 - len(chosen)]
        opts, defs = chosen + ["none of these"], T_DEFS
        assert len(opts) == size, (it["n"], len(opts), size)
    else:
        opts = list(o)
        defs = dict(DEFS_RULING)
        defs.update(it.get("defs", {}))
    if it.get("shuffle", True):
        body = [x for x in opts if x not in TERMINAL]
        tail = [x for x in opts if x in TERMINAL]
        rng.shuffle(body)
        opts = body + tail
    card = "\n".join(f"- {x}: {defs[x]}" for x in opts)
    return opts, card


def build_state(doc, layout, it):
    doc = doc.strip()
    if not it["rules"]:
        return doc
    intro, rules_first = layout
    block = intro.format(name=JNAME[it["j"]]) + "\n" + "\n".join(RULES[k] for k in it["rules"])
    return block + "\n\n" + doc if rules_first else doc + "\n\n" + block


def main():
    items = items1.ITEMS + items2.ITEMS + items3.ITEMS + items4.ITEMS + items5.ITEMS + items6.ITEMS + items7.ITEMS
    ns = [it["n"] for it in items]
    assert ns == list(range(1, 131)), "item numbers must be 1..130 in order"

    rows, errors = [], []
    next_id = 1
    for it in items:
        rng = random.Random(SEED * 1000 + it["n"])
        layout = (rng.choice(INTROS), rng.random() < 0.45)
        options, card = resolve_options(it, rng)
        qtype = "noul" if options is None else "choice"
        if qtype == "noul":
            card = "\n".join(f"- {LABEL[k]}: {RULES[k]}" for k in it.get("card", it["rules"]) if not k.startswith("MENU"))
            role = it.get("role", "aff")
        else:
            role = "choice"
        gid = f"g:{SOURCE}:{it['n']:03d}"
        variants = [(it["doc"], it["q"], it["gold"], None)]
        if "twin" in it:
            tw = it["twin"]
            tdoc = it["doc"]
            for old, new in tw["rep"]:
                c = tdoc.count(old)
                if c != 1:
                    errors.append(f"item {it['n']}: twin replacement found {c} times: {old[:60]!r}")
                tdoc = tdoc.replace(old, new)
            variants.append((tdoc, tw.get("q", it["q"]), tw["gold"], "twin"))
        base_id = None
        for doc, q, gold, kind in variants:
            state = build_state(doc, layout, it)
            rid = f"r_{SOURCE}_{next_id}"
            next_id += 1
            meta = {"domain": DOMAIN, "difficulty": it["d"]}
            if kind == "twin":
                meta["twin_of"] = base_id
            else:
                base_id = rid
            row = {"id": rid, "group_id": gid, "call_id": call_id(state, q, options, card), "split": "train",
                   "track": "HARD", "source": SOURCE, "state": state, "qtype": qtype, "instructions": q,
                   "options": options, "gold": gold, "role": role, "card": card, "meta": meta}
            rows.append(row)

    # ---------------- validation ----------------
    ids, cids = set(), set()
    by_id = {r["id"]: r for r in rows}
    for r in rows:
        tag = r["id"]
        for k in ["id", "group_id", "call_id", "split", "track", "source", "state", "qtype", "instructions",
                  "options", "gold", "role", "card", "meta"]:
            if k not in r:
                errors.append(f"{tag}: missing {k}")
        if r["id"] in ids:
            errors.append(f"{tag}: duplicate id")
        ids.add(r["id"])
        if r["call_id"] in cids:
            errors.append(f"{tag}: duplicate call_id")
        cids.add(r["call_id"])
        n_w = wc(r["state"])
        if not (80 <= n_w <= 450):
            errors.append(f"{tag}: state has {n_w} words")
        if not r["card"] or not all(line.startswith("- ") for line in r["card"].split("\n")):
            errors.append(f"{tag}: bad card")
        if r["qtype"] == "noul":
            if r["options"] is not None or r["gold"] not in (0, 1):
                errors.append(f"{tag}: bad noul row")
            if r["role"] not in ("aff", "neg"):
                errors.append(f"{tag}: bad role")
        else:
            o = r["options"]
            if not (isinstance(o, list) and 3 <= len(o) <= 28 and len(set(o)) == len(o)):
                errors.append(f"{tag}: bad options")
            if r["gold"] not in o:
                errors.append(f"{tag}: gold not in options")
            lines = r["card"].split("\n")
            if len(lines) != len(o) or any(not l.startswith(f"- {x}: ") for l, x in zip(lines, o)):
                errors.append(f"{tag}: card lines do not match options")
        m = r["meta"]
        if m.get("domain") != DOMAIN or m.get("difficulty") not in (1, 2, 3):
            errors.append(f"{tag}: bad meta")
        if "twin_of" in m:
            b = by_id.get(m["twin_of"])
            if b is None or b["group_id"] != r["group_id"] or b["gold"] == r["gold"] or b["call_id"] == r["call_id"]:
                errors.append(f"{tag}: bad twin link")
        if re.search(r"\b(correct answer|the answer is|gold label|gold answer)\b", r["state"], re.I):
            errors.append(f"{tag}: possible leakage phrase")

    base = [r for r in rows if "twin_of" not in r["meta"]]
    twins = [r for r in rows if "twin_of" in r["meta"]]
    yn_b = [r for r in base if r["qtype"] == "noul"]
    ch_b = [r for r in base if r["qtype"] == "choice"]
    yn_all = [r for r in rows if r["qtype"] == "noul"]
    ch_all = [r for r in rows if r["qtype"] == "choice"]

    gold_ch = Counter(r["gold"] for r in ch_all)
    top_ch = gold_ch.most_common(1)[0]
    yes_share = sum(r["gold"] for r in yn_all) / len(yn_all)
    if top_ch[1] / len(ch_all) > 0.40:
        errors.append(f"choice gold imbalance: {top_ch}")
    if not (0.40 <= yes_share <= 0.60):
        errors.append(f"yes/no imbalance: {yes_share:.2f}")
    phr = {qt: len({r["instructions"] for r in rows if r["qtype"] == qt}) for qt in ("noul", "choice")}
    for qt, k in phr.items():
        if k < 6:
            errors.append(f"too few phrasings for {qt}: {k}")

    if errors:
        print("VALIDATION ERRORS:")
        for e in errors:
            print("  ", e)
        sys.exit(1)

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, f"{DOMAIN}.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(os.path.join(OUT_DIR, f"{DOMAIN}.blind.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps({k: v for k, v in r.items() if k != "gold"}, ensure_ascii=False) + "\n")

    hist = Counter(len(r["options"]) for r in ch_b)
    hist_all = Counter(len(r["options"]) for r in ch_all)
    pos = Counter(round(r["options"].index(r["gold"]) / (len(r["options"]) - 1), 1) for r in ch_all)
    words = [wc(r["state"]) for r in rows]
    summary = {
        "rows": len(rows), "base_items": len(base), "twins": len(twins),
        "base_yes_no": len(yn_b), "base_choice": len(ch_b),
        "rows_yes_no": len(yn_all), "rows_choice": len(ch_all),
        "yes_share_all_yes_no_rows": round(yes_share, 3),
        "yes_share_base_yes_no": round(sum(r["gold"] for r in yn_b) / len(yn_b), 3),
        "choice_top_gold": [top_ch[0], top_ch[1], round(top_ch[1] / len(ch_all), 3)],
        "option_count_hist_base_choice": dict(sorted(hist.items())),
        "option_count_hist_all_choice": dict(sorted(hist_all.items())),
        "gold_relative_position_hist": dict(sorted(pos.items())),
        "distinct_phrasings": phr,
        "difficulty": dict(sorted(Counter(r["meta"]["difficulty"] for r in base).items())),
        "state_words_min_max_mean": [min(words), max(words), round(sum(words) / len(words), 1)],
        "jurisdictions": dict(Counter(it["j"] for it in items)),
    }
    print(json.dumps(summary, indent=1))
    with open(os.path.join(HERE, "summary.json"), "w") as f:
        json.dump(summary, f, indent=1)


if __name__ == "__main__":
    main()
